import pandas as pd 
#ถ้าไฟล์ไม่ใช่ UTF-8 ทำไยังไง
df = pd.read_csv('randomname.csv',encoding='utf-8')

# เลือกเฉพาะข้อมูลที่มีค่าซ้ำในคอลัมน์ 'รหัสประจำตัว'
# ใช้ `duplicated()` กับ `keep=False` เพื่อรวมข้อมูลที่ซ้ำทั้งหมด (ทั้งค่าแรกและค่าซ้ำ) พร้อมกับเรียงข้อมูลที่เลือกไว้ตามคอลัมน์ 'รหัสประจำตัว' 
df_dup = df[df.duplicated(subset=['รหัสประจำตัว'], keep=False)].sort_values(by='รหัสประจำตัว').reset_index(drop=True)


df_dup2 = df[df.duplicated(subset=['ชื่อคน'], keep=False)].sort_values(by='รหัสประจำตัว')


df = pd.concat([df_dup,df_dup2], axis=0)

dup_count = df.groupby(['รหัสประจำตัว', 'ชื่อคน']).size().reset_index(name='count').sort_values(by='รหัสประจำตัว')



print(df_dup)





