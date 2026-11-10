"""Wave 3 (2026-11-03, private): the whole West Virginia Code. parse.main(FIRST) first (chapters 61, 31D, 36, 46 from
the section pages, byte for byte as first published), then every other article from its official article PDF
(wvpdf.py; validated against the section pages), one act per article, dated by the sitemap lastmod as in parse.py.
Reads .cache only."""
import hashlib, json, os, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import parse as P
import wvpdf
from state_lib import key, sha, text_of

FIRST = ['61', '31D', '36', '46']
SITE = P.SITE
RAW = HERE / '.cache' / 'raw'


def raw(u):
    p = RAW / hashlib.sha256(u.encode()).hexdigest()
    return p.read_bytes() if p.exists() else None


def main():
    P.main(FIRST)
    out = HERE / 'corpus.json'
    c = json.loads(out.read_text('utf-8'))
    w3 = json.loads((HERE / '.cache' / 'w3-articles.json').read_text('utf-8'))
    sm = raw(SITE + 'sitemap.xml').decode('utf8')
    lastmod = sorted(set(re.findall(r'<lastmod>([^<]*)</lastmod>', sm)))
    date = lastmod[-1][:10]
    names = {}
    for u, _ in w3['articles']:
        ch = u[len(SITE):-1].split('-')[0]
        if ch in names:
            continue
        h = (raw(SITE + ch + '/') or b'').decode('utf8', 'replace')
        m = re.search(r"<h3[^>]*>(CHAPTER [^<]*)</h3>", h)
        arts = dict(re.findall(r"<a href='/%s-([0-9A-Z]+)/'>(ARTICLE [^<]*)</a>" % re.escape(ch), h))
        names[ch] = (P.norm(m.group(1)) if m else f'CHAPTER {ch}', {k: P.norm(v) for k, v in arts.items()})
    have = {a['slug'] for a in c['acts']}
    n = 0
    for u, _ in w3['articles']:
        ch, art = u[len(SITE):-1].split('-', 1)
        if ch in FIRST:
            continue
        b = raw(SITE + 'pdf/' + ch + '-' + art + '/')
        if not b or not b.startswith(b'%PDF'):
            continue
        secs = wvpdf.sections(b)
        if not secs:
            continue
        slug = key(f'chapter-{ch.lower()}-article', art)
        assert slug not in have, slug
        have.add(slug)
        ctitle, arts = names[ch]
        atitle = arts.get(art, f'ARTICLE {art}')
        units = {}
        for label, lines in secs:
            k = key('sec', label)
            base, i = k, 2
            while k in units:
                k = f'{base}-dup{i}'; i += 1
            lines = [('# ' + lines[0])] + lines[1:]
            units[k] = {'label': '§ ' + label, 'kind': 'section', 'text': text_of(lines)}
        c['acts'].append({'slug': slug, 'short': f'W. Va. Code {ch}-{art}', 'title': f'West Virginia Code, {ctitle} {atitle}'.replace('..', '.'),
                          'url': f'{SITE}{ch}-{art}/', 'first_law': None, 'earlier_laws': [],
                          'versions': [{'from': date, 'source_url': SITE + 'pdf/' + ch + '-' + art + '/', 'sha256': sha(b), 'units': units}]})
        n += 1
    c['decisions'].append(f'Wave 3 (2026-11-03): every other article was added from the Legislature\'s own article PDF (code.wvlegislature.gov/pdf/<chapter>-<article>/), one act per article, one unit per section, dated {date}, the lastmod the sitemap gave every page on 2026-11-03. Each text block of the PDF is one paragraph; running heads, page footers and the "WV Legislature" mark are left out. Checked against the section pages of chapter 61 article 2: every section identical apart from spacing before punctuation.')
    c['sources'][0]['notes'] = 'Every chapter: 61, 31D, 36 and 46 from the section pages (2026-10-30), the rest from the article PDFs (2026-11-03); section text only.'
    out.write_text(json.dumps(c, ensure_ascii=False, indent=1) + '\n', encoding='utf-8', newline='\n')
    print(n, 'articles added', len(c['acts']), 'acts')


main()
