"""
修改，允许输入飞利浦1、2、3延迟数据
修改了多余重复的代码


21年07月19日
姚泽山
"""

import pydicom
import os
from . import AnImageDataSorterUtility as SorterUtil
from . import AnImageDCMUtility as DCMUtil
import numpy as np


# 飞利浦
class AnImageDataSorterPhilips13:
    def __init__(self):
        self.intermediate_folder = ''

    def parse_m0_from_raw_folder(self, series):
        os.makedirs(os.path.join(self.intermediate_folder, 'asl', 'm0'), exist_ok=True)
        # image_data = pydicom.dcmread(self.seriesm0[2][1])
        # temporal_num = image_data[0x0020, 0x0105].value
        # dmrow = image_data[0x0028, 0x0010].value
        # v = np.zeros(((len(self.seriesm0) // 2), self.dmrow, self.dmrow))

        # 查看飞利浦M0的数据格式

        if "M0" in series.keys():
            m0keys = sorted(list(series["M0"][0].keys()))
            img = pydicom.dcmread(series["M0"][0][m0keys[1]], stop_before_pixels=True)
            first_slice_loc = img[0x0020, 0x1041].value
            img = pydicom.dcmread(series["M0"][0][m0keys[2]], stop_before_pixels=True)
            second_slice_locA = img[0x0020, 0x1041].value
            img = pydicom.dcmread(series["M0"][0][m0keys[len(series["M0"][0]) // 2 + 1]], stop_before_pixels=True)
            second_slice_locB = img[0x0020, 0x1041].value

            for slice_idx in range(len(series["M0"][0]) // 2):
                if first_slice_loc == second_slice_locA:
                    image_data = pydicom.dcmread(series["M0"][0][m0keys[slice_idx * 2 + 1]])
                elif first_slice_loc == second_slice_locB:
                    image_data = pydicom.dcmread(series["M0"][0][m0keys[slice_idx + 1]])
                image_data = SorterUtil.modify_series_uid(image_data, 'asl-m0', None)
                image_data = SorterUtil.add_AnImage_tag(image_data, 'asl-m0')
                image_data[0x0020, 0x0013].value = slice_idx + 1
                image_data.save_as(
                    os.path.join(self.intermediate_folder, 'asl', 'm0', '{:04d}.dcm'.format(slice_idx + 1)))
        else:
            m0keys = sorted(list(series["CBF"][0].keys()))
            for slice_idx in range(len(series["CBF"][0]) - 1):
                image_data = pydicom.dcmread(series["CBF"][0][m0keys[slice_idx + 1]])
                image_data = SorterUtil.modify_series_uid(image_data, 'asl-m0', None)
                image_data = SorterUtil.add_AnImage_tag(image_data, 'asl-m0')
                image_data[0x0020, 0x0013].value = slice_idx + 1
                image_data.save_as(
                    os.path.join(self.intermediate_folder, 'asl', 'm0', '{:04d}.dcm'.format(slice_idx + 1)))

        DCMUtil.dcm_to_nii(self.intermediate_folder, 'asl', 'm0')

    def parse_cbf_from_archive_folder(self, series):
        seriescbf = series["CBF"]
        for series_idx in range(len(seriescbf)):
            os.makedirs(os.path.join(self.intermediate_folder, 'asl', 'cbf{:d}'.format(series_idx + 1)), exist_ok=True)

            if len(seriescbf) > 0 and series_idx != 0:
                os.makedirs(os.path.join(self.intermediate_folder, 'asl',
                                         'cbf{:d}-{:d}'.format(series_idx + 1, series_idx)), exist_ok=True)

            test = pydicom.dcmread(seriescbf[series_idx][2])
            series = np.zeros((len(seriescbf[series_idx]), test[0x0028, 0x0010].value, test[0x0028, 0x0011].value))
            for slice_idx in range(len(seriescbf[series_idx]) - 1):
                image_data = pydicom.dcmread(seriescbf[series_idx][slice_idx + 1])
                array_data = image_data.pixel_array
                image_data = SorterUtil.modify_series_uid(image_data, 'asl-cbf{:d}'.format(series_idx + 1), None)
                image_data = SorterUtil.add_AnImage_tag(image_data, 'asl-cbf{:d}'.format(series_idx + 1))
                image_data.save_as(os.path.join(self.intermediate_folder, 'asl',
                                                'cbf{:d}'.format(series_idx + 1), '{:04d}.dcm'.format(slice_idx + 1)))
                series[image_data[0x0020, 0x0013].value - 1, :, :] = array_data

                if len(seriescbf) > 0 and series_idx != 0:
                    diffdata = array_data - series2[image_data[0x0020, 0x0013].value - 1, :, :]
                    image_data.PixelData = diffdata.astype(np.uint16)
                    image_data.remove_private_tags()
                    image_data = SorterUtil.modify_series_uid(image_data,
                                                              'asl-cbf{:d}-{:d}'.format(series_idx + 1, series_idx),
                                                              None)
                    image_data = SorterUtil.add_AnImage_tag(image_data,
                                                            'asl-cbf{:d}-{:d}'.format(series_idx + 1, series_idx))
                    image_data.save_as(os.path.join(self.intermediate_folder, 'asl',
                                                    'cbf{:d}-{:d}'.format(series_idx + 1, series_idx),
                                                    '{:04d}.dcm'.format(image_data[0x0020, 0x0013].value)))
            series2 = series
            DCMUtil.dcm_to_nii(self.intermediate_folder, 'asl', 'cbf{:d}'.format(series_idx + 1))
            if len(seriescbf) > 0 and series_idx != 0:
                DCMUtil.dcm_to_nii(self.intermediate_folder, 'asl', 'cbf{:d}-{:d}'.format(series_idx + 1, series_idx))

    def Sorter(self, intermediate_folder, series):
        self.intermediate_folder = intermediate_folder
        if not os.path.exists(os.path.join(self.intermediate_folder, 'asl')):
            os.mkdir(os.path.join(self.intermediate_folder, 'asl'))
        self.parse_m0_from_raw_folder(series)
        self.parse_cbf_from_archive_folder(series)
