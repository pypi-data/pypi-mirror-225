import os

import numpy
import numpy as np
import pydicom

from log import logger

from ._dicom import SeriesModel, DicomRequiredTags
from ._dicom_util import write_dicom_series
from .data_sorter_base import DataSorterBase
from .errors import *
from ._type import *
from typing import Union


class DataSorterStruct(DataSorterBase):
    def __init__(self, data_type, output_root, series_list):
        DataSorterBase.__init__(self, data_type, output_root, series_list)

    @staticmethod
    def validate_series(series_list: List[SeriesModel]):
        # 多个struct，优先选择轴状位的
        struct: SeriesModel
        # 只有一个轴位的，没得选
        if len(series_list) == 1:
            struct = series_list[0]
        else:
            # 多个选择其一使用
            struct_tra_list = []
            for s in series_list:
                if s.SliceDirection == SliceDirection.Axial:
                    struct_tra_list.append(s)
            if len(struct_tra_list) == 1:
                struct = struct_tra_list[0]
            elif len(struct_tra_list) > 1:
                # 优先选择分辨率高的、SeriesNumber号小的（号大的有可能是计算而来的）
                struct = sorted(struct_tra_list, key=lambda x: (x.SpacingBetweenSlices, x.SeriesNumber))[0]
            else:
                # 没有轴状位的序列
                struct = series_list[0]
        return struct

'''
这里是除了ASL以外的MR图像
T1、T2、T2 FLAIR、DWI
'''
class DataSorterT1(DataSorterStruct):
    def __init__(self, data_type, output_root, series_list):
        DataSorterBase.__init__(self, data_type, output_root, series_list)

    def Sorter(self):
        super(DataSorterT1, self).Sorter()

        self.T1 = self.validate_series(self.series_list)
        logger.debug(f"清洗的T1：{self.T1.SeriesDescription}，剖面：{self.T1.SliceDirection}，"
                         f"分辨率：{self.T1.PixelSpacing[0]}*{self.T1.PixelSpacing[1]}*{self.T1.SpacingBetweenSlices}")

        cur_series_number = SeriesNumberStartWith.T1
        T1_img = self.T1.load()[...,0]
        write_dicom_series(T1_img, self.T1, 't1', cur_series_number, os.path.join(self.output_root, 'struct', f't1'))

class DataSorterT2(DataSorterStruct):
    def __init__(self, data_type, output_root, series_list:List[SeriesModel]):
        DataSorterBase.__init__(self, data_type, output_root, series_list)

    def Sorter(self):
        super(DataSorterT2, self).Sorter()

        self.T2 = self.validate_series(self.series_list)
        logger.debug(f"清洗的T2：{self.T2.SeriesDescription}，剖面：{self.T2.SliceDirection}，"
                         f"分辨率：{self.T2.PixelSpacing[0]}*{self.T2.PixelSpacing[1]}*{self.T2.SpacingBetweenSlices}")

        cur_series_number = SeriesNumberStartWith.T2
        T2_img = self.T2.load()[...,0]
        write_dicom_series(T2_img, self.T2, 't2', cur_series_number, os.path.join(self.output_root, 'struct', f't2'))


class DataSorterT2FLAIR(DataSorterStruct):
    def __init__(self, data_type, output_root, series_list):
        DataSorterBase.__init__(self, data_type, output_root, series_list)

    def Sorter(self):
        super(DataSorterT2FLAIR, self).Sorter()

        self.T2FLAIR = self.validate_series(self.series_list)
        logger.debug(f"清洗的T2FLAIR：{self.T2FLAIR.SeriesDescription}，剖面：{self.T2FLAIR.SliceDirection}，"
                         f"分辨率：{self.T2FLAIR.PixelSpacing[0]}*{self.T2FLAIR.PixelSpacing[1]}*{self.T2FLAIR.SpacingBetweenSlices}")

        cur_series_number = SeriesNumberStartWith.T2FLAIR
        T2FLAIR_img = self.T2FLAIR.load()[..., 0]
        write_dicom_series(T2FLAIR_img, self.T2FLAIR, 't2 flair', cur_series_number, os.path.join(self.output_root, 'struct', f't2 flair'))

