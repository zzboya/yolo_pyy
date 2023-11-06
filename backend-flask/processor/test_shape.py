import os
import numpy as np
import cv2
import functools
from pathlib import Path


# 修改为自己的识别类别
class_names = ['BG', 'sugarcane']
width=600
height=600
width_big = 5472
height_big = 3648
# conf_threshold = 0.7 #置信度阈值
iou_threshold = 0.15  #重叠区域阈值
ROOT_DIR = os.getcwd()

MODEL_DIR='./logs'


def nms(bounding_boxes, confidence_score, threshold,label_boxes):
    if len(bounding_boxes) == 0:
        return [], []
    bounding_boxes=bounding_boxes.astype(float)
    label_boxes = np.array(label_boxes).reshape(-1)
    # Bounding boxes
    boxes = np.array(bounding_boxes)

    # coordinates of bounding boxes
    start_x = boxes[:, 0]
    start_y = boxes[:, 1]
    end_x = boxes[:, 2]
    end_y = boxes[:, 3]

    # Confidence scores of bounding boxes
    scorelist=np.array(confidence_score.reshape(-1)).astype(float)
    score = np.array(scorelist)

    # Picked bounding boxes
    picked_boxes = []
    picked_score = []
    picked_label=[]
    a=[]
    # Compute areas of bounding boxes
    areas = (end_x - start_x + 1) * (end_y - start_y + 1)

    # Sort by confidence score of bounding boxes
    order = np.argsort(score)

    # Iterate bounding boxes
    while order.size > 0:
        # The index of largest confidence score
        index = order[-1]
        if label_boxes[index] == "0":
            a.append(bounding_boxes[index])
        # Pick the bounding box with largest confidence score
        picked_boxes.append(bounding_boxes[index])
        picked_score.append(confidence_score[index])
        picked_label.append(label_boxes[index])
        # Compute ordinates of intersection-over-union(IOU)
        x1 = np.maximum(start_x[index], start_x[order[:-1]])
        x2 = np.minimum(end_x[index], end_x[order[:-1]])
        y1 = np.maximum(start_y[index], start_y[order[:-1]])
        y2 = np.minimum(end_y[index], end_y[order[:-1]])

        # Compute areas of intersection-over-union
        w = np.maximum(0.0, x2 - x1 + 1)
        h = np.maximum(0.0, y2 - y1 + 1)
        intersection = w * h

        # Compute the ratio between intersection and union
        ratio = intersection / (areas[index] + areas[order[:-1]] - intersection)

        left = np.where(ratio < threshold)
        order = order[left]
    return picked_boxes, picked_score,picked_label,a
# 裁剪小图的路径
data_root = Path(r'E:\model\yoloair-main\yoloair-main\images_patch\ShiSheng07')
# label_root=Path(r'E:\model\yoloair-main\yoloair-main\runs\detect\exp66\labelsvoc')
label_root=Path(r'E:\model\yoloair-main\yoloair-main\images_label\ShiSheng07\labelsvoc')
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
    # image = cv2.imread(path)
    # image = skimage.io.imread(path)
    # image = cv2.resize(image, (width, height))
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

    # 补充NMS代码
    N = len(label_dataset['rois'])
    # if not N:
    #     print("\n*** No instances to display *** \n")
    # else:
    #     assert r['rois'].shape[0] == r['masks'].shape[-1] == r['class_ids'].shape[0]
    for j in range(N):
        # Bounding box
        # if not np.any(r['rois'][j]):
        #     # Skip this instance. Has no bbox. Likely lost in image cropping.
        #     continue
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


print(List_detect) # List_detect为边框和空列表（没有甘蔗的图片），且第一维度的对象是同一张图片的
print(Score_detect) # Score_detect为置信度和空列表（没有甘蔗的图片），且同一子列表的置信度是同一张图片上所有边框的置信度

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

