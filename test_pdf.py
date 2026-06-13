from src.streamlit_dashboard.pdf_generator import generate_pdf_report
import pandas as pd
import matplotlib.pyplot as plt
import io

patient_data = pd.Series({'patient_id': 1, 'ecg_id': 100, 'age': 45, 'sex': 0})

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 5, 6])
buf = io.BytesIO()
plt.savefig(buf, format="png")
chart_bytes = buf.getvalue()

predictions = [0.1, 0.9, 0.2, 0.05, 0.01]
thresholds = {'NORM': 0.5, 'MI': 0.4, 'STTC': 0.4, 'CD': 0.4, 'HYP': 0.4}
classes = ['NORM', 'MI', 'STTC', 'CD', 'HYP']
verdict_title = '⚠️ ABNORMAL (Action Required)'
verdict_text = 'The physiological 1D pipeline detected abnormalities...'

try:
    generate_pdf_report(patient_data, chart_bytes, predictions, thresholds, classes, verdict_title, verdict_text)
    print('SUCCESS')
except Exception as e:
    import traceback
    traceback.print_exc()
