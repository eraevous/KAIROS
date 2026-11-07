#!/usr/bin/env python3
"""kairos.py: the Kairos Dev Kit installer. One file, standard library only, Python 3.10+.

WHAT IT DOES
    python kairos.py install    make ~/Kairos, clone the public Kairos repos into it, install the two
                                stdlib-only kits (relay-kit, Telosmith) for this user only, create a fresh
                                private records store, seed it with one decision, build the Cockpit page,
                                then run `check`.
    python kairos.py check      verify every piece and print an OK/FAIL table with a one-line fix per FAIL.
                                Exit code 0 when everything passes, 1 otherwise. Send this output when
                                asking for help.
    python kairos.py open       open the Cockpit (~/Kairos/cockpit/index.html) in your default browser.
    python kairos.py next       print the next three things to try, with exact commands for your OS.

    On Windows type `python`; on macOS and Linux type `python3`. The script works out which at run time.
    Options:  --name NAME   the owner name written into the records store (default: your login name)
              --no-pip      clone only; skip the pip installs (for a machine where pip is blocked)

WHAT IT NEVER DOES
    * It never asks for, needs or uses administrator rights. Everything is a per-user install
      (`pip install --user`), the way Python itself recommends for a machine you don't administer.
    * It never writes outside ~/Kairos (your home folder's Kairos subfolder), except for the per-user
      Python package folders that `pip install --user` always uses (on Windows %APPDATA%\\Python\\...,
      elsewhere ~/.local/...). Nothing is placed in Program Files, /usr, the registry, or your PATH.
    * It never touches an existing records store. The store it creates is new and private to you,
      at ~/Kairos/records. If one is already there, it is left exactly as it is.
    * It never talks to the network except: `git clone`/`git pull` from github.com and `pip install`
      of code from the clones it just made (which are on your disk). pip may additionally fetch its
      build helper (setuptools) from pypi.org when your Python does not already have it; the script
      tries to avoid even that by reusing the setuptools you have. Nothing is uploaded anywhere.
      No account, token or sign-in is needed or created.
    * It never installs a virtual environment. One is optional and never required; if you run this
      from inside one, the kits go into that venv instead of your user folder.

HOW TO UNINSTALL
    Delete the ~/Kairos folder. Then, if you also want the two kits gone:
        python -m pip uninstall relay-kit telosmith        (Windows)
        python3 -m pip uninstall relay-kit telosmith       (macOS, Linux)
    That is everything.

HOW IT IS BUILT (for readers of the code)
    Each step is a small function that returns a Result (ok, label, detail, fix). `install` runs the
    steps in order and never stops on a failed clone or pip install: it records the failure, says so,
    and goes on, because a partial kit is still useful and `check` will show what is missing.
    Subprocesses are always started with `sys.executable -m <module>` rather than by a command name,
    so a Scripts folder that is not on PATH (common on Windows per-user installs) never blocks anything.
    All paths are pathlib.Path objects joined with `/`, which pathlib turns into backslashes on Windows.
    `str(Path.home())` honours HOME on POSIX and USERPROFILE on Windows, so a test can point the whole
    thing at a scratch folder with HOME=/tmp/x python3 kairos.py install.
"""
from __future__ import annotations

import argparse
import datetime as dt
import getpass
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import sysconfig
import webbrowser
from pathlib import Path

# ----------------------------------------------------------------------------------------------------
# Constants: where things go and what gets cloned.
# ----------------------------------------------------------------------------------------------------

KIT_VERSION = "0.1.0"           # version of this installer, printed in the log and the check table
MIN_PY = (3, 10)                # the kits themselves need 3.10+; Fathom (clone only) wants 3.12+

HOME = Path.home()              # HOME on POSIX, USERPROFILE on Windows
ROOT = HOME / "Kairos"          # the one folder this script owns
REPOS = ROOT / "repos"
RECORDS = ROOT / "records"      # a FRESH private records store; never an existing one
COCKPIT = ROOT / "cockpit"
LOG = ROOT / "devkit-log.txt"   # every run appends here; "send us the output" can mean this file

