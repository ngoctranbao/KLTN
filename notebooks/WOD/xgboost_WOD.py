import pandas as pd
from lazypredict.Supervised import LazyClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
import numpy as np
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score
import matplotlib.pyplot as plt
label_encoder = LabelEncoder()
dataframe = pd.read_csv('./datasets/Dataset_WOD.csv')
dataframe.dropna(inplace=True)
dataframe.rename(columns=lambda x: x.lower(), inplace=True)

dataframe['label'] = label_encoder.fit_transform(dataframe['label'])

x = dataframe.drop(columns=['id', 'label'], axis=1)
y = dataframe['label']
scaler = StandardScaler().fit(x)
x = pd.DataFrame(scaler.transform(x))
# Khởi tạo LazyClassifier
clf = LazyClassifier(verbose=0, ignore_warnings=True, custom_metric=None)

# Sử dụng StratifiedKFold để tạo các fold
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

accuracy_list = []
precision_list = []
recall_list = []
f1_list = []

for train_index, test_index in skf.split(x, y):
    x_train, x_test = x.iloc[train_index], x.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]
    
    # Huấn luyện và dự đoán với LazyClassifier
    models, predictions = clf.fit(x_train, x_test, y_train, y_test)
    
    # Lấy dự đoán tốt nhất (mô hình có accuracy cao nhất)
    best_model = predictions['accuracy'].idxmax()
    y_pred = predictions[best_model]

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')

    accuracy_list.append(accuracy)
    precision_list.append(precision)
    recall_list.append(recall)
    f1_list.append(f1)
average_accuracy = np.mean(accuracy_list)
average_precision = np.mean(precision_list)
average_recall = np.mean(recall_list)
average_f1 = np.mean(f1_list)

std_accuracy = np.std(accuracy_list)
std_precision = np.std(precision_list)
std_recall = np.std(recall_list)
std_f1 = np.std(f1_list)

print("Average Accuracy: ", average_accuracy)
print("Standard Deviation Accuracy: ", std_accuracy)
print("Average Precision: ", average_precision)
print("Standard Deviation Precision: ", std_precision)
print("Average Recall: ", average_recall)
print("Standard Deviation Recall: ", std_recall)
print("Average F1: ", average_f1)
print("Standard Deviation F1: ", std_f1)
