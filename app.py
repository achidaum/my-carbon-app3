import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. ตั้งค่าการเชื่อมต่อและ Page
st.set_page_config(page_title="Carbon Tracker Pro", layout="centered")
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. ดีไซน์ CSS
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); }
    .stAlert { border-radius: 15px; background-color: rgba(255, 255, 255, 0.7); }
    h1 { color: #065f46 !important; text-align: center; }
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #10b981 0%, #059669 100%);
        color: white; border-radius: 12px; border: none; width: 100%; font-weight: bold; height: 3em;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>🌿 Carbon Daily Tracker</h1>", unsafe_allow_html=True)

st.info("""
**ที่มาของโปรเจกต์:** รายงานฉบับนี้จัดทำขึ้นภายใต้โครงการการประเมินและส่งเสริมการลดก๊าซเรือนกระจกระดับบุคคล 
เพื่อสร้างความ **"ตระหนัก"** รู้และเป็นเครื่องมือช่วยให้บุคคลทั่วไปประเมินการปล่อยก๊าซเรือนกระจก 
อ้างอิงฐานข้อมูลจาก **อบก.** เพื่อนำไปสู่การ **"ชดเชย"** หรือปรับลดในอนาคต
""")

# --- ส่วนรับข้อมูล ---
col1, col2 = st.columns(2)
with col1:
    transport = st.selectbox("เลือกประเภทพาหนะ", 
        ["รถยนต์ส่วนตัว (น้ำมัน)", "รถยนต์ไฟฟ้า (EV)", "รถจักรยานยนต์", "รถไฟฟ้า", "รถเมล์", "เดิน/ปั่นจักรยาน"])
    distance = st.number_input("ระยะทาง (กิโลเมตร)", min_value=0.0)
with col2:
    food_input = st.text_input("เมนูอาหารวันนี้", placeholder="เช่น ข้าวกะเพราเนื้อวัว")
    ac_hours = st.slider("เปิดแอร์ (ชม.)", 0, 12, 0)

# --- ส่วนประมวลผล ---
if st.button("ประเมินผลลัพธ์"):
    # คำนวณเบื้องต้น
    ef_map = {"รถยนต์ส่วนตัว (น้ำมัน)": 0.218, "รถยนต์ไฟฟ้า (EV)": 0.05, "รถจักรยานยนต์": 0.08, "รถไฟฟ้า": 0.02, "รถเมล์": 0.03, "เดิน/ปั่นจักรยาน": 0}
    food_carbon = 7.5 if "เนื้อวัว" in food_input else 1.2
    total = (distance * ef_map[transport]) + food_carbon + (ac_hours * 0.51)
    
    # แสดงผล Card (ปิดเครื่องหมายคำพูดครบถ้วน)
    st.markdown(f"""
        <div style="background: white; padding: 25px; border-radius: 20px; border-left: 10px solid #10b981; box-shadow: 0 10px 25px rgba(0,0,0,0.05);">
            <h3 style="margin:0; color: #4b5563;">ปริมาณคาร์บอนรวมวันนี้</h3>
            <h1 style="margin:0; color: #10b981; font-size: 45px;">{total:.2f} <span style="font-size: 20px; color: #9ca3af;">kgCO2e</span></h1>
            <hr>
            <p style="color: #6b7280; font-size: 14px;"><b>🍴 เมนู:</b> {food_input if food_input else 'ไม่ระบุ'}</p>
        </div>
    """, unsafe_allow_html=True)

    # --- บันทึกข้อมูลลง Google Sheets ---
    try:
        new_row = pd.DataFrame([{
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Transport": transport,
            "Food": food_input if food_input else "ไม่ระบุ",
            "Carbon": round(total, 2)
        }])
        df = conn.read(worksheet="Sheet1", ttl=0)
        updated_df = pd.concat([df, new_row], ignore_index=True)
        conn.update(worksheet="Sheet1", data=updated_df)
        st.toast("📊 บันทึกข้อมูลสำเร็จ!")
    except Exception as e:
        st.warning(f"⚠️ บันทึกไม่ได้: {e}")
