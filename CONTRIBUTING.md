# Contribute to KAIROS

KAIROS is the project index, public site and Dev Kit installer. Fixes to individual tools belong in those tools' repositories. For a first contribution here, pick one small public issue or one verifiable documentation correction. You don't have to install the Dev Kit.

1. Read [AGENTS.md](AGENTS.md), the [license](LICENSE) and the [CLA](CLA.md). Only the human contributor can confirm the CLA for their contribution. Leave it unchecked if not confirmed.
2. Fork this repository with your own GitHub account. Work on a branch in your fork and keep any agent in that checkout. Do not give it upstream write access, the maintainer's credentials, or access to private records. If a fact depends on private evidence, flag it rather than asking for access or guessing.
3. Keep the change small. For copy, verify claims against public sources and check links. If you touch the installer, run `python -m unittest discover -s tests` from the repo root. Say which checks you ran and which you did not.
4. Open a draft pull request from your fork to KAIROS `main`. Include what changed and why, any public evidence, tests, and agent involvement. Your GitHub account identifies the submitter; a model label or comment footer is attribution, not proof of authority. Confirm the CLA yourself before requesting review.
5. Check the PR's status for `checks / kairos-checks`. If checks are pending approval or unavailable, say so in the PR. A maintainer handles any required workflow approval. A green check is not review or acceptance; the maintainer decides whether to merge.

Don't place private handoffs, logs, account details or tokens in a public branch or PR. Follow the public site rules in [AGENTS.md](AGENTS.md) if changing `docs/`.

## How maintainership can change

Zach Rhodes is the current maintainer and makes the final merge decision. If a group of contributors earns his trust and wants to take responsibility for the project, he is willing to hand over maintainership, including merge authority. Contributing a fix, reviewing changes, or helping look after a part of the project are ways to start. No permissions change until an explicit handoff is agreed.
