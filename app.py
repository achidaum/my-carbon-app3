# 2. คำนวณคาร์บอนอาหาร
food_carbon = 1.2  # ค่าเริ่มต้น (Default) สำหรับอาหารทั่วไป
food_category = "เนื้อสัตว์ทั่วไป (หมู/ไก่/ปลา/ไข่)"
is_beef = False
food_text = food_input.lower()

if "เนื้อวัว" in food_text:
    food_carbon = 7.5
    food_category = "เนื้อวัว (ปศุสัตว์ขนาดใหญ่)"
    is_beef = True
elif any(x in food_text for x in ["ผัก", "สลัด", "เจ", "มังสวิรัติ", "ผลไม้"]):
    food_carbon = 0.4
    food_category = "พืชผัก/มังสวิรัติ"
