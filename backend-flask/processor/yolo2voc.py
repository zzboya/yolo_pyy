import os

def conver_labels(input_folder, output_folder):
    # 如果输出文件夹不存在，则创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # 打开txt文件
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            input_path = os.path.join(input_folder + filename)
            with open(input_path, 'r') as f:
                lines = f.readlines()

    # 定义输出文件路径
            output_file = os.path.join(output_folder, filename)

            if len(lines) == 0:
                with open(output_file, 'w+') as f_out:
                    f_out.write("0 0 0 0 0 0")
                continue

            # 逐行读取标签信息并写入输出文件中
            with open(output_file, 'w+') as f:
                for line in lines:
                    line = line.strip().split()
                    label = int(line[0])
                    center_x = float(line[1])
                    center_y = float(line[2])
                    width = float(line[3])
                    height = float(line[4])
                    conf = float(line[5])

                    # 计算左上坐标和右下坐标
                    x1 = int((center_x - width / 2) * 600)
                    y1 = int((center_y - height / 2) * 600)
                    x2 = int((center_x + width / 2) * 600)
                    y2 = int((center_y + height / 2) * 600)

                    # 将左上坐标和右下坐标写入输出文件中
                    f.write(f"{label} {x1} {y1} {x2} {y2} {conf} \n")

# input_folder_path = './images_label/ShiSheng03/labels/'
# output_folder = './images_label/ShiSheng03/labelsvoc'    #由x,y,w,h转换成x1,y1,x2,y2
# conver_labels(input_folder_path,output_folder)