import pandas as pd
import numpy as np
import math
import glob
import os
import re
import gc
from pathlib import Path
import warnings


# ตำแหน่ง และชื่อไฟล์
input_file = r"C:/Users/NT/Desktop/Intern/Python/Python-Basic/joint/j0000_6710.txt"
elec_bill_file = r"C:/Users/NT/Desktop/Intern/Python/Python-Basic/joint/electricity_bill_202410.csv"
exclude_gl_file = r"C:/Users/NT/Desktop/Intern/Python/Python-Basic/joint/exclude_gl_code_joint.csv"
expense_ratio_file = r"C:/Users/NT/Desktop/Intern/Python/Python-Basic/joint/expense_ratio_202411.csv"
j0103_ratio_file = r"C:/Users/NT/Desktop/Intern/Python/Python-Basic/joint/j0103_ratio.xlsx"

# ตำแหน่งที่เก็บไฟล์ผลลัพธ์
log_file = r"C:/Users/NT/Desktop/Intern/Python/Python-Basic/joint"
output_file = r"C:/Users/NT/Desktop/Intern/Python/Python-Basic/joint"
Path(log_file).mkdir(parents=True, exist_ok=True)
Path(output_file).mkdir(parents=True, exist_ok=True)

template_header = ["เลขที่เอกสาร","บรรทัดรายการ","รหัสบริษัท","ปีบัญชี","ประเภทเอกสาร","วันที่เอกสาร","วันที่ผ่านรายการ","การอ้างอิง","ข้อความส่วนหัว","สกุลเงิน","อัตราแลกเปลี่ยน","เลขที่สาขา","วันที่แปลงค่า","คีย์ผ่านรายการ","ประเภทบัญชี","รหัสบัญชี","รหัสบัญชีกระทบยอด","รหัสภาษี","จำนวนเงินสกุลในเอกสาร","จำนวนเงินสกุลในประเทศ","ฐานภาษีสกุลในเอกสาร","ฐานภาษีสกุลในประเทศ","ประเภทธุรกิจ","ศูนย์ต้นทุน","เขตตามหน้าที่","WBC","กิจกรรม","บริษัทคู่ค้า","วันที่คิดมูลค่า","วันที่ฐาน","เทอมการจ่ายชำระ","คีย์ธนาคาร","ผลิตภัณฑ์/บริการ","ผลิตภัณฑ์/บริการย่อย","ประเภทรายได้","กลุ่มลูกค้า","รหัสวัสดุ","โรงงาน","กระบวนการทางธุรกิจ","เซกเมนต์","การกำหนด","ข้อความรายการ","คีย์อ้างอิง 1 (ติดตามหนี้ )","คีย์อ้างอิง2 ","คีย์อ้างอิง 3","เลขที่อ้างอิงใบกำกับ","ปีใบกำกับอ้างอิง","บรรทัดใบกำกับอ้างอิง","ประเภทหักณที่จ่าย","รหัสภาษีหักณที่จ่าย","ฐานภาษีหักณที่จ่าย","ฐาน ภาษีหัก ณ ที่จ่าย (Local)","จำนวนภาษีหัก ณ ที่จ่าย","จำนวนภาษีหัก ณ ที่จ่าย (Local)","ประเภทหักณที่จ่าย_","รหัสภาษีหักณที่จ่าย_","ฐานภาษีหักณที่จ่าย_","ฐาน ภาษีหัก ณ ที่จ่าย (Local)_","จำนวนภาษีหัก ณ ที่จ่าย_","จำนวนภาษีหัก ณ ที่จ่าย (Local)_"]

# เตรียม template
df_template = pd.DataFrame(columns=template_header)

# ระบุทุกเดือน
month_name = "ต.ค. 67"
doc_date = "20241031"
year = "2024"

print(df_template)
 

pd.options.display.float_format = '{:,.4f}'.format # จัดรูปแบบการแสดงผลหน้าจอ เลขทศนิยม 2 ตำแหน่ง
# อ่านไฟล์ข้อมูลแบบ csv
df = pd.read_csv(Path(input_file), skiprows=3, converters={"สปก.ต้นทุน":str}, sep="\t" , encoding='tis-620') # joint file from SAP
df_ex_gl = pd.read_csv(Path(exclude_gl_file), converters={"รหัสบัญชี":str}) # gl ที่จะตัดออก
df_elec_bill = pd.read_csv(Path(elec_bill_file), converters={"สปก.ต้นทุน_bill":str}) # ค่าไฟฟ้า
df_ratio = pd.read_csv(Path(expense_ratio_file)) # เกณฑ์สัดส่วน
df_ratio_j0103 = pd.read_excel(Path(j0103_ratio_file))


