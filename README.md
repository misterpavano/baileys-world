# Bailey's World

> A flagship senior-dog sanctuary for North Carolina's Research Triangle — in memory of Bailey.

**Live site:** [https://misterpavano.github.io/baileys-world/](https://misterpavano.github.io/baileys-world/)

**Phase-one capitalization target:** $1.25M – $3.05M
**Location:** Raleigh Metro, NC (primary site search: Orange · Chatham · rural Durham)
**Status:** 501(c)(3) filing pending. Pre-formation / fiscal-sponsor bridge phase.

---

## What this is

A single-page investor site (`index.html`) for Bailey's World / Triangle Senior Dog Barn Sanctuary, plus the full modular business plan that backs it (`plan/`). Built in memory of Bailey — Wally's senior dog, adopted in 2020 after a failed Mississippi transport exposed the shelter system's structural weakness. She got the retirement phase she deserved. We're building this so other senior dogs can too.

The site thesis, model, and financial build are all self-contained in the page itself. The 9 plan appendices in `/plan/` back every claim with sourced research.

---

## Business plan

The investor narrative lives at the top; the supporting detail sits below it in modular appendices:

| | Appendix | What it covers |
| --- | --- | --- |
| 00 | [Master Plan](plan/00_MASTER_PLAN.md) | Thesis, ask, executive narrative |
| A | [Market & Competitive](plan/A_market_and_competitive.md) | Triangle demographics, Silver Tsunami, peer benchmarking (Old Friends SDS, Muttville, Frosted Faces) |
| B | [Operating Model](plan/B_operating_model.md) | Small-campus + foster network, intake, medical protocols, KPIs |
| C | [Site Strategy](plan/C_site_strategy.md) | 4-county scoring matrix, parcel screening, barn conversion |
| D | [Financial Model](plan/D_financial_model.md) | 5-year pro forma, three scenarios, sensitivities |
| E | [Capital Stack](plan/E_capital_stack.md) | Stack design, naming-rights ladder, grant landscape, planned giving |
| F | [Team & Governance](plan/F_team_governance_vet.md) | Founder, hiring roadmap, NC State CVM partnership, vet compliance |
| G | [Risk, Legal, Insurance](plan/G_risk_legal_insurance.md) | 40+ risk register, entity structure, insurance stack |
| H | [Impact & Roadmap](plan/H_impact_roadmap.md) | KPI dashboard, SROI, gated raise design, 24-month milestones |

---

## Repo structure

```
baileys-world/
├── index.html          # The investor site (self-contained; inline CSS + JS)
├── media/bailey.jpg    # Bailey's photo (used in Prologue + OG meta)
├── plan/               # 9 markdown appendices
└── README.md           # You are here
```

**No build step.** No npm. No dependencies to install. The site uses Tailwind via the Play CDN and Google Fonts — everything loads from the browser.

---

## Running locally

Just open `index.html` in any modern browser:

```bash
open index.html
```

Or serve it via any static server (useful for testing relative paths):

```bash
python3 -m http.server 8080
# then open http://localhost:8080
```

---

## Deploying

Currently deployed to GitHub Pages at the URL above. To deploy your own fork:

1. Fork this repo
2. Go to **Settings → Pages**
3. Source: **Deploy from a branch** → Branch: **main** → Folder: **/ (root)**
4. Save. URL is `https://<your-user>.github.io/<your-repo>/` in 1–3 minutes.

---

## Contact form

The "Join the Founders' Circle" form at the bottom of the page currently uses `mailto:` — it opens the visitor's native email client with a pre-filled structured message. Works everywhere, no hosting dependency.

To upgrade to a managed inbox (Formspree or Netlify Forms), see the inline comments in the form section of `index.html`.

---

## Contact

**Wally Mostafa** · Founder & Executive Director
Raleigh Metro, North Carolina

---

## License

The site code (HTML, CSS, JS) in this repo is MIT-licensed — reuse freely for your own animal-welfare nonprofit. The business plan content, imagery, and brand identity are © Bailey's World, Inc.

*Bailey — the reason this exists. She got the retirement phase she deserved.*
