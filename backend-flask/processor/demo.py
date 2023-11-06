import os
import cv2

# 读取甘蔗txt文件
with open('./images_big/ShiSheng01/ShiSheng01all.txt', 'r') as f:
    data = f.readlines()
boxes = [(float(p.strip().split()[0]), float(p.strip().split()[1]),
               float(p.strip().split()[2]), float(p.strip().split()[3]))
              for p in data]
scores = [float(p.strip().split()[4]) for p in data]
labels = [float(p.strip().split()[5]) for p in data]

# 打开图片
image_path = './images_big/ShiSheng01/ShiSheng01.jpg'
img = cv2.imread(image_path)

# 在图片上绘制标记和分数
for i, box in enumerate(boxes):
    # 绘制矩形框
    label = int(labels[i])
    score = f'{scores[i]:.2f}'
    prefix = 'sugarcane' if label == 0 else 'weed'
    color = (100, 49, 237) if label == 0 else (128, 0, 0)
    bg_long = 10 if label == 0 else 5
    cv2.rectangle(img, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), color, 4)

    # 绘制文本
    text_size, _ = cv2.getTextSize(f'{prefix}:{score}', cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
    x, y = int(box[0]), int(box[1])
    bg_size = (text_size[0] + 10, text_size[1] + 5)  # 底色尺寸
    bg_pos = (x, y - text_size[1] - 5)  # 底色位置
    cv2.rectangle(img, bg_pos, (bg_pos[0] + bg_size[0], bg_pos[1] + bg_size[1]), color, -1)  # 绘制底色
    cv2.putText(img, f'{prefix}:{score}', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

# 保存标记后的图片
output_path = './images_big/ShiSheng01/ShiSheng01test.png'
cv2.imwrite(output_path, img)