# df = pd.read_excel("/Users/seal/Library/CloudStorage/OneDrive-Personal/share/Datasource/2023/co/joint/j0101.xls", skiprows=3, engine="xlrd")
# ลบ ชื่อ column ที่มีช่องว่าง หรือ space ออก
# ลบช่องว่างและอักขระพิเศษในชื่อคอลัมน์
df.columns = df.columns.str.strip().str.replace(" ", "").str.replace("\n", "")

# ตรวจสอบชื่อคอลัมน์
print(df.columns)

# เลือกเฉพาะบรรทัดที่คอลัมน์แรกมีค่า '*'
df = df[df["Unnamed:1"] == "*"].reset_index()

# เลือกเฉพาะคอลัมน์ที่ต้องการ
df = df[["ออบเจค", "สปก.ต้นทุน", "ชื่อส่วนประกอบต้นทุน", "Val.inrep.cur."]]

#df.to_excel('df.xlsx')


# df["COST_CENTER"] = df['ออบเจค'].str[:7]
# condition
# df = df.astype({"Val.inrep.cur.": "float"})
# ตัดเครื่องหมาย , ( ) ออก
df["Val.inrep.cur."] = df["Val.inrep.cur."].replace(",", "", regex=True)
df["Val.inrep.cur."] = df["Val.inrep.cur."].replace("\(", "-", regex=True)
df["Val.inrep.cur."] = df["Val.inrep.cur."].replace("\)", "", regex=True)
df["Val.inrep.cur."] = df["Val.inrep.cur."].str.strip()
df["Val.inrep.cur."] = df["Val.inrep.cur."].astype(float)
# print(df)

# 2. เลือกเอาเฉพาะ รหัส GL ขึ้นต้นด้วย 54
df = df[df["สปก.ต้นทุน"].str[:2] == "54"]
## df = df.groupby(["ออบเจค", "สปก.ต้นทุน", "ชื่อส่วนประกอบต้นทุน"], dropna=False)["Val.inrep.cur."].sum().round(2)

# print("gl begin with 54")
# print(df)
# print(df["ออบเจค"].str[7:])   
df["activity"] = df["ออบเจค"].str[7:]
df_summary = df[["activity", "Val.inrep.cur."]].fillna(0)
df_summary = df_summary.groupby(["activity"]).sum()
print(df_summary)

# 3. รหัสบัญชีที่ตัดออก จากไฟล์ รหัสบัญชีที่ตัดออก.csv 
# print(df_ex_gl["รหัสบัญชี"])
# สร้าง list regex แทนค่า x ด้ว \d
regex_ex_gl = list(df_ex_gl["รหัสบัญชี"].str.replace("x", "\d"))
# print(regex_ex_gl)

# หา gl ที่ match กับ exclude gl เพื่อตัดออก
# https://stackoverflow.com/questions/47011170/multiple-pattern-using-regex-in-pandas
# https://toltman.medium.com/matching-multiple-regex-patterns-in-pandas-121d6127dd47
# print(df[df["สปก.ต้นทุน"].str.match("|".join(regex_ex_gl)) == True])
df = df[df["สปก.ต้นทุน"].str.match("|".join(regex_ex_gl)) == False].reset_index()
df.index += 1
# print("remove exclude gl")
print(df)       



# print(df[df["สปก.ต้นทุน"].str.match(r"51625101") == True])
# print(df[df["สปก.ต้นทุน"].str.match(r"5\d6421\d\d") == True])
# print(df[df["สปก.ต้นทุน"].str.match(r"5\d662102") == True])
# print(df[df["สปก.ต้นทุน"].str.match(r"5\d643\d\d\d") == True])

