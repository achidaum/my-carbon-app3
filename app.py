<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Carbon Footprint Calculator</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Kanit', sans-serif; background-color: #f0fdf4; }
        .card { background: white; border-radius: 1.5rem; box-shadow: 0 10px 25px rgba(0,0,0,0.05); }
    </style>
</head>
<body class="p-4 md:p-8">

    <div class="max-w-2xl mx-auto">
        <header class="text-center mb-8">
            <h1 class="text-3xl font-bold text-green-700">“มาดูกันว่าวันนี้คุณปล่อยคาร์บอนเท่าไหร่?”</h1>
            <p class="text-gray-500 mt-2 text-sm">*อ้างอิงเกณฑ์การคำนวณจาก อบก. (TGO)</p>
        </header>

        <div class="card p-6 mb-6">
            <section class="mb-8">
                <h3 class="text-xl font-semibold text-green-600 mb-4">🚗 1. การเดินทาง</h3>
                <div class="space-y-4">
                    <label class="block text-sm font-medium">เลือกประเภทพาหนะ:</label>
                    <select id="transportType" class="w-full p-3 border rounded-xl bg-gray-50">
                        <option value="car_fuel">รถยนต์ส่วนตัว (น้ำมัน)</option>
                        <option value="car_ev">รถยนต์ไฟฟ้า (EV)</option>
                        <option value="motorcycle">รถจักรยานยนต์</option>
                        <option value="public_train">รถไฟฟ้า (BTS/MRT)</option>
                        <option value="public_bus">รถเมล์</option>
                        <option value="walk">เดิน / ปั่นจักรยาน</option>
                    </select>
                    <label class="block text-sm font-medium">ระยะทางทั้งหมด (กิโลเมตร):</label>
                    <input type="number" id="distance" value="0" class="w-full p-3 border rounded-xl bg-gray-50">
                </div>
            </section>

            <section class="mb-8 border-t pt-6">
                <h3 class="text-xl font-semibold text-green-600 mb-4">🍔 2. การบริโภคอาหาร</h3>
                <div class="space-y-4">
                    <label class="block text-sm font-medium">ประเภทเนื้อสัตว์ที่ทานหลักๆ วันนี้:</label>
                    <select id="foodType" class="w-full p-3 border rounded-xl bg-gray-50">
                        <option value="beef">เนื้อวัว</option>
                        <option value="pork">เนื้อหมู</option>
                        <option value="chicken">เนื้อไก่</option>
                        <option value="fish">เนื้อปลา / ผัก</option>
                    </select>
                    <p class="text-xs text-gray-400">*คำนวณเฉลี่ยต่อมื้อตามมาตรฐาน</p>
                </div>
            </section>

            <section class="mb-8 border-t pt-6">
                <h3 class="text-xl font-semibold text-green-600 mb-4">💡 3. การใช้ไฟฟ้า</h3>
                <div class="space-y-4">
                    <label class="block text-sm font-medium">เปิดแอร์วันนี้กี่ชั่วโมง? (0-12 ชม.):</label>
                    <input type="range" id="acHours" min="0" max="12" value="0" class="w-full h-2 bg-green-200 rounded-lg appearance-none cursor-pointer">
                    <div class="text-center font-bold text-lg"><span id="acValue">0</span> ชั่วโมง</div>
                </div>
            </section>

            <button onclick="calculateCarbon()" class="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-4 rounded-2xl transition duration-300 shadow-lg">
                ประเมินผลลัพธ์
            </button>
        </div>

        <div id="resultCard" class="card p-8 hidden border-2 border-green-500">
            <h2 class="text-2xl font-bold text-center mb-4">ผลการประเมินของคุณ</h2>
            <div class="text-center mb-6">
                <span class="text-5xl font-bold text-green-600" id="totalCarbon">0</span>
                <span class="text-xl text-gray-600 ml-2">kgCO2e/วัน</span>
            </div>

            <div id="recommendations" class="space-y-4 text-gray-700">
                </div>

            <div class="mt-8 pt-6 border-t border-dashed">
                <h4 class="font-bold text-green-700 mb-3">🌿 แนวทางในการชดเชย:</h4>
                <ul class="list-disc pl-5 text-sm space-y-2">
                    <li>ต้นไม้ช่วยดูดซับก๊าซคาร์บอนไดออกไซด์ ลองปลูกเองในบ้าน หรือร่วมกิจกรรมปลูกป่า</li>
                    <li>ซื้อคาร์บอนเครดิตผ่านแพลตฟอร์ม <b>TGO (อบก.)</b> เพื่อสนับสนุนโครงการพลังงานสะอาด</li>
                    <li>เลือกซื้อสินค้าที่มีนโยบาย Net Zero หรือใช้วัสดุรีไซเคิล</li>
                </ul>
            </div>
        </div>
    </div>

    <script>
        const acSlider = document.getElementById('acHours');
        const acOutput = document.getElementById('acValue');
        acSlider.oninput = function() { acOutput.innerHTML = this.value; }

        function calculateCarbon() {
            // ค่าสัมประสิทธิ์ (Emission Factor) อ้างอิง อบก. โดยประมาณ
            const EF = {
                car_fuel: 0.21,    // kgCO2e/km
                car_ev: 0.05,      // kgCO2e/km (คำนวณจากค่าไฟ Grid)
                motorcycle: 0.08,  // kgCO2e/km
                public_train: 0.02,// kgCO2e/km
                public_bus: 0.03,  // kgCO2e/km
                walk: 0,
                beef: 7.5,         // kgCO2e/มื้อ (เฉลี่ย)
                pork: 1.5,         // kgCO2e/มื้อ
                chicken: 0.8,      // kgCO2e/มื้อ
                fish: 0.4,         // kgCO2e/มื้อ
                ac: 0.5            // kgCO2e/ชม (สำหรับแอร์ 12000 BTU)
            };

            const dist = parseFloat(document.getElementById('distance').value) || 0;
            const transType = document.getElementById('transportType').value;
            const foodType = document.getElementById('foodType').value;
            const acHrs = parseInt(document.getElementById('acHours').value);

            const carbonTrans = dist * EF[transType];
            const carbonFood = EF[foodType];
            const carbonAC = acHrs * EF.ac;
            const total = (carbonTrans + carbonFood + carbonAC).toFixed(2);

            document.getElementById('totalCarbon').innerText = total;
            
            let recHtml = `<h4 class="font-bold">💡 คำแนะนำสำหรับคุณ:</h4>`;

            // เงื่อนไขเดินทาง
            if(transType === 'car_fuel') {
                recHtml += `<p class="bg-blue-50 p-3 rounded-lg text-sm">🚗 <b>การเดินทาง:</b> ลองเปลี่ยนมาใช้ขนส่งสาธารณะ หรือเปลี่ยนเป็นรถยนต์ไฟฟ้า (EV)/Hybrid ช่วยลดมลพิษได้โดยตรง</p>`;
            }

            // เงื่อนไขอาหาร
            if(foodType === 'beef') {
                recHtml += `<p class="bg-red-50 p-3 rounded-lg text-sm">🥩 <b>อาหาร:</b> เนื้อวัวปล่อยก๊าซมีเทนสูง ลองเปลี่ยนเป็นโปรตีนจากพืชหรือไก่แทนบ้างนะ</p>`;
            }
            recHtml += `<p class="bg-yellow-50 p-3 rounded-lg text-sm">♻️ <b>เสมอ:</b> ลด Food Waste ทานอาหารให้หมด ช่วยลดการปล่อยมีเทนจากบ่อฝังกลบได้มาก</p>`;

            // เงื่อนไขแอร์
            let acStatus = acHrs <= 4 ? "เกณฑ์ดีมาก" : (acHrs <= 6 ? "เกณฑ์ปานกลาง" : "ปล่อยก๊าซสูง");
            let acColor = acHrs <= 4 ? "text-green-600" : (acHrs <= 6 ? "text-yellow-600" : "text-red-600");
            recHtml += `<p class="bg-gray-50 p-3 rounded-lg text-sm">❄️ <b>การใช้ไฟฟ้า:</b> การเปิดแอร์ ${acHrs} ชม. อยู่ใน <span class="${acColor} font-bold">${acStatus}</span> แนะนำตั้งที่ 25-26 องศา และใช้พัดลมช่วย</p>`;

            document.getElementById('recommendations').innerHTML = recHtml;
            document.getElementById('resultCard').classList.remove('hidden');
            window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
        }
    </script>
</body>
</html>
