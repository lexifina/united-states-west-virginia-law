# How this repository was made (United States (West Virginia))

This file is written by the build on 2026-11-13, the day the source data was retrieved.

## Sources

| Source | Address | Retrieved | Licence |
| --- | --- | --- | --- |
| West Virginia Code (code.wvlegislature.gov) | <https://code.wvlegislature.gov/> | 2026-10-30 | Statute text carries no copyright (Georgia v. Public.Resource.Org, 2020). The site's footer reads "Copyright (c) 2026 West Virginia Code" and states no reuse restriction. |

Every word of law in this repository comes from these sources. Lexifina reads them and records each act's dated versions, and the laws that made each change, in one corpus file. This repository is built from that file.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `chapter-20-article-0002d` | West Virginia Code, CHAPTER 20. NATURAL RESOURCES. ARTICLE 2D. WILDLIFE REHABILITATION. | 1 | 2026-10-13 to 2026-10-13 |

The build made 1 commits:

| Commits | Kind |
| ---: | --- |
| 1 | baseline texts where the record starts |
| 0 | named laws, court decisions and treaties |
| 0 | changes no amendment note explains, credited to the publisher |
| 0 | corrections to the existing record |
| 0 | printing or layout changes |

Other counts:
- 0 commits on the branch `future`: laws not yet in force on 2026-11-13.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 0 laws in the record.
- 1 tags.

## Dates

Each commit is dated at noon (America/New_York) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: No dated history is published: each act is the oldest version available, dated by the source's own currency statement (the lastmod date of the site's sitemap). https://code.wvlegislature.gov/sitemap.xml

## How the history is built

`tools/build.py` turns the corpus into this history in one pass: one commit per law, on the day it took effect. The same corpus always gives the same commit hashes. `tools/check_repo.py` reads every version back from git and compares it with the corpus. `tools/on.py` shows the law as it stood on any date. The corpus format is described in `tools/SCHEMA.md`.

- Corpus: sha256 `35754c3865c66751b77f45bfd768a5579460340eee7652e9861456f9703c18bf` (15801 bytes).
- Builder blob hashes (`git hash-object`): `build.py` `63170edd89e92292ac248dae17d79e486e4e9f19`, `check.py` `e340718c28cd5b0edbe37bdeab1aac31427ada66`, `on.py` `4a8aa1c9a5e6bd8cc831b90a6e68c5a6f448a13c`.
- Python 3.12.10; git version 2.46.0.windows.1.

## Checks

Not yet run for this build.

No second build of this corpus has been compared yet.

## Decisions made by hand

- Each act is a single "oldest version available": code.wvlegislature.gov publishes only the current text, with no dated history.
- All acts are dated 2026-10-13, the lastmod date the site's own sitemap.xml gives every page (the code is "updated regularly as new legislation takes effect").
- One act per article of a chapter; one unit per section, keyed by the section number the site prints.
- Only the section text is taken. The site's bill-history and signed-bill widgets are not part of the statute text and are not copied.
- Repealed sections keep the lines the site prints for them (heading, "Repealed", and the repealing Act).
- The West Virginia Constitution is not included: it is not used in this record.

## What AI did and did not do

The source readers and builders were developed under Lexifina's direction with coding assistants, including Claude Code and Codex.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- none
