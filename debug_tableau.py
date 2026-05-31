import requests
import urllib3
from tableauscraper import TableauScraper as TS

# ปิดการแจ้งเตือน SSL สีแดงบน Terminal
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def xray_tableau():
    # 💡 จุดตายอยู่ตรงนี้! ต้องเติมพารามิเตอร์บังคับเข้าโหมด Embed 
    url = "https://bi.nhso.go.th/views/NEW2568_/1-?:embed=y&:showVizHome=no"
    
    print("กำลังเจาะเกราะเข้าสู่โหมด Embed และข้ามระบบ SSL ของ สปสช. ...")
    
    session = requests.Session()
    # ทะลวงกำแพงใบรับรองความปลอดภัย (SSL Certificate)
    session.verify = False 
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    })
    
    ts = TS()
    ts.session = session
    
    try:
        ts.loads(url)
        workbook = ts.getWorkbook()
        
        print(f"\n✅ ทะลวงสำเร็จ! พบชีตข้อมูลทั้งหมด {len(workbook.worksheets)} ชีต\n")
        
        for ws in workbook.worksheets:
            print(f"📊 ชื่อตาราง (Worksheet): {ws.name}")
            if not ws.data.empty:
                print("รายชื่อคอลัมน์:", ws.data.columns.tolist())
                print("ตัวอย่างข้อมูล:")
                print(ws.data.iloc[0].to_dict())
            else:
                print("ตารางว่าง (Empty)")
            print("=" * 60)
            
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาด: {str(e)}")

if __name__ == "__main__":
    xray_tableau()