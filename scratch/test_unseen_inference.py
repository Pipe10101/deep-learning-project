import os
import json
import numpy as np
import pandas as pd
import tensorflow as tf
import wfdb
import scipy.signal as signal

# Load models, thresholds, and unseen metadata
multiclass_model = tf.keras.models.load_model('models/multiclass_1d_ecg_model.h5', compile=False)
binary_model = tf.keras.models.load_model('models/binary_1d_ecg_model.h5', compile=False)

with open('models/multiclass_thresholds_cnn.json', 'r') as f:
    thresholds = json.load(f)

df_unseen = pd.read_csv('data/unseen_demo_metadata.csv')

def preprocess_ecg_signal(record_path):
    try:
        record = wfdb.rdrecord(record_path)
        sig = record.p_signal
        fs = 100
        nyq = 0.5 * fs
        b, a = signal.butter(4, [0.5 / nyq, 40.0 / nyq], btype='band')
        filtered_sig = np.zeros_like(sig)
        for i in range(sig.shape[1]):
            filtered_sig[:, i] = signal.filtfilt(b, a, sig[:, i])
        mean = np.mean(filtered_sig, axis=0)
        std = np.std(filtered_sig, axis=0)
        std[std == 0] = 1.0
        norm_sig = (filtered_sig - mean) / std
        if norm_sig.shape[0] >= 1000:
            norm_sig = norm_sig[:1000, :]
        else:
            pad = np.zeros((1000 - norm_sig.shape[0], 12))
            norm_sig = np.vstack([norm_sig, pad])
        return norm_sig
    except Exception:
        return None

classes = ['NORM', 'MI', 'STTC', 'CD', 'HYP']

print("Patient ECG ID | Ground Truth | CNN Model Predictions (Sigmoid > Youden's Threshold)")
print("-" * 90)

results = []
for idx, row in df_unseen.iterrows():
    record_path = os.path.join('data/raw', row['filename_lr'])
    sig = preprocess_ecg_signal(record_path)
    if sig is not None:
        input_batch = tf.expand_dims(sig, 0)
        # Multiclass prediction
        preds = multiclass_model.predict(input_batch, verbose=0)[0]
        
        # Get active ground truths
        gts = [c for c in classes if row[f'label_{c}'] == 1]
        
        # Get model predicted active classes
        pred_actives = []
        pred_details = []
        for i, c in enumerate(classes):
            prob = preds[i]
            thresh = thresholds.get(c, 0.5)
            active = prob >= thresh
            if active:
                pred_actives.append(c)
            pred_details.append(f"{c}:{prob:.1%} (>{thresh:.3f})")
            
        print(f"ID: {row['ecg_id']} | GT: {gts} | Pred: {pred_actives} | Details: {', '.join(pred_details)}")
        
        results.append({
            'ecg_id': row['ecg_id'],
            'filename_lr': row['filename_lr'],
            'gt': gts,
            'pred': pred_actives,
            'correct': set(gts) == set(pred_actives)
        })
