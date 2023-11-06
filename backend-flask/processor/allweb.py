from crop_overlap_solo import split_image
from yolo2voc import conver_labels
from demo1 import big_detect
from quemiaobig import big_miss
import detect

class ImageDetection:
    def __init__(self, big_name):
        self.big_name = big_name
        self.input_big_path = f'./imagesbig/{big_name}.jpg'
        self.image_patch_path = f'./images_patch/{big_name}'
        self.label_yolo = f'./images_patch_detect/{big_name}/labels/'
        self.label_voc = f'./images_patch_detect/{big_name}/labelsvoc'

    def crop_and_detect(self):
        '''
        1.将大图裁剪为小图，并进行检测
        '''
        split_image(self.input_big_path, self.image_patch_path)
        opt = detect.parse_opt()
        opt.source = f'./images_patch/{self.big_name}'
        opt.project = './images_patch_detect'
        opt.name = f'{self.big_name}'
        detect.main(opt)

    def convert_labels(self):
        '''
        2.将yolo格式标签转换为voc格式
        '''
        conver_labels(self.label_yolo, self.label_voc)

    def detect_big_image(self):
        '''
        3.对标签进行去重，得到最终大图的检测结果
        '''
        result = big_detect(self.big_name)
        print("幼苗数量为：%d，杂草数量为：%d" % (result[0], result[1]))
        return result

    def mark_missing_plant(self):
        '''
        4.将缺苗框标记到大图上
        '''
        big_miss(self.big_name)
        miss = big_miss(self.big_name)
        print("缺苗数量为：{}".format(miss))
        output_path = f'./img_big_miss/{self.big_name}.jpg'
        return miss, output_path

    def run_detection(self):
        '''
        运行所有的检测任务，并返回幼苗数量、杂草数量和缺苗数量信息
        '''
        self.crop_and_detect()
        self.convert_labels()
        result = self.detect_big_image()
        miss, output_path = self.mark_missing_plant()
        return result[0], result[1], miss, output_path
