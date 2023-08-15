#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
# @Time    :  2021/12/4 14:10
# @Author  : chenxw
# @Email   : gisfanmachel@gmail.com
# @File    : aiSettings.py
# @Descr   : AI样本处理
# @Software: PyChar
import glob
import json
import xml.etree.ElementTree as ET
from xml.dom.minidom import Document
import cv2
import numpy as np
from PIL import Image

from vgis_utils.vgis_file.fileTools import FileHelper
from vgis_utils.vgis_image.imageTools import ImageHelper
from vgis_utils.vgis_string.stringTools import StringHelper


# AI样本格式转换
class FileFormatConverter:
    def __init__(self):
        pass

    # pascalVoc转yolo
    def pascalVoc2Yolo(self, xml_file_path, class_file_path, txt_file_path):
        classes_dict = {}
        # class_file_path= "classes.names"
        with open(class_file_path) as f:
            for idx, line in enumerate(f.readlines()):
                class_name = line.strip()
                classes_dict[class_name] = idx

        width, height, objects = self.__pascal_xml_reader(xml_file_path)

        lines = []
        # 标注内容的类别、归一化后的中心点x坐标，归一化后的中心点y坐标，归一化后的目标框宽度w，归一化后的目标况高度h（此处归一化指的是除以图片宽和高）
        for obj in objects:
            x, y, x2, y2 = obj['bbox']
            class_name = obj['name']
            label = classes_dict[class_name]
            cx = (x2 + x) * 0.5 / width
            cy = (y2 + y) * 0.5 / height
            w = (x2 - x) * 1. / width
            h = (y2 - y) * 1. / height
            line = "%s %.6f %.6f %.6f %.6f\n" % (label, cx, cy, w, h)
            lines.append(line)

        # txt_name = filename.replace(".xml", ".vgis_txt").replace("labels_voc", "labels")
        with open(txt_file_path, "w") as f:
            f.writelines(lines)
        # 内部函数，读取pascal xml文件

    # 内部函数，读取pascal xml文件
    def __pascal_xml_reader(self, file_path):
        """ Parse a PASCAL VOC xml vgis_file """
        tree = ET.parse(file_path)
        size = tree.find('size')
        width = int(size.find('width').text)
        height = int(size.find('height').text)
        objects = []
        for obj in tree.findall('object'):
            obj_struct = {}
            obj_struct['name'] = obj.find('name').text
            bbox = obj.find('bndbox')
            obj_struct['bbox'] = [int(bbox.find('xmin').text),
                                  int(bbox.find('ymin').text),
                                  int(bbox.find('xmax').text),
                                  int(bbox.find('ymax').text)]
            objects.append(obj_struct)
        return width, height, objects

    # labelme转yolo
    def labelme2Yolo(self, json_file_path, class_file_path, txt_file_path):
        classes_dict = {}
        # class_file_path= "classes.names"
        with open(class_file_path) as f:
            for idx, line in enumerate(f.readlines()):
                class_name = line.strip()
                classes_dict[class_name] = idx
        lines = []
        with open(json_file_path, 'r', encoding='utf8') as fp:
            json_data = json.load(fp)
            image_width = json_data.get("imageWidth")
            image_height = json_data.get("imageHeight")
            shapes_array = json_data.get("shapes")
            # 标注内容的类别、归一化后的中心点x坐标，归一化后的中心点y坐标，归一化后的目标框宽度w，归一化后的目标况高度h（此处归一化指的是除以图片宽和高）
            for shape_obj in shapes_array:
                class_name = shape_obj.get("label")
                # 针对烟囱样本采集时classname不标准的情况
                if class_name == "yc":
                    class_name = "chimney"
                points_array = shape_obj.get("points")
                x, y, x2, y2 = self.__get_envelop_of_labelme_points(points_array)
                label = classes_dict[class_name]
                cx = (x2 + x) * 0.5 / image_width
                cy = (y2 + y) * 0.5 / image_height
                w = (x2 - x) * 1. / image_width
                h = (y2 - y) * 1. / image_height
                line = "%s %.6f %.6f %.6f %.6f\n" % (label, cx, cy, w, h)
                lines.append(line)
        # txt_name = filename.replace(".xml", ".vgis_txt").replace("labels_voc", "labels")
        with open(txt_file_path, "w") as f:
            f.writelines(lines)

        # 内部函数，读取lalbelme标签点的坐标范围

    # 内部函数，获取labelme里坐标范围
    def __get_envelop_of_labelme_points(self, points_array):
        minx = points_array[0][0]
        miny = points_array[0][1]
        maxx = points_array[0][0]
        maxy = points_array[0][1]
        for point in points_array:
            tmpx = point[0]
            tmpy = point[1]
            if tmpx < minx:
                minx = tmpx
            if tmpy < miny:
                miny = tmpy
            if tmpx > maxx:
                maxx = tmpx
            if tmpy > maxy:
                maxy = tmpy
        return minx, miny, maxx, maxy

    # 加载自己的数据集，只需要所有 labelme 标注出来的 json 文件即可
    def load_dataset(self, path):
        dataset = []
        for json_file_path in glob.glob("{}/*json".format(path)):
            with open(json_file_path, 'r', encoding='utf8') as fp:
                json_data = json.load(fp)
                image_width = json_data.get("imageWidth")
                image_height = json_data.get("imageHeight")
                shapes_array = json_data.get("shapes")
                for shape_obj in shapes_array:
                    points_array = shape_obj.get("points")
                    xmin, ymin, xmax, ymax = self.__get_envelop_of_labelme_points(points_array)
                    # 偏移量
                    xmin = int(xmin) / image_width
                    ymin = int(ymin) / image_height
                    xmax = int(xmax) / image_width
                    ymax = int(ymax) / image_height
                    xmin = np.float64(xmin)
                    ymin = np.float64(ymin)
                    xmax = np.float64(xmax)
                    ymax = np.float64(ymax)
                    # 将Anchor的宽和高放入dateset，运行kmeans获得Anchor
                    dataset.append([xmax - xmin, ymax - ymin])
        return np.array(dataset)

    def __iou(self, box, clusters):
        """
        计算一个 ground truth 边界盒和 k 个先验框(Anchor)的交并比(IOU)值。
        参数box: 元组或者数据，代表 ground truth 的长宽。
        参数clusters: 形如(k,2)的numpy数组，其中k是聚类Anchor框的个数
        返回：ground truth和每个Anchor框的交并比。
        """
        x = np.minimum(clusters[:, 0], box[0])
        y = np.minimum(clusters[:, 1], box[1])
        if np.count_nonzero(x == 0) > 0 or np.count_nonzero(y == 0) > 0:
            raise ValueError("Box has no area")
        intersection = x * y
        box_area = box[0] * box[1]
        cluster_area = clusters[:, 0] * clusters[:, 1]
        iou_ = intersection / (box_area + cluster_area - intersection)
        return iou_

    def avg_iou(self, boxes, clusters):
        """
        计算一个ground truth和k个Anchor的交并比的均值。
        """
        return np.mean([np.max(self.__iou(boxes[i], clusters)) for i in range(boxes.shape[0])])

    def kmeans(self, boxes, k, dist=np.median):
        """
        利用IOU值进行K-means聚类
        参数boxes: 形状为(r, 2)的ground truth框，其中r是ground truth的个数
        参数k: Anchor的个数
        参数dist: 距离函数
        返回值：形状为(k, 2)的k个Anchor框
        """
        # 即是上面提到的r
        rows = boxes.shape[0]
        # 距离数组，计算每个ground truth和k个Anchor的距离
        distances = np.empty((rows, k))
        # 上一次每个ground truth"距离"最近的Anchor索引
        last_clusters = np.zeros((rows,))
        # 设置随机数种子
        np.random.seed()

        # 初始化聚类中心，k个簇，从r个ground truth随机选k个
        clusters = boxes[np.random.choice(rows, k, replace=False)]
        # 开始聚类
        while True:
            # 计算每个ground truth和k个Anchor的距离，用1-IOU(box,anchor)来计算
            for row in range(rows):
                distances[row] = 1 - self.__iou(boxes[row], clusters)
            # 对每个ground truth，选取距离最小的那个Anchor，并存下索引
            nearest_clusters = np.argmin(distances, axis=1)
            # 如果当前每个ground truth"距离"最近的Anchor索引和上一次一样，聚类结束
            if (last_clusters == nearest_clusters).all():
                break
            # 更新簇中心为簇里面所有的ground truth框的均值
            for cluster in range(k):
                clusters[cluster] = dist(boxes[nearest_clusters == cluster], axis=0)
            # 更新每个ground truth"距离"最近的Anchor索引
            last_clusters = nearest_clusters

        return clusters

    # yolo转pascalVOC
    def yolo2pascalVoc(self, txt_file_path, xml_file_path, pic_file_path, class_file_path):
        classes_dict = {}
        # class_file_path= "classes.names"
        with open(class_file_path) as f:
            for idx, line in enumerate(f.readlines()):
                class_name = line.strip()
                classes_dict[idx] = class_name
        file_name = FileHelper.get_file_name(txt_file_path)
        xmlBuilder = Document()
        annotation = xmlBuilder.createElement("annotation")  # 创建annotation标签
        xmlBuilder.appendChild(annotation)
        txtFile = open(txt_file_path)
        txtList = txtFile.readlines()
        img = cv2.imread(pic_file_path)
        Pheight, Pwidth, Pdepth = img.shape

        folder = xmlBuilder.createElement("folder")  # folder标签
        foldercontent = xmlBuilder.createTextNode("driving_annotation_dataset")
        folder.appendChild(foldercontent)
        annotation.appendChild(folder)  # folder标签结束

        filename = xmlBuilder.createElement("filename")  # filename标签
        filenamecontent = xmlBuilder.createTextNode(file_name)
        filename.appendChild(filenamecontent)
        annotation.appendChild(filename)  # filename标签结束

        filename = xmlBuilder.createElement("path")  # path标签
        filenamecontent = xmlBuilder.createTextNode(pic_file_path)
        filename.appendChild(filenamecontent)
        annotation.appendChild(filename)  # path标签结束

        size = xmlBuilder.createElement("size")  # size标签
        width = xmlBuilder.createElement("width")  # size子标签width
        widthcontent = xmlBuilder.createTextNode(str(Pwidth))
        width.appendChild(widthcontent)
        size.appendChild(width)  # size子标签width结束

        height = xmlBuilder.createElement("height")  # size子标签height
        heightcontent = xmlBuilder.createTextNode(str(Pheight))
        height.appendChild(heightcontent)
        size.appendChild(height)  # size子标签height结束

        depth = xmlBuilder.createElement("depth")  # size子标签depth
        depthcontent = xmlBuilder.createTextNode(str(Pdepth))
        depth.appendChild(depthcontent)
        size.appendChild(depth)  # size子标签depth结束

        annotation.appendChild(size)  # size标签结束

        for j in txtList:
            oneline = j.strip().split(" ")
            object = xmlBuilder.createElement("object")  # object 标签
            picname = xmlBuilder.createElement("name")  # name标签
            namecontent = xmlBuilder.createTextNode(classes_dict[oneline[0]])
            picname.appendChild(namecontent)
            object.appendChild(picname)  # name标签结束

            pose = xmlBuilder.createElement("pose2")  # pose标签
            posecontent = xmlBuilder.createTextNode("Unspecified")
            pose.appendChild(posecontent)
            object.appendChild(pose)  # pose标签结束

            truncated = xmlBuilder.createElement("truncated")  # truncated标签
            truncatedContent = xmlBuilder.createTextNode("0")
            truncated.appendChild(truncatedContent)
            object.appendChild(truncated)  # truncated标签结束

            difficult = xmlBuilder.createElement("difficult")  # difficult标签
            difficultcontent = xmlBuilder.createTextNode("0")
            difficult.appendChild(difficultcontent)
            object.appendChild(difficult)  # difficult标签结束

            bndbox = xmlBuilder.createElement("bndbox")  # bndbox标签
            xmin = xmlBuilder.createElement("xmin")  # xmin标签
            mathData = int(((float(oneline[1])) * Pwidth + 1) - (float(oneline[3])) * 0.5 * Pwidth)
            xminContent = xmlBuilder.createTextNode(str(mathData))
            xmin.appendChild(xminContent)
            bndbox.appendChild(xmin)  # xmin标签结束

            ymin = xmlBuilder.createElement("ymin")  # ymin标签
            mathData = int(((float(oneline[2])) * Pheight + 1) - (float(oneline[4])) * 0.5 * Pheight)
            yminContent = xmlBuilder.createTextNode(str(mathData))
            ymin.appendChild(yminContent)
            bndbox.appendChild(ymin)  # ymin标签结束

            xmax = xmlBuilder.createElement("xmax")  # xmax标签
            mathData = int(((float(oneline[1])) * Pwidth + 1) + (float(oneline[3])) * 0.5 * Pwidth)
            xmaxContent = xmlBuilder.createTextNode(str(mathData))
            xmax.appendChild(xmaxContent)
            bndbox.appendChild(xmax)  # xmax标签结束

            ymax = xmlBuilder.createElement("ymax")  # ymax标签
            mathData = int(((float(oneline[2])) * Pheight + 1) + (float(oneline[4])) * 0.5 * Pheight)
            ymaxContent = xmlBuilder.createTextNode(str(mathData))
            ymax.appendChild(ymaxContent)
            bndbox.appendChild(ymax)  # ymax标签结束

            object.appendChild(bndbox)  # bndbox标签结束

            annotation.appendChild(object)  # object标签结束

        f = open(xml_file_path, 'w')
        xmlBuilder.writexml(f, indent='\t', newl='\n', addindent='\t', encoding='utf-8')
        f.close()

    # pascalVoc转labelme
    def pascalVoc2Labelme(self, xml_file_path, pic_file_path, json_file_path):
        # classes_dict = {}
        # # class_file_path= "classes.names"
        # with open(class_file_path) as f:
        #     for idx, line in enumerate(f.readlines()):
        #         class_name = line.strip()
        #         classes_dict[class_name] = idx
        width, height, objects = self.__pascal_xml_reader(xml_file_path)
        shapes_array = []
        for obj in objects:
            x, y, x2, y2 = obj['bbox']
            class_name = obj['name']
            # label = classes_dict[class_id]
            shape_dict = {}
            shape_dict["label"] = class_name
            points_array = [[float(x), float(y)], [float(x2), float(y)], [float(x2), float(y2)], [float(x), float(y2)]]
            shape_dict["points"] = points_array
            shape_dict["group_id"] = None
            shape_dict["shape_type"] = "polygon"
            shape_dict["flags"] = {}
            shapes_array.append(shape_dict)
        json_file_dict = self.__build_lableme_json_dict(shapes_array, pic_file_path)
        self.__write_json_file(json_file_dict, json_file_path)

    # 内部函数，构建labelme的json字典数据
    def __build_lableme_json_dict(self, shapes_array, pic_file_path):
        json_file_dict = {}
        json_file_dict["version"] = "4.6.0"
        json_file_dict["flags"] = {}
        json_file_dict["shapes"] = shapes_array
        json_file_dict["imagePath"] = FileHelper.get_file_name(pic_file_path)
        # 图像的base64取值有问题
        # json_file_dict["imageData"] = ImageHelper.convert2Base64(pic_file_path)
        json_file_dict["imageData"] = None
        img = Image.open(pic_file_path)
        json_file_dict["imageHeight"] = img.height
        json_file_dict["imageWidth"] = img.width
        return json_file_dict

    # 内部函数，将字典对象写入json文件
    def __write_json_file(self, json_file_dict, json_file_path):
        json_str = json.dumps(json_file_dict, indent=4)
        with open(json_file_path, 'w') as json_file:
            json_file.write(json_str)

    # DOTA转labelme
    def DOTA2Labelme(self, txt_file_path, pic_file_path, json_file_path):
        txtFile = open(txt_file_path)
        txtList = txtFile.readlines()
        shapes_array = []
        # 前两行不读
        for j in txtList[2:]:
            oneline = j.strip().split(" ")
            label = oneline[8]
            shape_dict = {}
            shape_dict["label"] = label
            points_array = [[float(oneline[0]), float(oneline[1])], [float(oneline[2]), float(oneline[3])],
                            [float(oneline[4]), float(oneline[5])], [float(oneline[6]), float(oneline[7])]]
            shape_dict["points"] = points_array
            shape_dict["group_id"] = None
            shape_dict["shape_type"] = "polygon"
            shape_dict["flags"] = {}
            shapes_array.append(shape_dict)
        json_file_dict = self.__build_lableme_json_dict(shapes_array, pic_file_path)
        self.__write_json_file(json_file_dict, json_file_path)

    # UCAS转labelme
    def UCAS2Labelme(self, txt_file_path, pic_file_path, json_file_path, label_name):
        txtFile = open(txt_file_path)
        txtList = txtFile.readlines()
        shapes_array = []
        for j in txtList:
            oneline = j.strip().split("\t")
            shape_dict = {}
            shape_dict["label"] = label_name
            # 校正前的范围,不是矩形
            points_array = [[float(oneline[0]), float(oneline[1])], [float(oneline[2]), float(oneline[3])],
                            [float(oneline[4]), float(oneline[5])], [float(oneline[6]), float(oneline[7])]]
            # 校正后的范围
            # minx = float(oneline[9])
            # miny = float(oneline[10])
            # maxx = minx+float(oneline[11])
            # maxy = miny+float(oneline[12])
            # points_array = [[minx, miny], [maxx, miny],
            #                 [maxx, maxy], [minx, maxy]]
            shape_dict["points"] = points_array
            shape_dict["group_id"] = None
            shape_dict["shape_type"] = "polygon"
            shape_dict["flags"] = {}
            shapes_array.append(shape_dict)
        json_file_dict = self.__build_lableme_json_dict(shapes_array, pic_file_path)
        self.__write_json_file(json_file_dict, json_file_path)

    # NWPU转labelme
    def NWPU2Labelme(self, txt_file_path, class_file_path, pic_file_path, json_file_path):
        classes_dict = {}
        # class_file_path= "classes.names"
        with open(class_file_path) as f:
            for idx, line in enumerate(f.readlines()):
                class_name = line.strip()
                classes_dict[idx] = class_name
        txtFile = open(txt_file_path)
        txtList = txtFile.readlines()
        shapes_array = []
        for j in txtList:
            oneline = j.strip().split(",")
            class_id = oneline[2]
            shape_dict = {}
            shape_dict["label"] = classes_dict[class_id]
            minx_str = StringHelper.get_number_in_str(oneline[0].split(",").replace(" ", ""))
            miny_str = StringHelper.get_number_in_str(oneline[1].split(",").replace(" ", ""))
            maxx_str = StringHelper.get_number_in_str(oneline[2].split(",").replace(" ", ""))
            maxy_str = StringHelper.get_number_in_str(oneline[3].split(",").replace(" ", ""))
            minx = float(minx_str)
            miny = float(miny_str)
            maxx = float(maxx_str)
            maxy = float(maxy_str)
            points_array = [[minx, miny], [maxx, miny],
                            [maxx, maxy], [minx, maxy]]
            shape_dict["points"] = points_array
            shape_dict["group_id"] = None
            shape_dict["shape_type"] = "polygon"
            shape_dict["flags"] = {}
            shapes_array.append(shape_dict)
        json_file_dict = self.__build_lableme_json_dict(shapes_array, pic_file_path)
        self.__write_json_file(json_file_dict, json_file_path)

    # HRSC转为labelme
    def HRSC2Labelme(self, xml_file_path, pic_file_path, json_file_path, label_name):
        tree = ET.parse(xml_file_path)
        shapes_array = []
        HRSC_Objects = tree.find('HRSC_Objects')
        if len(HRSC_Objects.findall('HRSC_Object')) > 0:
            for obj in HRSC_Objects.findall('HRSC_Object'):
                shape_dict = {}
                shape_dict["label"] = label_name
                minx_str = obj.find('box_xmin').text
                miny_str = obj.find('box_ymin').text
                maxx_str = obj.find('box_xmax').text
                maxy_str = obj.find('box_ymax').text
                minx = float(minx_str)
                miny = float(miny_str)
                maxx = float(maxx_str)
                maxy = float(maxy_str)
                points_array = [[minx, miny], [maxx, miny],
                                [maxx, maxy], [minx, maxy]]
                shape_dict["points"] = points_array
                shape_dict["group_id"] = None
                shape_dict["shape_type"] = "polygon"
                shape_dict["flags"] = {}
                shapes_array.append(shape_dict)
            json_file_dict = self.__build_lableme_json_dict(shapes_array, pic_file_path)
            self.__write_json_file(json_file_dict, json_file_path)
        else:
            print("当前图片的标签数据为空")

    # 根据labelme标签数据生成二值图
    def build_binary_image_by_lableme(self, input_pic_file_path, result_pic_file_path, json_file_path):
        image_operator = ImageHelper()
        while_region_array = []
        with open(json_file_path, 'r', encoding='utf8') as fp:
            json_data = json.load(fp)
            shapes_array = json_data.get("shapes")
            for shape_obj in shapes_array:
                points_array = shape_obj.get("points")
                region_data = []
                for each_point in points_array:
                    region_data.append(each_point[0])
                    region_data.append(each_point[1])
                while_region_array.append(region_data)
        image_operator.build_binary_image(input_pic_file_path, result_pic_file_path, while_region_array)

    # VEDAI转换为pascalVoc
    def vedai2PascalVoc(self, txt_file_path, xml_file_path, pic_file_path):
        img_data = cv2.imread(pic_file_path)
        txt_data = open(txt_file_path, 'r').readlines()
        boxes_all = self.__format_vedai_label(txt_data)
        self.save_to_xml(xml_file_path, img_data.shape[0], img_data.shape[1], boxes_all)

    # 内部函数，转换为pascalvoc
    def __save_to_pascal_xml(self, save_path, im_height, im_width, objects_axis):
        im_depth = 0
        object_num = len(objects_axis)
        doc = Document()

        annotation = doc.createElement('annotation')
        doc.appendChild(annotation)

        folder = doc.createElement('folder')
        folder_name = doc.createTextNode('VOC2007')
        folder.appendChild(folder_name)
        annotation.appendChild(folder)

        filename = doc.createElement('filename')
        filename_name = doc.createTextNode(save_path.split('/')[-1])
        filename.appendChild(filename_name)
        annotation.appendChild(filename)

        source = doc.createElement('source')
        annotation.appendChild(source)

        database = doc.createElement('database2')
        database.appendChild(doc.createTextNode('The VOC2007 Database'))
        source.appendChild(database)

        annotation_s = doc.createElement('annotation')
        annotation_s.appendChild(doc.createTextNode('PASCAL VOC2007'))
        source.appendChild(annotation_s)

        image = doc.createElement('vgis_image')
        image.appendChild(doc.createTextNode('flickr'))
        source.appendChild(image)

        flickrid = doc.createElement('flickrid')
        flickrid.appendChild(doc.createTextNode('322409915'))
        source.appendChild(flickrid)

        owner = doc.createElement('owner')
        annotation.appendChild(owner)

        flickrid_o = doc.createElement('flickrid')
        flickrid_o.appendChild(doc.createTextNode('knautia'))
        owner.appendChild(flickrid_o)

        name_o = doc.createElement('name')
        name_o.appendChild(doc.createTextNode('dear_jing'))
        owner.appendChild(name_o)

        size = doc.createElement('size')
        annotation.appendChild(size)
        width = doc.createElement('width')
        width.appendChild(doc.createTextNode(str(im_width)))
        height = doc.createElement('height')
        height.appendChild(doc.createTextNode(str(im_height)))
        depth = doc.createElement('depth')
        depth.appendChild(doc.createTextNode(str(im_depth)))
        size.appendChild(width)
        size.appendChild(height)
        size.appendChild(depth)
        segmented = doc.createElement('segmented')
        segmented.appendChild(doc.createTextNode('0'))
        annotation.appendChild(segmented)
        for i in range(object_num):
            objects = doc.createElement('object')
            annotation.appendChild(objects)
            object_name = doc.createElement('name')
            object_name.appendChild(doc.createTextNode(str(objects_axis[i][-1])))
            objects.appendChild(object_name)
            pose = doc.createElement('pose2')
            pose.appendChild(doc.createTextNode('Unspecified'))
            objects.appendChild(pose)
            truncated = doc.createElement('truncated')
            truncated.appendChild(doc.createTextNode(str(objects_axis[i][9])))
            objects.appendChild(truncated)
            difficult = doc.createElement('difficult')
            difficult.appendChild(doc.createTextNode(str(objects_axis[i][8])))
            objects.appendChild(difficult)
            bndbox = doc.createElement('bndbox')
            objects.appendChild(bndbox)

            x0 = doc.createElement('x0')
            x0.appendChild(doc.createTextNode(str((objects_axis[i][0]))))
            bndbox.appendChild(x0)
            y0 = doc.createElement('y0')
            y0.appendChild(doc.createTextNode(str((objects_axis[i][4]))))
            bndbox.appendChild(y0)

            x1 = doc.createElement('x1')
            x1.appendChild(doc.createTextNode(str((objects_axis[i][1]))))
            bndbox.appendChild(x1)
            y1 = doc.createElement('y1')
            y1.appendChild(doc.createTextNode(str((objects_axis[i][5]))))
            bndbox.appendChild(y1)

            x2 = doc.createElement('x2')
            x2.appendChild(doc.createTextNode(str((objects_axis[i][2]))))
            bndbox.appendChild(x2)
            y2 = doc.createElement('y2')
            y2.appendChild(doc.createTextNode(str((objects_axis[i][6]))))
            bndbox.appendChild(y2)

            x3 = doc.createElement('x3')
            x3.appendChild(doc.createTextNode(str((objects_axis[i][3]))))
            bndbox.appendChild(x3)
            y3 = doc.createElement('y3')
            y3.appendChild(doc.createTextNode(str((objects_axis[i][7]))))
            bndbox.appendChild(y3)

        f = open(save_path, 'w')
        f.write(doc.toprettyxml(indent=''))
        f.close()

    # 内部函数，格式化vedai
    def __format_vedai_label(self, txt_list):
        # class_list = ['plane', 'boat', 'camping_car', 'car', 'pick-up', 'tractor', 'truck', 'van', 'vehicle']
        class_list = {'plane': 31, 'boat': 23, 'camping_car': 5, 'car': 1, 'pick-up': 11, 'tractor': 4, 'truck': 2,
                      'van': 9,
                      'vehicle': 10, 'others': 0}
        format_data = []

        for i in txt_list:
            if len(i.split(' ')) < 14:
                continue
            flag = False
            for k, v in class_list.items():
                if v == int(i.split(' ')[3].split('\n')[0]):
                    format_data.append(
                        [float(xy) for xy in i.split(' ')[6:14]] + [int(x) for x in i.split(' ')[4:6]] + [k]
                    )
                    flag = True
            if not flag:
                format_data.append(
                    [float(xy) for xy in i.split(' ')[6:14]] + [int(x) for x in i.split(' ')[4:6]] + ['others']
                )

        return np.array(format_data)