# หักค่าไฟฟ้า ด้วยเงื่อนไข GL Code & Business Process Object (costcenter+activity)
# ด้วยการลบออก เช่น เดิมมี 100 ลบออก 20 เหลือ 80
# print("Electricity bill")
# print(df[df["สปก.ต้นทุน"].str.match(r"54661102") == True])

print(df_elec_bill)
# ประมวลผลข้อมูลค่าไฟฟ้า เพื่อนำไปต่อเพิ่มกับข้อมูลการปรับ joint 
# 
# ถ้ารหัสบัญชีเป็น 5x7xxxxx ให้ segment = 19301 ; regex "5\d7\d\d\d\d\d" 
# ถ้ารหัสบัญชีเป็น 5x6xxxxx ให้ segment = 19201 ; regex "5\d6\d\d\d\d\d"

df_elec_bill["เซกเมนต์"] = ""
segment = df_elec_bill["สปก.ต้นทุน_bill"].str.match("5\d7\d\d\d\d\d")
df_elec_bill.loc[segment, "เซกเมนต์"] = "19301"
segment = df_elec_bill["สปก.ต้นทุน_bill"].str.match("5\d6\d\d\d\d\d")
df_elec_bill.loc[segment, "เซกเมนต์"] = "19201"


elec_bill = pd.DataFrame()
elec_bill_ori = pd.DataFrame()

# keep original
# GL ขึ้นต้นด้วย 54
elec_bill_ori["กระบวนการทางธุรกิจ"] = df_elec_bill["ออบเจค_bill"]
elec_bill_ori["รหัสบัญชี"] = df_elec_bill["สปก.ต้นทุน_bill"]
elec_bill_ori["ชื่อส่วนประกอบต้นทุน"] = df_elec_bill["ชื่อส่วนประกอบต้นทุน_bill"]
elec_bill_ori["จำนวนเงินสกุลในเอกสาร"] = df_elec_bill["Val.in rep.cur._bill"]
elec_bill_ori["จำนวนเงินสกุลในประเทศ"] = df_elec_bill["Val.in rep.cur._bill"]
elec_bill_ori["activity"] = df_elec_bill["ออบเจค_bill"].str[7:]
elec_bill_ori["รหัสกิจกรรม"] = elec_bill_ori["activity"]
elec_bill_ori["คีย์ผ่านรายการ"] = "50"
elec_bill_ori["เซกเมนต์"] = df_elec_bill["เซกเมนต์"]
elec_bill_ori["flag_elec_bill"] = True  # บอกให้รู้ว่าเป็นรายการค่าไฟฟ้า

# เปลี่ยนเป็น GL ขึ้นต้นด้วย 51
elec_bill["กระบวนการทางธุรกิจ"] = df_elec_bill["ออบเจค_bill"].str[:7] + "S2210"
elec_bill["รหัสบัญชี"] = "51" + df_elec_bill["สปก.ต้นทุน_bill"].str[2:]
elec_bill["ชื่อส่วนประกอบต้นทุน"] = df_elec_bill["ชื่อส่วนประกอบต้นทุน_bill"]
elec_bill["จำนวนเงินสกุลในเอกสาร"] = df_elec_bill["Val.in rep.cur._bill"]
elec_bill["จำนวนเงินสกุลในประเทศ"] = df_elec_bill["Val.in rep.cur._bill"]
elec_bill["activity"] = df_elec_bill["ออบเจค_bill"].str[7:]
elec_bill["รหัสกิจกรรม"] = elec_bill["activity"]
elec_bill["คีย์ผ่านรายการ"] = "40"
elec_bill["เซกเมนต์"] = df_elec_bill["เซกเมนต์"]
elec_bill["flag_elec_bill"] = True # บอกให้รู้ว่าเป็นรายการค่าไฟฟ้า

elec_bill_template = pd.concat([elec_bill_ori, elec_bill])
#print(elec_bill_template)

