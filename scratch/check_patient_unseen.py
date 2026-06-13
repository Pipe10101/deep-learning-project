import os
import pandas as pd
import ast

def main():
    ptbxl = pd.read_csv('ptbxl_database.csv')
    multiclass_meta = pd.read_csv('data/subset_multiclass_metadata.csv')
    binary_meta = pd.read_csv('data/subset_metadata_2000.csv')
    
    # Get sets of patient IDs used in training
    multiclass_patients = set(multiclass_meta['patient_id'].tolist())
    binary_patients = set(binary_meta['patient_id'].tolist())
    all_used_patients = multiclass_patients.union(binary_patients)
    
    print(f"Total unique patients used in training: {len(all_used_patients)}")
    
    # Define target superclasses
    scp_df = pd.read_csv('scp_statements.csv', index_col=0)
    scp_df = scp_df[scp_df.diagnostic == 1.0]
    scp_to_class = scp_df['diagnostic_class'].dropna().to_dict()
    
    def get_superclasses(scp_codes_dict):
        classes = set()
        for code, conf in scp_codes_dict.items():
            if code in scp_to_class:
                if conf > 50:
                    classes.add(scp_to_class[code])
        return list(classes)
        
    ptbxl['scp_codes_dict'] = ptbxl['scp_codes'].apply(lambda x: ast.literal_eval(x))
    ptbxl['diagnostic_classes'] = ptbxl['scp_codes_dict'].apply(get_superclasses)
    ptbxl = ptbxl[ptbxl['diagnostic_classes'].apply(len) > 0]
    
    # Filter to patients not in training
    ptbxl_unseen_patients = ptbxl[~ptbxl['patient_id'].isin(all_used_patients)]
    
    # Check signal files on disk
    base_dir = 'data/raw'
    unseen_records = []
    
    for idx, row in ptbxl_unseen_patients.iterrows():
        filename = row['filename_lr']
        record_path = os.path.join(base_dir, filename)
        if os.path.exists(record_path + '.hea'):
            unseen_records.append(row)
            
    df_unseen = pd.DataFrame(unseen_records).reset_index(drop=True)
    print(f"Total unseen patient records on disk: {len(df_unseen)}")
    
    if len(df_unseen) > 0:
        # Keep one record per patient
        df_unseen = df_unseen.drop_duplicates(subset=['patient_id'])
        print(f"Deduplicated unseen patient records on disk: {len(df_unseen)}")
        
        # Add labels
        superclasses = ['NORM', 'MI', 'STTC', 'CD', 'HYP']
        for sc in superclasses:
            df_unseen[f'label_{sc}'] = df_unseen['diagnostic_classes'].apply(lambda x: 1 if sc in x else 0)
            print(f"  {sc} count: {df_unseen[f'label_{sc}'].sum()}")

if __name__ == '__main__':
    main()
