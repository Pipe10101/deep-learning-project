import os

pdf_py = 'src/streamlit_dashboard/pdf_generator.py'

with open(pdf_py, 'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "safe_text(" in line and "pdf.cell(" in line:
        # replace the last ", 0, 1)" with "), 0, 1)" but only if we haven't already
        if line.count("(") > line.count(")"):
            lines[i] = line.replace(', 0, 1)', '), 0, 1)')

with open(pdf_py, 'w') as f:
    f.writelines(lines)