# print("ข้อมูลค่าไฟฟ้า รหัสบัญชีขึ้นด้วย 51 ที่ใส่กลับและต้องเปลี่ยนรหัสกิจกรรม")
# row_filter = elec_bill.loc[(elec_bill["flag_elec_bill"] == True) & (elec_bill["รหัสบัญชี"].str[:2] == "51")]
# print("บรรทัด (index row) ที่จะต้องเปลี่ยน")
# print(row_filter.index)
# print(df_merge.loc[row_filter.index.values, "กระบวนการทางธุรกิจ"].str[:7] + "S2210")
# print("ก่อนเปลี่ยนรหัสกิจกรรม")
# print(elec_bill.loc[(elec_bill["flag_elec_bill"] == True) & (elec_bill["รหัสบัญชี"].str[:2] == "51")])
# elec_bill.loc[row_filter.index.values, "กระบวนการทางธุรกิจ"] = elec_bill.loc[row_filter.index.values, "กระบวนการทางธุรกิจ"].str[:7] + "S2210"
# print("หลังเปลี่ยนรหัสกิจกรรมเป็น S2210")
# print(elec_bill.loc[(elec_bill["flag_elec_bill"] == True) & (elec_bill["รหัสบัญชี"].str[:2] == "51")])
# end # ประมวลผลข้อมูลค่าไฟฟ้า เพื่อนำไปต่อเพิ่มกับข้อมูลการปรับ joint 


# 4. หักค่าไฟฟ้า 
df_df_elec_bill = pd.merge(df, df_elec_bill, how="left", left_on=["ออบเจค", "สปก.ต้นทุน"], right_on=["ออบเจค_bill", "สปก.ต้นทุน_bill"])
df_df_elec_bill = df_df_elec_bill[["ออบเจค", "สปก.ต้นทุน", "ชื่อส่วนประกอบต้นทุน", "Val.inrep.cur.", "Val.in rep.cur._bill"]].fillna(0)
df_df_elec_bill["val_calculate"] = df_df_elec_bill["Val.inrep.cur."] - df_df_elec_bill["Val.in rep.cur._bill"]
df_df_elec_bill["activity"] = df_df_elec_bill["ออบเจค"].str[7:]
df_df_elec_bill["flag_elec_bill"] = False
print(df_df_elec_bill)

## print(df_df_elec_bill[df_df_elec_bill["สปก.ต้นทุน"].str.match(r"54661102") == True])  # ทดสอบ
# print(df_ratio)


# เอาสัดส่วนเข้ามาเพื่อใช้คำนวณ

# รวมข้อมูล df_df_elec_bill กับ df_ratio จับคู่จาก "activity" กับ "รหัสกิจกรรม" และลบแถวที่มีค่า NaN ในคอลัมน์ 'รหัสกิจกรรม'
df_J = pd.merge(df_df_elec_bill, df_ratio, how="left", left_on=["activity"], right_on=["รหัสกิจกรรม"]).dropna(subset='รหัสกิจกรรม')

# แสดงผลลัพธ์ของตารางค่า J
print("ตารางค่า J ทุกตัวยกเว้น J0103")
print(df_J)


# รวมข้อมูล df_df_elec_bill กับ df_ratio_j0103 จับคู่จากคอลัมน์ "ออบเจค" และลบแถวที่มีค่า NaN ในคอลัมน์ 'รหัสกิจกรรม'
df_only_J0103 = pd.merge(df_df_elec_bill, df_ratio_j0103, how="left", on="ออบเจค").dropna(subset='รหัสกิจกรรม')


# แสดงผลลัพธ์ของตารางเฉพาะค่า J0103
print("ตารางเฉพาะค่า J0103")
print(df_only_J0103)


# รวมข้อมูล df_J กับ df_only_J0103
df_cal_ = pd.concat([df_J, df_only_J0103], axis=0)


# 5. คำนวณสัดส่วนตาม % ที่กำหนด
df_cal_["51"] = df_cal_["val_calculate"] * df_cal_["GL_51"]
df_cal_["53"] = df_cal_["val_calculate"] * df_cal_["GL_53"]
df_cal_["51"] = df_cal_["51"].round(2)
df_cal_["53"] = df_cal_["53"].round(2)

# 6. รหัส GL ขึ้นต้นด้วย 54 ได้จากรหัสขึ้นต้นด้วย 51 + 53
df_cal_["54"] = df_cal_["51"] + df_cal_["53"]
df_cal_["54"] = df_cal_["54"].round(2)


# ลบบรรทัดที่มีค่าเป็น 0 ออก
df_cal_ = df_cal_.drop(df_cal_[(df_cal_['51'] == 0) & (df_cal_['53'] == 0)].index)


#ตรวจสอบผล
print(df_cal_)

