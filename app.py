import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.set_page_config(page_title="BĐS Dashboard", layout="wide")

st.title("📊 Dashboard Phân Tích Giá Nhà Vinhomes Smart City")
st.markdown("---")


@st.cache_data
def load_data_from_db():
    DB_URI = "postgresql://postgres:phuc12a2k44%40%40@db.arakuwmtpefdhwcbvdgv.supabase.co:5432/postgres"
    engine = create_engine(DB_URI)

    query = "SELECT * FROM properties"
    df = pd.read_sql(query, engine)
    return df


with st.spinner("Đang đồng bộ dữ liệu từ Supabase Cloud..."):
    df = load_data_from_db()

st.success(f"Đã tải thành công {len(df)} bất động sản từ Cloud Database!")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🗄️ Dữ liệu đã làm sạch (Cleaned Data)")

    st.dataframe(df, use_container_width=True)

with col2:
    st.subheader("📈 Phân bố giá nhà (VND)")
    if "price" in df.columns:
        st.bar_chart(df["price"])
    else:
        st.warning("Không tìm thấy cột 'price' để vẽ biểu đồ.")
