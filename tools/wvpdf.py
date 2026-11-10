"""Read a West Virginia Code article PDF (code.wvlegislature.gov/pdf/<ch>-<art>/) into sections (private; no network).

sections(pdf bytes) -> [(label '61-2-1', [lines])]: each text block is one paragraph (its lines joined), the running
head ("West Virginia Code §..."), the foot (date, "Page n of m", "§...") and the "WV Legislature" mark are dropped, and a
paragraph that a page break splits is joined again.
"""
import re
import pymupdf
from state_lib import norm

HEAD = re.compile(r'^§\s*([0-9A-Z]+-[0-9A-Z]+-[0-9A-Za-z.]+?)\.?\s')


def _join(txt):
    out = ''
    for l in txt.split('\n'):
        l = l.strip()
        if not l:
            continue
        if not out:
            out = l
        elif out.endswith('-') and not out.endswith(' -'):
            out += l
        else:
            out += ' ' + l
    return out


def sections(data):
    d = pymupdf.open(stream=data, filetype='pdf')
    paras = []   # (page, y0, text)
    for pn, page in enumerate(d):
        h = page.rect.height
        for b in page.get_text('blocks'):
            x0, y0, x1, y1, txt = b[:5]
            t = _join(txt)
            if not t or b[6] != 0:
                continue
            if t == 'WV Legislature' or y0 > h - 80 or (y0 < 70 and t.startswith('West Virginia Code')):
                continue
            paras.append((pn, y0, t))
    out, cur, last_pn = [], None, -1
    for pn, y0, t in paras:
        m = HEAD.match(t + ' ')
        if m and not t[m.end(1):].startswith('.') and t[m.end(1):].strip():
            m = None   # a reference at the start of a paragraph, not a heading: a heading has '.' after the number or stands alone
        if m and t.startswith('§'):
            cur = (m.group(1), [t])
            out.append(cur)
        elif cur is not None:
            if pn != last_pn and cur[1] and len(cur[1]) > 1 and not re.search(r'[.:;!?")\]]$', cur[1][-1]):
                cur[1][-1] = cur[1][-1] + ' ' + t
            else:
                cur[1].append(t)
        last_pn = pn
    res = []
    for lab, ls in out:
        ls = [norm(x) for x in ls]
        # a heading the PDF wraps onto a second text block ("...; commutation of" / "Sentences; reprieves; ...") is one line
        if (len(ls) > 1 and re.match(r'^§\s*\S+?\.\s', ls[0]) and not re.search(r'[.)\]]$', ls[0])
                and len(ls[1]) < 200 and ls[1].endswith('.')):
            ls = [ls[0] + ' ' + ls[1]] + ls[2:]
        res.append((lab, ls))
    return res
