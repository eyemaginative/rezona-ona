## Summary
- Add the missing **Exchange Fairness Add‑On (FSE + FFB)** spec page with an **At‑a‑glance** section.
- Add a small **FFB Badge** UI component (docs page + CSS) and wire it via `extra_css` in `mkdocs.yml`.

## Files
- `docs/specs/exchange-fairness-addon.md`
- `docs/components/ffb-badge.md`
- `docs/assets/stylesheets/extra.css`
- `mkdocs.append.yml` (merge these keys into your `mkdocs.yml`)

## After merge
- Merge the `extra_css` and `Components` nav bits from `mkdocs.append.yml` into your `mkdocs.yml` (or overwrite your file if convenient).
- Push to `main` and the `docs` workflow will redeploy. The badge examples will render and the spec link will work.
