import streamlit as st
import pandas as pd

# --- 1. ตั้งค่าหน้าตาแอป ---
st.set_page_config(page_title="Thai Carbon Daily Tracker", layout="centered")

# ปรับแต่ง CSS ให้สวยงาม
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    h1 { color: #15803d; text-align: center; }
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #22c55e 0%, #16a34a 100%);
        color: white; border-radius: 12px; border: none; width: 100%; font-weight: bold; height: 3.5em;
    }
    .result-card {
        background: white; padding: 25px; border-radius: 20px; 
        border-top: 10px solid #22c55e; box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        text-align: center;
    }
    .advice-section {
        background: #ffffff; padding: 20px; border-radius: 15px;
        border-left: 5px solid #10b981; margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>🌿 Thai Carbon Daily Tracker</h1>", unsafe_allow_html=True)

st.info("""
**เป้าหมาย:** เพื่อให้คุณตระหนักถึงการปล่อยคาร์บอนในหนึ่งวัน โดยเปรียบเทียบกับค่าเฉลี่ยของคนไทย 
และเรียนรู้วิธีการปรับลดและชดเชยเพื่อโลกที่ยั่งยืน
""")

# --- ส่วนรับข้อมูล ---
col1, col2 = st.columns(2)
with col1:
    st.markdown("#### 🚗 การเดินทาง")
    transport = st.selectbox("พาหนะหลักวันนี้", 
        ["รถยนต์ส่วนตัว (น้ำมัน)", "รถยนต์ไฟฟ้า (EV)", "รถจักรยานยนต์", "รถไฟฟ้า (BTS/MRT)", "รถเมล์", "
