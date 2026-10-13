# Validation record

Notebook numerical assertions passed during in-memory execution; the notebook and CSV hashes are unchanged. The aggregate validator checks sample sizes, manual/built-in agreement, p-value corrections, confidence-interval widths, histogram normalization, standardization, age suppression and all nine required figures.

Browser checks: all 10 SVG charts, 12 result tables and four overview metrics populate. Both title selectors expose 32 groups; pair selection updates both corresponding charts; legend checkboxes hide/show series; manual methods expand. Desktop and 390px mobile layouts inspected. Corrected the title-sort exception and grid overflow. The HTML now embeds the same validated aggregate JSON, avoiding a separate data-fetch failure. A visible loading/error message replaces silent failure.

Public bundle allowlist: index.html, styles.css, app.js and summary.json. No CSV, respondent rows, notebook, credentials or remote script dependencies are included.

The controlled browser does not expose a private/incognito session option. An unauthenticated HTTP check and deployed-browser check will be recorded in the local delivery record after publication; an incognito check must not be claimed as completed.
