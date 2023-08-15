#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
# @Time    :  2023/3/23 11:02
# @Author  : chenxw
# @Email   : gisfanmachel@gmail.com
# @File    : ocrTools.py
# @Descr   : 
# @Software: PyCharm
import base64
import json
import os
import urllib
import requests

# 高精度OCR
def ocr_file_high_precision_version(API_KEY, SECRET_KEY, file_path):
    (file_pre_path, temp_filename) = os.path.split(file_path)
    (shot_name, file_ext) = os.path.splitext(temp_filename)
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=" + get_access_token(API_KEY,
                                                                                                     SECRET_KEY)
    # pdf能识别出签名，但不准，同时字符中间的空格会去掉,结果有46行
    if file_ext.lower() == ".pdf":
        payload = "pdf_file=" + get_file_content_as_base64(file_path, True)
    # 图片识别不出签名，但字符中间的空格能识别，结果有45行
    else:
        payload = "image=" + get_file_content_as_base64(file_path, True)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    json_dict = json.loads(response.text)
    return json_dict


# 高精度ORC并返回像素位置
def ocr_file_high_precision_versio_position(API_KEY, SECRET_KEY, file_path):
    (file_pre_path, temp_filename) = os.path.split(file_path)
    (shot_name, file_ext) = os.path.splitext(temp_filename)
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate?access_token=" + get_access_token(API_KEY, SECRET_KEY)
    # pdf能识别出签名，但不准，同时字符中间的空格会去掉,结果有46行
    if file_ext.lower() == ".pdf":
        payload = "pdf_file=" + get_file_content_as_base64(file_path, True)
    # 图片识别不出签名，但字符中间的空格能识别，结果有45行
    else:
        payload = "image=" + get_file_content_as_base64(file_path, True)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    json_dict = json.loads(response.text)
    return json_dict


def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content


def get_access_token(API_KEY, SECRET_KEY):
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


if __name__ == '__main__':
    file_path = "E:\\work-维璟\\2 项目实施\\2.1行业应用部\\54保险OCR识别\原油附件压缩包\\附件2收到版.pdf"
    ocr_file_high_precision_version(file_path)