GITHUB = "https://github.com/eraevous"
# name -> (install with pip?, one-line description). Order matters: relay-kit and Telosmith first,
# because the records store and the Cockpit need them.
PUBLIC_REPOS = {
    "relay-kit": (True, "coordination records, ledgers and the Cockpit page"),
    "Telosmith": (True, "keeps the recorded reasons for code attached to the code (`aec`)"),
    "Fathom": (False, "offline data-review reports for a CSV (needs pandas; see `next`)"),
    "QAT-Kits": (False, "cognitive tools as contract-checked specs; runs from the checkout"),
}
# The pip "project name" each clone installs as, so `pip show` and uninstall know them.
PIP_NAMES = {"relay-kit": "relay-kit", "Telosmith": "telosmith"}
# The module each kit can be run as, so PATH never matters: python -m relaykit, python -m aec.
MODULES = {"relay-kit": "relaykit", "Telosmith": "aec"}

IS_WINDOWS = os.name == "nt"
PY = "python" if IS_WINDOWS else "python3"   # what the USER should type; internally we use sys.executable
BRAND = "Kairos"


# ----------------------------------------------------------------------------------------------------
# Small helpers: results, printing, running programs.
# ----------------------------------------------------------------------------------------------------

class Result:
    """One row of the check table. `fix` is the one line a non-developer can act on when ok is False."""

    def __init__(self, label: str, ok: bool, detail: str = "", fix: str = ""):
        self.label, self.ok, self.detail, self.fix = label, ok, detail, fix

    def __bool__(self):
        return self.ok


def say(msg: str = "") -> None:
    """Print to the screen and append to the log file (when ~/Kairos exists). Never raises."""
    print(msg, flush=True)
    try:
        if ROOT.is_dir():
            with open(LOG, "a", encoding="utf-8") as f:
                f.write(msg + "\n")
    except OSError:
        pass


def tilde(p: Path | str) -> str:
    """Show a path relative to the home folder, as ~/..., so logs don't leak the user's name."""
    s = str(p)
    h = str(HOME)
    return "~" + s[len(h):] if s.startswith(h) else s


def run(cmd: list[str], cwd: Path | None = None, env: dict | None = None, timeout: int = 900):
    """Run a program and capture its output. Returns (returncode, combined output). A missing
    program or a timeout is reported as a failure, never as an exception, so the caller just reads
    the code."""
    try:
        p = subprocess.run(cmd, cwd=str(cwd) if cwd else None, env=env, timeout=timeout,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                           encoding="utf-8", errors="replace")
        return p.returncode, p.stdout
    except FileNotFoundError:
        return 127, f"{cmd[0]} is not installed or not on PATH"
    except subprocess.TimeoutExpired:
        return 124, f"{cmd[0]} took longer than {timeout}s and was stopped"


def pymod(module: str, *args: str) -> list[str]:
    """`python -m module args`, using the very interpreter running this script."""
    return [sys.executable, "-m", module, *args]


def user_scripts_dir() -> Path:
    """Where `pip install --user` puts command-line entry points (relay-kit.exe, aec.exe)."""
    scheme = "nt_user" if IS_WINDOWS else "posix_user"
    return Path(sysconfig.get_path("scripts", scheme=scheme))


def in_venv() -> bool:
    """True when this Python is a virtual environment; `--user` is refused there, so we omit it."""
    return sys.prefix != getattr(sys, "base_prefix", sys.prefix)


def on_path(folder: Path) -> bool:
    parts = [Path(p).resolve() for p in os.environ.get("PATH", "").split(os.pathsep) if p]
    try:
        return folder.resolve() in parts
    except OSError:
        return False


# ----------------------------------------------------------------------------------------------------
# Checks: each returns a Result and changes nothing.
# ----------------------------------------------------------------------------------------------------

def check_python() -> Result:
    v = sys.version_info
    ok = (v.major, v.minor) >= MIN_PY
    return Result("Python 3.10+", ok, f"{platform.python_version()} at {tilde(sys.executable)}",
                  "Install Python 3.10 or newer from python.org (tick 'Add python.exe to PATH' on Windows), then run this again.")


def check_git() -> Result:
    code, out = run(["git", "--version"])
    return Result("git", code == 0, out.strip() if code == 0 else "not found",
                  "git is not installed; install it from git-scm.com (defaults are fine), close and reopen your terminal, then run this again.")


def check_pip() -> Result:
    code, out = run(pymod("pip", "--version"))
    return Result("pip", code == 0, out.strip().split(" (")[0] if code == 0 else "not found",
                  f"pip is missing from this Python; run `{PY} -m ensurepip --user`, then run this again.")


