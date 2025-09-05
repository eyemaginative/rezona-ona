# UI Component: Fair‑Flow Badge (FFB)

Use this lightweight chip to display a venue’s **FFB grade** anywhere in the docs or app prototypes.

## Markup
```html
<span class="ffb-badge grade-A" title="FFB grade A — excellent">FFB A</span>
<span class="ffb-badge grade-B">FFB B</span>
<span class="ffb-badge grade-C">FFB C</span>
<span class="ffb-badge grade-D">FFB D</span>
<span class="ffb-badge grade-F">FFB F</span>
```

## Notes
- Grades map to thresholds defined in the spec (lateness, missing, uptime).
- In a real app, you’d render the grade dynamically from `get_badge(venue)`.
