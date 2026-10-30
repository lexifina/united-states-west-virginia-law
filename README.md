# United States (West Virginia): law history in git

The law of West Virginia as a git history: one file per provision, with `git blame` and `git log` working line by line. It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law).

**What is in it now (a first build, not complete)**

| Folder | Act | Versions | History |
| --- | --- | ---: | --- |
| `chapter-61-article-*/` | West Virginia Code, Chapter 61: Crimes and Their Punishment, one folder per article | 1 | 36 articles, 590 sections, text as of 2026-10-13 |
| `chapter-31d-article-*/` | West Virginia Code, Chapter 31D: West Virginia Business Corporation Act, one folder per article | 1 | 16 articles, 190 sections, text as of 2026-10-13 |
| `chapter-36-article-*/` | West Virginia Code, Chapter 36: Estates, Property and Conveyances, one folder per article | 1 | 15 articles, 275 sections, text as of 2026-10-13 |

**Source.** The [West Virginia Code](https://code.wvlegislature.gov/) site of the West Virginia Legislature. English. Only the section text is taken; the site's bill-history and signed-bill widgets are not copied.

## Dates

code.wvlegislature.gov publishes only the current text. Each article is therefore one version, "oldest version available", dated 2026-10-13, the lastmod date the site's own sitemap gives every page. Later builds will add later versions on top.

## How it is checked

Every version is read back from git on the day it took effect and on the day before (`tools/check_repo.py`) and must match `corpus.json`; the results are in `REPRODUCE.md`.

## What "author" means

The author of a commit is the law that made the change, with an e-mail address that cannot exist (`<law key>@code.wvlegislature.gov.invalid`). In this first build no dated history is available, so every commit is credited to the publisher as "oldest version available". The committer is always Lexifina.

## Limits

A first build: a few chapters of the West Virginia Code. There is no history before the date above.
