import pandas   as pd 

# สร้าง DataFrame ตัวอย่าง
data = {
    'ชื่อ': ['A', 'B', 'A', 'B', 'C', 'C', 'A'],
    'คะแนน': [10, 15, 10, 20, 10, 15, 20]
}
df = pd.DataFrame(data)

# จัดกลุ่มข้อมูลตามคอลัมน์ "ชื่อ" และหาผลรวมของคะแนนในแต่ละกลุ่ม
result = df.groupby('ชื่อ')['คะแนน'].sum()

# นับจำนวนครั้งที่แต่ละชื่อและคะแนนซ้ำกัน
dup_count = df.groupby(['ชื่อ', 'คะแนน']).size().reset_index(name='Count')

# นับจำนวนครั้งที่ชื่อแต่ละตัวซ้ำกัน
name_counts = df['ชื่อ'].value_counts()
print(name_counts)


