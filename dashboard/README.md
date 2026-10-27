# Workforce Insights — Question 4

Public dashboard: https://developer-compensation-peinado.bronzemoon5.chatgpt.site

A static HTML/CSS/JavaScript dashboard with bundled Plotly 4.1.1. This avoids a Python server, runtime data uploads and external chart dependencies. It uses fixed verified aggregates from the latest notebook and interpretations from Julian_Peinado_1012953314_assignment1.pdf. Ten interactive views accompany all nine original notebook figures.

## Run locally

1. Install Python 3.12 (only the standard library is needed to serve the existing dashboard).
2. From this dashboard directory, run `python -m http.server 8768 --bind 127.0.0.1 --directory dist`.
3. Open http://127.0.0.1:8768 in a modern browser. JavaScript must be enabled.

## Reproduce the results

The source bundle intentionally excludes the CSV and notebook. Place this directory at `dashboard/` within the original assignment repository, keeping the original `notebooks/`, data and `reports/` paths.

1. Optionally create a virtual environment; install `python -m pip install -r dashboard/requirements.txt` from the assignment root.
2. Run `python dashboard/tools/build_summary.py`. It executes the notebook’s own calculations in memory with its seed, assertions, filters and methods, extracts exact saved PNG outputs, and verifies key stored results. It does not edit the inputs.
3. Run `python dashboard/tools/embed_summary.py`.
4. Run `python dashboard/tools/validate.py` and `node --check dashboard/dist/app.js`.
5. Repeat report consistency checks if either source document changes. The published summary records SHA-256 hashes of all three inputs. Do not claim report consistency after an unreviewed source change.

Runtime: local Plotly JavaScript only; requirements.txt covers optional regeneration. The library retains its MIT license notice in its header. https://plotly.com/javascript/getting-started/

## Publish an update

1. Keep the existing Site identity in `.openai/hosting.json`; use its isolated source checkout.
2. Update and validate `dist/`; never publish the parent assignment folder.
3. Use the Sites source-workflow helper to commit, push and package the exact checked source. Pass credentials through hidden stdin only.
4. Save that pushed commit/archive as a Site version, then deploy that saved version. Preserve public access.
5. Wait for deployment status `succeeded`, then test the public URL below. Static hosts can alternatively serve `dist/` directly over HTTPS; no server build or environment secrets are required.

## Submission and public-access check

1. Open a fresh incognito/private browser window, with no ChatGPT session.
2. Paste https://developer-compensation-peinado.bronzemoon5.chatgpt.site directly. No login should be requested.
3. Confirm 20,312 selected respondents and the $17,243.91 mean gap; check all sections, both title selectors, pair selection and figure disclosures.
4. Resize to a phone width; tables scroll within their cards and charts fit the viewport.
5. Put this same URL on the first page of the written report.

Keep the Site public, enabled and undeleted until final grades are released. No shutdown is scheduled and there is no runtime API token or expiring chart CDN dependency; future uptime depends on the hosting service and account. See COVERAGE.md and VALIDATION.md for checks and limitations.
