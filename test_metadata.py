import os
import pandas as pd
metadata_path = 'data/unseen_demo_metadata.csv'
if os.path.exists(metadata_path):
    df = pd.read_csv(metadata_path)
    valid_records = []
    for i, row in df.iterrows():
        record_path = os.path.join('data/raw', row['filename_lr'])
        if os.path.exists(record_path + '.hea'):
            valid_records.append(row)
        else:
            print(f"Missing: {record_path}.hea")
    print(f"Valid records: {len(valid_records)}")
else:
    print("Metadata path not found.")
