#!/usr/bin/env python3
"""
Build script: converts each .md appendix to a branded HTML page.
Uses pandoc for markdown → HTML conversion, then wraps in our template.

Outputs:
  plan/00_MASTER_PLAN.html
  plan/A_market_and_competitive.html
  ...
  plan/H_impact_roadmap.html
  plan/index.html (visual index of all)
"""
import re
import subprocess
from pathlib import Path

PLAN = Path(__file__).parent

# Ordered appendix manifest — [(source .md, output .html, letter, eyebrow, title, lede, blurb)]
APPENDICES = [
    ("00_MASTER_PLAN.md", "00_MASTER_PLAN.html", "00", "Master Plan",
     "Bailey's World — the thesis",
     "A flagship senior-dog sanctuary for North Carolina's Research Triangle. Phase-one capitalization $1.2M–$3.0M. Named in memory of Bailey.",
     "Investor-readable executive narrative. Thesis, ask, 5-year pro forma, the case for the first flagship."),
    ("A_market_and_competitive.md", "A_market_and_competitive.html", "A", "Appendix A",
     "Market & competitive landscape",
     "Triangle demographics, the Silver Tsunami quantified, donor density, peer-sanctuary benchmarking, and the white-space thesis.",
     "Triangle demographics, Silver Tsunami quantified, peer sanctuaries (Old Friends, Muttville, Frosted Faces), donor density. White-space confirmed."),
    ("B_operating_model.md", "B_operating_model.html", "B", "Appendix B",
     "Operating model",
     "Small on-site campus plus distributed foster network. Intake protocols, length-of-stay math, staffing, medical protocols, tech stack, hospice design.",
     "Small campus + foster network. Intake, medical, staffing, KPIs, hospice program, adoption funnel, tech stack."),
    ("C_site_strategy.md", "C_site_strategy.html", "C", "Appendix C",
     "Site strategy",
     "Four-county scoring matrix across Chatham, Orange, Durham, and Wake. Parcel screening, barn conversion reality, utilities, case studies.",
     "4-county scoring matrix (Chatham 4.05 · Orange 3.90 · Durham 3.45 · Wake 2.85). Parcel diligence, barn conversion, Triangle comps."),
    ("D_financial_model.md", "D_financial_model.html", "D", "Appendix D",
     "Financial model",
     "Five-year pro forma in three scenarios. CapEx build, OpEx schedule, unit economics, sensitivities, 12-month cash flow.",
     "5-year pro forma · Low / Mid / High. CapEx build, OpEx schedule, unit economics, sensitivities, cash flow."),
    ("E_capital_stack.md", "E_capital_stack.html", "E", "Appendix E",
     "Capital stack",
     "Structured mission capital — not venture equity. Naming-rights ladder, DAF and PRI strategy, grant landscape, planned-giving program.",
     "Stack design (founding gifts · DAFs · PRI · grants · events), naming-rights ladder, investor personas, planned-giving program."),
    ("F_team_governance_vet.md", "F_team_governance_vet.html", "F", "Appendix F",
     "Team, governance & veterinary",
     "Founder bio, year-one hiring roadmap, board and advisory recruitment targets, NC State CVM partnership, veterinary staffing and compliance.",
     "Founder, Year-1 hiring roadmap, board/advisory recruitment, NC State CVM partnership, vet staffing, NCVMB compliance."),
    ("G_risk_legal_insurance.md", "G_risk_legal_insurance.html", "G", "Appendix G",
     "Risk, legal & insurance",
     "Forty-plus item risk register, 501(c)(3) entity structure, IP, insurance stack, compliance calendar.",
     "40+ risk register (capital, real estate, regulatory, operational, brand, financial). Entity structure, IP, insurance, compliance."),
    ("H_impact_roadmap.md", "H_impact_roadmap.html", "H", "Appendix H",
     "Impact & gated roadmap",
     "KPI dashboard, SROI methodology, the three-stage / five-gate raise, 24-month milestone roadmap, sustainability plan.",
     "KPI dashboard, SADs + SROI, 3-stage gated raise, 24-month milestone roadmap, endowment and sustainability plan."),
]

FOOTER_HTML = '''
<footer class="site-foot">
  <div class="site-foot__inner">
    <div>
      <h3>Bailey's <em>World.</em></h3>
      <p>A 501(c)(3) senior-dog sanctuary for North Carolina's Research Triangle. In memory of Bailey. She got the retirement phase she deserved — we're building this so other senior dogs can too.</p>
    </div>
    <nav class="site-foot__nav">
      <a href="../index.html">Home</a>
      <a href="index.html">Appendix index</a>
      <a href="../index.html#ask">Join the Circle</a>
      <a href="https://github.com/misterpavano/baileys-world" target="_blank" rel="noopener">GitHub</a>
    </nav>
  </div>
  <p class="site-foot__legal">© 2026 Bailey's World, Inc. · 501(c)(3) pending · Raleigh Metro, NC</p>
</footer>
'''

