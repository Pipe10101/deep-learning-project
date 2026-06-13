import pandas as pd
df = pd.read_csv('data/unseen_demo_metadata.csv')
print(df[['label_NORM', 'label_MI', 'label_STTC', 'label_CD', 'label_HYP']].sum())
