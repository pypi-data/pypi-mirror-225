"""
在ge13_data_check里增加检查后延迟标记时间的值以及顺序
之前默认认为标记时间的时间差是0.5秒，文件夹顺序是对的

修改了多余重复的代码用变量代替或用函数归纳
修改了跟Siemens有关的描述 => GE

22年02月06日
姚泽山
"""

import os
import pydicom
import numpy as np
from .AnImageASLUtility import AnImageASLUtility
from . import AnImageDCMUtility as DCMUtil


# GE1-3延迟处理
class AnImageDataSorterGE13:
    def __init__(self):
        self.intr_fldr = ''
        self.delay_num = 0
        self.debugMode = False
        self.raw_data_pwpd = np.zeros((1, 1, 1, 1))
        self.raw_data_cbf = np.zeros((1, 1, 1, 1))
        self.dmst, self.dmsl = 0, 0
        self.dmipp, self.dmiop = [], []
        self.dmrow, self.dmcol, self.dmslc = 0, 0, 0
        self.m0_delay_order, self.m0_delay_list = [], []
        self.cbf_delay_order, self.cbf_delay_list = [], []
        self.descending_order = False
        self.aslutil = AnImageASLUtility()

    def set_up_aslutil(self, seriesm0):
        m0keys = sorted(list(seriesm0[0].keys()))
        image_data = pydicom.dcmread(seriesm0[0][m0keys[1]])
        self.aslutil.set_vendor('ge')
        self.aslutil.set_delay_list(self.m0_delay_list)
        self.aslutil.set_measure_list([1] * self.delay_num)
        self.aslutil.set_scan_parameter(image_data)

    def generate_asl_data(self, seriesm0, seriescbf):
        os.makedirs(os.path.join(self.intr_fldr, 'asl'), exist_ok=True)
        m0keys = sorted(list(seriesm0[self.m0_delay_order[0]].keys()))
        ref_img = seriesm0[self.m0_delay_order[0]][m0keys[1]]

        # 从3DASL图复制当中的M0图
        for series_idx in range(self.delay_num):
            m0keys = sorted(list(seriesm0[self.m0_delay_order[series_idx]].keys()))
            for slice_idx in range(self.dmslc):
                image_data = pydicom.dcmread(seriesm0[self.m0_delay_order[series_idx]][m0keys[slice_idx + 1]])
                self.raw_data_pwpd[:, :, slice_idx, series_idx] = image_data.pixel_array

            if self.descending_order:
                cutting = int(self.dmslc / 2)
                self.raw_data_pwpd[:, :, :cutting, series_idx] = \
                    np.flip(self.raw_data_pwpd[:, :, :cutting, series_idx], axis=2)
                self.raw_data_pwpd[:, :, cutting:, series_idx] = \
                    np.flip(self.raw_data_pwpd[:, :, cutting:, series_idx], axis=2)

        self.raw_data_pwpd[self.raw_data_pwpd < 0] = 0
        self.aslutil.set_raw_data(self.raw_data_pwpd)
        self.aslutil.gen_m0()
        self.aslutil.gen_mask()

        output_array = self.aslutil.get_m0()[:, :, :, 0]
        os.makedirs(os.path.join(self.intr_fldr, 'asl', 'm0'), exist_ok=True)
        series_param = [1, 1, 0]
        DCMUtil.create_dcm_series(output_array, ref_img, self.intr_fldr, 'asl', 'm0', series_param)
        DCMUtil.dcm_to_nii(self.intr_fldr, 'asl', 'm0')

        # 从CBF图复制CBF图，或，从原始数据重建CBF图
        if len(seriescbf) == 0:
            self.aslutil.gen_plds()
            self.aslutil.gen_cbfs_ge()
            output_array = self.aslutil.get_cbfs()
        else:
            for series_idx in range(self.delay_num):
                cbfkeys = sorted(list(seriescbf[self.cbf_delay_order[series_idx]].keys()))
                for slice_idx in range(int(self.dmslc / 2)):
                    image_data = pydicom.dcmread(seriescbf[self.cbf_delay_order[series_idx]][cbfkeys[slice_idx + 1]])
                    array_data = image_data.pixel_array
                    self.raw_data_cbf[:, :, slice_idx, series_idx] = array_data

            if self.descending_order:
                self.raw_data_cbf = self.raw_data_cbf[:, :, ::-1, :]
            output_array = self.raw_data_cbf

        for series_idx in range(self.delay_num):
            os.makedirs(os.path.join(self.intr_fldr, 'asl',
                                     'cbf{:d}'.format(series_idx + 1)), exist_ok=True)
            series_param = [10 + series_idx + 1, 1, 0]
            DCMUtil.create_dcm_series(output_array[:, :, :, series_idx], ref_img, self.intr_fldr, 'asl',
                                      'cbf{:d}'.format(series_idx + 1), series_param)
            DCMUtil.dcm_to_nii(self.intr_fldr, 'asl',
                               'cbf{:d}'.format(series_idx + 1))

        # 若一个延迟以上，生成差异图和3个参数图
        if self.delay_num > 1:
            output_array = output_array[:, :, :, 1:] - output_array[:, :, :, :-1]
            for series_idx in range(1, self.delay_num):
                os.makedirs(os.path.join(self.intr_fldr, 'asl',
                                         'cbf{:d}-{:d}'.format(series_idx + 1, series_idx)), exist_ok=True)
                series_param = [20 + series_idx + 1, 1, 1000]
                DCMUtil.create_dcm_series(output_array[:, :, :, series_idx - 1], ref_img, self.intr_fldr, 'asl',
                                          'cbf{:d}-{:d}'.format(series_idx + 1, series_idx), series_param)
                DCMUtil.dcm_to_nii(self.intr_fldr, 'asl',
                                   'cbf{:d}-{:d}'.format(series_idx + 1, series_idx))

            target_files = ["mcbf", "att", "acbv"]
            scaling = [10, 1000, 1000]
            self.aslutil.gen_plds()
            self.aslutil.gen_wd()
            self.aslutil.gen_att_mapping_DAI()
            self.aslutil.gen_cbf_tcorr_ge()
            self.aslutil.gen_acbv()

            for file_idx in range(len(target_files)):
                os.makedirs(os.path.join(self.intr_fldr, 'asl', '{}'.format(target_files[file_idx])), exist_ok=True)
                if file_idx == 0:
                    output_array = self.aslutil.get_mcbf()
                elif file_idx == 1:
                    output_array = self.aslutil.get_att()
                elif file_idx == 2:
                    output_array = self.aslutil.get_acbv()
                series_param = [30 + file_idx + 1, scaling[file_idx], 0]
                DCMUtil.create_dcm_series(output_array, ref_img, self.intr_fldr, 'asl',
                                          '{}'.format(target_files[file_idx]), series_param)
                DCMUtil.dcm_to_nii(self.intr_fldr, 'asl',
                                   '{}'.format(target_files[file_idx]))

    def ge13_data_check(self, seriesm0, seriescbf):
        image_data = pydicom.dcmread([i for i in seriesm0[0].values()][1], stop_before_pixels=True)
        self.delay_num = len(seriesm0)
        try:
            self.dmslc = image_data[0x0020, 0x1002].value
        except:
            raise Exception('Can not get number of slice!')
        try:
            self.dmrow = image_data[0x0028, 0x0010].value
        except:
            raise Exception('Can not get Row size')
        try:
            self.dmcol = image_data[0x0028, 0x0011].value
        except:
            raise Exception('Can not get Column size')
        try:
            self.dmst = image_data[0x0018, 0x0050].value
        except:
            raise Exception('Can not get SliceThickness')
        try:
            self.dmsl = image_data[0x0020, 0x1041].value
        except:
            raise Exception('Can not get SliceLocation')
        try:
            self.dmipp = image_data[0x0020, 0x0032].value
        except:
            raise Exception('Can not get ImagePositionPatient')
        try:
            self.dmiop = image_data[0x0020, 0x0037].value
        except:
            raise Exception('Can not get ImageOrientationPatient')

        temp_img1 = pydicom.dcmread(seriesm0[0][2], stop_before_pixels=True)
        temp_img2 = pydicom.dcmread(seriesm0[0][3], stop_before_pixels=True)
        self.descending_order = ((temp_img2["00201041"].value - temp_img1["00201041"].value) < 0)

        self.raw_data_pwpd = np.zeros((self.dmrow, self.dmcol, self.dmslc, self.delay_num))
        self.raw_data_cbf = np.zeros((self.dmrow, self.dmcol, int(self.dmslc / 2), self.delay_num))

        if seriesm0:  # 查看PWPD图像的后延迟标记时间以及顺序
            m0_delay_list = []
            for series_idx in seriesm0:
                m0_delay_list.append(series_idx[0][1] / 1000)
            self.m0_delay_order = sorted(range(len(m0_delay_list)), key=lambda k: m0_delay_list[k])
            self.m0_delay_list = sorted(m0_delay_list)

        if seriescbf:  # 查看CBF图像的后延迟标记时间以及顺序
            cbf_delay_list = []
            for series_idx in seriescbf:
                cbf_delay_list.append(series_idx[0][1] / 1000)
            self.cbf_delay_order = sorted(range(len(cbf_delay_list)), key=lambda k: cbf_delay_list[k])
            self.cbf_delay_list = sorted(cbf_delay_list)

    def Sorter(self, intermediate_folder, series, debugMode=False):
        self.intr_fldr = intermediate_folder
        self.debugMode = debugMode

        seriesm0 = series["PWPD"]
        seriescbf = {}
        if "CBF" in series.keys():
            seriescbf = series["CBF"]

        self.ge13_data_check(seriesm0, seriescbf)
        print(self.cbf_delay_list)
        self.set_up_aslutil(seriesm0)
        self.generate_asl_data(seriesm0, seriescbf)
