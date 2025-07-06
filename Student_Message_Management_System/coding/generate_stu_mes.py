import random

# 数据生成工具
surnames = ["王", "李", "张", "刘", "陈", "杨", "赵", "黄", "周", "吴"]
male_names = ["伟", "强", "磊", "洋", "勇", "军", "超", "明", "鹏", "浩", "鑫", "宇", "帆", "旭", "峰", "博"]
female_names = ["敏", "静", "秀", "丽", "娟", "艳", "婷", "琳", "莹", "洁", "梅", "雪", "芳", "娜", "雯", "玥"]
dorm_buildings = {"男": "B", "女": "G"}  # 不同性别不同楼号

# 生成学生列表
students = []
male_count, female_count = 16, 12 

# 分配宿舍（4人一间）
male_dorms = [f"B10{i}" for i in range(1, 5)] * 4  # B101-B104
female_dorms = [f"G20{i}" for i in range(1, 4)] * 4  # G201-G203

random.shuffle(male_dorms)
random.shuffle(female_dorms)

# 生成男生数据
for i in range(male_count):
    stu_id = 20240001 + i
    name = random.choice(surnames) + random.choice(male_names)
    dorm = male_dorms[i]
    phone = "1" + "".join(random.choices("0123456789", k=10))
    students.append(("男", stu_id, name, dorm, phone))

# 生成女生数据
for i in range(female_count):
    stu_id = 20240001 + male_count + i
    name = random.choice(surnames) + random.choice(female_names)
    dorm = female_dorms[i]
    phone = "1" + "".join(random.choices("0123456789", k=10))
    students.append(("女", stu_id, name, dorm, phone))

# 随机打乱顺序（使学号不分性别连续）
random.shuffle(students)

# 写入文件
with open("../dataset/a.txt", "w", encoding="utf-8") as f:
    f.write("学号 姓名 性别 宿舍号码 电话号码\n")
    for gender, stu_id, name, dorm, phone in students:
        f.write(f"{stu_id} {name} {gender} {dorm} {phone}\n")

print("学生信息生成完毕，已保存到指定文件夹中。")