import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score, precision_recall_curve, average_precision_score
import ast

SUPERCLASSES = ['NORM', 'MI', 'STTC', 'CD', 'HYP']

def main():
    metadata_path = 'data/subset_multiclass_metadata.csv'
    probs_path = 'models/clean_oof_multiclass_probs.npy'
    
    if not os.path.exists(probs_path):
        print(f"File {probs_path} not found. Run train_multiclass_ecg_model.py first.")
        return
        
    df = pd.read_csv(metadata_path)
    probs = np.load(probs_path)
    
    y_true = []
    for i, row in df.iterrows():
        y_true.append([row[f'label_{sc}'] for sc in SUPERCLASSES])
    y_true = np.array(y_true)
    
    os.makedirs('reports/figures', exist_ok=True)
    
    # 1. Plot ROC Curves
    plt.figure(figsize=(10, 8))
    colors = ['blue', 'red', 'green', 'orange', 'purple']
    
    for i, class_name in enumerate(SUPERCLASSES):
        fpr, tpr, _ = roc_curve(y_true[:, i], probs[:, i])
        auc = roc_auc_score(y_true[:, i], probs[:, i])
        plt.plot(fpr, tpr, color=colors[i], lw=2, label=f'{class_name} (AUC = {auc:.3f})')
        
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontsize=12)
    plt.ylabel('True Positive Rate', fontsize=12)
    plt.title('Multi-Label Diagnostic Classification ROC Curves', fontsize=14, fontweight='bold')
    plt.legend(loc="lower right")
    plt.grid(alpha=0.3)
    roc_fig_path = 'reports/figures/multiclass_roc_curve.png'
    plt.savefig(roc_fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved {roc_fig_path}")

    # 2. Plot PR Curves
    plt.figure(figsize=(10, 8))
    for i, class_name in enumerate(SUPERCLASSES):
        precision, recall, _ = precision_recall_curve(y_true[:, i], probs[:, i])
        pr_auc = average_precision_score(y_true[:, i], probs[:, i])
        plt.plot(recall, precision, color=colors[i], lw=2, label=f'{class_name} (PR-AUC = {pr_auc:.3f})')
        
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('Recall (Sensitivity)', fontsize=12)
    plt.ylabel('Precision (PPV)', fontsize=12)
    plt.title('Multi-Label Diagnostic Classification PR Curves', fontsize=14, fontweight='bold')
    plt.legend(loc="lower left")
    plt.grid(alpha=0.3)
    pr_fig_path = 'reports/figures/multiclass_pr_curve.png'
    plt.savefig(pr_fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved {pr_fig_path}")

if __name__ == '__main__':
    main()
