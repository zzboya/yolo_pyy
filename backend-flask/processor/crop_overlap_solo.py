import os
import shutil
import cv2  # 引入opencv库
import math  # 引入数学运算库
from PIL import Image
import numpy as np
import PIL
PIL.Image.MAX_IMAGE_PIXELS = None


def padding_image(input_folder, file_name, window_size):
    # print(img_path)
    img_path = os.path.join(input_folder, file_name)
    # print(img_path)
    img = Image.open(img_path)
    # 计算填充
    width, height = img.size
    imgsz = 0
    pad_width = (window_size - (width % window_size)) % window_size
    pad_height = (window_size - (height % window_size)) % window_size
    imgsz = max(width + pad_width, height + pad_height, imgsz)
    # 执行填充
    padded_img = Image.new(
        "RGB", (width + pad_width, height + pad_height), color=(0, 0, 0))
    padded_img.paste(img)

    # 保存处理后的图片
    output_img_path = os.path.join(input_folder, file_name)
    padded_img.save(output_img_path)

    # 关闭图像以节省资源
    img.close()
    padded_img.close()


def split_image(file_name, save_path):
    # 定义保存小图像的路径
    # save_path = './images_patch/DongYe1'
    # 如果不存在该路径，则创建该路径
    if os.path.exists(save_path):
        shutil.rmtree(save_path)
    os.makedirs(save_path)
    image = Image.open(file_name)
    image_np = np.array(image)
    if len(image_np.shape) == 3 and image_np.shape[2] == 3:
        image_np = np.transpose(image_np, (2, 0, 1))
    windows = split_image_1(image_np, window_size, step_size)

    # 定义小图像的大小
    height = 600
    width = 600

    # 定义重叠部分的大小
    over_x = 219
    over_y = 194
    h_val = height - over_x
    w_val = width - over_y

    # 定义mandatory变量，表示是否严格要求每个小图像必须都是指定的大小
    mandatory = False

    # 使用cv2库读取图片
    print('file_name::'+file_name)
    img = cv2.imread(file_name)
    # 将图片缩放为指定大小
    img = cv2.resize(img, (5472, 3648))
    # print(img.shape)

    # 获取原始图片的大小
    original_height = img.shape[0]
    original_width = img.shape[1]

    # 计算最大的行数和列数
    max_row = float((original_height - height) / h_val) + 1
    max_col = float((original_width - width) / w_val) + 1

    # 判断是否需要用ceil函数对结果进行向上取整
    if mandatory == False:
        max_row = math.ceil(max_row)
        max_col = math.ceil(max_col)
    else:
        max_row = math.floor(max_row)
        max_col = math.floor(max_col)

    # print(max_row)
    # print(max_col)

    # 定义一个列表，用于存储所有的小图像
    images = []
    # 使用for循环遍历每一行
    for i in range(max_row):
        # 定义一个临时列表，用于存储当前行的小图像
        images_temp = []
        # 使用for循环遍历每一列
        for j in range(max_col):
            # 定义保存小图像的路径
            temp_path = save_path + '/' + str(i) + '_' + str(j) + '_'
            # 判断当前列是否是最右边的不完整部分
            if ((width + j * w_val) > original_width and (i * h_val + height) <= original_height):
                # 裁剪得到指定大小的小图像
                temp = img[i * h_val:i * h_val +
                           height, j * w_val:original_width, :]
                # 定义该小图像的保存路径
                temp_path = temp_path + \
                    str(temp.shape[0]) + '_' + str(temp.shape[1]) + '.jpg'
                # 将小图像保存到指定路径
                cv2.imwrite(temp_path, temp)
                # 将小图像添加到当前行的列表中
                images_temp.append(temp)
            # 判断当前行是否是最下面的不完整部分
            elif ((height + i * h_val) > original_height and (j * w_val + width) <= original_width):
                temp = img[i * h_val:original_height,
                           j * w_val:j * w_val + width, :]
                temp_path = temp_path + \
                    str(temp.shape[0]) + '_' + str(temp.shape[1]) + '.jpg'
                cv2.imwrite(temp_path, temp)
                images_temp.append(temp)
            # 判断是否是最后一张小图像
            elif ((width + j * w_val) > original_width and (i * h_val + height) > original_height):
                temp = img[i * h_val:original_height,
                           j * w_val:original_width, :]
                temp_path = temp_path + \
                    str(temp.shape[0]) + '_' + str(temp.shape[1]) + '.jpg'
                cv2.imwrite(temp_path, temp)
                images_temp.append(temp)
            else:
                # 剩下的情况都是正常的完整小图像
                temp = img[i * h_val:i * h_val + height,
                           j * w_val:j * w_val + width, :]
                temp_path = temp_path + \
                    str(temp.shape[0]) + '_' + str(temp.shape[1]) + '.jpg'
                cv2.imwrite(temp_path, temp)
                images_temp.append(temp)

        # 将当前行的小图像列表添加到总列表中
        images.append(images_temp)

    # 输出小图像的个数
    # print(len(images))

# split_image('./imagesbig/DongYe10.jpg', './images_patch/DongYe10')


def split_image_1(image, window_size=640, stride=320):
    _, h, w = image.shape
    windows = []
    for y in range(0, h - window_size + 1, stride):
        for x in range(0, w - window_size + 1, stride):
            windows.append(image[:, y:y + window_size, x:x + window_size])
    return windows
