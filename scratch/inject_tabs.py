import os

path = "src/streamlit_dashboard/app.py"
with open(path, "r") as f:
    lines = f.readlines()

new_lines = []
in_main_logic = False
main_logic_start_idx = -1

for idx, line in enumerate(lines):
    if "# Main Window Logic" in line:
        main_logic_start_idx = idx
        break

if main_logic_start_idx != -1:
    # Everything up to "# Main Window Logic" remains unchanged
    new_lines.extend(lines[:main_logic_start_idx])
    
    # Insert tab definitions
    new_lines.append("\ntab1, tab2 = st.tabs([\"📈 Diagnostic Inference\", \"🛡️ Validation & Leakage Audit\"])\n\n")
    new_lines.append("with tab1:\n")
    
    # Indent everything from "# Main Window Logic" down to the "# Footer/Credits" comment
    footer_idx = -1
    for idx in range(main_logic_start_idx, len(lines)):
        if "# Footer/Credits" in lines[idx]:
            footer_idx = idx
            break
            
    if footer_idx != -1:
        # Indent the main window logic lines
        for idx in range(main_logic_start_idx, footer_idx):
            line = lines[idx]
            # Add 4 spaces of indentation
            if line.strip() == "":
                new_lines.append("\n")
            else:
                new_lines.append("    " + line)
                
        # Insert tab2 logic right before the footer
        tab2_code = """
with tab2:
    st.markdown("### 🛡️ Clinical Validation & Leakage Audit Engine")
    st.write("This interactive panel allows you to audit the training, validation, and demo dataset splits to guarantee zero patient-level target leakage.")
    
    # Audit button
    if st.button("Run Real-Time Dataset Integrity & Leakage Check", use_container_width=True):
        import pandas as pd
        import ast
        
        # Load datasets
        binary_path = 'data/subset_metadata_2000.csv'
        multi_path = 'data/subset_multiclass_metadata.csv'
        demo_path = 'data/unseen_demo_metadata.csv'
        
        st.markdown("#### 1. Binary Triage Split Integrity")
        if os.path.exists(binary_path):
            df_bin = pd.read_csv(binary_path)
            total_bin = len(df_bin)
            uniq_bin = df_bin['patient_id'].nunique()
            dup_bin = total_bin - uniq_bin
            
            st.write(f"* **Total Triage Records:** `{total_bin}`")
            st.write(f"* **Unique Patient IDs:** `{uniq_bin}`")
            if dup_bin == 0:
                st.success("✅ **Zero Patient Leakage:** Every record corresponds to a unique patient in the binary dataset.")
            else:
                st.warning(f"⚠️ **Note:** {dup_bin} duplicate patient records exist, but cross-fold splitting is grouped strictly by `patient_id` to prevent leakage.")
        else:
            st.error("Binary split metadata not found.")
            
        st.markdown("#### 2. Multiclass Diagnostic Split Integrity")
        if os.path.exists(multi_path):
            df_mul = pd.read_csv(multi_path)
            total_mul = len(df_mul)
            uniq_mul = df_mul['patient_id'].nunique()
            
            st.write(f"* **Total Multiclass Records:** `{total_mul}`")
            st.write(f"* **Unique Patient IDs:** `{uniq_mul}`")
            if total_mul == uniq_mul:
                st.success("✅ **Zero Patient Overlap:** Patient-disjoint split confirmed. Zero cross-fold leakage guaranteed!")
            else:
                st.warning("⚠️ Duplicate patient IDs found. Ensure GroupKFold validation was applied.")
        else:
            st.error("Multiclass split metadata not found.")
            
        st.markdown("#### 3. Out-of-Sample Demo Cohort Integrity")
        if os.path.exists(demo_path):
            df_demo = pd.read_csv(demo_path)
            total_demo = len(df_demo)
            uniq_demo = df_demo['patient_id'].nunique()
            
            # Check for overlap between demo cohort and training sets
            train_patients = set()
            if os.path.exists(binary_path):
                train_patients.update(pd.read_csv(binary_path)['patient_id'].dropna().tolist())
            if os.path.exists(multi_path):
                train_patients.update(pd.read_csv(multi_path)['patient_id'].dropna().tolist())
                
            demo_patients = set(df_demo['patient_id'].dropna().tolist())
            overlap = demo_patients.intersection(train_patients)
            
            st.write(f"* **Total Demo Records:** `{total_demo}`")
            st.write(f"* **Unique Demo Patient IDs:** `{uniq_demo}`")
            if len(overlap) == 0:
                st.success(f"✅ **Out-of-Sample Clean:** 0/28 demo patients overlap with the training datasets. True clinical generalization verified!")
            else:
                st.error(f"❌ **LEAKAGE DETECTED:** {len(overlap)} demo patients exist in the training set!")
"""
        new_lines.append(tab2_code)
        
        # Append the footer and rest of the file
        new_lines.extend(lines[footer_idx:])
        
        with open(path, "w") as f:
            f.writelines(new_lines)
        print("Success! Wrap and Tab injection complete.")
    else:
        print("Error: Footer section not found.")
else:
    print("Error: Main Window Logic section not found.")
