import glob

def replace_in_file(filepath, old, new):
    with open(filepath, 'r') as f:
        content = f.read()
    if old in content:
        content = content.replace(old, new)
        with open(filepath, 'w') as f:
            f.write(content)

for md in glob.glob('reports/*.md'):
    replace_in_file(md, "✅ **ACCEPTED** (Alternative Model)", "❌ **REJECTED** (Alternative Model)")
    replace_in_file(md, "✅ **ACCEPTED** (Secondary Model)", "❌ **REJECTED** (Secondary Model)")

