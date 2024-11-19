import pandas as pd  


# อ่านข้อมูลจากไฟล์ CSV ที่ชื่อ 'randomname.csv' และเก็บไว้ในตัวแปร df
df = pd.read_csv('randomname.csv')  

# ตรวจสอบแถวที่มีข้อมูลซ้ำในคอลัมน์ 'รหัสประจำตัว'
# คืนค่าเป็น Series ของ True/False โดย True หมายถึงแถวที่ซ้ำ
print(df.duplicated(subset='รหัสประจำตัว'))

# ลบแถวที่ซ้ำในคอลัมน์ 'รหัสประจำตัว' โดยเก็บแค่แถวแรกที่พบ
# ผลลัพธ์จะเป็น DataFrame ใหม่ที่ไม่มีข้อมูลซ้ำในคอลัมน์ 'รหัสประจำตัว'
print(df.drop_duplicates(subset='รหัสประจำตัว'))
