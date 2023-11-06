import os
folder = './runs/detect/exp5/labels'
sg =0
wd=0
for filename in os.listdir(folder):
    if filename.endswith('.txt'):
        with open(os.path.join(folder,filename),'r') as f:
            for line in f:
                elements = line.split()  # 分割每行元素
                print(elements[0])
                if elements[0] == '0':
                    sg += 1  # 将每个元素转换为整数并累加到总和中
                else:
                    wd += 1
print("sg:", sg)
print("wd:", wd)