#df_cal_.to_excel('df_cal_.xlsx')


# เรียงข้อมูลเพื่อเตรียมแบ่งไฟล์
df_cal_ = df_cal_.sort_values(["activity", "สปก.ต้นทุน"])
df_cal_ = df_cal_.reset_index(drop=True)

# ทำการแบ่ง บรรทัด 166 มาจาก 166 * 3 = 498 บรรทัด ใน 1 file ต้องไม่เกิน 500 บรรทัด, 3 มาจากรหัสบัญชีสามตัว 51,53,54
# https://stackoverflow.com/questions/44729727/pandas-slice-large-dataframe-into-chunks
n = math.ceil(len(df_cal_) / 166)   # ปัดเลขขึ้นเป็นจำนวนเต็ม ถ้ามีเศษ
list_df = np.array_split(df_cal_, n)
# print(len(list_df))
list_ = []
for file in range(len(list_df)):
    list_df[file]["file"] = file + 1    # หมายเลขกำหนดของไฟล์
    list_df[file].index += 1
    list_.append(list_df[file])
# print(list_df[0])
# del df_cal_
# gc.collect()
df_cal_ratio = pd.concat(list_)
# file ค่าไฟฟ้านับต่อจากข้อมูล ปรับ joint
elec_bill_template["file"] = n + 1


# save ลง log file เพื่อใช้ตรวจสอบ
df_cal_ratio.to_excel(Path(log_file + "joint_log_" + doc_date + ".xlsx"), float_format="%.4f")




# นับจำนวนบรรทัดแยกตามกิจกรรม
print(df_cal_ratio["activity"].value_counts())
data_dict = {}
data_dict = df_cal_ratio["activity"].value_counts().to_dict()
print(data_dict)
print(data_dict.keys())
print(data_dict.values())

# 100 - 20 เหลือ 80 เอา 80 มาคูณ สรุปเกณฑ์ปันส่วน Joint ตาม % ของ Jxxxx 
# ได้มาใหม่ 3 บรรทัด เป็น GL ขึ้นต้นด้วย 51, 53, โดย 54 ได้จาก 51+53
# ตัวอื่นที่เหลือที่ไม่ใช่ค่าไฟฟ้า ให้เอาตัวมันเองมาคูณกับ สรุปเกณฑ์ปันส่วน Joint ออกมาเป็น 51,53, 54 = 51+53



# จัดลง template 
# เอามาที่ Joint มาเรียงกัน 51,53,54

# เลขที่เอกสาร running ตาม Joint 00001, 00002, 00003 
# บรรทัดรายการ running ที่ละ Joint 0001,0002,0003,0004,0005, ...
# วาง column 51,53,54 เพื่อ a+b=c แล้ว แปลง column มาเป็น row / max row = 150

# ข้อความส่วนหัว เปลี่ยนไปตาม รหัส Joint กับ งวด เช่น ปป.ค่าใช้จ่ายAct. J0101  ต.ค. 66

# การ recheck เอา ผลรวมของ คีย์ผ่านรายการ 40  และผลรวมของคีย์ผ่านรายการ 50 ที่ละ joint มาลบกัน ต้องเป็น 0
# ตัด template file -> csv 

df_51 = pd.DataFrame()
df_53 = pd.DataFrame()
df_54 = pd.DataFrame()

df_51["กระบวนการทางธุรกิจ"] = df_cal_ratio["ออบเจค"]
df_53["กระบวนการทางธุรกิจ"] = df_cal_ratio["ออบเจค"]
df_54["กระบวนการทางธุรกิจ"] = df_cal_ratio["ออบเจค"]

df_51["file"] = df_cal_ratio["file"]
df_53["file"] = df_cal_ratio["file"]
df_54["file"] = df_cal_ratio["file"]


df_51["flag_elec_bill"] = df_cal_ratio["flag_elec_bill"]
df_53["flag_elec_bill"] = df_cal_ratio["flag_elec_bill"]
df_54["flag_elec_bill"] = df_cal_ratio["flag_elec_bill"]

# คีย์ผ่านรายการ ต้องเติม 40 ถ้า GL เป็น 51,53 
# คีย์ผ่านรายการ ต้องเติม 50 ถ้า GL เป็น 54 

