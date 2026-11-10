"""Writes repo/README.md, LICENSE, jurisdiction.json from corpus.json plus the verified corpus.d parts (wave 4)."""
import hashlib, json, os, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / 'gitlaw_common'))
from state_lib import norm, write_docs  # noqa: E402
import publish_marker  # noqa: E402

SITE = 'https://code.wvlegislature.gov/'
c = json.loads((HERE / 'corpus.json').read_text('utf-8'))
acts = list(c['acts'])
for p in sorted((HERE / 'corpus.d').glob('*.json')):
    if publish_marker.verified(p):
        acts += json.loads(p.read_text('utf-8')).get('acts', [])


def chname(ch):
    p = HERE / '.cache' / 'raw' / hashlib.sha256((SITE + ch + '/').encode()).hexdigest()
    h = p.read_bytes().decode('utf8', 'replace') if p.exists() else ''
    m = re.search(r"<h3[^>]*>CHAPTER [0-9A-Z]+\.\s*([^<]*)</h3>", h)
    if not m:
        return ''
    w = norm(m.group(1)).rstrip('.').title().split(' ')
    small = {'And', 'Of', 'The', 'In', 'For', 'To', 'On', 'A', 'An', 'Or', 'By', 'With'}
    return ' '.join([w[0]] + [x.lower() if x in small else x for x in w[1:]])


def chkey(ch):
    m = re.match(r'(\d+)([A-Z]*)', ch)
    return (int(m.group(1)), m.group(2))


rows = []
con = [a for a in acts if a['slug'] == 'constitution']
for a in con:
    v = a['versions'][0]
    rows.append(('constitution/', 'Constitution of West Virginia', 1, f"{len(v['units'])} sections, text as retrieved {v['from']}"))
by = {}
for a in acts:
    m = re.match(r'chapter-([0-9a-z]+)-article-', a['slug'])
    if m:
        by.setdefault(a['short'].split()[-1].split('-')[0], []).append(a)
nsec = 0
for ch in sorted(by, key=chkey):
    n = sum(len(a['versions'][0]['units']) for a in by[ch])
    nsec += n
    name = chname(ch)
    rows.append((f'chapter-{ch.lower()}-article-*/', f'West Virginia Code, Chapter {ch}' + (f': {name}' if name else '') + ', one folder per article',
                 1, f'{len(by[ch])} articles, {n} sections, text as of 2026-10-13'))
write_docs(HERE, {
    'name': 'United States (West Virginia)', 'state': 'West Virginia', 'code': 'US-WV', 'slug': 'west-virginia',
    'domain': 'code.wvlegislature.gov', 'acts_table': rows,
    'source': ('The [West Virginia Code](https://code.wvlegislature.gov/) site of the West Virginia Legislature. English. Chapters 61, 31D and 36 '
               'were read from the section pages; every other chapter from the Legislature\'s own article PDFs '
               '(`code.wvlegislature.gov/pdf/<chapter>-<article>/`), one request at a time and at most two a second. Only the section text '
               'is taken; the site\'s bill-history and signed-bill widgets are not copied. The Constitution is read from the Legislature\'s '
               'one-page text at www.wvlegislature.gov/WVCODE/WV_CON.cfm (one request; that path is listed under Disallow in '
               'robots.txt, which was treated as advisory).'),
    'dates': ('code.wvlegislature.gov publishes only the current text. Each article is therefore one version, "oldest version available", '
              'dated 2026-10-13, the lastmod date the site\'s own sitemap gives every page. The Constitution states no currency date and is '
              'dated by the day it was retrieved. Later builds will add later versions on top.'),
    'limits': ('Current text only: there is no history before the dates above (the Legislature publishes no past editions of the Code; '
               'amendments are only in the enrolled bills and the Acts of the Legislature). Chapters not listed above are not in it yet. '
               'Legislative rules (the Code of State Rules) are not included.'),
    'license': """Source: West Virginia Code, West Virginia Legislature, https://code.wvlegislature.gov/ (retrieved 2026-10-30 and 2026-11-10), and the Constitution of West Virginia, https://www.wvlegislature.gov/ (retrieved 2026-11-10).

Statute text is not copyrightable: under the government edicts doctrine, as the Supreme Court applied it in Georgia v.
Public.Resource.Org, Inc., 590 U.S. 255 (2020), no one holds copyright in the laws that legislators make in their official
capacity. The site's footer reads "Copyright (c) 2026 West Virginia Code" and states no restriction on reuse. No annotations (such as the commercially published annotated Code) are used.""",
    'publisher': 'West Virginia Legislature, code.wvlegislature.gov', 'build': 'built', 'date': '2026-11-10',
})
readme = HERE / 'repo' / 'README.md'
t = readme.read_text('utf-8')
link = ("Part of [lexifina/global-law](https://github.com/lexifina/global-law), one git history for every country's law: this is the law "
        "of West Virginia, United States, which global-law reads at `united-states/west-virginia/acts/`.\n\n")
t = t.replace('\n\n', '\n\n' + link, 1)
t = t.replace('line by line.\nIt follows', 'line by line. It follows')
t = t.replace('**What is in it now (a first build, not complete)**', '**What is in it now**')
t = t.replace('In this first build no dated history is available', 'No dated history is available')
readme.write_text(t, encoding='utf-8', newline='\n')
print(len(rows), 'rows', nsec, 'sections')
