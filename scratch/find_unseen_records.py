import os
import pandas as pd

# Load database & metadata files
ptbxl = pd.read_csv('data/ptbxl_database.csv')
multiclass_meta = pd.read_csv('data/subset_multiclass_metadata.csv')
binary_meta = pd.read_csv('data/subset_metadata_2000.csv')

# Get sets of filenames used in training
multiclass_files = set(multiclass_meta['filename_lr'].tolist())
binary_files = set(binary_meta['filename_lr'].tolist())
all_used_files = multiclass_files.union(binary_files)

# Find records on disk that are NOT in the used files
base_dir = 'data/raw'
unseen_records = []

for idx, row in ptbxl.iterrows():
    filename = row['filename_lr']
    if filename not in all_used_files:
        # Check if the file exists on disk
        record_path = os.path.join(base_dir, filename)
        if os.path.exists(record_path + '.hea'):
            unseen_records.append(row)

df_unseen = pd.DataFrame(unseen_records)
print(f"Total unseen records on disk: {len(df_unseen)}")
if len(df_unseen) > 0:
    print("Example unseen records:")
    print(df_unseen[['ecg_id', 'filename_lr']].head(10))
    # Save unseen records metadata
    df_unseen.to_csv('data/unseen_demo_metadata.csv', index=False)
