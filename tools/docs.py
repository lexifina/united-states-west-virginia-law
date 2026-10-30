"""Writes repo/README.md, LICENSE, jurisdiction.json from corpus.json."""
import json
import os
import sys

from state_lib import write_docs

HERE = os.path.dirname(os.path.abspath(__file__))
c = json.load(open(os.path.join(HERE, 'corpus.json'), encoding='utf-8'))
names = {'61': 'Crimes and Their Punishment', '31D': 'West Virginia Business Corporation Act', '36': 'Estates, Property and Conveyances', '46': 'Uniform Commercial Code'}
rows = []
for ch in names:
    acts = [a for a in c['acts'] if a['slug'].startswith(f'chapter-{ch.lower()}-article-')]
    if acts:
        n = sum(len(a['versions'][0]['units']) for a in acts)
        rows.append((f'chapter-{ch.lower()}-article-*/', f'West Virginia Code, Chapter {ch}: {names[ch]}, one folder per article', 1, f'{len(acts)} articles, {n} sections, text as of 2026-10-13'))
write_docs(HERE, {
    'name': 'United States (West Virginia)', 'state': 'West Virginia', 'code': 'US-WV', 'slug': 'west-virginia',
    'domain': 'code.wvlegislature.gov', 'acts_table': rows,
    'source': 'The [West Virginia Code](https://code.wvlegislature.gov/) site of the West Virginia Legislature. English. Only the section text is taken; the site\'s bill-history and signed-bill widgets are not copied.',
    'dates': 'code.wvlegislature.gov publishes only the current text. Each article is therefore one version, "oldest version available", dated 2026-10-13, the lastmod date the site\'s own sitemap gives every page. Later builds will add later versions on top.',
    'limits': 'A first build: a few chapters of the West Virginia Code. The other chapters, the Acts of the Legislature, legislative rules and the State Constitution are not included (the Legislature\'s Constitution page is under a path its robots.txt disallows). There is no history before the date above.',
    'license': """Source: West Virginia Code, West Virginia Legislature, https://code.wvlegislature.gov/ (retrieved 2026-10-30).

Statute text is not copyrightable: under the government edicts doctrine, as the Supreme Court applied it in Georgia v.
Public.Resource.Org, Inc., 590 U.S. 255 (2020), no one holds copyright in the laws that legislators make in their official
capacity. The site's footer reads "Copyright (c) 2026 West Virginia Code" and states no restriction on reuse; its robots.txt
disallows only /wp-admin/. No annotations (such as the commercially published annotated Code) are used.""",
    'publisher': 'West Virginia Legislature, code.wvlegislature.gov', 'build': 'built', 'date': '2026-10-30',
})
