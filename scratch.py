import tensorflow as tf
import numpy as np
import pandas as pd
import json
import os
import wfdb
import scipy.signal as signal

def preprocess_ecg_signal(record_path):
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

metadata_path = '/Users/felipedeleon/Desktop/Deep Ler,Project/data/unseen_demo_metadata.csv'
df = pd.read_csv(metadata_path)

patients = [14102, 18118]
model_path = '/Users/felipedeleon/Desktop/Deep Ler,Project/models/multiclass_1d_ecg_model.h5'
multiclass_model = tf.keras.models.load_model(model_path, compile=False)

thresh_path = '/Users/felipedeleon/Desktop/Deep Ler,Project/models/multiclass_thresholds_cnn.json'
with open(thresh_path, 'r') as f:
    thresholds = json.load(f)

classes = ['NORM', 'MI', 'STTC', 'CD', 'HYP']

for p in patients:
    row = df[df['patient_id'] == p].iloc[0]
    filename = row['filename_lr']
    print(f"\nPatient {p} (ECG {row['ecg_id']})")
    print(f"Ground Truth: NORM={row['label_NORM']}, MI={row['label_MI']}, STTC={row['label_STTC']}, CD={row['label_CD']}, HYP={row['label_HYP']}")
    print(f"Report: {row['report']}")
    
    record_path = os.path.join('/Users/felipedeleon/Desktop/Deep Ler,Project/data/raw', filename)
    norm_sig = preprocess_ecg_signal(record_path)
    input_batch = tf.expand_dims(norm_sig, 0)
    
    predictions = multiclass_model.predict(input_batch)[0]
    
    for c, prob in zip(classes, predictions):
        cutoff = thresholds.get(c, 0.5)
        print(f"  {c}: {prob:.4f} (Cutoff: {cutoff:.4f}) -> {'POSITIVE' if prob >= cutoff else 'NEGATIVE'}")
