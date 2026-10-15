# Selected population revision

The current analysis is `notebooks/peinado_1012953314_assignment1.ipynb`.
The matching report is `peinado_1012953314_assignment1_selected.docx` (and its PDF export).
Earlier report versions and the dashboard retain the former population and should not be
used as results for the selected population.

The supplied 20,407 rows lose 2 explicit retired classifications and 93 ages above 80,
with zero overlap, leaving 20,312. Age 80 remains eligible. Missing ages remain outside
the age plot. Employment limitations and the separate treatment of salary extremes are
explained in both deliverables. The source CSV is unchanged.

To reproduce from the repository root:

1. Run `python src/reproduce_selected_report.py` with the notebook dependencies,
   `nbformat`, `nbclient`, and a registered Python kernel. This executes all notebook
   cells and writes a temporary local calculation cache.
2. Run `python src/prepare_selected_report.py` in that scientific Python environment.
3. Run `python src/build_selected_report.py` with `python-docx` available. This uses
   the existing revised Word report as the layout source and writes the selected version.
4. Run `python src/export_selected_report_pdf.py` with ReportLab and python-docx available to generate the verified PDF layout. On Windows, `src/export_selected_report.ps1` is an optional native Word export alternative.

Report numbers and plots are generated from the same calculation cache as the executed
notebook. Intermediate files are under `tmp/sample_selection`; they are not required to
run the notebook. The notebook itself remains independently reproducible from the CSV.

Verification: all 28 notebook code cells completed without errors; all nine figures and
all six PDF pages were visually reviewed. The selected DOCX contains synchronized
content, but its native Word layout remains unverified because Word export stalled.
The PDF is the verified written-report deliverable.

