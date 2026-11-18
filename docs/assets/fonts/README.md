# Fonts

Self-hosted so the site makes no external requests.

| File | Family | Source | Licence |
|---|---|---|---|
| `fraunces.woff2` | Fraunces (variable: weight 300–700, optical size 24–144; SOFT 50 and WONK 0 fixed) | [google/fonts `ofl/fraunces`](https://github.com/google/fonts/tree/main/ofl/fraunces) | SIL OFL 1.1, `OFL-Fraunces.txt` |
| `sourcesans3.woff2` | Source Sans 3 (variable weight) | [google/fonts `ofl/sourcesans3`](https://github.com/google/fonts/tree/main/ofl/sourcesans3) | SIL OFL 1.1, `OFL-SourceSans3.txt` |

Both are subset to Latin-1 plus common punctuation and arrows with `pyftsubset` (fontTools); Fraunces was first instanced with `fonttools varLib.instancer`. To regenerate, fetch the variable TTFs from the source folders and run:

```
fonttools varLib.instancer "Fraunces[SOFT,WONK,opsz,wght].ttf" SOFT=50 WONK=0 opsz=24:144 wght=300:700 -o fr.ttf
pyftsubset fr.ttf --unicodes="U+0000-00FF,U+0131,U+0152-0153,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2190-2193,U+2212,U+2248,U+2264-2265,U+00D7" --flavor=woff2 --layout-features='kern,liga,lnum,tnum' --output-file=fraunces.woff2
pyftsubset "SourceSans3[wght].ttf" --unicodes="U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2190-2193,U+2212,U+2215,U+2248,U+2264-2265,U+25CF,U+2713,U+00D7" --flavor=woff2 --layout-features='kern,liga,calt,lnum,tnum,onum,case' --output-file=sourcesans3.woff2
```

Characters outside the subset fall back to the system font.
