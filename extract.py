import requests
import json
import time
import os
from dotenv import load_dotenv

# Load các biến từ file .env
load_dotenv()


def fetch_real_estate_data(keyword, max_pages=5):
    print(f"Đang bắt đầu cào dữ liệu cho từ khóa: {keyword}...")
    all_listings = []

    url = os.getenv("CHOTOT_API_URL", "https://gateway.chotot.com/v1/public/ad-listing")
    user_agent = os.getenv("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

    headers = {
        "User-Agent": user_agent,
        "Accept": "application/json",
    }

    for page in range(1, max_pages + 1):
        print(f"Đang cào trang {page}...")
        params = {
            "cg": "1000",  # Mã danh mục bất động sản
            "q": keyword,
            "o": (page - 1) * 20,
            "limit": 20,
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            listings = data.get("ads", [])

            if not listings:
                print("Không còn tin nào để cào.")
                break
            all_listings.extend(listings)

            time.sleep(1)
        except requests.exceptions.RequestException as e:
            print(f"Lỗi khi cào dữ liệu: {e}")
            break
    return all_listings


def save_to_json(data, filename):
    if not data:
        print("Không có dữ liệu để lưu.")
        return
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Đã lưu thành công {len(data)} bản ghi vào file {filename}!")


def main():
    search_keyword = os.getenv("SEARCH_KEYWORD", "vinhomes smart city")
    properties = fetch_real_estate_data(keyword=search_keyword, max_pages=5)
    save_to_json(properties, "vinhomes_smart_city_listings.json")


if __name__ == "__main__":
    main()