df_51["ศูนย์ต้นทุน"] = df_cal_ratio['ออบเจค'].str[:7]
df_51["รหัสบัญชี"] = "51" + df_cal_ratio['สปก.ต้นทุน'].str[2:]
df_51["คีย์ผ่านรายการ"] = "40"

df_53["ศูนย์ต้นทุน"] = df_cal_ratio['ออบเจค'].str[:7] # เลือกทางซ้ายมา 7 ตำแหน่ง 
df_53["รหัสบัญชี"] = "53" + df_cal_ratio['สปก.ต้นทุน'].str[2:] # right เลือกทางขวา ตัดสองตำแหน่งซ้ายออก
df_53["คีย์ผ่านรายการ"] = "40"

df_54["ศูนย์ต้นทุน"] = df_cal_ratio['ออบเจค'].str[:7]
df_54["รหัสบัญชี"] = df_cal_ratio['สปก.ต้นทุน']
df_54["คีย์ผ่านรายการ"] = "50"

df_51["จำนวนเงินสกุลในเอกสาร"] = df_cal_ratio["51"]
df_53["จำนวนเงินสกุลในเอกสาร"] = df_cal_ratio["53"]
df_54["จำนวนเงินสกุลในเอกสาร"] = df_cal_ratio["54"]

df_51["activity"] = df_cal_ratio["activity"]
df_53["activity"] = df_cal_ratio["activity"]
df_54["activity"] = df_cal_ratio["activity"]



# แปลงจาก columns มาเป็น row เตรียมลง template
df_merge = pd.concat([df_54, df_51, df_53]).reset_index(drop=True)
print("ข้อมูลที่คำนวณแล้ว")
print(df_merge)



# delete ยอดเงิน = 0 ออก
# 
print("จำนวนเงินเป็น 0 หรือไม่มีค่า")
print(df_merge[df_merge["จำนวนเงินสกุลในเอกสาร"].isnull()])
print(df_merge[df_merge["จำนวนเงินสกุลในเอกสาร"] == 0])
# เอาเฉพาะที่มีจำนวนเงิน ไม่เอา null, 0
df_merge = df_merge.drop(df_merge[df_merge["จำนวนเงินสกุลในเอกสาร"].isnull()].index)
df_merge = df_merge.drop(df_merge[df_merge["จำนวนเงินสกุลในเอกสาร"] == 0].index)
print("หลังจากลบข้อมูลค่า 0 ออก")
print(df_merge[df_merge["จำนวนเงินสกุลในเอกสาร"].isnull()])
print(df_merge[df_merge["จำนวนเงินสกุลในเอกสาร"] == 0])
df_merge = df_merge.reset_index(drop=True)

# 7. หาค่าติดลบ
mask = df_merge["จำนวนเงินสกุลในเอกสาร"] < 0
print("จำนวนเงิน < 0")
print(df_merge[mask])
# print(df_merge[mask].index)

# ทำค่าติดลบให้เป็นบวก
# กรณีเป็นค่าลบ ให้เปลี่ยนเป็น + แล้ว ให้เปลี่ยน คีย์ผ่านรายการ จากเดิม 40 เป็น 50 และ เปลี่ยนจาก เดิม 50 เป็น 40
df_merge.loc[mask, "จำนวนเงินสกุลในเอกสาร"] = df_merge.loc[mask, "จำนวนเงินสกุลในเอกสาร"].abs()
# หารายการที่เป็น 40, 50
mask_40 = df_merge.loc[mask & (df_merge["คีย์ผ่านรายการ"] == "40"), "คีย์ผ่านรายการ"]
mask_50 = df_merge.loc[mask & (df_merge["คีย์ผ่านรายการ"] == "50"), "คีย์ผ่านรายการ"]

# เปลี่ยน 40 เป็น 50, เปลี่ยน 50 เป็น 40
df_merge.iloc[mask_40.index.values, df_merge.columns.get_loc("คีย์ผ่านรายการ")] = "50"
df_merge.iloc[mask_50.index.values, df_merge.columns.get_loc("คีย์ผ่านรายการ")] = "40"

# print(df_merge.iloc[mask_40.index.values, df_merge.columns.get_loc("คีย์ผ่านรายการ")])
# print(df_merge.iloc[mask_50.index.values, df_merge.columns.get_loc("คีย์ผ่านรายการ")])
###

