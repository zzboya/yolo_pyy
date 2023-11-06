import os
from PIL import Image, ImageDraw
import sys


def big_miss(big_name):
    # 读取txt文件中的坐标点
    with open(f'./processor/quemiao_point_fanzhuan/{big_name}.txt', 'r') as f:
        points = f.readlines()
    points = [tuple(map(float, p.strip().split())) for p in points]
    count_miss = len(points)
    # print(f"共有{len(points)}个缺苗点")

    # 打开图片
    image_path = f'./processor/imagesbig//{big_name}.jpg'
    img = Image.open(image_path)

    # 在图片上绘制标记
    draw = ImageDraw.Draw(img)
    for point in points:
        draw.rectangle([point[0] - 50, point[1] - 50, point[0] +
                       50, point[1] + 50], outline=(255, 255, 255), width=8)

    # 保存标记后的图片
    output_path = f'./processor/img_big_miss/{big_name}.jpg'
    img.save(output_path)

    return count_miss


if __name__ == '__main__':
    if len(sys.argv) > 1:
        big_name = sys.argv[1]    # 获取第一个命令行参数作为big_name
    else:
        big_name = 'ShiSheng01'   # 默认为ShiSheng01

    big_miss(big_name)
