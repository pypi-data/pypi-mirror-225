"""
西门子的PASL后处理
2022-02-11 模块建立
姚泽山
"""

import os
import pydicom
import SimpleITK as sitk
import numpy as np
import math
from . import AnImageDCMUtility as DCMUtil
from . import AnImageDataSorterUtility as SorterUtil
from scipy.ndimage import gaussian_filter


# 西门子PASL1延迟处理
class AnImageDataSorterSiemensPASL:

    def __init__(self):
        self.intermediate_folder = ''
        self.slice_order = 0
        self.slice_num = 0
        self.delay_time = 0
        self.delay_num = 0
        self.delay_rep = 0
        self.label_dur = 0
        self.debugMode = False
        self.formatpack = []
        self.row = 0
        self.col = 0
        self.reader_ref = []
        self.writer_cur = []
        self.ref_image_data = []

    def generate_cbf_2d_pasl(self, series):
        os.makedirs(os.path.join(self.intermediate_folder, 'asl', 'cbf1'), exist_ok=True)
        os.makedirs(os.path.join(self.intermediate_folder, 'asl', 'm0'), exist_ok=True)
        series.pop(0)
        keys = list(series.keys())
        keys.sort()
        image_data = pydicom.dcmread(series[keys[0]])
        self._get_format_pack(image_data)

        m0 = image_data.pixel_array
        SorterUtil.demosaic(image_data, m0, 'asl-m0', 'm0', self.intermediate_folder, self.formatpack)

        pwi = np.zeros(np.shape(m0))
        repetitions = int((len(keys) - 1) / 2)

        for file_idx in range(1, repetitions * 2, 2):
            label = pydicom.dcmread(series[keys[file_idx]]).pixel_array.astype(float)
            control = pydicom.dcmread(series[keys[file_idx + 1]]).pixel_array.astype(float)
            pwi += (control - label) / repetitions

        # calculating using simple model
        extra_factor = 2  # TODO 需要用更多数据摸索，这是友谊医院数据
        u_cnv = 6000  # units conversion from mL/g/s to mL/100g/min
        bb_p = 0.9  # mL/g, blood-brain partition coefficient
        t_inv = self.delay_time  # sec, inversion time
        t1_b = 1.65  # sec, relaxation of blood at 3.0T
        lab_eff = 0.98  # labeling efficiency for PASL
        l_dur = self.label_dur  # sec, labeling duration

        m0[m0 < 1] = 1
        pwi[pwi < 0] = 0

        upper_param = u_cnv * bb_p * np.exp(t_inv / t1_b)
        lower_param = 2 * lab_eff * l_dur
        cbf_pasl_calc = pwi / m0 * upper_param / lower_param * extra_factor

        mask = self._gen_mask(m0)
        cbf_pasl_calc = np.multiply(cbf_pasl_calc, mask)
        cbf_pasl_calc = gaussian_filter(cbf_pasl_calc, 0.7)
        cbf_pasl_calc = cbf_pasl_calc.astype(np.int16)
        SorterUtil.demosaic_sitk(image_data, cbf_pasl_calc, 'cbf1', self.intermediate_folder, self.formatpack)

    def generate_cbf_3d_pasl(self, series_m0, series_perf, extra_factor):
        if extra_factor is None or extra_factor == 0:
            raise Exception('extra_factor 未设置')

        os.makedirs(os.path.join(self.intermediate_folder, 'asl', 'cbf1'), exist_ok=True)
        os.makedirs(os.path.join(self.intermediate_folder, 'asl', 'm0'), exist_ok=True)
        series_m0.pop(0)
        series_perf.pop(0)
        keys = list(series_m0.keys())
        keys.sort()
        image_data = pydicom.dcmread(series_m0[keys[0]])
        if "MOSAIC" in image_data[0x0008, 0x0008].value:
            self._get_format_pack(image_data)
            # TODO: extra_factor自己猜的，需要更多的验证，这是苏州第一医院的
            extra_factor = 32 / extra_factor
            m0 = image_data.pixel_array * extra_factor
            SorterUtil.demosaic(image_data, m0, 'asl-m0', 'm0', self.intermediate_folder, self.formatpack)
        else:
            for slice_idx in range(len(keys)):
                image_data = pydicom.dcmread(series_m0[keys[slice_idx]])
                DCMUtil.copy_dcm_slice(image_data, self.intermediate_folder, 'asl', 'm0', slice_idx)
                image_arr = image_data.pixel_array
                if slice_idx == 0:
                    [a, b] = np.shape(image_arr)
                    m0 = np.zeros((a, b, len(keys)))
                # TODO: extra_factor自己猜的，需要更多验证，这是一脉阳光的
                extra_factor = 32 / extra_factor
                m0[:, :, slice_idx] = image_arr * extra_factor

            DCMUtil.dcm_to_nii(self.intermediate_folder, 'asl', 'm0')
            m0 = SorterUtil.to_mosaic(m0)

        keys = list(series_perf.keys())
        keys.sort()
        image_data = pydicom.dcmread(series_perf[keys[0]])
        self._get_format_pack(image_data)

        pwi = np.zeros(np.shape(m0))
        repetitions = int(len(keys) / 2)
        for file_idx in range(0, repetitions * 2, 2):
            control = pydicom.dcmread(series_perf[keys[file_idx]]).pixel_array.astype(float)
            label = pydicom.dcmread(series_perf[keys[file_idx + 1]]).pixel_array.astype(float)
            pwi += (control - label) / repetitions

        # calculating using simple model
        u_cnv = 6000  # units conversion from mL/g/s to mL/100g/min
        bb_p = 0.9  # mL/g, blood-brain partition coefficient
        t_inv = self.delay_time  # sec, inversion time
        t1_b = 1.65  # sec, relaxation of blood at 3.0T
        lab_eff = 0.98  # labeling efficiency for PASL
        l_dur = self.label_dur  # sec, labeling duration

        m0[m0 < 1] = 1
        mask = self._gen_mask(m0)

        check = np.multiply(mask, pwi)

        if sum(check.flatten()) < 0:
            pwi = -pwi
        pwi[pwi < 0] = 0

        upper_param = u_cnv * bb_p * np.exp(t_inv / t1_b)
        lower_param = 2 * lab_eff * l_dur
        cbf_pasl_calc = pwi / m0 * upper_param / lower_param
        cbf_pasl_calc = np.multiply(cbf_pasl_calc, mask)
        cbf_pasl_calc = gaussian_filter(cbf_pasl_calc, 0.7)
        cbf_pasl_calc = cbf_pasl_calc.astype(np.int16)
        SorterUtil.demosaic_sitk(image_data, cbf_pasl_calc, 'cbf1', self.intermediate_folder, self.formatpack)

    def parse_pasl_from_archive_folder(self, series):
        os.makedirs(os.path.join(self.intermediate_folder, 'asl', 'mcbf'), exist_ok=True)
        os.makedirs(os.path.join(self.intermediate_folder, 'asl', 'att'), exist_ok=True)
        os.makedirs(os.path.join(self.intermediate_folder, 'asl', 'acbv'), exist_ok=True)
        os.makedirs(os.path.join(self.intermediate_folder, 'asl', 'm0'), exist_ok=True)
        series.pop(0)
        for file_idx in series.keys():
            image_data = pydicom.dcmread(series[file_idx])
            self._get_format_pack(image_data)
            if image_data[0x0020, 0x4000].value == 'M0 Image':
                SorterUtil.demosaic(image_data, image_data.pixel_array, 'asl-m0', 'm0',
                                    self.intermediate_folder,
                                    self.formatpack)
            elif image_data[0x0020, 0x4000].value == 'relCBF':
                cbf_arr = image_data.pixel_array
                SorterUtil.demosaic(image_data, image_data.pixel_array, 'asl-mcbf', 'mcbf',
                                    self.intermediate_folder,
                                    self.formatpack)
            elif image_data[0x0020, 0x4000].value == 'Bolus Arrival Time (BAT) Image':
                att_arr = image_data.pixel_array
                if [0x0028, 0x1053] in image_data:
                    image_data[0x0028, 0x1053].value = 0.001
                else:
                    image_data.add_new([0x0028, 0x1053], 'DS', 0.001)
                SorterUtil.demosaic(image_data, image_data.pixel_array, 'asl-att', 'att',
                                    self.intermediate_folder,
                                    self.formatpack)

        image_data = pydicom.dcmread(series[file_idx])
        image_data.add_new([0x0028, 0x1053], 'DS', 0.001)
        SorterUtil.demosaic(image_data, cbf_arr * att_arr / 60, 'asl-acbv', 'acbv',
                            self.intermediate_folder,
                            self.formatpack)

    def siemens_data_check(self, seriesm0):
        self.reader_ref = sitk.ImageFileReader()
        self.reader_ref.LoadPrivateTagsOn()
        try:
            self.reader_ref.SetFileName(seriesm0[1])
            self.ref_image_data = self.reader_ref.Execute()
        except:
            self.reader_ref.SetFileName([i for i in seriesm0.values()][1])
            self.ref_image_data = self.reader_ref.Execute()

        try:
            self.slice_num = int(float(self.reader_ref.GetMetaData("0019|100a")))
        except:
            raise Exception('slice number not found')

        if float(self.reader_ref.GetMetaData("0020|1041")) >= 0:
            self.slice_order = "descending"
        elif float(self.reader_ref.GetMetaData("0020|1041")) < 0:
            self.slice_order = "ascending"

    def _gen_mask(self, input_image):
        threshold = 0.5 * np.sum(np.multiply(input_image, input_image)) / np.sum(input_image)
        output_image = np.zeros(np.shape(input_image))
        output_image[input_image >= threshold] = 1
        return output_image

    def _get_format_pack(self, image_data):
        self.row = image_data[0x0028, 0x0010].value
        self.col = image_data[0x0028, 0x0011].value
        slice_num = image_data[0x0019, 0x100A].value
        sn = math.ceil(np.sqrt(slice_num))
        dmrow = image_data[0x0028, 0x0010].value // sn
        siemensst = image_data[0x0018, 0x0050].value
        siemenssl = image_data[0x0020, 0x1041].value
        siemensipp = image_data[0x0020, 0x0032].value
        siemensiop = [1, 0, 0, 0, 1, 0]
        self.formatpack = [slice_num, sn, dmrow, siemensst, siemenssl, siemensipp, siemensiop]

    def Sorter(self, intermediate_folder, series_asl, delay_time, delay_rep, label_dur, extra_factor, debugMode=False):
        self.intermediate_folder = intermediate_folder
        self.debugMode = debugMode
        if type(delay_time) == list:
            self.delay_time = delay_time[0]
        elif type(delay_time) == float:
            self.delay_time = delay_time
        if type(label_dur) == list:
            self.label_dur = label_dur[0]
        elif type(label_dur) == float:
            self.label_dur = label_dur

        os.makedirs(os.path.join(self.intermediate_folder, 'asl'), exist_ok=True)
        if "PARAMETER_FIT" in series_asl.keys():
            self.parse_pasl_from_archive_folder(series_asl["PARAMETER_FIT"][0])
        elif "2DPASL_RAW" in series_asl.keys():
            self.generate_cbf_2d_pasl(series_asl["2DPASL_RAW"][0])
        elif "3DPASL_PERF" in series_asl.keys():
            if "3DPASL_M0" in series_asl.keys():
                self.generate_cbf_3d_pasl(series_asl["3DPASL_M0"][0], series_asl["3DPASL_PERF"][0], extra_factor)
            else:
                self.generate_cbf_3d_pasl(series_asl["3DPASL_PERF"][0].copy(), series_asl["3DPASL_PERF"][0], extra_factor)

        # self.seriesdelay = seriesdelay
        # self.delay_rep = delay_rep
        # self.delay_num = len(init_delay)
        # self.init_delay = float(init_delay[0])  # 导进来的init_delay其实是每一个delay的时间点
        # if self.delay_num == 1:
        #     self.interval = float(0)
        # else:
        #     self.interval = float(init_delay[1] - init_delay[0])
        # self.debugMode = debugMode
        # if not os.path.exists(os.path.join(self.intermediate_folder, 'asl')):
        #     os.mkdir(os.path.join(self.intermediate_folder, 'asl'))
        #
        # if self.seriesdelay == 2:
        #     self.parse_pasl_from_archive_folder(seriesm0)
        # elif self.seriesdelay == 1:
        #     self.parse_2Dpasl_from_archive_folder(seriesm0)
        # elif (self.seriesdelay == 5) or (self.seriesdelay == 1):
        #     self.siemens_data_check(seriesm0)
        #     self.generate_from_raw_folder(seriesm0)
