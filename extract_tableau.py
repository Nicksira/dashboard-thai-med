from tableauscraper import TableauScraper as TS
import json

# 1. วางลิงก์ Tableau ที่ได้จากการกดปุ่ม Share ลงที่นี่
tableau_url = "วางลิงก์_TABLEAU_ตรงนี้"

print("กำลังเจาะระบบ Session และดาวน์โหลดโครงสร้างข้อมูลระดับ Enterprise...")
ts = TS()
ts.loads(tableau_url)
workbook = ts.getWorkbook()

print(f"เจาะระบบสำเร็จ! พบตารางข้อมูลซ่อนอยู่ทั้งหมด {len(workbook.worksheets)} ชุด\n")

# 2. กวาดข้อมูลจากทุก Worksheet ที่ซ่อนอยู่ออกมาแสดง
for sheet in workbook.worksheets:
    print(f"--- 📊 ชื่อตาราง: {sheet.name} ---")
    
    # ข้อมูลที่ถูกดึงออกมาจะอยู่ในรูปแบบ Pandas DataFrame (ตารางคลีน 100%)
    data = sheet.data
    print(data.head()) # พรีวิวข้อมูล 5 บรรทัดแรก
    print("-" * 50)
    
    # 3. (เสริม) หากคุณเจอชื่อตารางของอำเภอสระแก้ว สามารถสั่งให้บอทเซฟเป็น JSON อัตโนมัติได้
    # เพียงเปลี่ยนคำว่า "ชื่อตารางอำเภอ" ให้ตรงกับ sheet.name ที่มีข้อมูล
    if sheet.name == "ชื่อตารางอำเภอ":
        # บันทึกเป็น data.json เพื่อนำไปเชื่อมกับ React + Cloudflare 
        data.to_json("public/data.json", orient="records", force_ascii=False)
        print(f"✅ บันทึกฐานข้อมูลของ {sheet.name} ลงไฟล์ data.json สำเร็จ!")