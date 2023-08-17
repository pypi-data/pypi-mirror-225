"""
应用JAVA程序来做空间矫正和血流灌注重建的处理西门子单延迟、5延迟数据版本
2021-11-14 模块建立
姚泽山
"""

import os
import shutil
import subprocess
import json

import matplotlib
import pydicom
import SimpleITK as sitk
import numpy as np
import math
from . import AnImageDataSorterUtility as SorterUtil
from . import AnImageDCMUtility as DCMUtil
from matplotlib import pyplot as plt


# 西门子1，5延迟处理
class AnImageDataSorterSiemens5:

    def __init__(self):
        self.intermediate_folder = ''
        self.data_type = ""
        self.slice_order = ""
        self.slice_num = 0
        self.init_delay = 0
        self.delay_num = 0
        self.interval = 0
        self.delay_rep = 0
        self.debugMode = False
        self.formatpack = []
        self.row = 0
        self.col = 0
        self.reader_ref = []
        self.writer_cur = []
        self.ref_image_data = []
        self.temp_value = []

    def generate_from_raw_folder(self, seriesm0):
        # print("层数 = {:d}".format(self.slice_num))
        os.makedirs(os.path.join(self.intermediate_folder, "java_temp", "reordered"), exist_ok=True)
        os.makedirs(os.path.join(self.intermediate_folder, "java_temp", "reconstructed"), exist_ok=True)
        self._make_json()

        for i in range(0, len(seriesm0[0]) - 1, 1):
            index = 1 + i * self.slice_num
            # print(seriesm0[0][index])
            shutil.copyfile(seriesm0[0][index], os.path.join(self.intermediate_folder, "java_temp",
                                                          "reordered", "temp_dcm_{:04d}.dcm".format(i)))
        jar_folder = os.path.join(os.getcwd(), "UCLA_java_jar")

        print(jar_folder)
        response = subprocess.run(
            [
                "java", "-jar",
                "-Djava.library.path={}".format(os.path.join(jar_folder, "lib")),
                os.path.join(jar_folder, "ASL_yao_JAVA-master.jar"),
                os.path.join(self.intermediate_folder, "java_temp", "param.json")
            ]
        )
        if response.returncode != 0:
            raise Exception("Java程序运行失败，编号: {:d}".format(response.returncode))

        if os.path.isfile(os.path.join(self.intermediate_folder, "java_temp", "reconstructed", "finished.txt")):
            print("完成用Java的图像重建，开始用Python来调整标签")

        if self.delay_num == 1:
            file_list = ["m0", "cbf"]
            scaling_list = [1, 0.1]
            self._3d_dcm_to_2d_and_nii(file_list[0], file_list[0], 20, scaling_list[0])
            self._3d_dcm_to_2d_and_nii(file_list[1], "asl-" + file_list[1]+"1", 21, scaling_list[1])

        if self.delay_num == 5:  # TODO 增加CBF2-1的输出
            file_list = ["m0", "mcbf", "att", "acbv", "cbf1", "cbf2", "cbf3", "cbf4", "cbf5"]
            scaling_list = [1, 0.1, 0.01, 0.001, 0.1, 0.1, 0.1, 0.1, 0.1]
            self._3d_dcm_to_2d_and_nii(file_list[0], file_list[0], 20, scaling_list[0])
            self._save_head_motion_graph()
            for file_idx in range(1, len(file_list)):
                self._3d_dcm_to_2d_and_nii(file_list[file_idx], "asl-"+file_list[file_idx],
                                           file_idx+20, scaling_list[file_idx])

        print("删除java_temp文件夹，开始自动化所CMD应用")
        shutil.rmtree(os.path.join(self.intermediate_folder, "java_temp"))

    def _save_head_motion_graph(self):
        file_path = os.path.join(self.intermediate_folder, "java_temp", "reconstructed", "headMotion.json")
        save_path = os.path.join(self.intermediate_folder, "headMotion.png")
        with open(file_path, 'r') as f:
            data = json.load(f)
        # print(data)
        fig = plt.figure()
        matplotlib.rcParams['font.family'] = "simsun"
        fig.set_size_inches(6, 2)
        xdata = np.linspace(1, len(data["controlFD"]), len(data["controlFD"]))
        plt.plot(xdata, data["controlFD"], 'bo-', label='无标记像')
        plt.plot(xdata, data["labelFD"], 'ro-', label='标记像')
        plt.xticks(xdata)
        plt.xlabel("图片序号")
        plt.ylabel("头动(mm)")
        plt.legend()
        plt.tight_layout()
        plt.savefig(save_path, dpi=200)
        plt.figure().clear()
        plt.close()
        plt.cla()
        plt.clf()

    def _make_json(self):
        param_json_dict = {"data_type": self.data_type,
                           "slice_order": self.slice_order,
                           "slice_num": self.slice_num,
                           "init_delay": self.init_delay,
                           "delay_num": self.delay_num,
                           "interval": self.interval,
                           "delay_rep": self.delay_rep,
                           "load_path": os.path.join(self.intermediate_folder, "java_temp", "reordered"),
                           "save_path": os.path.join(self.intermediate_folder, "java_temp", "reconstructed")}

        with open(os.path.join(self.intermediate_folder, "java_temp", "param.json"), "w") as fp:
            json.dump(param_json_dict, fp, indent=4)
        print("json文件保存")

    def _3d_dcm_to_2d_and_nii(self, input_name, series_description, series_id, scaling):

        output = DCMUtil.iterative_seq_tag_search(self.ref_image_data, "00200032", [])
        img_pos_pat = output[0]
        output = DCMUtil.iterative_seq_tag_search(self.ref_image_data, "00201041", [])
        if len(output) == 0:
            slice_loc = float(img_pos_pat[2])
        else:
            slice_loc = output[0]
        output = DCMUtil.iterative_seq_tag_search(self.ref_image_data, "00180088", [])
        spacing = float(output[0])
        output = DCMUtil.iterative_seq_tag_search(self.ref_image_data, "00280030", [])
        px_spacing = output[0]
        if input_name == "cbf":
            input_name_mod = input_name+"1"
        else:
            input_name_mod = input_name

        os.makedirs(os.path.join(self.intermediate_folder, 'asl', input_name_mod), exist_ok=True)
        print("读取 "+input_name)
        image = pydicom.dcmread(os.path.join(self.intermediate_folder, "java_temp",
                                             "reconstructed", input_name.upper()+".dcm"))
        arr = image.pixel_array
        self.writer = sitk.ImageFileWriter()
        self.writer.KeepOriginalImageUIDOn()

        skip_tag_list = []
        for i in range(arr.shape[0]):
            image = sitk.GetImageFromArray(arr[i, :, :].astype(np.uint16))

            copy_list = [
                "0010|0010",  # Patient Name
                "0010|0020",  # Patient ID
                "0010|0030",  # Patient Birth Date
                "0020|000d",  # Study Instance UID, for machine consumption
                "0020|0010",  # Study ID, for human consumption
                "0008|0020",  # Study Date
                "0008|0030",  # Study Time
                "0008|0050",  # Accession Number
                "0008|0060",  # Modality
                "0008|0070",  # Manufacturer
                "0008|0080",  # Institution Name
                "0008|1030",  # Study Description
                "0018|0050",  # Slice Thickness
                "0020|0037",  # Image Orientation Patient
                "0028|0030",  # Pixel Spacing
                "0018|0088",  # Slice Spacing
                "0020|000e",  # Series UID
            ]

            for elem in copy_list:
                try:
                    image.SetMetaData(elem, str(self.ref_image_data[elem.replace("|", "")].value))
                except Exception:
                    if elem not in skip_tag_list:
                        skip_tag_list.append(elem)
                        print("跳过了标签：{}".format(elem))

            # image.SetMetaData("0008|0008", "ORIGINAL\\SECONDARY\\ASL\\ANIMAGE")
            image.SetMetaData("0008|0050", str(self.slice_num))
            image.SetMetaData("0020|0013", str(i + 1))
            image.SetMetaData("0020|0037", "1\\0\\0\\0\\1\\0")  # 强制三维图像的垂直性
            image.SetMetaData("0020|0032", str(img_pos_pat[0]) + "\\" + str(img_pos_pat[1]) + "\\" +
                              str(float(img_pos_pat[2]) + i * spacing - (slice_loc >= 0) * 40 * spacing))
            image.SetMetaData("0020|1041", str(slice_loc + i * spacing - (slice_loc >= 0) * 40 * spacing))
            save_path = os.path.join(self.intermediate_folder, "asl", input_name_mod, "{:04}.dcm".format(i + 1))

            self.writer.SetFileName(save_path)
            self.writer.Execute(image)

            temp_image = pydicom.dcmread(save_path)
            temp_image = SorterUtil.add_AnImage_tag(temp_image, series_description)
            temp_image = SorterUtil.modify_series_uid(temp_image, series_description, series_id)
            temp_image[0x0018,0x0088].value = spacing
            temp_image[0x0028,0x0030].value = [float(px_spacing[0]), float(px_spacing[1])]
            if [0x0028, 0x1052] in temp_image:
                temp_image[0x0028, 0x1052].value = 0
            else:
                temp_image.add_new([0x0028, 0x1052], "DS", 0)
            if [0x0028, 0x1053] in temp_image:
                temp_image[0x0028, 0x1053].value = scaling
            else:
                temp_image.add_new([0x0028, 0x1053], "DS", scaling)
            temp_image.save_as(save_path, write_like_original=False)

        DCMUtil.dcm_to_nii(self.intermediate_folder, 'asl', input_name_mod)

    def parse_m0_from_raw_folder(self, seriesm0):
        os.makedirs(os.path.join(self.intermediate_folder, 'asl', 'm0'), exist_ok=True)
        try:
            image_data = pydicom.dcmread(seriesm0[1])
        except:
            image_data = pydicom.dcmread([i for i in seriesm0.values()][1])
        # m0 = image_data.pixel_array
        self.row = image_data[0x0028, 0x0010].value
        self.col = image_data[0x0028, 0x0011].value
        # mask = np.zeros((self.row, self.col))
        # threshold = 0.15
        # mask[m0 < m0.max() * threshold] = 1
        if "MOSAIC" in image_data[0x0008, 0x0008].value:
            slice_num = image_data[0x0019, 0x100A].value
        else:
            slice_num = image_data[0x0028, 0x0008].value
        sn = math.ceil(np.sqrt(slice_num))
        dmrow = image_data[0x0028, 0x0010].value // sn
        siemensst = image_data[0x0018, 0x0050].value
        siemenssl = image_data[0x0020, 0x1041].value
        siemensipp = image_data[0x0020, 0x0032].value
        siemensiop = [1, 0, 0, 0, 1, 0]
        self.formatpack = [slice_num, sn, dmrow, siemensst, siemenssl, siemensipp, siemensiop]
        SorterUtil.demosaic(image_data, image_data.pixel_array, 'asl-m0', 'm0', self.intermediate_folder, self.formatpack)

    def siemens_data_check(self, seriesm0):
        try:
            self.ref_image_data = pydicom.dcmread(seriesm0[0][1])
        except:
            self.ref_image_data = pydicom.dcmread([i for i in seriesm0[0].values()][1])

        if "MOSAIC" in self.ref_image_data[0x0008, 0x0008].value:
            self.data_type = "5delay_mosaic"
            try:
                self.slice_num = int(float(self.ref_image_data[0x0019, 0x100a].value))
            except:
                raise Exception('slice number not found')
            # if float(self.ref_image_data[0x0020,0x1041].value) >= 0:
            #     self.slice_order = "descending"
            # elif float(self.ref_image_data[0x0020,0x1041].value) < 0:
            #     self.slice_order = "ascending"
            self.slice_order = "ascending"
        else:
            self.data_type = "5delay_3d"
            self.slice_num = self.ref_image_data[0x0028, 0x0008].value
            print("该pCASL序列是3D文件（非mosaic）")

    def Sorter(self, intermediate_folder, seriesm0, delay_time, delay_rep, debugMode=False):
        self.intermediate_folder = intermediate_folder
        self.delay_rep = delay_rep
        self.delay_num = len(delay_time)
        self.init_delay = float(delay_time[0])  # 导进来的init_delay其实是每一个delay的时间点
        if len(delay_time) > 1:
            self.interval = float(delay_time[1] - delay_time[0])
        else:
            self.interval = float(0)
        self.debugMode = debugMode
        os.makedirs(os.path.join(self.intermediate_folder, 'asl'), exist_ok=True)
        self.siemens_data_check(seriesm0)
        self.generate_from_raw_folder(seriesm0)
