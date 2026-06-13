import pandas as pd

df = pd.read_csv('data/unseen_demo_metadata.csv')
row = df[df['ecg_id'] == 21272]
if not row.empty:
    r = row.iloc[0]
    pathologies = []
    if r['label_NORM'] == 1: pathologies.append("Normal")
    if r['label_MI'] == 1: pathologies.append("MI")
    if r['label_STTC'] == 1: pathologies.append("STTC")
    if r['label_CD'] == 1: pathologies.append("CD")
    if r['label_HYP'] == 1: pathologies.append("HYP")
    pathology_str = ", ".join(pathologies)
    
    label = f"Patient {r['patient_id']:.0f} (ECG ID {r['ecg_id']} | Age {r['age']:.0f} | {r['sex'] == 0 and 'M' or 'F'} | Ground Truth: {pathology_str})"
    print("Label in dropdown:")
    print(label)
else:
    print("Record 21272 not found.")
