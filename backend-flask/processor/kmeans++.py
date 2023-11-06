import numpy as np
from sklearn.cluster import KMeans
import yaml
import os
from PIL import Image

def load_dataset(path, img_size, augment=False):
    # 读取数据集配置文件
    with open(path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    # 解析数据集文件路径
    root = os.path.dirname(path)
    dataset_path = os.path.join(root, data["train"])
    names_path = os.path.join(root, data["names"])

    # 读取类别名称列表
    with open(names_path) as f:
        class_names = f.read().splitlines()

    # 读取数据集中的图像和标注框
    dataset = []
    with open(dataset_path) as f:
        lines = f.readlines()
        for line in lines:
            img_path, *boxes = line.strip().split()
            img_path = os.path.join(root, img_path)

            # 读取图像
            img = Image.open(img_path)
            w, h = img.size

            # 读取标注框
            boxes = [list(map(float, box.split(","))) for box in boxes]
            boxes = [[x * img_size / w, y * img_size / h, w * img_size / h, h * img_size / h] for x, y, w, h in boxes]

            dataset.append({"image_path": img_path, "boxes": boxes, "class_names": class_names})

    return dataset


def kmeans_plus_plus(path, n=9, img_size=640, thr=4.0, gen=1000, verbose=True):
    # 读取数据集
    dataset = load_dataset(path, img_size=img_size, augment=False)

    # 将数据集中的标注框的宽高比缩放到 [0, 1] 范围内
    wh = np.concatenate([d["wh"] for d in dataset], 0)
    wh = wh / img_size
    wh = wh[wh[:, 0] < thr]

    # 使用 KMeans++ 算法进行聚类
    kmeans = KMeans(n_clusters=n, init="k-means++", max_iter=gen, verbose=verbose)
    kmeans.fit(wh)

    # 将聚类中心还原到原始尺寸
    anchors = kmeans.cluster_centers_ * img_size

    # 对锚定框按面积排序
    area = anchors[:, 0] * anchors[:, 1]
    sorted_indices = np.argsort(area)

    return anchors[sorted_indices]

# 对数据集重新计算 anchors
new_anchors = kmeans_plus_plus('./data/sugarcane.yaml', 9, 640, 4.0, 1000, True)
print(new_anchors)
