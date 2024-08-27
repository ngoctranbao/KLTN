import pandas as pd
import glob

# Chỉ định các file CSV muốn gộp
csv_files = [
    "./datasets/Dataset_v1.6.csv",
    "./datasets/Dataset_v1.7.csv",
    "./datasets/Dataset_v1.8.csv",
    "./datasets/Dataset_v1.9.csv"
]

# Đọc và gộp tất cả các file CSV
combined_df = pd.concat((pd.read_csv(f) for f in csv_files), ignore_index=True)

# Loại bỏ các bản ghi trùng id, giữ lại bản ghi cuối cùng
combined_df = combined_df.drop_duplicates(subset='id', keep='last')

# Lưu DataFrame sau khi đã loại bỏ bản ghi trùng lặp
combined_df.to_csv('./datasets/combined_dataset.csv', index=False)