# pascalxml转labelme成单元测试方法
def pascalVoc2Labelme_test(file_converter):
    xml_file_path = "G:\\AI\\train_data\\样本\\oiltank\\Annotation\\xml\\oiltank_1.xml"
    # class_file_path = "G:\\AI\\train_data\\样本\\oiltank\\Annotation\\classes.names"
    pic_file_path = "G:\\AI\\train_data\\样本\\oiltank\\JPEGImages\\oiltank_1.jpg"
    json_file_path = "G:\\AI\\train_data\\样本\\oiltank\\Annotation\\labelme\\oiltank_1.json"
    file_converter.pascalVoc2Labelme(xml_file_path, pic_file_path, json_file_path)


def build_binary_image_by_lableme_test(file_converter):
    input_pic_file_path = "G:\\AI\\train_data\\样本\\oiltank\\JPEGImages\\oiltank_1.jpg"
    result_pic_file_path = "G:\\AI\\train_data\\样本\\oiltank\\BianryImages\\oiltank_1.jpg"
    json_file_path = "G:\\AI\\train_data\\样本\\oiltank\\Annotation\\labelme\\oiltank_1.json"
    file_converter.build_binary_image_by_lableme(input_pic_file_path, result_pic_file_path, json_file_path)


def UCAS2Labelme_test(file_converter):
    txt_file_path = "G:\\AI\\train_data\\样本\\UCAS_AOD\\中科院大学高清航拍目标数据集合\\CAR\\P0001.vgis_txt"
    pic_file_path = "G:\\AI\\train_data\\样本\\UCAS_AOD\\中科院大学高清航拍目标数据集合\\CAR\\P0001.png"
    json_file_path = "G:\\AI\\train_data\\样本\\UCAS_AOD\\中科院大学高清航拍目标数据集合\\CAR\\P0001.json"
    file_converter.UCAS2Labelme(txt_file_path, pic_file_path, json_file_path, "car")


