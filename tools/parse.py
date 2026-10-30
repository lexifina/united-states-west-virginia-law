"""Parse the cached West Virginia Code section pages into corpus.json. Reads only .cache; no network.

Usage: python -X utf8 parse.py 61 31D 36   (the chapters to include; each must be fully fetched)
"""
import hashlib
import json
import os
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

from state_lib import Act, key, norm, sha, text_of, write_corpus

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = Path(HERE) / '.cache'
SITE = 'https://code.wvlegislature.gov/'
CODE_DATE = '2026-10-13'   # lastmod the site's own sitemap.xml gives every page
RETRIEVED = '2026-10-30'


def cached(u):
    p = CACHE / (hashlib.sha256(u.encode()).hexdigest() + '.html')
    return p.read_bytes() if p.exists() else None


def sections_of(ch, urls):
    pat = re.compile(r'^' + re.escape(SITE) + re.escape(ch) + r'-([0-9A-Z]+)-([0-9A-Za-z.]+)/$')
    out = []
    for u in urls:
        m = pat.match(u)
        if m:
            out.append((u, m.group(1), m.group(2)))
    return out


def main(chapters):
    sm = cached(SITE + 'sitemap.xml')
    urls = re.findall(r'<loc>([^<]*)</loc>', sm.decode('utf8'))
    acts = {}
    counts = {}
    for ch in chapters:
        for u, art, sec in sections_of(ch, urls):
            b = cached(u)
            if b is None:
                raise SystemExit(f'not fetched: {u}')
            s = BeautifulSoup(b.decode('utf8'), 'lxml')
            st = s.find(class_='sectiontext')
            if st is None:
                raise SystemExit(f'no section text: {u}')
            ah = s.find(class_='art-head')
            box = s.find(id='chpsel-container')
            h3 = box.find('h3') if box else None
            ctitle = norm(h3.get_text(' ')) if h3 else f'CHAPTER {ch}'
            atitle = norm(ah.get_text(' ')) if ah else f'ARTICLE {art}'
            slug = key(f'chapter-{ch.lower()}-article', art)
            a = acts.get(slug)
            if a is None:
                a = acts[slug] = Act(slug, f'W. Va. Code {ch}-{art}', f'West Virginia Code, {ctitle} {atitle}'.replace('..', '.'),
                                     f'{SITE}{ch}-{art}/', CODE_DATE, source_url=f'{SITE}{ch}-{art}/')
                a._raw = b''
            a._raw += b
            lines = []
            for el in st.find_all(['h4', 'p']):
                t = norm(el.get_text(' '))
                if not t:
                    continue
                lines.append(('# ' + t) if not lines and el.name == 'h4' else t)
            if not lines:
                raise SystemExit(f'empty: {u}')
            label = f'{ch}-{art}-{sec}'
            a.add(key('sec', label), '§ ' + label, 'section', text_of(lines))
            counts[ch] = counts.get(ch, 0) + 1
    out = []
    for a in acts.values():
        a.sha256 = sha(a._raw)
        out.append(a)
    country = {'code': 'US-WV', 'name': 'United States (West Virginia)', 'slug': 'united-states-west-virginia', 'lang': 'en',
               'tz': 'America/New_York', 'future_branch': 'future',
               'publisher': {'name': 'West Virginia Code (West Virginia Legislature)', 'email': 'code@code-wvlegislature-gov.invalid'},
               'default_in_force_rule': {'text': 'No dated history is published: each act is the oldest version available, dated by the source\'s own currency statement (the lastmod date of the site\'s sitemap).',
                                         'source': SITE + 'sitemap.xml'},
               'licence_note': 'Statute text is not copyrightable (Georgia v. Public.Resource.Org, 2020). Source: West Virginia Code, code.wvlegislature.gov, West Virginia Legislature.'}
    sources = [{'name': 'West Virginia Code (code.wvlegislature.gov)', 'url': SITE, 'retrieved': RETRIEVED,
                'licence': 'Statute text carries no copyright (Georgia v. Public.Resource.Org, 2020). The site\'s footer reads "Copyright (c) 2026 West Virginia Code" and states no reuse restriction; robots.txt disallows only /wp-admin/.',
                'notes': 'Chapters ' + ', '.join(chapters) + '; section text only.'}]
    decisions = [
        'Each act is a single "oldest version available": code.wvlegislature.gov publishes only the current text, with no dated history.',
        f'All acts are dated {CODE_DATE}, the lastmod date the site\'s own sitemap.xml gives every page (the code is "updated regularly as new legislation takes effect").',
        'One act per article of a chapter; one unit per section, keyed by the section number the site prints.',
        'Only the section text is taken. The site\'s bill-history and signed-bill widgets are not part of the statute text and are not copied.',
        'Repealed sections keep the lines the site prints for them (heading, "Repealed", and the repealing Act).',
        'The West Virginia Constitution is not included: the Legislature\'s page for it is under /WVCODE/, which the Legislature\'s robots.txt disallows.']
    write_corpus(HERE, country, sources, out, decisions)
    print(counts)


if __name__ == '__main__':
    sys.path.insert(0, HERE)
    main(sys.argv[1:])