df_merge["จำนวนเงินสกุลในประเทศ"] = df_merge["จำนวนเงินสกุลในเอกสาร"]
# df_merge["activity"] = df_merge['กระบวนการทางธุรกิจ'].str[7:]

# จัดเรียงข้อมูลตาม รหัสกิจกรรม และ รหัสบัญชี
df_merge = df_merge.sort_values(["file", "activity", "รหัสบัญชี"])
df_merge = df_merge.reset_index(drop=True)
df_merge.index += 1
# df_merge.drop("index", axis=True, inplace=True)

# พิมพ์มาดูเล่น ตรวจสอบความถูกต้อง
print(df_merge)
print(df_merge["activity"].value_counts())
data_dict = {}
data_dict = df_merge["activity"].value_counts().to_dict()
print(data_dict)
print(data_dict.keys())
print(data_dict.values())


# เอาค่าไฟฟ้ามารวม
df_merge = pd.concat([df_merge, elec_bill_template])
#df_merge.to_excel('df_merge.xlsx')

# 
# https://stackoverflow.com/questions/17775935/sql-like-window-functions-in-pandas-row-numbering-in-python-pandas-dataframe
# df['RN'] = df.sort_values(['data1','data2'], ascending=[True,False]).groupby(['key1']).cumcount() + 1

# กำหนดเลขบรรทัด ตาม column ที่กำหนด, กำหนดที่ file column
df_merge["บรรทัดรายการ"] = df_merge.groupby(["file"]).cumcount() + 1
# https://stackoverflow.com/questions/50050617/assign-unique-numeric-group-ids-to-groups-in-pandas
df_merge["เลขที่เอกสาร"] = (df_merge.groupby(["file", "activity"]).cumcount()==0).astype(int)
df_merge["เลขที่เอกสาร"] = df_merge["เลขที่เอกสาร"].cumsum()
# https://stackoverflow.com/questions/17950374/converting-a-column-within-pandas-dataframe-from-int-to-string
# https://www.skytowner.com/explore/adding_leading_zeros_to_strings_of_a_column_in_pandas

# ใส่เลข 0 นำหน้าจำนวน 4 ตำแหน่ง
df_merge["บรรทัดรายการ"] = df_merge["บรรทัดรายการ"].apply(str)
df_merge["บรรทัดรายการ"] = df_merge["บรรทัดรายการ"].str.zfill(4)
# ใส่เลข 0 นำหน้าจำนวน 5 ตำแหน่ง
df_merge["เลขที่เอกสาร"] = df_merge["เลขที่เอกสาร"].apply(str)
df_merge["เลขที่เอกสาร"] = df_merge["เลขที่เอกสาร"].str.zfill(5)

# หาเลขที่เอกสารล่าสุด ก่อนจะขึ้นรายการค่าไฟฟ้า 
# รายการค่าไฟฟ้ากำหนด เลขที่เอกสาร เป็นเลขเดียว ไม่ running ตามกิจกรรม
print(df_merge.loc[df_merge["flag_elec_bill"]==False,"เลขที่เอกสาร"].astype(int).max())
doc_id_max = df_merge.loc[df_merge["flag_elec_bill"]==False,"เลขที่เอกสาร"].astype(int).max() + 1 # บวกเพิ่ม 1
doc_id_elec_bill = str(doc_id_max).zfill(5)
df_merge.loc[df_merge["flag_elec_bill"]==True, "เลขที่เอกสาร"] = doc_id_elec_bill
# เปลี่ยน activity
df_merge.loc[df_merge["flag_elec_bill"]==True, "activity"] = df_merge.loc[df_merge["flag_elec_bill"]==True, "activity"] + "-S2210" 

# print(df_template)

# ถ้ารหัสบัญชีเป็น 5x7xxxxx ให้ segment = 19301 ; regex "5\d7\d\d\d\d\d" 
# ถ้ารหัสบัญชีเป็น 5x6xxxxx ให้ segment = 19201 ; regex "5\d6\d\d\d\d\d"
df_merge["เซกเมนต์"] = ""
segment = df_merge["รหัสบัญชี"].str.match("5\d7\d\d\d\d\d")    # หาบรรทัดที่ GL เป็น 5x7xxxxx
df_merge.loc[segment, "เซกเมนต์"] = "19301"

