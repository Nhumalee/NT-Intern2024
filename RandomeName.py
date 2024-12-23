import pandas as pd
data = {
    "รหัสประจำตัว": [
        12345, 12346, 12345, 12347, 12348, 12345, 12349, 12346, 12350, 12351, 
        12350, 12352, 12353, 12350, 12354, 12352, 12355, 12355, 12357, 12355, 
        12356, 12356, 12358, 12356, 12359, 12358, 12357, 12359, 12360, 12360, 
        12361, 12362, 12363, 12362, 12361, 12363, 12364, 12365, 12363, 12364, 
        12366, 12366, 12367, 12367, 12368, 12368, 12369, 12369, 12370, 12370, 
        12371, 12371, 12372, 12372, 12373, 12374, 12373, 12374, 12375, 12375, 
        12376, 12377, 12377, 12378, 12377, 12378, 12379, 12379, 12380, 12381, 
        12380, 12381, 12382, 12382, 12383, 12384, 12384, 12385, 12385, 12386, 
        12387, 12386, 12388, 12387, 12388, 12389, 12390, 12390, 12391, 12391, 
        12392, 12392, 12393, 12394, 12394, 12395, 12395, 12396, 12397, 12396
    ],
    "ชื่อคน": [
        "สมชาย", "สมหญิง", "สุเมธ", "จิราภรณ์", "ธนา", "ธีรชัย", "พัชรินทร์", "กิตติศักดิ์", "วรวุฒิ", "สมบัติ", 
        "อนุชา", "สุริยา", "สิรินทร์", "ภิญโญ", "นันทนา", "ภัทรา", "ภูมิ", "มนัส", "ศิริวัฒน์", "พิทยา", "อุดม", 
        "สุทธิกา", "ดลพงษ์", "จิรัตน์", "นิธิศ", "เอกชัย", "มาลี", "กาญจนา", "วรพล", "ธิศรา", "ลลิตา", "ศิริชัย", 
        "อมร", "จุฑามาศ", "สุรชัย", "วีระยุทธ", "อรพรรณ", "อาทิตย์", "อรพิมล", "อนิล", "กาญจนาภา", "พัชรา", 
        "มานพ", "ตุ๊กตา", "รัชนี", "ทรงพร", "สุรศักดิ์", "จุฑามาศ", "ภัทรา", "สุดารัตน์", "พิสิษฐ์", "บรรจง", 
        "สุเมธ", "เจษฎา", "นิภาพร", "ประทีป", "ตฤณ", "ดวงใจ", "ณัฐชัย", "อัจฉรา", "จิราธิวัฒน์", "ศุภชัย", 
        "นิธิศ", "ปิยะ", "ขวัญ", "วรพล", "ศิริวัฒน์", "ดวงใจ", "มาลี", "เทียน", "สมพร", "ศิริวัฒน์", "เพชร", 
        "อริสา", "สุทิน", "สมพร", "ธนพัฒน์", "วรวุฒิ", "ปณิตา", "เฉลิม", "ณิชาภา", "วิไล", "กิตติศักดิ์", 
        "อภิรักษ์", "สรวง", "วงศ์จันทร์", "วรชัย", "สุดารัตน์", "อนุชิต", "ภัทรา", "สิริกุล", "สิรินทร์", "มานะ",
        "พรชัย", "สมบัติ", "อรรณพ", "นนท์", "ชนัญญา", "พัชรชัย", "กรรณิการ์"
    ]
}

# ตรวจสอบความยาวของคอลัมน์
print(len(data["รหัสประจำตัว"]))

print(len(data["ชื่อคน"]))

# ถ้าความยาวไม่เท่ากัน แก้ไขให้เท่ากัน เช่น ลบหรือเพิ่มข้อมูลให้ครบ
                          

df = pd.DataFrame(data)
df.to_csv("randomname.csv", index=False, encoding='utf-8-sig')