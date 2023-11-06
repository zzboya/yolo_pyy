import cv2
import math
import numpy as np
import functools

from pathlib import Path


def custom_sort(x, y):
    x = x.split(tag)[-1].split('.')[0].split('_')
    x = [int(i) for i in x]
    y = y.split(tag)[-1].split('.')[0].split('_')
    y = [int(i) for i in y]
    for i in range(len(x)):
        if (x[i] > y[i]):
            return 1
        elif (x[i] < y[i]):
            return -1;
        elif (i == len(x) - 1):
            return 0


tag = '\\'  # 路径分隔符

data_root = Path('./runs/detect/exp44') # 分块图片的路径
temp_path = './recover_big/8.jpg' # 拼接后保存的路径及文件名

height = 600
width = 600

# overlap
over_x = 219
over_y = 194
h_val = height - over_x
w_val = width - over_y

images_path = data_root.glob('*')
images_path = [str(path) for path in images_path]
images_path = sorted(images_path, key=functools.cmp_to_key(custom_sort))
# print(images_path)

s = set()
for path in images_path:
    path = path.split(tag)[-1].split('_')
    s.add(int(path[0]))
# print(s)

output = []
for i in range(len(s)):
    output.append([])

for path in images_path:
    image = cv2.imread(path)
    path = path.split(tag)[-1].split('.')[0].split('_')
    if (int(path[3]) == width):
        if (int(path[1]) == 0):
            output[int(path[0])].append(image[:, :, :])
        else:
            output[int(path[0])].append(image[:, over_y:, :])
    else:
        output[int(path[0])].append(image[:, over_y:, :])

temp = []
for i in range(len(output)):
    t = np.concatenate(output[i], 1)
    if (i == 0):
        temp.append(t[:, :, :])
    else:
        temp.append(t[over_x:, :, :])

temp = np.concatenate(temp, 0)

cv2.imwrite(temp_path, temp)


