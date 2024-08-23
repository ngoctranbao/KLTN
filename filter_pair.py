import pandas as pd
import argparse

def update_pairs(source_file):
    # Đọc dữ liệu từ file đích (các ID đã tồn tại)
    destination_file = "./datasets/Pairs.csv"
    old_pairs = pd.read_csv(destination_file)
    old_ids = set(old_pairs['id'])

    # Đọc dữ liệu từ nguồn mới
    new_pairs = pd.read_csv(source_file)

    # Lọc ra các ID mới chưa tồn tại trong file đích
    new_pairs_filtered = new_pairs[~new_pairs['id'].isin(old_ids)]

    # Ghi các ID mới vào file đích
    if not new_pairs_filtered.empty:
        new_pairs_filtered.to_csv(destination_file, mode='a', header=False, index=False)

    # Hiển thị kết quả
    print(new_pairs_filtered)

if __name__ == "__main__":
    # Thiết lập phân tích tham số dòng lệnh
    parser = argparse.ArgumentParser(description='Update pairs by adding new ones from a source CSV file.')
    parser.add_argument('-s', '--source', required=True, help='Path to the source CSV file (new pairs).')

    # Phân tích tham số dòng lệnh
    args = parser.parse_args()

    # Gọi hàm update_pairs với source_file từ tham số dòng lệnh
    update_pairs(args.source)