class DataSorterDWI(DataSorterBase):
    def __init__(self, data_type, output_root, series_list: List[SeriesModel]):
        DataSorterBase.__init__(self, data_type, output_root, series_list)

        self.DWI_list:List[SeriesModel] = []
        self.ADC_list:List[SeriesModel] = []
        reg_DWI_list:List[SeriesModel] = []
        for series in self.series_list:
            series_description:str = series.SeriesDescription.lower()
            if series_description.find('adc') > -1 or series_description.find('apparent diffusion coefficient') > -1:
                if series_description.find('eadc') > -1 or series_description.find('exponential') > -1:
                    continue
                self.ADC_list.append(series)
            elif series_description.find('dwi') > -1 or series_description.find('tracew') > -1:
                if series_description.find('reg') > -1:
                    reg_DWI_list.append(series)
                else:
                    self.DWI_list.append(series)
        if len(self.DWI_list) == 0:
            self.DWI_list = reg_DWI_list
        self.series_list = self.DWI_list + self.ADC_list

    def validate_series(self):
        if len(self.DWI_list) < 1:
            raise MissingSequenceError('DWI')
        elif len(self.DWI_list) > 1:
            logger.warning(f'发现{len(self.DWI_list)}组DWI数据')

        # 判断DWI序列的多B值是否同属于一个序列
        self.is_find_multi_volume = False
        for dwi in self.DWI_list:
            if dwi.Repetition > 1:
                self.DWI = dwi
                self.is_find_multi_volume = True
                break

        # 多B值不在同一个序列，必须要求DWI_list大于1
        if (not self.is_find_multi_volume):
            if len(self.DWI_list) < 2:
                self.DWI = self.DWI_list[0]
                # 当DWI不足报个警告，不再抛异常；当需要计算ADC的时候，再判断是否抛异常
                logger.warning('DWI序列缺少两个不同B值的Series')
                # raise NeedTwoBValueDWIError()
            else:
                self.DWI = self.DWI_list[0]
                # 判断层数是否一致
                if len(set([i.SliceNumber for i in self.DWI_list])) != 1:
                    raise SpaceIsDifferentError('DWI')

        # ADC序列验证，允许不存在。
        if len(self.ADC_list) < 1:
            logger.info(f'未发现ADC序列')
            self.ADC = None

            # DWI不足无法计算ADC
            if (not self.is_find_multi_volume) and len(self.DWI_list) < 2:
                raise NeedTwoBValueDWIError()

        else:
            logger.debug(f'发现{len(self.ADC_list)}组ADC数据')
            self.ADC = self.ADC_list[0]

        if self.ADC is not None and self.DWI.SliceNumber != self.ADC.SliceNumber:
            raise SpaceIsDifferentError('DWI', 'ADC')


    @staticmethod
    def get_tag(dcm_obj: Union[DicomRequiredTags, pydicom.Dataset], key, default=None):
        if isinstance(dcm_obj, DicomRequiredTags):
            return dcm_obj.get_tag(key, default=default)
        else:
            return DicomRequiredTags.get_key(key, dcm_obj, default)

    def find_multi_instance(self):
        multi_instances = []

        # 多B值不在同一个序列, 找到第二个Volume的位置
        if self.is_find_multi_volume:
            multi_slice_number = [i for i in range(self.DWI.Repetition)] if self.DWI.is_second_arrangement_mode \
                else [i * self.DWI.SliceNumber for i in range(self.DWI.Repetition)]

            # 3D dicom的B值在PerFrameFunctionalGroupsSequence中
            for i in multi_slice_number:
                if self.DWI.dicom_image_type == DICOM_IMAGE_TYPE.DICOM_IMAGE_TYPE_3D:
                    multi_instances.append(self.get_tag(self.DWI.PerFrameFunctionalGroupsSequence[i], (0x0018, 0x9117))[0])
                else:
                    multi_instances.append(self.DWI[i])
            DWI_image = self.DWI.load()
            return multi_instances, DWI_image
        else:
            for dwi in self.DWI_list:
                if self.DWI.dicom_image_type == DICOM_IMAGE_TYPE.DICOM_IMAGE_TYPE_3D:
                    multi_instances.append(self.get_tag(dwi.PerFrameFunctionalGroupsSequence[0], (0x0018, 0x9117))[0])
                else:
                    multi_instances.append(dwi[0])
            return multi_instances, np.concatenate([i.load() for i in self.DWI_list], axis=-1)



    def Sorter(self):
        super(DataSorterDWI, self).Sorter()
        self.validate_series()
        multi_instances, DWI_volume = self.find_multi_instance()

        b_value_list = []
        # 读取每组的B值
        for instance in multi_instances:
            # 标准dicom中的B值(弥散系数)标签信息
            b_value = self.get_tag(instance, (0x0018, 0x9087), 0)
            if self.DWI.Manufacturer == MANUFACTURER.kMANUFACTURER_GE:
                b_value = b_value if b_value != 0 else \
                    self.get_tag(instance, (0x0043, 0x1039), [0])[0]

            elif self.DWI.Manufacturer == MANUFACTURER.kMANUFACTURER_SIEMENS:
                b_value = b_value if b_value != 0 else \
                    self.get_tag(instance, (0x0019, 0x100C), 0)

            elif self.DWI.Manufacturer in [MANUFACTURER.kMANUFACTURER_PHILIPS, MANUFACTURER.kMANUFACTURER_UIH]:
                pass
            else:
                raise UnSupportDataTypeError(self.DWI.Manufacturer)
            b_value_list.append(b_value)
        b_value_list = [int(i) for i in b_value_list]
        logger.info(f'DWI发现的B值：{b_value_list}')


        cur_series_number = SeriesNumberStartWith.DWI
        for b_value, slice in zip(b_value_list, range(DWI_volume.shape[-1])):
            write_dicom_series(DWI_volume[..., slice], self.DWI, f'dwi-b{b_value}', cur_series_number,
                               os.path.join(self.output_root, 'dwi', f'b{b_value}'))
            cur_series_number += 1

        rescale_type = '10^-6 mm^2/s'
        if self.ADC is not None:
            # ADC， 确定单位
            rescale_type_1 = self.ADC.get_tag((0x0028, 0x1054), '')
            rescale_type_2 = self.ADC.get_tag((0x2005, 0x140B), '')
            if rescale_type_1 != '':
                rescale_type = rescale_type_1
            elif rescale_type_2 != '':
                rescale_type = rescale_type_2

            rescale = 1000 if rescale_type == '10^-3 mm^2/s' else 1
            ADC_img = self.ADC.load(rescale)[...,0]
            write_dicom_series(ADC_img, self.DWI, 'dwi-adc', cur_series_number,
                               os.path.join(self.output_root, 'dwi', 'adc'))

        else: # 需要计算ADC
            # 验证B值是否符合要求
            first_b_value, first_volume = b_value_list[0], DWI_volume[...,0]
            second_b_value, second_volume = b_value_list[1], DWI_volume[...,1]
            logger.info(f'DWI使用的两个B值：{first_b_value}, {second_b_value}')
            if first_b_value == 0 and second_b_value == 0:
                raise DiffusionBValueMissingError()

            logger.debug(f'开始计算ADC')
            # 使second_b_value等于较大B值的那个图像
            if first_b_value > second_b_value:
                first_b_value, second_b_value = second_b_value, first_b_value
                first_volume, second_volume = second_volume, first_volume
            ADC_img = np.log(first_volume / second_volume) / (second_b_value - first_b_value)
            ADC_img[np.isinf(ADC_img) | np.isnan(ADC_img)] = 0
            ADC_img *= 10**6
            ADC_img[ADC_img < 0] = -256

            write_dicom_series(ADC_img, self.DWI, 'dwi-adc', cur_series_number,
                               os.path.join(self.output_root, 'dwi', 'adc'))