import os
import glob

def replace_in_file(filepath, old, new):
    with open(filepath, 'r') as f:
        content = f.read()
    if old in content:
        content = content.replace(old, new)
        with open(filepath, 'w') as f:
            f.write(content)

app_py = 'src/streamlit_dashboard/app.py'

# Strip "Multi-Heartbreaker" and "late-fusion" branding
replace_in_file(app_py, "Multi-Heartbreaker CardioAI™", "CardioAI™")
replace_in_file(app_py, "Multi-Heartbreaker CardioAI(TM)", "CardioAI(TM)")
replace_in_file(app_py, "Powered by 1D ResNet & Late-Fusion Multimodal Networks", "Powered by 1D ResNet (ECG-Only)")
replace_in_file(app_py, "Multi-Heartbreaker Triage Engine", "CardioAI Triage Engine")
replace_in_file(app_py, "Multi-Heartbreaker Diagnostic Engine", "CardioAI Diagnostic Engine")

pdf_py = 'src/streamlit_dashboard/pdf_generator.py'
replace_in_file(pdf_py, "Multi-Heartbreaker CardioAI(TM)", "CardioAI(TM)")

# Add safe_text to PDF Generator
with open(pdf_py, 'r') as f:
    pdf_content = f.read()

if "def safe_text" not in pdf_content:
    pdf_content = pdf_content.replace(
        "def generate_pdf_report(",
        "def safe_text(txt):\n    return str(txt).encode('latin-1', 'replace').decode('latin-1')\n\ndef generate_pdf_report("
    )
    # Apply safe_text to cell and multi_cell calls
    pdf_content = pdf_content.replace("pdf.cell(0, 10, 'Patient Demographic Context'", "pdf.cell(0, 10, safe_text('Patient Demographic Context')")
    pdf_content = pdf_content.replace("pdf.cell(0, 6, f\"Patient ID:", "pdf.cell(0, 6, safe_text(f\"Patient ID:")
    pdf_content = pdf_content.replace("pdf.cell(0, 6, f\"Age:", "pdf.cell(0, 6, safe_text(f\"Age:")
    pdf_content = pdf_content.replace("pdf.cell(0, 6, f\"Report Date:", "pdf.cell(0, 6, safe_text(f\"Report Date:")
    pdf_content = pdf_content.replace("pdf.cell(0, 8, verdict_title", "pdf.cell(0, 8, safe_text(verdict_title")
    pdf_content = pdf_content.replace("pdf.multi_cell(0, 6, verdict_text)", "pdf.multi_cell(0, 6, safe_text(verdict_text))")
    pdf_content = pdf_content.replace("pdf.cell(0, 6, f\"{c}:", "pdf.cell(0, 6, safe_text(f\"{c}:")
    
    with open(pdf_py, 'w') as f:
        f.write(pdf_content)

print("Streamlit UI fixed!")