HEAD_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title} — Bailey's World</title>
<meta name="description" content="{description}" />
<meta property="og:title" content="{title} — Bailey's World" />
<meta property="og:description" content="{description}" />
<meta property="og:type" content="article" />
<meta property="og:image" content="../media/bailey.jpg" />
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cpath fill='%238B2635' d='M12 6c-1.7 0-3 1.3-3 3s1.3 3 3 3 3-1.3 3-3-1.3-3-3-3zm8 0c-1.7 0-3 1.3-3 3s1.3 3 3 3 3-1.3 3-3-1.3-3-3-3zM7 13c-1.7 0-3 1.3-3 3s1.3 3 3 3 3-1.3 3-3-1.3-3-3-3zm18 0c-1.7 0-3 1.3-3 3s1.3 3 3 3 3-1.3 3-3-1.3-3-3-3zm-9 3c-3.3 0-6 3.1-6 7 0 2.2 1.8 4 4 4h4c2.2 0 4-1.8 4-4 0-3.9-2.7-7-6-7z'/%3E%3C/svg%3E" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,300..900,100&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="appendix.css" />
</head>
<body>
'''

NAV_HTML = '''<nav class="nav">
  <a href="../index.html" class="nav__logo">Bailey's <em>World</em></a>
  <div class="nav__links">
    <a href="index.html" class="nav__link">Appendices</a>
    <a href="../index.html" class="nav__link">Home</a>
  </div>
  <a href="../index.html#ask" class="nav__cta">Join the Circle</a>
</nav>
'''

SCRIPT_HTML = '''<script>
// Active-section highlight in the TOC
const toc = document.querySelector('.toc');
const headings = document.querySelectorAll('.prose h2');
if (toc && headings.length) {
  const links = new Map();
  toc.querySelectorAll('a').forEach(a => {
    const id = a.getAttribute('href').replace('#', '');
    links.set(id, a);
  });
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        links.forEach(a => a.classList.remove('active'));
        const a = links.get(e.target.id);
        if (a) a.classList.add('active');
      }
    });
  }, { rootMargin: '-10% 0px -60% 0px' });
  headings.forEach(h => obs.observe(h));
}
// Wrap tables in horizontal-scroll containers for mobile
document.querySelectorAll('.prose table').forEach(table => {
  const wrap = document.createElement('div');
  wrap.className = 'table-scroll';
  table.parentNode.insertBefore(wrap, table);
  wrap.appendChild(table);
});
</script>
</body>
</html>
'''


def md_to_html(md_path: Path) -> str:
    """Run pandoc on a markdown file and return rendered HTML fragment."""
    result = subprocess.run(
        ["pandoc",
         "--from=markdown+pipe_tables+fenced_code_blocks+backtick_code_blocks+auto_identifiers+implicit_header_references",
         "--to=html5",
         "--no-highlight",
         str(md_path)],
        capture_output=True, text=True, check=True,
    )
    return result.stdout


def extract_title_and_strip_h1(html: str) -> tuple[str, str]:
    """Pull out the first <h1>...</h1> so we can use it as title; remove from body."""
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    if not m:
        return ("", html)
    title = re.sub(r'<[^>]+>', '', m.group(1)).strip()
    html_without = html.replace(m.group(0), '', 1)
    return (title, html_without)


def strip_second_header_if_subtitle(html: str) -> str:
    """Many files have H1 then immediately ## subtitle. Keep H2s as section headers."""
    return html


def build_toc(html: str) -> tuple[str, list[tuple[str, str]]]:
    """
    Extract H2 headings and their ids. If pandoc didn't generate ids, generate them.
    Returns the modified HTML (with ids on H2s) and a list of (id, text).
    """
    def slugify(text: str) -> str:
        s = re.sub(r'<[^>]+>', '', text).lower()
        s = re.sub(r'[^a-z0-9\s-]', '', s)
        s = re.sub(r'\s+', '-', s.strip())
        return s[:60] or 'section'

    seen = set()
    toc = []
    def h2_handler(m):
        attrs = m.group(1) or ''
        text = m.group(2)
        id_match = re.search(r'id="([^"]+)"', attrs)
        if id_match:
            hid = id_match.group(1)
        else:
            hid = slugify(text)
            base = hid; i = 2
            while hid in seen:
                hid = f"{base}-{i}"; i += 1
            attrs = (attrs + f' id="{hid}"').strip()
        seen.add(hid)
        plain = re.sub(r'<[^>]+>', '', text).strip()
        toc.append((hid, plain))
        return f'<h2{" " + attrs if attrs else ""}>{text}</h2>'

    new_html = re.sub(r'<h2([^>]*)>(.*?)</h2>', h2_handler, html, flags=re.DOTALL)
    return new_html, toc


def build_appendix_page(idx: int) -> Path:
    src_name, out_name, letter, eyebrow, title, lede, blurb = APPENDICES[idx]
    md_path = PLAN / src_name
    out_path = PLAN / out_name

    html_body = md_to_html(md_path)
    # pandoc's first H1 is our title — remove from body (we render it separately in the hero).
    _, html_body = extract_title_and_strip_h1(html_body)
    # If an immediate H2 subtitle exists, also strip it (it's the H1 subtitle line in our MD files)
    # Our files have "# Title" then "## Subtitle" structure; keep the subtitle for context.
    html_body, toc = build_toc(html_body)

    # Build TOC ordered list
    toc_html = ''
    if toc:
        items = ''.join(f'<li><a href="#{hid}">{text}</a></li>' for hid, text in toc)
        toc_html = f'''<aside class="toc" aria-label="Sections">
  <p class="toc__label">Sections</p>
  <ol>{items}</ol>
