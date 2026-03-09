import pandas as pd
from sqlalchemy import create_engine


def get_db_engine(db_uri):
    print(f"Đang kết nối đến cơ sở dữ liệu với URI: {db_uri}...")
    try:
        engine = create_engine(db_uri)
        return engine
    except Exception as e:
        print(f"Không thể kết nối đến cơ sở dữ liệu: {e}")
        return None


def main():
    DB_URI = "postgresql://postgres:phuc12a2k44%40%40@db.arakuwmtpefdhwcbvdgv.supabase.co:5432/postgres"
    engine = get_db_engine(DB_URI)
    if engine:
        print("Đang đọc dữ liệu sạch từ file CSV...")
        try:
            df = pd.read_csv("vinhomes_clean.csv")
            print(f"Bắt đầu đẩy {len(df)} dòng dữ liệu lên Cloud...")
            df.to_sql("properties", engine, if_exists="replace", index=False)
            print("Dữ liệu đã được đẩy lên Cloud thành công!")
        except Exception as e:
            print(f"Đã xảy ra lỗi khi đọc file CSV hoặc đẩy dữ liệu lên Cloud: {e}")


if __name__ == "__main__":
    main()
