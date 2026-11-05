# Source for Julie's Market Cafe demo

- `../index.html` + `../img/` = the live GitHub Pages site (built file).
- `src.html` = editable source. `__MENU__` and `__MARKET__` are filled by `build.py`
  from `data/menu.json` (193 catering dishes, verified against jebani.com) and
  `data/market_items.json` (58 cafe items from Uber Eats).
- `build.py` writes `site/index.html` for the claude.ai preview; the GitHub Pages
  version wraps that output in a full HTML document with a noindex tag.
- `backups/` = earlier versions (v7 before animation upgrade, v10 before logo,
  v12, v14 before the three counters, v17 before inbox hiding) and the
  without-counters page.
- Photos: `img/{dish id}-{n}.webp` catering, `img/m-{hash}.webp` cafe,
  `img/logo-mark*.png` Julie's logo, `img/icon-*.png` round icons.