print(detect_box) # 所有边框组成的列表，每一个子列表代表一个边框，空列表表示图片中没有甘蔗
print(List_all) # 所有边框组成的列表，每一个子列表代表一个边框，没有空列表
print(List) # 每一个元素代表一张图片上所有的边框，不包含没有甘蔗的图片
print(score_box)
print(score_all)
print(Score)
print(np.shape(List_detect))
print(np.shape(Score_detect))
box = np.array(List_all)
scores = np.array(score_all)
print(box)
print(scores)
# selected_indices = tf.image.non_max_suppression(box,scores=scores,max_output_size=300,iou_threshold=iou_threshold)
# # max_output_size为检测的最多目标数
# selected_boxes = tf.gather(box,selected_indices)
# print(type(selected_boxes))
picked_boxes, picked_score,picked_label,a = nms(box, confidence_score = scores, threshold = iou_threshold,label_boxes=label_all)
print(picked_boxes)
print(type(picked_boxes))
print(picked_score)
print(type(picked_score))
print(len(picked_boxes))
print(len(picked_score))
count_sugarcane = len(a)
picked_boxes = np.array(picked_boxes)
picked_score = np.array(picked_score)
print(picked_boxes)
Class_id = [1] * len(picked_boxes)
Class_id = np.array(Class_id)
print(Class_id)
print(type(Class_id))

# 大图的读取路径
# IMAGE_DIR_big = os.path.join(ROOT_DIR, "images_big")
# file_names_big = next(os.walk(IMAGE_DIR_big))[2]
# image_big = skimage.io.imread(os.path.join(IMAGE_DIR_big, random.choice(file_names_big)))
data_root_big = Path('./images_big')
images_path_big = data_root_big.glob('*')
images_path_big = [str(path) for path in images_path_big]
# imc=io.imread(r'E:\model\yoloair-main\yoloair-main\images_big\ShiSheng07.jpg')
# for path in images_path_big:
#     # image = cv2.imread(path)
#     image = io.imread(path)
#     image = cv2.resize(image, (width_big, height_big))
#     # path = path.split(tag)[-1].split('.')[0].split('_')
#     for xyxy in picked_boxes:
#         save_one_box(xyxy, image, file=data_root_big/ 'xxx.jpg', BGR=True)
#
#     # r = results[0]
#     # num_surgarcne = len(r['class_ids'])
#     # count = count + num_surgarcne
#     iou = str(iou_threshold)+"_num"+str(len(picked_boxes))
    # visualize2.display_instances(path, image, picked_boxes , Class_id,
    #                             class_names, picked_score, title=iou)
    # iou = str(iou_threshold) + "_num" + str(len(box))
    # visualize2.display_instances(path, image, box, Class_id,
    #                              class_names, scores, title=iou)
print("本次检测甘蔗的株数为：%d" % count_sugarcane)

