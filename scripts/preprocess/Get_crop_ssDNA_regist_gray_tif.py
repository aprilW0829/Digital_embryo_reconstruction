###  测序时候多个胚胎切片放在了一个slice上测序，后续处理得到每个胚胎切片的转录组，需要根据自己人为从整张slice的ssDNA图像中圈出单个胚胎切片的ssDNA图像单独保存，方便后续从整张slice的gem的表达文件中提取分析
#    eg: D05419F6_ssDNA_regist.tif (整张slice) --->  D05419F6_E7.0-4_S33_ssDNA_regist_gray.tif (单个胚胎切片)

import os
import cv2
import numpy as np
import pandas as pd
import subprocess


#folder_path = "/data/work/01.Data/01.tissuecut_image/tissuecut"
folder_path = '/data5/wangxin/20250701_digi_embryo/raw_data/01.Data/05.tissuecut_image_raw/E6.0_embryo/'
file_list = os.listdir(folder_path)


file_names = []
for filename in os.listdir(folder_path):
    file_name = filename.split('.tif')[0]
    file_names.append(file_name)
unique_file_names = pd.unique(file_names)
print(unique_file_names)
print(len(unique_file_names))


#unique_file_names = ['Y01070C5_E6.5-1_S8','Y01070C5_E6.5-1_S9','Y01047C2_E6.5-1_S24','Y01047C2_E6.5-1_S25','Y01047C2_E6.5-1_S26']
#print(unique_file_names)


#search_directory = "/data/input/Files/ResultData/Workflow/MouseEmbryo3D_E7.5_E8.5/"
#find_command = f"find {search_directory} -type f -name '*_ssDNA_regist.tif'"
search_directory = '/data5/wangxin/20250701_digi_embryo/raw_data/01.Data/06.ssDNA/'
find_command = f"find {search_directory} -type f -name '*_ssDNA_regist.tif'"
found_file_paths = subprocess.run(find_command, shell=True, text=True, capture_output=True).stdout.strip().split('\n')
found_file_paths
print(len(found_file_paths))


SN_to_path = {os.path.basename(path).split('_')[0]: path for path in found_file_paths}
SN_to_path


#folder_output_path = "/data/work/01.Data/01.tissuecut_image/tissuecut_ssDNA/"
folder_output_path = '/data5/wangxin/20250701_digi_embryo/raw_data/01.Data/01.tissuecut_image/tissuecut_ssDNA/MouseEmbryo3D_tissuecut_ssDNA_image/'
for i in unique_file_names:
    SN = i.split('_')[0]
    file_name = os.path.join(folder_output_path, i+'_ssDNA_regist_gray.tif')
    print(file_name)
    if not os.path.exists(file_name):
        print(i)
        print(SN)
        # 构建文件的完整路径
        file1_path = os.path.join(folder_path, i+'.tif') # cropped tif
        print(file1_path)

        if SN in SN_to_path:
            print(f"Match SN_ssDNA_regist.tif found for {i}: {SN_to_path[SN]}")
            file2_path = SN_to_path[SN]
            print(file2_path)
        else:
            print(f"No match SN_ssDNA_regist.tif found for {i}")

        # 读取第一张图片
        image1 = cv2.imread(file1_path, cv2.IMREAD_GRAYSCALE)

        # 读取第二张图片
        image2 = cv2.imread(file2_path, cv2.IMREAD_GRAYSCALE)

        # 确保两张图片的尺寸相同
        if image1.shape[:2] != image2.shape[:2]:
            raise ValueError(f"图片 {file1_path} 和 {file2_path} 的尺寸不一致")

        # 创建一个新的图像，初始化为全黑
        new_image = np.zeros_like(image2)

        # 遍历像素并根据第一张图像的像素值来设置第二张图像的像素值
        for x in range(image1.shape[1]):
            for y in range(image1.shape[0]):
                if image1[y, x] == 255:
                    new_image[y, x] = image2[y, x]

        # 保存结果图像，使用第一张图片的文件名作为输出文件名
        cv2.imwrite(file_name, new_image)
