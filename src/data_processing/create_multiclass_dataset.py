import pandas as pd
import ast
import os

def main():
    print("Reading scp_statements.csv...")
    scp_df = pd.read_csv('scp_statements.csv', index_col=0)
    scp_df = scp_df[scp_df.diagnostic == 1.0]
    
    # Mapping from detailed scp code to 5 superclasses (NORM, MI, STTC, CD, HYP)
    # The index is the scp_code (like 'NDT', 'NORM', etc.)
    # The column is 'diagnostic_class'
    scp_to_class = scp_df['diagnostic_class'].dropna().to_dict()
    
    print("Reading ptbxl_database.csv...")
    df = pd.read_csv('ptbxl_database.csv')
    df['scp_codes_dict'] = df['scp_codes'].apply(lambda x: ast.literal_eval(x))
    
    # Globally drop duplicate patient_id to guarantee no patient exists in multiple rows
    df = df.drop_duplicates(subset=['patient_id'])
    
    # Define our 5 target superclasses
    superclasses = ['NORM', 'MI', 'STTC', 'CD', 'HYP']
    
    def get_superclasses(scp_codes_dict):
        classes = set()
        for code, conf in scp_codes_dict.items():
            if code in scp_to_class:
                if conf > 50: # Only confident diagnoses
                    classes.add(scp_to_class[code])
        return list(classes)
        
    df['diagnostic_classes'] = df['scp_codes_dict'].apply(get_superclasses)
    
    # Drop rows that don't belong to any of the 5 superclasses
    df = df[df['diagnostic_classes'].apply(len) > 0]
    
    # Create multi-label columns
    for sc in superclasses:
        df[f'label_{sc}'] = df['diagnostic_classes'].apply(lambda x: 1 if sc in x else 0)
        
    print(f"Total available records with a valid superclass: {len(df)}")
    
    # Stratified sampling to ensure enough representation
    # Let's target 1000 records where each class is present
    samples = []
    sampled_indices = set()
    for sc in superclasses:
        # Get all available for this class that haven't been sampled yet
        pool = df[(df[f'label_{sc}'] == 1) & (~df.index.isin(sampled_indices))]
        n_sample = min(len(pool), 1000)
        sc_sample = pool.sample(n=n_sample, random_state=42)
        samples.append(sc_sample)
        sampled_indices.update(sc_sample.index)
        
    subset = pd.concat(samples).reset_index(drop=True)
    # Re-shuffle the final dataset
    subset = subset.sample(frac=1.0, random_state=42).reset_index(drop=True)
    
    print(f"Selected {len(subset)} unique patient records for Multiclass MVP.")
    for sc in superclasses:
        print(f"  {sc} count: {subset[f'label_{sc}'].sum()}")
        
    os.makedirs('data', exist_ok=True)
    subset.to_csv("data/subset_multiclass_metadata.csv", index=False)
    print("Saved to data/subset_multiclass_metadata.csv")

if __name__ == '__main__':
    main()