def check_clone(name: str) -> Result:
    d = REPOS / name
    ok = (d / ".git").is_dir()
    return Result(f"clone {name}", ok, tilde(d) if ok else "missing",
                  f"Run `{PY} kairos.py install` again (it only re-clones what is missing); if it still fails, "
                  f"check that https://github.com/eraevous/{name} opens in your browser.")


def check_module(repo: str) -> Result:
    """Is the kit importable and does its CLI answer `--help`? Uses `python -m`, so PATH is irrelevant."""
    mod = MODULES[repo]
    code, out = run(pymod(mod, "--help"), timeout=60)
    ok = code == 0
    first = next((ln.strip() for ln in out.splitlines() if ln.strip()), "")
    return Result(f"{PY} -m {mod} --help", ok, first[:60] if ok else out.strip().splitlines()[-1][:80] if out.strip() else "no output",
                  f"Run `{PY} -m pip install --user -e {tilde(REPOS / repo)}`, then run this again.")


def check_command_on_path(cmd: str) -> Result:
    """Informational: is the short command (relay-kit, aec) usable as typed? Failing this is not fatal,
    because every instruction we print uses `python -m` instead. The fix tells them the exact folder."""
    found = shutil.which(cmd)
    scripts = user_scripts_dir()
    if found:
        return Result(f"`{cmd}` on PATH", True, tilde(found))
    exe = scripts / (cmd + (".exe" if IS_WINDOWS else ""))
    if exe.exists():
        return Result(f"`{cmd}` on PATH", True, f"optional: installed at {tilde(exe)} but that folder is not on PATH; "
                      f"`{PY} -m {MODULES['relay-kit'] if cmd == 'relay-kit' else 'aec'}` works regardless")
    return Result(f"`{cmd}` on PATH", True, f"optional: not found; `{PY} -m ...` is used instead")


