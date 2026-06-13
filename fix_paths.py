import glob

def replace_in_file(filepath, old, new):
    with open(filepath, 'r') as f:
        content = f.read()
    if old in content:
        content = content.replace(old, new)
        with open(filepath, 'w') as f:
            f.write(content)

for script in glob.glob('src/automated_reporting/*.py'):
    replace_in_file(script, 
        "'/Users/felipedeleon/.gemini/antigravity-ide/brain/6c49e3f0-dfd4-410a-818f-fdc8211ffc20/", 
        "'reports/")
    replace_in_file(script, "final_ecg_report_document.md", "final_ecg_report.md")
    replace_in_file(script, "methodology_guide_document.md", "methodology_guide.md")
    # if walkthrough is written to reports/, let's assume it should stay in repo root or reports/
    replace_in_file(script, "'walkthrough.md'", "'reports/walkthrough.md'")
