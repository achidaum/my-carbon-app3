import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime

# 1. ตั้งค่าหน้าตาแอป
st.set_page_config(page_title="Carbon Tracker Pro", layout="centered")

# 2. เชื่อมต่อ Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. ปรับแต่งดีไซน์ด้วย CSS
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); }
    h1 { color: #065f46 !important; text-align: center; }
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #10b981 0%, #059669 100%);
        color: white; border-radius: 12px; border: none; width: 100%; font-weight: bold; height: 3em;
    }
    .result-card {
        background: white; padding: 25px; border-radius: 20px; 
        border-left: 10px solid #10b981; box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>🌿 Carbon Daily Tracker</h1>", unsafe_allow_html=True)

st.info("""
**เป้าหมายของกิจกรรมนี้:** เพื่อให้คุณได้ตระหนักถึงผลกระทบจากการใช้ชีวิตประจำวัน 
และร่วมกันปรับลดการปล่อยก๊าซเรือนกระจกเพื่ออนาคตที่ยั่งยืน
""")

# --- ส่วนรับข้อมูลจากผู้ใช้ ---
col1, col2 = st.columns(2)
with col1:
    st.markdown("#### 🚗 การเดินทาง")
    transport = st.selectbox("เลือกประเภทพาหนะ", 
        ["รถยนต์ส่วนตัว (น้ำมัน)", "รถยนต์ไฟฟ้า (EV)", "รถจักรยานยนต์", "รถไฟฟ้า (BTS/MRT)", "รถเมล์", "เดิน/ปั่นจักรยาน"])
    distance = st.number_input("ระยะทาง (กิโลเมตร)", min_value=0.0, step=1.0)
with col2:
    st.markdown("#### 🍔 อาหาร")
    food_input = st.text_input("วันนี้ทานเมนูอะไร?", placeholder="เช่น ข้าวกะเพราเนื้อวัว")
    st.markdown("#### 💡 พลังงาน")
    ac_hours = st.slider("เปิดแอร์กี่ชั่วโมง?", 0, 24, 0)

st.markdown("<br>", unsafe_allow_html=True)

# --- ส่วนประมวลผล ---
if st.button("ประเมินผลลัพธ์"):
    # 1. คำนวณคาร์บอนการเดินทาง
    ef_map = {
        "รถยนต์
