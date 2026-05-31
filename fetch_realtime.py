import os
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def ultimate_full_state_memory():
    url = "https://medata.nhso.go.th/dashboard.viz?ref=wEJcuu5y"
    brain_file = "tableau_brain.json"
    
    is_training = not os.path.exists(brain_file)
    
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    if is_training:
        print("🎓 [โหมดฝึกสอน Full State] ระบบกำลังเปิดหน้าจอให้คุณตั้งค่าฟิลเตอร์...")
    else:
        print("👻 [โหมด Ghost Monitor] บอทมีความจำสมบูรณ์แบบแล้ว กำลังแอบทำงานอยู่นอกจอ...")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        if not is_training:
            # ซ่อนหน้าต่างทะลุนอกจอ
            driver.set_window_position(-3000, 0)
            
        driver.get(url)
        
        # ==========================================
        # 1. โหมดฝึกสอนบอทแบบ Full State
        # ==========================================
        if is_training:
            print("\n========================================================")
            print("🛑 บอทพร้อมเรียนรู้แล้ว! กรุณาทำตามนี้:")
            print("1. ไปที่แท็บ '3-บริการแพทย์แผนไทย'")
            print("2. กดเลือกฟิลเตอร์ให้ครบ (เช่น เลือก 'เขต 6 ระยอง' ก่อน แล้วค่อยเลือก 'สระแก้ว')")
            print("3. รอจนกราฟของสระแก้วขึ้นครบสมบูรณ์")
            print("4. กลับมาที่ Terminal แล้วกดปุ่ม [Enter]")
            print("========================================================\n")
            input("👉 ตั้งค่าหน้าจอเสร็จแล้ว กด [Enter] เพื่อบันทึกสมองแบบ Full State...")
            
            driver.set_script_timeout(30)
            js_train = """
            let callback = arguments[arguments.length - 1];
            let viz = document.querySelector('tableau-viz');
            
            async function extractFullBrain() {
                try {
                    let wb = viz.workbook;
                    let activeSheet = await wb.activateSheetAsync("3-บริการแพทย์แผนไทย");
                    let sheets = activeSheet.worksheets || [activeSheet];
                    
                    let memory = [];
                    // 🌟 กวาดสายตาเก็บฟิลเตอร์ "ทุกตัว" ที่คุณตั้งค่าไว้บนหน้าจอ
                    for (let s of sheets) {
                        let filters = await s.getFiltersAsync();
                        for (let f of filters) {
                            if (f.appliedValues && f.appliedValues.length > 0 && f.appliedValues.length < 50) {
                                let values = f.appliedValues.map(v => v.value);
                                memory.push({
                                    sheet: s.name,
                                    field: f.fieldName,
                                    values: values
                                });
                            }
                        }
                    }
                    
                    if (memory.length === 0) return callback({error: "ไม่พบการตั้งค่าฟิลเตอร์เลย"});
                    callback({success: true, brain: memory});
                } catch(e) { callback({error: e.toString()}); }
            }
            extractFullBrain();
            """
            
            result = driver.execute_async_script(js_train)
            if result.get("error"):
                print(f"❌ ล้มเหลว: {result['error']}")
                return
            
            brain_data = result.get("brain")
            with open(brain_file, "w", encoding="utf-8") as f:
                json.dump(brain_data, f, ensure_ascii=False, indent=2)
            
            print(f"\n✅ บอทจดจำลำดับการกรองแบบ Cascading ได้สมบูรณ์แบบ! ({len(brain_data)} ขั้นตอน):")
            for b in brain_data:
                print(f"   -> ฟิลด์ [{b['field']}] = {b['values']}")
            print("\n🚀 การฝึกสอนเสร็จสิ้น! พิมพ์ python3 fetch_realtime.py อีกครั้งเพื่อเริ่มการรันทำข้อมูลจริงได้เลยครับ")
            return
            
        # ==========================================
        # 2. โหมดทำงานจริง (นำความจำมาเรียงลำดับ)
        # ==========================================
        print("⏳ [1/5] โหลดหน้าเว็บ และเตรียมระบบ (รอ 25 วินาที)...")
        time.sleep(25)
        
        with open(brain_file, "r", encoding="utf-8") as f:
            brain_data = json.load(f)
            
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 0);")
        
        driver.set_script_timeout(300)
        print(f"⚡ [2/5] นำความจำ Full State มาเจาะระบบทีละชั้น (ตามลำดับที่คุณสอน)...")
        
        js_scrape = """
        let callback = arguments[arguments.length - 1];
        let viz = document.querySelector('tableau-viz');
        let brain = BRAIN_PLACEHOLDER;
        
        async function scrape() {
            try {
                if (viz.initializationP) await viz.initializationP;
                let wb = viz.workbook;
                let activeSheet = await wb.activateSheetAsync("3-บริการแพทย์แผนไทย");
                await new Promise(r => setTimeout(r, 6000));
                
                let sheets = activeSheet.worksheets || [activeSheet];
                
                // 🌟 ฉีดความจำแบบขั้นบันได (เขต -> จังหวัด) ป้องกัน API พัง
                for (let b of brain) {
                    let targetSheet = sheets.find(s => s.name === b.sheet);
                    if (targetSheet) {
                        try {
                            await targetSheet.applyFilterAsync(b.field, b.values, "replace");
                            await new Promise(r => setTimeout(r, 2000)); // รอโหลดชั้นต่อไป
                        } catch(e) {}
                    }
                }
                
                // รอให้เซิร์ฟเวอร์คายข้อมูลสระแก้วออกมาครบ
                await new Promise(r => setTimeout(r, 10000)); 
                
                let hospSheet = sheets.find(s => s.name === 's3-proced-chart-hcode-point');
                let servSheet = sheets.find(s => s.name === 's3-proced-compare-point');
                
                if (!hospSheet || !servSheet) return callback({error: "หา Sheet เป้าหมายไม่เจอ Tableau โหลดไม่ทัน"});
                
                let baseHospData = await hospSheet.getSummaryDataAsync({maxRows: 0});
                let hospitals = baseHospData.data.map(r => r[0].formattedValue || r[0].value);
                
                let targetList = [
                    "บ้านโรงเรียน", "ทับพริก", "หนองปรือ", "ผ่านศึก", "บ้านใหม่หนองไทร", 
                    "คลองทับจันทร์", "นิคมสร้างตนเองคลองน้ำใส", "หันทราย", "คลองน้ำใส", 
                    "ป่าไร่", "ฟากห้วย", "เมืองไผ่", "คลองหว้า", "หนองสังข์", "ภูน้ำเกลี้ยง", "ท่าข้าม"
                ];
                
                let result = {
                    hospitals_base: baseHospData.data.map(r => r.map(c => c.formattedValue || c.value)),
                    relations: {},
                    debug_count: hospitals.length
                };
                
                for (let i = 0; i < hospitals.length; i++) {
                    let hName = hospitals[i];
                    if (!targetList.some(t => hName.includes(t))) continue;
                    
                    try {
                        let hFilterName = "Hname";
                        let sFilters = await servSheet.getFiltersAsync();
                        for(let hf of sFilters) {
                            if(hf.fieldName.toLowerCase().includes("hname") || hf.fieldName.includes("หน่วยบริการ")) {
                                hFilterName = hf.fieldName; break;
                            }
                        }
                        
                        await servSheet.applyFilterAsync(hFilterName, [hName], "replace");
                        await new Promise(r => setTimeout(r, 1200));
                        let filteredServ = await servSheet.getSummaryDataAsync({maxRows: 0});
                        result.relations[hName] = filteredServ.data.map(r => r.map(c => c.formattedValue || c.value));
                    } catch(e) { }
                }
                
                callback({success: true, data: result});
                
            } catch (err) {
                callback({error: err.message || err.toString()});
            }
        }
        scrape();
        """.replace("BRAIN_PLACEHOLDER", json.dumps(brain_data))
        
        result = driver.execute_async_script(js_scrape)
        
        if result.get("error"):
            print(f"❌ [Error จาก JS]: {result['error']}")
            return
            
        print("⚙️ [3/5] ดึงข้อมูลดิบเสร็จสิ้น! กำลังประกอบร่างฐานข้อมูล...")
        data_payload = result.get("data", {})
        print(f"📌 [Debug Info] สแกนพบสถานพยาบาลทั้งหมด: {data_payload.get('debug_count', 0)} แห่ง (ถ้าเกิน 100 คือเจาะระบบสำเร็จ!)")
        
        target_keywords = [
            "บ้านโรงเรียน", "ทับพริก", "หนองปรือ", "ผ่านศึก", "บ้านใหม่หนองไทร", 
            "คลองทับจันทร์", "นิคมสร้างตนเองคลองน้ำใส", "หันทราย", "คลองน้ำใส", 
            "ป่าไร่", "ฟากห้วย", "เมืองไผ่", "คลองหว้า", "หนองสังข์", "ภูน้ำเกลี้ยง", "ท่าข้าม"
        ]

        hospitals_dict = { kw: {"name": f"รพ.สต. {kw}", "points": 0, "amount": 0, "services": []} for kw in target_keywords }
        services_dict = {}

        found = 0
        for row in data_payload.get("hospitals_base", []):
            if len(row) >= 2:
                name = str(row[0]).strip()
                for keyword in target_keywords:
                    if keyword in name:
                        points = int(str(row[1]).replace(',', '').split('.')[0])
                        hospitals_dict[keyword]["name"] = name
                        hospitals_dict[keyword]["points"] = points
                        hospitals_dict[keyword]["amount"] = points
                        found += 1
                        break

        relations = data_payload.get("relations", {})
        for hName, sRows in relations.items():
            for keyword in target_keywords:
                if keyword in hName:
                    for row in sRows:
                        if len(row) >= 2:
                            s_name = str(row[0]).strip()
                            s_points = int(str(row[1]).replace(',', '').split('.')[0])
                            if s_points > 0 and s_name != "None":
                                hospitals_dict[keyword]["services"].append({
                                    "name": s_name, "points": s_points, "amount": s_points
                                })
                                if s_name not in services_dict:
                                    services_dict[s_name] = {"name": s_name, "points": 0, "amount": 0}
                                services_dict[s_name]["points"] += s_points
                                services_dict[s_name]["amount"] += s_points
                    break

        hospitals_clean = list(hospitals_dict.values())
        for h in hospitals_clean:
            h["services"].sort(key=lambda x: x['points'], reverse=True)
        hospitals_clean.sort(key=lambda x: x['points'], reverse=True)

        services_clean = list(services_dict.values())
        services_clean.sort(key=lambda x: x['points'], reverse=True)

        total_points = sum(h['points'] for h in hospitals_clean)
        final_json = {
            "overview": {"total_points": total_points, "total_amount": total_points},
            "services": services_clean,
            "hospitals": hospitals_clean
        }
        
        os.makedirs("public", exist_ok=True)
        with open("public/data.json", "w", encoding="utf-8") as f:
            json.dump(final_json, f, ensure_ascii=False, indent=2)
            
        print(f"✅ [4/5] บันทึกข้อมูลลง public/data.json เรียบร้อย!")
        print(f"🎯 [5/5] ค้นพบเป้าหมายเครือข่ายที่มีผลงานแล้ว {found}/16 แห่ง")
        print(f"💰 ยอดรวมเครือข่ายอัปเดตล่าสุด: {total_points:,} Point")

    except Exception as e:
        print(f"❌ Error ร้ายแรง: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    ultimate_full_state_memory()