def xywh2xyxy(label,x,y,w,h, w1, h1, img,score):
    labels = ['sugarcane', 'weed']
    # print("原图宽高:\nw1={}\nh1={}".format(w1, h1))
    #边界框反归一化
    x_t = x
    y_t = y
    w_t = w
    h_t = h
    # print("反归一化后输出：\n第一个:{}\t第二个:{}\t第三个:{}\t第四个:{}\t\n\n".format(x_t,y_t,w_t,h_t))

    #计算坐标
    # top_left_x = x_t - w_t / 2
    # top_left_y = y_t - h_t / 2
    # bottom_right_x = x_t + w_t / 2
    # bottom_right_y = y_t + h_t / 2
    # print('标签:{}'.format(labels[int(label)]))
    # print("左上x坐标:{}".format(top_left_x))
    # print("左上y坐标:{}".format(top_left_y))
    # print("右下x坐标:{}".format(bottom_right_x))
    # print("右下y坐标:{}".format(bottom_right_y))
    label_int=int(label)
    x_center = (w+x)/2
    y_center = (h+y)/2
    # 绘图  rectangle()函数需要坐标为整数
    if label_int==0:
        cv2.rectangle(img, (int(x), int(y)), (int(w), int(h)), (100,49,237), 4)     #(100,49,237)sugarcane  (0,0,255)
        cv2.circle(img, (int(x_center), int(y_center)), 10, (0, 0, 0), -1)   #中心点
        #cv2.putText(img, labels[label_int]+' '+'{:.2f}'.format(float(score[0])), (int(x), int(y)-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (100,49,237), 2)
        #
        text = labels[label_int] + ' ' + '{:.2f}'.format(float(score[0]))
        (text_width, text_height) = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, thickness=2)[0]
        # Set the text start position
        text_offset_x = int(x)
        text_offset_y = int(y) - 5
        # Make the coords of the box with a small padding of two pixels
        box_coords = (
        (text_offset_x, text_offset_y + 5), (text_offset_x + text_width + 2, text_offset_y - text_height - 2))
        cv2.rectangle(img, box_coords[0], box_coords[1], (100,49,237), cv2.FILLED)
        cv2.putText(img, text, (text_offset_x, text_offset_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255),
                    thickness=2)




    else:
        cv2.rectangle(img, (int(x), int(y)), (int(w), int(h)), (128,0,0), 4)       #(128,0,0)zacao     (255,0,0)
        #cv2.putText(img, labels[label_int]+' '+'{:.2f}'.format(float(score[0])), (int(x), int(y)-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (128,0,0), 2)
        #
        text = labels[label_int] + ' ' + '{:.2f}'.format(float(score[0]))
        (text_width, text_height) = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, thickness=2)[0]
        # Set the text start position
        text_offset_x = int(x)
        text_offset_y = int(y) - 5
        # Make the coords of the box with a small padding of two pixels
        box_coords = (
            (text_offset_x, text_offset_y + 5), (text_offset_x + text_width + 2, text_offset_y - text_height - 2))
        cv2.rectangle(img, box_coords[0], box_coords[1], (128,0,0), cv2.FILLED)
        cv2.putText(img, text, (text_offset_x, text_offset_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255),
                    thickness=2)

    # cv2.imshow('show', img)
    cv2.imwrite(r'E:\model\yoloair-main\yoloair-main\images_big\ShiSheng07\iou0.15.png',img)


    cv2.waitKey(0)  # 按键结束
    cv2.destroyAllWindows()
img = cv2.imread(str(r'E:\model\yoloair-main\yoloair-main\images_big\ShiSheng07\ShiSheng07.jpg'))
h1, w1 = img.shape[:2]
bbox_index = 0
with open(r'E:\model\yoloair-main\yoloair-main\images_big\ShiSheng07\ShiSheng07.txt', "w+") as f:
    data = f.read()
    for i,x1 in enumerate(picked_boxes):
        # 反归一化并得到左上和右下坐标，画出矩形框
        x, y, w, h =x1
        label=picked_label[i]
        score=picked_score[i]

        if int(label) == 0 :
            #f.write(str(bbox_index) + '  ' + str((w+x)/2) + '  ' + str((h+y)/2) +  '  ' + str(label) + '\n')
            f.write(str((w + x) / 2) + '  ' + str((h + y) / 2) + '\n')
            bbox_index += 1
        xywh2xyxy(label,x,y,w,h, w1, h1, img,score)

# count = os.listdir(IMAGE_DIR)
# # print(len(count))
#
# for i in range(0,len(count)):
#     path = os.path.join(IMAGE_DIR, count[i])
#     if os.path.isfile(path):
#         # file_names = next(os.walk(IMAGE_DIR))[2]
#         image = skimage.io.imread(os.path.join(IMAGE_DIR, count[i]))
#         image = cv2.resize(image, (width, height))
#
#         # Run detection
#         results = model.detect([image], verbose=1)
#         r = results[0]
#         visualize.display_instances(count[i],image, r['rois'], r['masks'], r['class_ids'],
#                                     class_names, r['scores'])




# count = os.listdir(IMAGE_DIR)
#
# for i in range(0,len(count)):
#     path = os.path.join(IMAGE_DIR, count[i])
#     if os.path.isfile(path):
#         file_names = next(os.walk(IMAGE_DIR))[2]
#         image = skimage.io.imread(os.path.join(IMAGE_DIR, count[i]))
#         image = cv2.resize(image, (width, height))
#
#         # Run detection
#         results = model.detect([image], verbose=1)
#         r = results[0]
#         visualize.display_instances(count[i],image, r['rois'], r['masks'], r['class_ids'],
#                                     class_names, r['scores'])

