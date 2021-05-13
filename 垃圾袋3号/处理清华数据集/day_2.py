import os
path="/Users/wyw/Desktop/软件杯/第七题/数据集/THUCNews/彩票/"   # 目录
files=os.listdir(path)  # 读取该下的所有文本
for i in files:
    f1 = open(i ,"r")
    data = f1.read().splitlines()
    for j in data:
        print(j)