def HRSC2Labelme_test(file_converter):
    xml_file_path = "G:\\AI\\train_data\\样本\\HRSC2016\\HRSC\\HRSC2016\\FullDataSet\\Annotations\\100000001.xml"
    pic_file_path = "G:\\AI\\train_data\\样本\\HRSC2016\\HRSC\\HRSC2016\\FullDataSet\\AllImages\\100000001.bmp"
    json_file_path = "G:\\AI\\train_data\\样本\\HRSC2016\\HRSC\\HRSC2016\\FullDataSet\\labelme\\100000001.json"
    file_converter.HRSC2Labelme(xml_file_path, pic_file_path, json_file_path, "boat")


def Labelme2Yolo_test(file_converter):
    json_file_path = "G:\\AI\\train_data\\样本\\send\\火电站\高矮烟囱_汇总\\LabelImages\\00004_3.json"
    class_file_path = "G:\\AI\\train_data\\样本\\send\\火电站\\高矮烟囱_汇总\\Yolo\\classes.names"
    txt_file_path = "G:\\AI\\train_data\\样本\\send\\火电站\\高矮烟囱_汇总\\Yolo\\labels\\00004_3.vgis_txt"
    file_converter.labelme2Yolo(json_file_path, class_file_path, txt_file_path)


# 主入口,进行测试
if __name__ == '__main__':
    try:
        file_converter = FileFormatConverter()
        # 测试pascalvoc转换labelme
        # pascalVoc2Labelme_test(file_converter)
        # 测试lablme标签生成二值图
        # build_binary_image_by_lableme_test(file_converter)
        # 测试UCAS转labelme
        # UCAS2Labelme_test(file_converter)
        # 测试HRSC转labelme
        # HRSC2Labelme_test(file_converter)
        # 测试labelme转yolo
        Labelme2Yolo_test(file_converter)

    except Exception as tm_exp:
        print("测试用例失败：{}".format(str(tm_exp)))
