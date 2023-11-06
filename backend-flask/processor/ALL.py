from .crop_overlap_solo import split_image
from . import detect
from .yolo2voc import conver_labels
from .demo1 import big_detect
from .quemiaobig import big_miss


def detect_big_image(big_name):
    # 定义路径和参数
    input_big_path = f'./processor/imagesbig/{big_name}.jpg'
    image_patch_path = f'./processor/images_patch/{big_name}'
    opt = detect.parse_opt()
    opt.source = f'./processor/images_patch/{big_name}'
    opt.project = './processor/images_patch_detect'
    opt.name = f'{big_name}'
    label_yolo = f'./processor/images_patch_detect/{big_name}/labels/'
    label_voc = f'./processor/images_patch_detect/{big_name}/labelsvoc'

    # 裁剪大图为小图
    split_image(input_big_path, image_patch_path)

    # 对小图进行检测
    detect.main(opt)

    # 将标签转换为VOC格式
    conver_labels(label_yolo, label_voc)

    # 对小图检测结果进行合并
    result = big_detect(big_name)
    print("幼苗数量为：%d，杂草数量为：%d" % (result[0], result[1]))

    # 在大图上标记缺苗框
    miss_count = big_miss(big_name)
    print("缺苗数量为：{}".format(miss_count))
    output_path = f'./processor/img_big_miss/{big_name}.jpg'

    return result, miss_count, output_path

# detect_big_image('ShiSheng03')