segment = df_merge["รหัสบัญชี"].str.match("5\d6\d\d\d\d\d")    # หาบรรทัดที่ GL เป็น 5x6xxxxx
df_merge.loc[segment, "เซกเมนต์"] = "19201"

# df_merge = df_merge.reset_index(drop=True)
# df_template = df_template.reset_index(drop=True)
# https://github.com/pandas-dev/pandas/issues/55928
# FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
with warnings.catch_warnings():
    # TODO: pandas 2.1.0 has a FutureWarning for concatenating DataFrames with Null entries
    warnings.filterwarnings("ignore", category=FutureWarning)
    df_template_output = pd.concat([df_merge, df_template], axis=0, ignore_index=True)

'''df_template["เลขที่เอกสาร"] = df_merge["เลขที่เอกสาร"]
df_template["บรรทัดรายการ"] = df_merge["บรรทัดรายการ"]
df_template["การอ้างอิง"] = df_merge["เลขที่เอกสาร"]
df_template["รหัสบัญชี"] = df_merge["รหัสบัญชี"]
df_template["จำนวนเงินสกุลในเอกสาร"] = df_merge["จำนวนเงินสกุลในเอกสาร"]
df_template["จำนวนเงินสกุลในประเทศ"] = df_merge["จำนวนเงินสกุลในประเทศ"]
df_template["ศูนย์ต้นทุน"] = df_merge["ศูนย์ต้นทุน"]
df_template["กระบวนการทางธุรกิจ"] = df_merge["กระบวนการทางธุรกิจ"]
df_template["เซกเมนต์"] = df_merge["เซกเมนต์"]
df_template["activity"] = df_merge["activity"]
df_template["file"] = df_merge["file"]'''


df_template_output["รหัสบริษัท"] = "1000"
df_template_output["ปีบัญชี"] = year
df_template_output["ประเภทเอกสาร"] = "BA"
df_template_output["วันที่เอกสาร"] = doc_date
df_template_output["วันที่ผ่านรายการ"] = doc_date
df_template_output["ข้อความส่วนหัว"] = "ปป.ค่าใช้จ่ายAct. "
df_template_output["สกุลเงิน"] = "THB"
df_template_output["อัตราแลกเปลี่ยน"] = "1"
df_template_output["ประเภทบัญชี"] = "S"
df_template_output["รหัสภาษี"] = "VX"
df_template_output["เขตตามหน้าที่"] = "Z0"
df_template_output["ข้อความส่วนหัว"] = df_template_output["ข้อความส่วนหัว"] + df_template_output["activity"] + " " + month_name 
df_template_output["ข้อความรายการ"] = df_template_output["ข้อความส่วนหัว"]
df_template_output["file"] = df_template_output["file"].astype(int)

# https://www.geeksforgeeks.org/how-to-create-multiple-csv-files-from-existing-csv-file-using-pandas/
# save แยกไฟล์ ตามจำนวน running ใน column "file"
for file, group in df_template_output.groupby(df_template_output["file"]):
    file_name = f"{file}_" + doc_date + ".csv"  # ตั้งชื่อไฟล์ 1_20240131.csv
    group = group[template_header] # เอาเฉพาะ column ที่กำหนด
    group.to_csv(Path(output_file+file_name), index=False, header=False) # เขียนลงไฟล์

# เอาเฉพาะ column ที่กำหนด
df_template_output = df_template_output[template_header]

# เขียนผลลัพธ์ลงไฟล์
df_template_output.to_csv(Path(output_file + "joint_template_" + doc_date + ".csv"), index=False, header=True, float_format="%.2f")
df_template_output.to_excel(Path(output_file + "joint_template_" + doc_date + ".xlsx"), index=False, header=True, float_format="%.2f")
df_template_output.to_excel(Path(output_file + "joint_template_no_header_" + doc_date + ".xlsx"), index=False, header=False, float_format="%.2f")
df_merge.to_csv(Path(output_file + "j0000_output_" + doc_date + ".csv"), float_format="%.2f")
df_merge.to_excel(Path(output_file + "j0000_output_" + doc_date + ".xlsx"), float_format="%.2f")
