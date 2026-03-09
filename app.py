import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# 1. Cấu hình trang Dashboard
st.set_page_config(page_title="BĐS Price Dashboard", layout="wide")
st.title("📊 Real-time Real Estate Price Tracker")
st.markdown("Dự án theo dõi giá chung cư Vinhomes Smart City - Tây Mỗ")


# 2. Hàm kết nối Database sử dụng Secrets
def get_connection():
    try:
        # Lấy thông tin từ mục Secrets trên Streamlit Cloud
        db_config = st.secrets["postgres"]

        # Tạo chuỗi kết nối chuẩn PostgreSQL
        conn_url = (
            f"postgresql://{db_config['username']}:{db_config['password']}"
            f"@{db_config['host']}:{db_config['port']}/{db_config['database']}"
        )

        # pool_pre_ping giúp kiểm tra kết nối còn sống hay không trước khi truy vấn
        engine = create_engine(conn_url, pool_pre_ping=True)
        return engine
    except Exception as e:
        st.error(f"❌ Không thể cấu hình chuỗi kết nối: {e}")
        return None


# 3. Hàm đọc dữ liệu
def load_data():
    engine = get_connection()
    if engine:
        try:
            # Sửa lại tên bảng (table_name) đúng với bảng trong Database của bạn
            query = "SELECT * FROM bds_prices ORDER BY scraped_at DESC"
            df = pd.read_sql(query, engine)
            return df
        except Exception as e:
            st.error(f"❌ Lỗi truy vấn dữ liệu: {e}")
            return None
    return None


# 4. Hiển thị dữ liệu lên Giao diện
data = load_data()

if data is not None and not data.empty:
    # Hiển thị các chỉ số tổng quan (Metrics)
    col1, col2, col3 = st.columns(3)
    col1.metric("Tổng số tin đăng", len(data))
    col2.metric("Giá trung bình (tỷ)", f"{data['price'].mean():.2f}")
    col3.metric("Diện tích TB (m2)", f"{data['area'].mean():.1f}")

    # Vẽ biểu đồ biến động giá
    st.subheader("📈 Biến động giá theo thời gian")
    fig = px.line(
        data, x="scraped_at", y="price", title="Giá căn hộ qua các lần cào dữ liệu"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Hiển thị bảng dữ liệu chi tiết
    st.subheader("📋 Danh sách dữ liệu chi tiết")
    st.dataframe(data)
else:
    st.warning("⚠️ Hiện tại chưa có dữ liệu trong Database hoặc lỗi kết nối.")
    st.info(
        "Vui lòng kiểm tra lại mục Secrets trên Streamlit Cloud và Whitelist IP trên Database."
    )
