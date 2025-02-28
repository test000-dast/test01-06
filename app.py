import streamlit as st
import pandas as pd
import altair as alt

# ✅ ดูค่า query params ว่า mode=view จริงหรือไม่
st.write("Query Params:", st.query_params)

query_params = st.query_params
mode = query_params.get("mode", [""])[0]  # ถ้าไม่มีให้เป็น ""

st.set_page_config(page_title="Multi-File Dashboard", page_icon="📊", layout="wide")

st.title("📊 Multi-File Dashboard")

# ✅ ใช้ Session State เก็บไฟล์ที่อัปโหลด
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

# ✅ ถ้า mode ไม่ใช่ "view" ให้แสดงตัวอัปโหลดไฟล์
if mode != "view":
    uploaded_files = st.file_uploader(
        "📂 อัปโหลดไฟล์ CSV (หลายไฟล์ได้)", type=["csv"], accept_multiple_files=True
    )
    if uploaded_files:
        st.session_state.uploaded_files = uploaded_files  # เก็บไว้ใน session state
else:
    uploaded_files = st.session_state.uploaded_files  # โหลดจาก session state

if uploaded_files:
    for file in uploaded_files:
        df = pd.read_csv(file)

        if df.empty:
            st.error(f"⚠️ ไฟล์ **{file.name}** ไม่มีข้อมูล!")
            continue

        st.write(f"✅ **ไฟล์: {file.name}**")

        columns = df.columns.tolist()
        x_axis = columns[0]  # ให้ default เป็นคอลัมน์แรก
        y_axis = columns[1] if len(columns) > 1 else None

        if y_axis and pd.api.types.is_numeric_dtype(df[y_axis]):
            df = df.sort_values(by=y_axis, ascending=False)

            st.write(f"### กราฟของ {file.name}")

            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X(x_axis, type="ordinal", sort=df[x_axis].tolist()),
                y=alt.Y(y_axis, type="quantitative")
            ).properties(width=800, height=400)

            st.altair_chart(chart, use_container_width=True)
