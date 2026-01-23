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
**เป้าหมาย:** เพื่อให้คุณตระหนักถึงการปล่อยคาร์บอนในหนึ่งวัน โดยเปรียบเทียบกับค่าเฉลี่ยของคนไทย (10.4 kgCO2e)
และเรียนรู้วิธีการปรับลดและชดเชยเพื่อโลกที่ยั่งยืน
""")

# --- ส่วนรับข้อมูล ---
col1, col2 = st.columns(2)
with col1:
    st.markdown("#### 🚗 การเดินทาง")
    transport = st.selectbox("พาหนะหลักวันนี้", 
        ["รถยนต์ส่วนตัว (น้ำมัน)", "รถยนต์ไฟฟ้า (EV)", "รถจักรยานยนต์", "รถไฟฟ้า (BTS/MRT)", "รถเมล์", "เดิน/ปั่นจักรยาน"])
    distance = st.number_input("ระยะทาง (กิโลเมตร)", min_value=0.0, step=1.0, value=10.0)
    
    st.markdown("#### 💡 พลังงาน")
    ac_hours = st.slider("เปิดแอร์วันนี้ (ชั่วโมง)", 0, 24, 0)

with col2:
    st.markdown("#### 🍽️ การบริโภคอาหาร (3 มื้อ)")
    food_1 = st.text_input("มื้อเช้า", placeholder="เช่น ข้าวหมูแดง")
    food_2 = st.text_input("มื้อกลางวัน", placeholder="เช่น กะเพราเนื้อวัว")
    food_3 = st.text_input("มื้อเย็น", placeholder="เช่น สลัดผัก")

st.markdown("<br>", unsafe_allow_html=True)

# --- ส่วนประมวลผล ---
if st.button("คำนวณและดูแนวทางจัดการ"):
    # 1. คำนวณคาร์บอน
    ef_map = {
        "รถยนต์ส่วนตัว (น้ำมัน)": 0.218, 
        "รถยนต์ไฟฟ้า (EV)": 0.05, 
        "รถจักรยานยนต์": 0.08, 
        "รถไฟฟ้า (BTS/MRT)": 0.02, 
        "รถเมล์": 0.03, 
        "เดิน/ปั่นจักรยาน": 0
    }
    carbon_transport = distance * ef_map[transport]
    
    def calc_food(text):
        if not text: return 0.0
        t = text.lower()
        if any(x in t for x in ["เนื้อวัว", "เนื้อ", "beef"]): return 7.5
        if any(x in t for x in ["ผัก", "สลัด", "เจ", "มังสวิรัติ"]): return 0.4
        return 1.2
    
    total_food_carbon = calc_food(food_1) + calc_food(food_2) + calc_food(food_3)
    carbon_ac = ac_hours * 0.
