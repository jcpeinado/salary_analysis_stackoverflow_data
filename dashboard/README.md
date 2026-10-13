# Workforce Insights dashboard

Buildless, dependency-free HTML/CSS/JavaScript dashboard for MIE1624 Question 4. All numerical displays derive from `dist/summary.json`. Ten SVG charts include the nine required figures and an additional confidence-interval view.

## Preview

From the repository root: `python -m http.server 8766 --directory dashboard/dist`, then visit the printed localhost address. Local previews do not satisfy the assignment's public-link requirement.

## Reproduce aggregates

From the assignment repository, run `python dashboard/tools/build_summary.py` with the notebook's scientific Python dependencies installed. The script resolves the notebook and CSV relative to that repository, executes its analysis in memory, validates integrity and exports only the explicit aggregate allowlist. It does not modify the notebook or dataset. The source repository for hosting intentionally omits those inputs.

Run `python dashboard/tools/embed_summary.py` after regenerating summaries. It embeds the same aggregate JSON into HTML so the dashboard does not depend on a separate data request. Run `python dashboard/tools/validate.py` for aggregate identity, coverage and bundle checks. Syntax-check the client with `node --check dashboard/dist/app.js`.

## Publish

The complete deployable static root is `dist/`. Sites identity is recorded in `.openai/hosting.json`. Publish through the Sites source-workflow helper from an isolated checkout containing only this directory's files. Never package or publish the parent assignment repository. Credentials belong only in the helper's hidden standard input, not files or arguments.

The site must remain public, enabled and undeleted until grades are released. Sites did not supply an automatic expiry date in its creation metadata; future availability depends on the hosting service and account remaining active. There is no scheduled shutdown or dashboard-side dependency on an expiring external API.

## Validation

See `COVERAGE.md` for every question-to-source mapping and privacy transformations. `VALIDATION.md` records checks actually completed, including the exact public-access checks and any browser limitations.