def check_records() -> Result:
    dec = RECORDS / "governance" / "decisions.jsonl"
    if not dec.exists():
        return Result("records store", False, f"{tilde(RECORDS)} has no governance/decisions.jsonl",
                      f"Run `{PY} kairos.py install` again; it creates the store if the folder is missing or empty.")
    lines = [ln for ln in dec.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if not lines:
        return Result("records store", False, "created but has no decision yet",
                      f"Run `{PY} kairos.py install` again to seed DEC-001.")
    try:
        first = json.loads(lines[0])
        return Result("records store", True, f"{len(lines)} decision line(s); {first.get('id')}: {str(first.get('decision', ''))[:50]}...")
    except ValueError:
        return Result("records store", False, "decisions.jsonl line 1 is not JSON",
                      f"Something edited the ledger by hand. Move {tilde(RECORDS)} aside and run install again.")


def check_cockpit() -> Result:
    page = COCKPIT / "index.html"
    ok = page.is_file() and page.stat().st_size > 0
    return Result("cockpit page", ok, tilde(page) if ok else "missing",
                  f"Run `{PY} -m relaykit cockpit --root {tilde(RECORDS)} --out {tilde(COCKPIT)} --brand {BRAND}`.")


def all_checks() -> list[Result]:
    rows = [check_python(), check_git(), check_pip()]
    rows += [check_clone(n) for n in PUBLIC_REPOS]
    rows += [check_module("relay-kit"), check_module("Telosmith")]
    rows += [check_command_on_path("relay-kit"), check_command_on_path("aec")]
    rows += [check_records(), check_cockpit()]
    return rows


def print_table(rows: list[Result]) -> bool:
    """Print the OK/FAIL table with a fix line under each FAIL. Returns True when all rows pass."""
    width = max(len(r.label) for r in rows)
    say(f"\nKairos Dev Kit {KIT_VERSION} check, {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}, "
        f"{platform.system()} {platform.release()}, home {tilde(ROOT)}")
    say("-" * (width + 50))
    for r in rows:
        say(f"{'OK  ' if r.ok else 'FAIL'}  {r.label.ljust(width)}  {r.detail}")
        if not r.ok and r.fix:
            say(f"      {' ' * width}  fix: {r.fix}")
    say("-" * (width + 50))
    good = all(r.ok for r in rows)
    say("All checks passed." if good else f"{sum(not r.ok for r in rows)} check(s) failed. "
        f"Follow the fix lines, or send this whole output to whoever gave you the kit.")
    return good


# ----------------------------------------------------------------------------------------------------
# Install steps. Each changes one thing and reports.
# ----------------------------------------------------------------------------------------------------

def step_folders() -> Result:
    for d in (ROOT, REPOS, RECORDS, COCKPIT):
        d.mkdir(parents=True, exist_ok=True)
    return Result("folders", True, f"{tilde(ROOT)}/{{repos,records,cockpit}}")


def step_clone(name: str) -> Result:
    """Clone depth 1 the first time; `git pull --ff-only` on later runs. A failure is reported, not fatal."""
    dest = REPOS / name
    if (dest / ".git").is_dir():
        code, out = run(["git", "-C", str(dest), "pull", "--ff-only", "--quiet"], timeout=300)
        if code == 0:
            return Result(f"clone {name}", True, "already present; pulled")
        return Result(f"clone {name}", True, "already present; pull failed (kept as is): " + out.strip().splitlines()[-1][:70])
    if dest.exists() and any(dest.iterdir()):
        return Result(f"clone {name}", False, f"{tilde(dest)} exists but is not a git clone",
                      f"Move or rename {tilde(dest)}, then run install again.")
    code, out = run(["git", "clone", "--depth", "1", "--quiet", f"{GITHUB}/{name}", str(dest)], timeout=600)
    if code != 0:
        last = out.strip().splitlines()[-1] if out.strip() else "no output"
        return Result(f"clone {name}", False, last[:90],
                      "Check your internet connection and that github.com opens in a browser, then run install again.")
    return Result(f"clone {name}", True, "cloned (depth 1)")


def step_pip(repo: str) -> Result:
    """`pip install --user -e <clone>`. Editable, so a later `git pull` updates the kit without
    reinstalling. Tries, in order: reuse the setuptools we already have (no PyPI round trip); let pip
    fetch its build helper; and, on a Linux that marks its Python 'externally managed', the flag that
    still keeps the install in the user folder."""
    src = REPOS / repo
    if not (src / "pyproject.toml").exists():
        return Result(f"pip install {repo}", False, "no clone to install from", f"Fix `clone {repo}` first.")
    base = pymod("pip", "install", "--quiet", "--disable-pip-version-check")
    user = [] if in_venv() else ["--user"]
    attempts = []
    try:
        import setuptools  # noqa: F401  (only to decide whether build isolation can be skipped)
        attempts.append(base + user + ["--no-build-isolation", "-e", str(src)])
    except ImportError:
        pass
    attempts.append(base + user + ["-e", str(src)])
    last = ""
    for cmd in attempts:
        code, out = run(cmd, timeout=900)
        if code == 0:
            return Result(f"pip install {repo}", True, "installed for this user" + (" (into the active venv)" if in_venv() else ""))
        last = out
        if "externally-managed-environment" in out:
            code, out = run(cmd + ["--break-system-packages"], timeout=900)
            if code == 0:
                return Result(f"pip install {repo}", True, "installed for this user (Python is 'externally managed'; user folder used)")
            last = out
    tail = " | ".join(ln.strip() for ln in last.strip().splitlines()[-2:])[:160]
    return Result(f"pip install {repo}", False, tail,
                  f"Run `{PY} -m pip install --user -e {tilde(src)}` by hand and read its last lines; then run install again.")


def owner_name(given: str | None) -> str:
    """The name written into the records store. relay-kit wants one word; we lower-case and strip
    anything that is not a letter, digit, dot, dash or underscore."""
    raw = given or os.environ.get("KAIROS_NAME") or getpass.getuser() or "owner"
    name = re.sub(r"[^\w.-]", "", raw.strip().replace(" ", "-")).lower()
    return name or "owner"


def step_records(name: str) -> Result:
    """`relay-kit init ~/Kairos/records --owner NAME`. Only when the folder is empty: init refuses a
    non-empty folder, which is exactly the guarantee we want (never touch an existing store)."""
    dec = RECORDS / "governance" / "decisions.jsonl"
    if dec.exists():
        return Result("records store", True, "already present; left untouched")
    if any(RECORDS.iterdir()):
        return Result("records store", False, f"{tilde(RECORDS)} is not empty and is not a records store",
                      f"Move {tilde(RECORDS)} aside, then run install again.")
    code, out = run(pymod("relaykit", "init", str(RECORDS), "--owner", name), timeout=120)
    if code != 0:
        return Result("records store", False, out.strip().splitlines()[-1][:120] if out.strip() else "init failed",
                      f"Run `{PY} -m relaykit init {tilde(RECORDS)} --owner {name}` by hand and read the message.")
    return Result("records store", True, f"created for owner '{name}'")


def step_seed(name: str) -> Result:
    """Append DEC-001 through the kit's own ledger tool (never by writing the file ourselves), so the
    line gets its id, date and the append-only check the kit applies. --offline because this store
    has no shared copy on GitHub; RELAYKIT_ACTOR names who recorded it."""
    dec = RECORDS / "governance" / "decisions.jsonl"
    if not dec.exists():
        return Result("seed DEC-001", False, "no records store", "Fix `records store` first.")
    if any(ln.strip() for ln in dec.read_text(encoding="utf-8").splitlines()):
        return Result("seed DEC-001", True, "ledger already has a decision; nothing appended")
    today = dt.date.today().isoformat()
    row = {
        "status": "adopted",
        "decision": f"This is {name}'s Kairos records store, created by the Dev Kit on {today}.",
        "scope": "this records store",
        "decider": name,
        "basis": f"{name} ran `kairos.py install` (Kairos Dev Kit {KIT_VERSION})",
        "locator": f"kairos.py install, {today}",
    }
    env = dict(os.environ, RELAYKIT_ACTOR=name)
    code, out = run(pymod("relaykit", "ledger", "append", "--dir", str(RECORDS / "governance"), "--offline",
                          "decision", json.dumps(row)), env=env, timeout=120)
    if code != 0:
        return Result("seed DEC-001", False, out.strip().splitlines()[-1][:120] if out.strip() else "append failed",
                      f"Run `{PY} kairos.py install` again; if it repeats, send the output.")
    new_id = out.strip().splitlines()[-1] if out.strip() else "?"
    return Result("seed DEC-001", True, f"appended {new_id}: {row['decision']}")


def step_cockpit() -> Result:
    """Build the static Cockpit page from the records. Rebuilding into the same folder is allowed."""
    code, out = run(pymod("relaykit", "cockpit", "--root", str(RECORDS), "--out", str(COCKPIT), "--brand", BRAND), timeout=300)
    if code != 0:
        return Result("cockpit page", False, out.strip().splitlines()[-1][:140] if out.strip() else "build failed",
                      f"Run `{PY} -m relaykit cockpit --root {tilde(RECORDS)} --out {tilde(COCKPIT)} --brand {BRAND}` by hand and read the message.")
    return Result("cockpit page", True, f"written to {tilde(COCKPIT / 'index.html')}")


def report(r: Result) -> None:
    say(f"  {'ok  ' if r.ok else 'FAIL'}  {r.label}: {r.detail}")
    if not r.ok and r.fix:
        say(f"        fix: {r.fix}")


# ----------------------------------------------------------------------------------------------------
# Subcommands.
# ----------------------------------------------------------------------------------------------------

def cmd_install(args) -> int:
    say(f"Kairos Dev Kit {KIT_VERSION}: install into {tilde(ROOT)} ({dt.datetime.now().strftime('%Y-%m-%d %H:%M')})")
    say("This needs no administrator rights and writes only inside that folder (plus pip's per-user package folder).")

    # 0. Preconditions we cannot work around.
    py, git = check_python(), check_git()
    report(py)
    report(git)
    if not py:
        say(f"\nStopping: {py.fix}")
        return 1
    if not git:
        say(f"\nStopping: {git.fix}")
        return 1

    # 1. Folders.
    report(step_folders())

    # 2. Clones. A failure is noted and skipped; the rest continues.
    say("\nCloning the public repos (shallow; a few MB each):")
    cloned = {}
    for name in PUBLIC_REPOS:
        r = step_clone(name)
        report(r)
        cloned[name] = r.ok
    skipped = [n for n, ok in cloned.items() if not ok]
    if skipped:
        say(f"  skipped: {', '.join(skipped)} (see the fix lines above; install continues)")

    # 3. pip installs of the two stdlib-only kits.
    if args.no_pip:
        say("\n--no-pip given: skipping the pip installs. `check` will report the kits as missing.")
    else:
        pip = check_pip()
        report(pip)
        if pip:
            say("\nInstalling the kits for this user (editable, from the clones):")
            for name, (install, _) in PUBLIC_REPOS.items():
                if install and cloned.get(name):
                    report(step_pip(name))
            scripts = user_scripts_dir()
            if not in_venv() and not on_path(scripts):
                say(f"  note: {tilde(scripts)} is not on your PATH, so typing `relay-kit` or `aec` alone won't work.")
                say(f"        Every command we show uses `{PY} -m relaykit` / `{PY} -m aec` instead, which always works.")
                say(f"        To see the folder yourself: {PY} -c \"import sysconfig;print(sysconfig.get_path('scripts', scheme='{'nt_user' if IS_WINDOWS else 'posix_user'}'))\"")
        else:
            say(f"\n  {pip.fix}")

    # 4. Records store, seed, cockpit. All go through relay-kit; if it isn't importable they fail with a fix.
    name = owner_name(args.name)
    say(f"\nRecords store for owner '{name}' (fresh and private; an existing one is never touched):")
    report(step_records(name))
    report(step_seed(name))
    say("\nCockpit page:")
    report(step_cockpit())

    # 5. Check everything and leave the table on screen.
    good = print_table(all_checks())
    if good:
        say(f"\nDone. Next: {PY} kairos.py next")
    return 0 if good else 1


def cmd_check(args) -> int:
    return 0 if print_table(all_checks()) else 1


def cmd_open(args) -> int:
    page = COCKPIT / "index.html"
    if not page.is_file():
        say(f"No cockpit page at {tilde(page)}. Run `{PY} kairos.py install` first.")
        return 1
    say(f"Opening {tilde(page)} in your default browser...")
    if not webbrowser.open(page.resolve().as_uri()):
        say(f"Your browser could not be started automatically. Open this file yourself: {page}")
        return 1
    return 0


def cmd_next(args) -> int:
    repos = tilde(REPOS)
    sep = "\\" if IS_WINDOWS else "/"
    demo = f"{repos}{sep}Telosmith{sep}docs{sep}demo.md"
    say(f"Kairos Dev Kit: the next three things to try (commands for {platform.system()}).\n")
    say("1. Open the Cockpit: the page built from your own records store (one decision so far, yours).")
    say(f"     {PY} kairos.py open")
    say(f"   The page is a plain file: {tilde(COCKPIT / 'index.html')}. Nothing on it is live or online.\n")
    say("2. Run Telosmith's 90-second demo: a toy project whose recorded reasons stay attached to its code.")
    say(f"     {PY} -m aec --version")
    say(f"   then follow {demo} step by step, typing `{PY} -m aec` wherever it says `aec`.")
    if IS_WINDOWS:
        say("   The demo's shell snippets are written for bash; on Windows use Git Bash (installed with git), "
            "or read each step and do the file edits by hand in Notepad.")
    say("")
    say("3. Try Fathom on a CSV you have: an offline data-review report, nothing leaves your machine.")
    say("   Fathom needs pandas, so this one install does reach pypi.org (the only step that does), and Python 3.12+:")
    say(f"     {PY} -m pip install --user -e {repos}{sep}Fathom")
    say(f"     {PY} -m fathom liftoff your.csv --out {tilde(ROOT / 'fathom-out')}")
    say(f"   then open {tilde(ROOT / 'fathom-out')}{sep}liftoff.html and read the Brief.\n")
    say(f"Anything odd? Run `{PY} kairos.py check` and send the output. To remove everything, delete {tilde(ROOT)}.")
    return 0


def main(argv=None) -> int:
    # A Windows console may not be UTF-8; never let a stray character in a tool's output crash us.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(errors="replace")
            except (ValueError, OSError):
                pass
    ap = argparse.ArgumentParser(prog=f"{PY} kairos.py", description="The Kairos Dev Kit: install, check, open, next.",
                                 epilog="No admin rights; writes only inside ~/Kairos; uninstall by deleting that folder.")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("install", help="create ~/Kairos, clone the repos, install the kits, build the Cockpit, then check")
    p.add_argument("--name", help="owner name for the records store (one word; default: your login name)")
    p.add_argument("--no-pip", action="store_true", help="clone only; skip the pip installs")
    p.set_defaults(fn=cmd_install)
    sub.add_parser("check", help="verify every piece; OK/FAIL table; exit 1 on any FAIL").set_defaults(fn=cmd_check)
    sub.add_parser("open", help="open the Cockpit page in your browser").set_defaults(fn=cmd_open)
    sub.add_parser("next", help="the next three things to try, with exact commands").set_defaults(fn=cmd_next)
    args = ap.parse_args(argv)
    if not args.cmd:
        ap.print_help()
        return 0
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
