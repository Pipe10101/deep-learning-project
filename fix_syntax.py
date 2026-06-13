import os

pdf_py = 'src/streamlit_dashboard/pdf_generator.py'

with open(pdf_py, 'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "safe_text(" in line and "pdf.cell(" in line:
        if line.count("(") > line.count(")"):
            # find the end of the f-string or string
            # we know it ends with ", 0, 1)"
            lines[i] = line.replace('", 0, 1)', '"), 0, 1)')
    if "safe_text(" in line and "pdf.multi_cell(" in line:
        pass

with open(pdf_py, 'w') as f:
    f.writelines(lines)