</aside>'''
    else:
        toc_html = ''  # no TOC for short pages

    # Prev / next nav
    prev_link = ''
    next_link = ''
    if idx > 0:
        _, prev_out, _, prev_eye, prev_title, _, _ = APPENDICES[idx - 1]
        prev_link = f'''<a href="{prev_out}" class="prev">
  <span class="paper__nav__label">← {prev_eye}</span>
  <span class="paper__nav__title">{prev_title}</span>
</a>'''
    else:
        prev_link = f'''<a href="../index.html" class="prev">
  <span class="paper__nav__label">← Home</span>
  <span class="paper__nav__title">Back to Bailey's World</span>
</a>'''
    if idx < len(APPENDICES) - 1:
        _, next_out, _, next_eye, next_title, _, _ = APPENDICES[idx + 1]
        next_link = f'''<a href="{next_out}" class="next">
  <span class="paper__nav__label">{next_eye} →</span>
  <span class="paper__nav__title">{next_title}</span>
</a>'''
    else:
        next_link = f'''<a href="index.html" class="next">
  <span class="paper__nav__label">Appendix index →</span>
  <span class="paper__nav__title">All sections</span>
</a>'''

    head = HEAD_HTML.format(title=title, description=blurb)

    page = f'''{head}{NAV_HTML}
<article>
  <header class="paper__head">
    <div class="container">
      <p class="label paper__eyebrow">{eyebrow}</p>
      <h1 class="paper__title">{title}</h1>
      <p class="paper__lede">{lede}</p>
    </div>
  </header>

  <div class="paper__body">
    {toc_html}
    <div class="prose">
      {html_body}
    </div>
  </div>

  <footer class="paper__foot">
    <nav class="paper__nav" aria-label="Appendix navigation">
      {prev_link}
      {next_link}
    </nav>
  </footer>
</article>

{FOOTER_HTML}
{SCRIPT_HTML}'''

    out_path.write_text(page)
    return out_path


def build_index() -> Path:
    """Build plan/index.html — the card grid of all appendices."""
    cards = []
    for i, (src, out, letter, eyebrow, title, lede, blurb) in enumerate(APPENDICES):
        lead_cls = ' index__card--lead' if i == 0 else ''
        cards.append(f'''<a href="{out}" class="index__card{lead_cls}">
  <div class="index__card-letter">{letter}</div>
  <p class="index__card-label">{eyebrow}</p>
  <h3 class="index__card-title">{title}</h3>
  <p class="index__card-blurb">{blurb}</p>
</a>''')
    grid = '\n'.join(cards)

    head = HEAD_HTML.format(
        title="Business Plan",
        description="The Bailey's World modular business plan — nine appendices backing every claim the investor site makes.",
    )
    page = f'''{head}{NAV_HTML}
<header class="index__head">
  <div class="container">
    <p class="label paper__eyebrow">The business plan</p>
    <h1 class="index__title">Nine appendices.<br/><em>One sanctuary.</em></h1>
    <p class="index__lede">The modular business plan behind Bailey's World. Every claim on the investor site is backed by one of these — sourced, benchmarked, and ready for due diligence.</p>
  </div>
</header>

<section class="index__grid">
  {grid}
</section>

{FOOTER_HTML}
</body>
</html>'''
    out = PLAN / "index.html"
    out.write_text(page)
    return out


def main():
    built = []
    for i in range(len(APPENDICES)):
        p = build_appendix_page(i)
        built.append(p.name)
    idx = build_index()
    built.append(idx.name)
    print(f"Built {len(built)} pages:")
    for name in built:
        print(f"  · {name}")


if __name__ == "__main__":
    main()
