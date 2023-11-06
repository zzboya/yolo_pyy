# detect.py

import sys
from pathlib import Path

import numpy as np
import cv2
import functools
from pathlib import Path


def big_detect(big_name):
    iou_threshold = 0.15  # 重叠区域阈值
    def soft_nms(bounding_boxes, confidence_score, threshold, label_boxes):
        # # 如果没有边界框，则返回空列表
        if len(bounding_boxes) == 0:
            return [], []
        bounding_boxes=bounding_boxes.astype(float)
        label_boxes = np.array(label_boxes).reshape(-1)
        # 边界框
        boxes = np.array(bounding_boxes)

        # coordinates of bounding boxes
        start_x = boxes[:, 0]
        start_y = boxes[:, 1]
        end_x = boxes[:, 2]
        end_y = boxes[:, 3]

        # 边界框置信度得分
        scorelist=np.array(confidence_score.reshape(-1)).astype(float)
        score = np.array(scorelist)

        # 挑选的边界框
        picked_boxes = []
        picked_score = []
        picked_label=[]
        sg = []
        wd = []
        # 计算所有边界框的面积
        areas = (end_x - start_x + 1) * (end_y - start_y + 1)

        # 根据边界框置信度得分排序
        order = np.argsort(score)

        # 遍历边界框
        while order.size > 0:
            # The index of largest confidence score
            index = order[-1]
            if label_boxes[index] == "0":
                sg.append(bounding_boxes[index])
            else:
                wd.append(bounding_boxes[index])
            # 选择得分最高的边界框
            picked_boxes.append(bounding_boxes[index])
            picked_score.append(confidence_score[index])
            picked_label.append(label_boxes[index])
            # 计算交并比(IOU)
            x1 = np.maximum(start_x[index], start_x[order[:-1]])
            x2 = np.minimum(end_x[index], end_x[order[:-1]])
            y1 = np.maximum(start_y[index], start_y[order[:-1]])
            y2 = np.minimum(end_y[index], end_y[order[:-1]])

            # 计算交集面积
            w = np.maximum(0.0, x2 - x1 + 1)
            h = np.maximum(0.0, y2 - y1 + 1)
            intersection = w * h

            # 计算交并比
            ratio = intersection / (areas[index] + areas[order[:-1]] - intersection)

            left = np.where(ratio < threshold)
            order = order[left]
        return picked_boxes, picked_score, picked_label, sg, wd

    # 裁剪小图的路径
    data_root = Path(f'./processor/images_patch/{big_name}')
    label_root=Path(f'./processor/images_patch_detect/{big_name}/labelsvoc')
    tag = '\\'  # 路径分隔符
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
    images_path = data_root.glob('*')
    images_path = [str(path) for path in images_path]
    images_path = sorted(images_path, key=functools.cmp_to_key(custom_sort))
    count = 0
    List = []
    Score = []
    List_all = []
    score_all = []
    label_all=[]
    List_detect = [[] for _ in range(117)]
    Score_detect = [[] for _ in range(117)]
    for i,path in enumerate(images_path):
        # 1.获取每张图的名字
        image_name = path.split(tag)[-1].split('.')[0]
        path = path.split(tag)[-1].split('.')[0].split('_')

        #2.根据名字去标签文件
        label_path=label_root.joinpath(image_name+'.txt')

        #3.读取文件的信息
        label_list = []
        with open(label_path, 'r') as file_obj:  # 打开文件
            for line in file_obj:  # 跳过前2行数据
                if not line:  # 如果存在空白行则执行下一次循环，跳过空白行
                    continue
                line_arr = []  # 用于存储每一行的数据
                for i, data in enumerate(line.split(' ')):
                    data_value = data.strip()  # 删除数字两边的空格
                    line_arr.append(str(data_value))  # 若文件中有字符，则需字符串格式保存
                label_list.append(line_arr)  # 将每一行数据保存
        label_list=np.array(label_list)
        label_dataset={}
        label_dataset['label']=label_list[:,0:1]
        label_dataset['rois']=label_list[:,1:5]
        label_dataset['scores']=label_list[:,5:6]
        # results = model.detect([image], verbose=1)
        r = label_dataset

        N = len(label_dataset['rois'])

        for j in range(N):
            x1,y1,x2,y2 = r['rois'][j]
            y1 = int(y1) + 381 * int(path[0]) # 381 = 600 - 219(高方向重叠像素）
            x1 = int(x1) + 406 * int(path[1]) # 406 = 600 - 194（宽方向重叠像素）
            y2 = int(y2) + 381 * int(path[0])
            x2 = int(x2) + 406 * int(path[1])
            r['rois'][j] = x1,y1,x2,y2 #获取所有标定框坐标
        s = r['rois'].tolist()
        # print(s)
        t = r['scores'].tolist()
        # print(t)
        l=r['label'].tolist()
        if s not in List_all:
            List_all = List_all + s
        if s != []:
            if s not in List:
                List.append(s)
        List_detect[i] = s

        if t not in score_all:
            score_all = score_all + t
        if t !=[]:
            if t not in Score:
                Score.append(t)
        Score_detect[i] = t

        if l not in label_all:
            label_all = label_all + l

    detect_box = []
    for i in range(len(List_detect)):
        if len(List_detect[i]) != 0:
            for lst1 in List_detect[i]:
                detect_box.append(lst1)
        else:
            detect_box.append([])
    score_box = []
    for j in range(len(Score_detect)):
        if len(Score_detect[j]) != 0:
            for sco1 in Score_detect[j]:
                score_box.append(sco1)
        else:
            score_box.append([])

    box = np.array(List_all)
    scores = np.array(score_all)
    picked_boxes, picked_score,picked_label,sg, wd = soft_nms(box, confidence_score = scores, threshold = iou_threshold, label_boxes=label_all)
    count_sugarcane = len(sg)
    count_weed = len(wd)
    picked_boxes = np.array(picked_boxes)
    picked_score = np.array(picked_score)
    # print(picked_boxes)
    Class_id = [1] * len(picked_boxes)
    Class_id = np.array(Class_id)

    #print("本次检测甘蔗的株数为：%d" % count_sugarcane)
    #print("本次检测杂草的株数为：%d" % count_weed)

    def rect(label,x1,y1,x2,y2, img,score):   #画框
        labels = ['sugarcane', 'weed']
        label_int=int(label)
        # 绘图  rectangle()函数需要坐标为整数
        if label_int==0:
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (100,49,237), 4)     #会不会问题出在这里，因为每次都用的Img大图
            #cv2.circle(img, (int(x_center), int(y_center)), 10, (0, 0, 0), -1)   #中心点
            text = labels[label_int] + ' ' + '{:.2f}'.format(float(score[0]))
            (text_width, text_height) = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, thickness=2)[0]
            # Set the text start position
            text_offset_x = int(x1)
            text_offset_y = int(y1) - 5
            # Make the coords of the box with a small padding of two pixels
            box_coords = (
            (text_offset_x, text_offset_y + 5), (text_offset_x + text_width + 2, text_offset_y - text_height - 2))
            cv2.rectangle(img, box_coords[0], box_coords[1], (100,49,237), cv2.FILLED)
            cv2.putText(img, text, (text_offset_x, text_offset_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255),
                        thickness=2)

        else:
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (128,0,0), 4)       #(128,0,0)zacao     (255,0,0)
            text = labels[label_int] + ' ' + '{:.2f}'.format(float(score[0]))
            (text_width, text_height) = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, thickness=2)[0]
            # Set the text start position
            text_offset_x = int(x1)
            text_offset_y = int(y1) - 5
            # Make the coords of the box with a small padding of two pixels
            box_coords = (
                (text_offset_x, text_offset_y + 5), (text_offset_x + text_width + 2, text_offset_y - text_height - 2))
            cv2.rectangle(img, box_coords[0], box_coords[1], (128,0,0), cv2.FILLED)
            cv2.putText(img, text, (text_offset_x, text_offset_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255),
                        thickness=2)

    img = cv2.imread(str(f'./processor/imagesbig/{big_name}.jpg'))

    for i,boxes in enumerate(picked_boxes):
        x1, y1, x2, y2 = boxes
        label=picked_label[i]
        score=picked_score[i]

        rect(label, x1, y1, x2, y2, img, score)  # 这个是生成大图结果

    cv2.imwrite(f'./processor/images_big_detect/{big_name}.png',img)
    #print('大图已经检测完毕')
    return count_sugarcane, count_weed

if __name__ == '__main__':
    if len(sys.argv) > 1:
        big_name = sys.argv[1]    # 获取第一个命令行参数作为big_name
    else:
        big_name = 'ShiSheng01'   # 默认为ShiSheng01

    big_detect(big_name)