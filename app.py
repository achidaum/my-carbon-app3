import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime

# --- 1. ตั้งค่าหน้าตาแอป ---
st.set_page_config(page_title="Thai Carbon Daily Tracker", layout="wide")

# เชื่อมต่อ Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# ปรับแต่ง CSS ให้สวยงามและทันสมัย
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    h1 { color: #15803d; text-align: center; font-family: 'Sarabun', sans-serif; }
    .stNumberInput, .stSelectbox, .stTextInput { border-radius: 10px; }
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #22c55e 0%, #16a34a 100%);
        color: white; border-radius: 15px; border: none; width: 100%; font-weight: bold; height: 3.5em; font-size: 18px;
        box-shadow: 0 4px 15px rgba(22, 163, 74, 0.2);
    }
    .result-card {
        background: white; padding: 30px; border-radius: 25px; 
        border-top: 8px solid #22c55e; box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        text-align: center;
    }
    .food-section { background: #f0fdf4; padding: 20px; border-radius: 15px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>🌿 Thai Carbon Daily Tracker</h1>", unsafe_allow_html=True)
st.caption("<center>บันทึกพฤติกรรมประจำวันเพื่อโลกที่ยั่งยืน (อิงเกณฑ์ค่าเฉลี่ยประชากรไทย)</center>", unsafe_allow_html=True)

# --- ส่วนรับข้อมูล ---
with st.container():
    col_a, col_b = st.columns([1, 1], gap="large")
    
    with col_a:
        st.markdown("### 🚗 การเดินทางและการใช้ไฟ")
        transport = st.selectbox("✈️ ประเภทพาหนะหลักวันนี้", 
            ["รถยนต์ส่วนตัว (น้ำมัน)", "รถยนต์ไฟฟ้า (EV)", "รถจักรยานยนต์", "รถไฟฟ้า (BTS/MRT)", "รถเมล์", "เดิน/ปั่นจักรยาน"])
        distance = st.number_input("📍 ระยะทางรวม (กิโลเมตร)", min_value=0.0, step=0.5, value=10.0)
        ac_hours = st.slider("❄️ เปิดเครื่องปรับอากาศรวม (ชั่วโมง)", 0, 24, 8)

    with col_b:
        st.markdown("### 🍽️ การบริโภคอาหาร (3 มื้อ)")
        with st.expander("คลิกเพื่อระบุเมนูอาหาร", expanded=True):
            food_1 = st.text_input("🍳 มื้อเช้า", placeholder="เช่น ข้าวเหนียวหมูปิ้ง")
            food_2 = st.text_input("🍜 มื้อกลางวัน", placeholder="เช่น ก๋วยเตี๋ยวไก่")
            food_3 = st.text_input("🍱 มื้อเย็น", placeholder="เช่น สลัดผัก หรือ ข้าวผัดเนื้อวัว")

st.markdown("<br>", unsafe_allow_html=True)

# --- ส่วนคำนวณ Logic ---
if st.button("คำนวณผลลัพธ์และบันทึกข้อมูล"):
    # 1. คำนวณคาร์บอนเดินทาง
    ef_map = {"รถยนต์ส่วนตัว (น้ำมัน)": 0.218, "รถยนต์ไฟฟ้า (EV)": 0.05, "รถจักรยานยนต์": 0.08, "รถไฟฟ้า (BTS/MRT)": 0.02, "รถเมล์": 0.03, "เดิน/ปั่นจักรยาน": 0}
    carbon_transport = distance * ef_map[transport]
    
    # 2. คำนวณคาร์บอนอาหาร (แยก 3 มื้อ)
    def calc_food(text):
        if not text: return 0.0
        text = text.lower()
        if any(x in text for x in ["เนื้อวัว", "เนื้อ", "beef"]): return 7.5
        if any(x in text for x in ["ผัก", "สลัด", "เจ", "มังสวิรัติ"]): return 0.4
        return 1.2 # ค่าเฉลี่ย หมู/ไก่/ไข่
    
    carbon_food = calc_food(food_1) + calc_food(food_2) + calc_food(food_3)
    
    # 3. คำนวณคาร์บอนไฟฟ้า
    carbon_ac = ac_hours * 0.51
    
    # 4. ยอดรวม
    total = carbon_transport + carbon_food + carbon_ac

    # --- บันทึกลง Google Sheets ---
    try:
        new_row = pd.DataFrame([{
            "Date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Transport": transport,
            "Distance": distance,
            "Food_Morning": food_1,
            "Food_Lunch": food_2,
            "Food_Dinner": food_3,
            "AC_Hours": ac_hours,
            "Total_Carbon": round(total, 2)
        }])
        existing_data = conn.read(worksheet="Sheet1")
        updated_df = pd.concat([existing_data, new_row], ignore_index=True)
        conn.update(worksheet="Sheet1", data=updated_df)
        st.toast("บันทึกข้อมูลสำเร็จ!", icon="✅")
    except:
        st.warning("บันทึกลง Sheet ไม่สำเร็จ (โปรดเช็คการเชื่อมต่อ)")

    # --- ส่วนแสดงผลเกณฑ์วัด (อิงค่าเฉลี่ยไทย 10.4 kg/วัน) ---
    st.markdown("---")
    col_res1, col_res2, col_res3 = st.columns([1, 2, 1])
    with col_res2:
        st.markdown(f"""
            <div class="result-card">
                <p style="color: #64748b; font-size: 18px; margin-bottom: 5px;">ปริมาณคาร์บอนของคุณวันนี้</p>
                <h1 style="font-size: 60px; margin: 0; color: #16a34a;">{total:.2f} <span style="font-size: 24px;">kgCO2e</span></h1>
                <p style="color: #94a3b8;">ค่าเฉลี่ยคนไทยอยู่ที่ประมาณ 10.4 - 11.0 kg ต่อวัน</p>
            </div>
        """, unsafe_allow_html=True)

        if total <= 6.0:
            st.success("🟢 **ระดับ: ดีเยี่ยม (Low Carbon)** - คุณใช้ชีวิตได้เป็นมิตรต่อโลกมาก! ต่ำกว่าค่าเฉลี่ยประเทศอย่างมีนัยสำคัญ")
        elif total <= 11.0:
            st.warning("🟡 **ระดับ: ปานกลาง (Average)** - คุณอยู่ในเกณฑ์มาตรฐานของคนไทยทั่วไป พยายามลดการใช้ไฟหรือเนื้อวัวจะช่วยได้มากขึ้น")
        else:
            st.error("🚨 **ระดับ: ปล่อยก๊าซสูง (High Carbon)** - วันนี้คุณปล่อยคาร์บอนสูงกว่าค่าเฉลี่ยคนไทย ควรพยายามปรับลดกิจกรรมบางส่วน")

st.markdown("<br><hr>", unsafe_allow_html=True)
st.caption("🔍 **เกณฑ์อ้างอิง:** ค่าเฉลี่ยการปล่อยก๊าซเรือนกระจกรายบุคคลของประเทศไทย (ปี 2567-2568) ประมาณ 3.8 - 4.0 ตัน/ปี หรือเฉลี่ยวันละ 10.4 - 11.0 kgCO2e อ้างอิงสถิติจาก TGO และ Worldometer")
