import pandas as pd
import json


def load_json_to_dataframe(json_file):
    print(f"Đang tải dữ liệu từ file {json_file}...")
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        return df
    except FileNotFoundError:
        print(f"File {json_file} không tồn tại.")
        return None


def clean_data(df):
    print("Đang làm sạch dữ liệu...")

    columns_to_keep = [
        "list_id",
        "subject",
        "price",
        "size",
        "rooms",
    ]

    existing_cols = [col for col in columns_to_keep if col in df.columns]
    df_clean = df[existing_cols].copy()

    df_clean = df_clean.dropna(subset=["price", "size"])

    df_clean["price"] = pd.to_numeric(df_clean["price"], errors="coerce")
    df_clean["size"] = pd.to_numeric(df_clean["size"], errors="coerce")

    # xóa dòng lỗi sau khi ép kiểu
    df_clean = df_clean.dropna(subset=["price", "size"])
    df_clean = df_clean.rename(columns={"size": "area_m2"})

    print("Dữ liệu đã được làm sạch.")
    return df_clean


def main():
    df_raw = load_json_to_dataframe("vinhomes_smart_city_listings.json")
    if df_raw is not None:
        df_cleaned = clean_data(df_raw)
        print("\n--- BÁO CÁO DỮ LIỆU ĐÃ LÀM SẠCH ---")
        print(f"Kích thước bảng mới: {df_cleaned.shape}")
        print("\n5 dòng chuẩn bị đưa dữ liệu lên Cloud:")
        print(df_cleaned.head())

        cleaned_filename = "vinhomes_clean.csv"
        df_cleaned.to_csv(cleaned_filename, index=False, encoding="utf-8")
        print(f"\nĐã xuất file sạch ra: {cleaned_filename}")


if __name__ == "__main__":
    main()
