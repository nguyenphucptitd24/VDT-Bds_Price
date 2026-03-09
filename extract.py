import requests
import json
import time


def fetch_real_estate_data(keyword, max_pages=5):
    print(f"Đang bắt đầu cào dữ liệu cho từ khóa: {keyword}...")
    all_listings = []

    url = "https://gateway.chotot.com/v1/public/ad-listing"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json",
    }
    for page in range(1, max_pages + 1):  # Cào 5 trang đầu tiên
        print(f"Đang cào trang {page}...")
        params = {
            "cg": "1000",  # Mã danh mục bất động sản
            "q": keyword,  # Từ khóa tìm kiếm
            "o": (page - 1) * 20,  # Vị trí bắt đầu
            "limit": 20,  # Số tin trên mỗi trang
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Kiểm tra lỗi HTTP
            data = response.json()
            listings = data.get("ads", [])
            if not listings:
                print("Không còn tin nào để cào.")
                break
            all_listings.extend(listings)

            time.sleep(1)  # Tạm dừng giữa các yêu cầu để tránh bị chặn
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
    properties = fetch_real_estate_data(keyword="vinhomes smart city", max_pages=5)
    save_to_json(properties, "vinhomes_smart_city_listings.json")


if __name__ == "__main__":
    main()
