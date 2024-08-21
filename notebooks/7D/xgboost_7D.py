from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from xgboost import XGBClassifier
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score
import numpy as np

label_encoder = LabelEncoder()
dataframe = pd.read_csv('./../../datasets/Dataset_7D.csv')
dataframe.dropna(inplace=True)
dataframe.rename(columns=lambda x: x.lower(), inplace=True)

dataframe['label'] = label_encoder.fit_transform(dataframe['label'])

x = dataframe.drop(columns=['id', 'label', 'number_of_token_creation_of_creator', 'token_creator_holding_ratio', 'lp_lock_ratio', 'lp_creator_holding_ratio'], axis=1)
y = dataframe['label']
scaler = StandardScaler().fit(x)
x = pd.DataFrame(scaler.transform(x))

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
accuracy_list = []
precision_list = []
recall_list = []
f1_list = []

for train_index, test_index in skf.split(x, y):
    x_train, x_test = x.iloc[train_index], x.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]

    xgboost_model = XGBClassifier(objective="binary:logistic", n_estimators=20, random_state=42, eval_metric=["auc", "error", "error@0.6"])
    xgboost_model.fit(x_train, y_train, eval_set=[(x_test, y_test)], verbose=False)

    y_pred = xgboost_model.predict(x_test)

    accuracy = accuracy_score(y_pred, y_test)
    precision = precision_score(y_pred, y_test)
    recall = recall_score(y_pred, y_test)
    f1 = f1_score(y_pred, y_test)

    accuracy_list.append(accuracy)
    precision_list.append(precision)
    recall_list.append(recall)
    f1_list.append(f1)

average_accuracy = sum(accuracy_list) / len(accuracy_list)
average_precision = sum(precision_list) / len(precision_list)
average_recall = sum(recall_list) / len(recall_list)
average_f1 = sum(f1_list) / len(f1_list)

average_accuracy = sum(accuracy_list) / len(accuracy_list)
average_precision = sum(precision_list) / len(precision_list)
average_recall = sum(recall_list) / len(recall_list)
average_f1 = sum(f1_list) / len(f1_list)

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

import matplotlib.pyplot as plt

# Tạo mảng chứa số fold
folds = range(1, len(accuracy_list) + 1)

# Định dạng plot
plt.figure(figsize=(10, 6))

# Vẽ đường kết quả cho từng fold
plt.plot(folds, accuracy_list, marker='o', label='Accuracy')
plt.plot(folds, precision_list, marker='o', label='Precision')
plt.plot(folds, recall_list, marker='o', label='Recall')
plt.plot(folds, f1_list, marker='o', label='F1')

# Chú thích và nhãn
plt.xlabel('Fold')
plt.ylabel('Score')
plt.title('Scores for each fold')
plt.xticks(folds)
plt.legend()
plt.grid(True)

# Hiển thị plot
plt.show()
plt.savefig('scores_plot.png')