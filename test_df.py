import os
import pandas as pd
metadata_path = 'data/unseen_demo_metadata.csv'
df = pd.read_csv(metadata_path)
valid_records = []
for i, row in df.iterrows():
    record_path = os.path.join('data/raw', row['filename_lr'])
    if os.path.exists(record_path + '.hea'):
        valid_records.append(row)
df_valid = pd.DataFrame(valid_records)
print(df_valid.head())
print("Columns:", df_valid.columns)
