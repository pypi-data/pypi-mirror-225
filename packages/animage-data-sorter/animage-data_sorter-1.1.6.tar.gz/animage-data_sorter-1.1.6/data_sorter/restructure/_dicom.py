import os

# import gdcm
import numpy as np
import pydicom
from log import logger
from nibabel.nicom import csareader
from pydicom.errors import InvalidDicomError
from typing import Dict, List

from .errors import *
from ._type import *


def demosaic(mosaic_mat: np.ndarray, slice_num: int):
    n_rows = n_cols = int(np.ceil(np.sqrt(slice_num)))
    img_width, img_height = mosaic_mat.shape[1], mosaic_mat.shape[0]
    img_width //= n_cols
    img_height //= n_rows

    _3d_mat = np.zeros((img_height, img_width, slice_num))
    for i in range(slice_num):
        x_start = i % n_cols * img_width
        y_start = i // n_cols * img_height
        _3d_mat[::, :, i] = mosaic_mat[y_start:y_start + img_height, x_start:x_start + img_width]

    return _3d_mat


def csa_ascii_read_key(csa_ascii_list: list, key: str, default=None):
    value = ''
    exist_flag = False
    for ascii in csa_ascii_list:
        if ascii.startswith(key):
            exist_flag = True
            value = ascii.split('=')[-1].strip().strip('')
    if exist_flag:
        return value
    elif default is None:
        raise CsaHeaderMissingKeyError(key)
    else:
        return default


def get_csa_ascii_list(dataset: pydicom.Dataset) -> list:
    try:
        csa_header_series = csareader.read(DicomRequiredTags.get_key((0x0029, 0x1020), dataset))
        MrPhoenixProtocol = csa_header_series['tags']['MrPhoenixProtocol']['items'][0]
        csa_ascii_begin = '### ASCCONV BEGIN'
        csa_ascii_end = '### ASCCONV END'
        csa_ascii = MrPhoenixProtocol[
                    MrPhoenixProtocol.find(csa_ascii_begin):MrPhoenixProtocol.find(csa_ascii_end)].split('\n')
        return csa_ascii
    except:
        return []


# dicom必要的标签信息
class DicomRequiredTags:
    def __init__(self, dataset: pydicom.Dataset):
        # Patient信息；允许没有
        self.PatientName = self.get_key((0x0010, 0x0010), dataset, '')
        self.PatientID = self.get_key((0x0010, 0x0020), dataset, '')
        self.PatientBirthDate = self.get_key((0x0010, 0x0030), dataset, '')
        self.PatientSex = self.get_key((0x0010, 0x0040), dataset, '')
        self.PatientAge = self.get_key((0x0010, 0x1010), dataset, '')
        self.PatientSize = self.get_key((0x0010, 0x1020), dataset, '')
        self.PatientWeight = self.get_key((0x0010, 0x103D), dataset, '')
        self.PatientPosition = self.get_key((0x0018, 0x5100), dataset, '')

        # Study信息，处理UID其余运行没有
        self.StudyInstanceUID = self.get_key((0x0020, 0x000D), dataset)
        self.StudyDescription = self.get_key((0x0008, 0x1030), dataset, '')
        self.StudyDate = self.get_key((0x0008, 0x0020), dataset, '')
        self.StudyTime = self.get_key((0x0008, 0x0030), dataset, '')
        self.StudyID = self.get_key((0x0020, 0x0010), dataset, '')

        # Series信息
        self.SeriesInstanceUID = self.get_key((0x0020, 0x000E), dataset)
        self.SeriesDescription = self.get_key((0x0008, 0x103E), dataset)
        self.SeriesDate = self.get_key((0x0008, 0x0021), dataset, '')
        self.SeriesTime = self.get_key((0x0008, 0x0031), dataset, '')
        self.SeriesNumber = self.get_key((0x0020, 0x0011), dataset, '')

        # 设备信息
        self.Manufacturer = MANUFACTURER.str2MANUFACTURER(self.get_key((0x0008, 0x0070), dataset))
        self.ManufacturerModelName = self.get_key((0x0008, 0x1090), dataset, UnKnown)
        self.Modality = MODALITY.str2MODALITY(self.get_key((0x0008, 0x0060), dataset))
        self.InstitutionName = self.get_key((0x0008, 0x0080), dataset, '')
        self.ProtocolName = self.get_key((0x0018, 0x1030), dataset, '')

        # 序列名
        self.PulseSequenceName = self.get_key((0x0018, 0x9005), dataset, '')
        self.SamplesPerPixel = self.get_key((0x0028, 0x0002), dataset, 1)
        if self.SamplesPerPixel != 1:
            # 不是原始的灰度图像忽略即可
            raise PhotometricRGBError()

        # 图像信息
        self.SOPInstanceUID = self.get_key((0x0008, 0x0018), dataset)
        self.InstanceNumber = self.get_key((0x0020, 0x0013), dataset)
        self.ImageMat = dataset.pixel_array

        # RealWorldValueMappingSequence = self.get_key((0x0040, 0x9096), dataset, [])
        # # 0028,1053和0028,1052定义的重新缩放斜率和截距，除了飞利浦以外，这是定义 缩放斜率和截距唯一的地方。
        # if len(RealWorldValueMappingSequence) > 0 and self.Manufacturer == MANUFACTURER.kMANUFACTURER_PHILIPS:
        #     self.RescaleSlope = self.get_key((0x0040, 0x9225), RealWorldValueMappingSequence[0], 1)
        #     self.RescaleIntercept = self.get_key((0x0040, 0x9224), RealWorldValueMappingSequence[0], 0)
        # else:
        if True:
            self.RescaleSlope = self.get_key((0x0028, 0x1053), dataset, 1)
            self.RescaleIntercept = self.get_key((0x0028, 0x1052), dataset, 0)

        if len(self.ImageMat.shape) == 3:
            self.dicom_image_type = DICOM_IMAGE_TYPE.DICOM_IMAGE_TYPE_3D
            # 每个切片放在第三维
            self.ImageMat = self.ImageMat.swapaxes(0, 2)
            self.ImageMat = self.ImageMat.swapaxes(0, 1)

            # 3D格式的图像信息在 5200|9229 共享信息 或者 5200|9230 每帧信息中
            # 5200|9229 不存在的话到 5200|9230中找
            try:
                SharedFunctionalGroupsSequence = self.get_key((0x5200, 0x9229), dataset)
                PixelMeasures = self.get_key((0x0028, 0x9110), SharedFunctionalGroupsSequence[0])
                PixelValueTransformation = self.get_key((0x0028, 0x9145), SharedFunctionalGroupsSequence[0])
            except:
                SharedFunctionalGroupsSequence = self.get_key((0x5200, 0x9230), dataset)
                PixelMeasures = self.get_key((0x0028, 0x9110), SharedFunctionalGroupsSequence[0])
                PixelValueTransformation = self.get_key((0x0028, 0x9145), SharedFunctionalGroupsSequence[0])

            self.RescaleSlope = self.get_key((0x0028, 0x1053), PixelValueTransformation[0])
            self.RescaleIntercept = self.get_key((0x0028, 0x1052), PixelValueTransformation[0])
            self.SliceThickness = self.get_key((0x0018, 0x0050), PixelMeasures[0])
            self.SpacingBetweenSlices = self.get_key((0x0018, 0x0088), PixelMeasures[0], self.SliceThickness)
            self.PixelSpacing = self.get_key((0x0028, 0x0030), PixelMeasures[0])

            self.ImagePositionPatientList = []
            Orientation_list = set()
            self.PerFrameFunctionalGroupsSequence = self.get_key((0x5200, 0x9230), dataset)
            for frame in self.PerFrameFunctionalGroupsSequence:
                PlanePositionSequence = self.get_key((0x0020, 0x9113), frame)
                ImagePosition = self.get_key((0x0020, 0x0032), PlanePositionSequence[0])
                PlaneOrientationSequence = self.get_key((0x0020, 0x9116), frame)
                ImageOrientation = self.get_key((0x0020, 0x0037), PlaneOrientationSequence[0])
                self.ImagePositionPatientList.append(ImagePosition)
                Orientation_list.add(tuple(ImageOrientation))

            # todo：有点问题，只有方向无偏角的时候才正确。
            self.SliceLocation = self.ImagePositionPatientList[0][2]

            if len(Orientation_list) != 1:
                raise Exception('3D图像方向不一致')
            self.ImageOrientationPatient = list(list(Orientation_list)[0])


        elif len(self.ImageMat.shape) == 2:
            # 有可能是Mosaic图像，也有可能是普通2D图像
            self.dicom_image_type = DICOM_IMAGE_TYPE.DICOM_IMAGE_TYPE_2D
            self.PixelSpacing = self.get_key((0x0028, 0x0030), dataset)
            self.ImagePositionPatient = self.get_key((0x0020, 0x0032), dataset)
            self.ImageOrientationPatient = self.get_key((0x20, 0x0037), dataset)
            self.SliceLocation = self.get_key((0x0020, 0x1041), dataset)

            # 层厚/像素间距拥有其中一个标签即可
            self.SliceThickness = self.get_key((0x0018, 0x0050), dataset)
            # 层间距不存在则认为层间距=层厚
            self.SpacingBetweenSlices = self.get_key((0x0018, 0x0088), dataset, self.SliceThickness)
        else:
            raise UnSupportDataTypeError

        self.BitsAllocated = self.get_key((0x0028, 0x0100), dataset)
        self.BitsStored = self.get_key((0x0028, 0x0101), dataset)
        self.HighBit = self.get_key((0x0028, 0x0102), dataset)
        self.Rows = self.get_key((0x0028, 0x0010), dataset)
        self.Columns = self.get_key((0x0028, 0x0011), dataset)
        self.PixelRepresentation = self.get_key((0x0028, 0x0103), dataset)
        self.PhotometricInterpretation = self.get_key((0x0028, 0x0004), dataset, 'MONOCHROME2')  # 默认最大值白色
        # 什么剖面图
        self.SliceDirection = affine2Orientation(self.ImageOrientationPatient)
        self._raw_dataset = dataset

    @staticmethod
    def get_key(key, dataset: pydicom.Dataset, default=None):
        '''
        key不存在并且default未设置，则抛异常
        :param key:
        :param dataset:
        :param default:
        :return:
        '''
        if key not in dataset:
            if default is None:
                raise DicomMissingTagError(key)
            return default
        else:
            return dataset[key].value

    def get_tag(self, key, default=None):
        return self.get_key(key, self._raw_dataset, default)


class InstanceModel(DicomRequiredTags):
    def __init__(self, dataset: pydicom.Dataset, dcm_path: str):
        super().__init__(dataset)
        self.dcm_path = dcm_path

    def save_as(self, file_name):
        self._raw_dataset.save_as(file_name)


class SeriesModel(List[InstanceModel]):
    def __init__(self, instance: InstanceModel, raw_dataset: pydicom.Dataset):
        list.__init__(self)
        self._unique_uid = set()  # 记录instanceUID；避免重复文件
        self.PatientName = instance.PatientName
        self.PatientID = instance.PatientID
        self.PatientBirthDate = instance.PatientBirthDate
        self.PatientSex = instance.PatientSex
        self.PatientAge = instance.PatientAge
        self.PatientSize = instance.PatientSize
        self.PatientWeight = instance.PatientWeight
        self.PatientPosition = instance.PatientPosition
        self.StudyInstanceUID = instance.StudyInstanceUID
        self.StudyDescription = instance.StudyDescription
        self.StudyDate = instance.StudyDate
        self.StudyTime = instance.StudyTime
        self.StudyID = instance.StudyID
        self.SeriesInstanceUID = instance.SeriesInstanceUID
        self.SeriesDescription = instance.SeriesDescription
        self.SeriesDate = instance.SeriesDate
        self.SeriesTime = instance.SeriesTime
        self.SeriesNumber = instance.SeriesNumber
        self.Manufacturer = instance.Manufacturer
        self.ManufacturerModelName = instance.ManufacturerModelName
        self.Modality = instance.Modality
        self.InstitutionName = instance.InstitutionName
        self.ProtocolName = instance.ProtocolName
        self.SamplesPerPixel = instance.SamplesPerPixel
        self.RescaleSlope = instance.RescaleSlope
        self.RescaleIntercept = instance.RescaleIntercept
        self.BitsAllocated = instance.BitsAllocated
        self.BitsStored = instance.BitsStored
        self.HighBit = instance.HighBit
        self.Rows = instance.Rows
        self.Columns = instance.Columns
        self.SliceThickness = instance.SliceThickness
        self.SpacingBetweenSlices = instance.SpacingBetweenSlices
        self.PixelSpacing = instance.PixelSpacing
        self.PixelRepresentation = instance.PixelRepresentation
        self.PhotometricInterpretation = instance.PhotometricInterpretation

        self.SliceDirection = instance.SliceDirection
        self.PulseSequenceName = instance.PulseSequenceName
        self.SliceNumber = 0

        self.Repetition = 1  # 表示有多少组数据，（拥有控制像, 标记像）重复次数为1/2
        self.dicom_image_type = instance.dicom_image_type
        if self.dicom_image_type == DICOM_IMAGE_TYPE.DICOM_IMAGE_TYPE_3D:
            self.PerFrameFunctionalGroupsSequence = instance.PerFrameFunctionalGroupsSequence

        # 序列完整之后再获取坐标信息
        self.ImagePositionPatientList: List
        self.ImagePositionPatient: List
        self.ImageOrientationPatient: List
        self.SliceLocation: List
        self.z_reversed: bool = False  # 默认Z轴为增加

        if self.Modality != MODALITY.MODALITY_MR:
            raise UnSupportDataTypeError(self.Modality)

        if self.Manufacturer == MANUFACTURER.kMANUFACTURER_SIEMENS:
            # 判断是否为MOSAIC
            self.MosaicSliceNumber = instance.get_tag((0x0019, 0x100A), 0)
            if self.MosaicSliceNumber > 0 and self.dicom_image_type == DICOM_IMAGE_TYPE.DICOM_IMAGE_TYPE_2D:
                self.dicom_image_type = DICOM_IMAGE_TYPE.DICOM_IMAGE_TYPE_MOSAIC

                # MOSAIC图像需要进一步解析 CSA头部信息
                csa_header_image = csareader.read(instance.get_tag((0x0029, 0x1010), raw_dataset))
                # 用于辨别方向
                self.SliceNormalVector = csa_header_image['tags']['SliceNormalVector']['items']

            # 读取CSA Header 用于辨别PCASL 或者是 PASL
            csa_ascii_list = get_csa_ascii_list(raw_dataset)
            if self.PulseSequenceName == '':
                self.PulseSequenceName = csa_ascii_read_key(csa_ascii_list, 'tSequenceFileName', '')
            self.asl_type, self.data_type = self.inference_data_type(
                self.Manufacturer, self.PulseSequenceName, self.SeriesDescription)
        elif self.Manufacturer == MANUFACTURER.kMANUFACTURER_PHILIPS:
            self.asl_type, self.data_type = self.inference_data_type(self.Manufacturer,
                                                                     series_description=self.SeriesDescription)
        elif self.Manufacturer == MANUFACTURER.kMANUFACTURER_GE:
            self.asl_type, self.data_type = self.inference_data_type(self.Manufacturer,
                                                                     series_description=self.SeriesDescription)
        elif self.Manufacturer == MANUFACTURER.kMANUFACTURER_UIH:
            self.asl_type, self.data_type = self.inference_data_type(self.Manufacturer,
                                                                     series_description=self.SeriesDescription)
        else:
            # 暂未开发完成
            raise UnSupportDataTypeError('暂不支持除西门子外的数据处理')

    def get_tag(self, key, default=None):
        return self[0].get_tag(key, default)

    def append(self, instance: InstanceModel):
        if instance.SeriesInstanceUID != self.SeriesInstanceUID:
            logger.warning(
                f'The UID({instance.SeriesInstanceUID}) of the instance is different from that of the series({self.SeriesInstanceUID})')
            return
        # 已记录的文件排除
        if instance.SOPInstanceUID in self._unique_uid:
            logger.debug(f'{instance.SOPInstanceUID} dicom文件重复，被忽略')
            return
        self._unique_uid.add(instance.SOPInstanceUID)
        super().append(instance)

    def finish_handle(self):
        # 所有图像都获取之后、完整后的操作
        # 首先根据instanceNumber进行图片排序
        self.sort(key=lambda x: x.InstanceNumber)
        self.SliceLocation = self[0].SliceLocation
        self.ImageOrientationPatient = self[0].ImageOrientationPatient

        if self.dicom_image_type == DICOM_IMAGE_TYPE.DICOM_IMAGE_TYPE_MOSAIC:
            self.ImagePositionPatient = self[0].ImagePositionPatient

            self.SliceNumber = self.MosaicSliceNumber
            self.Repetition = len(self)  # 不除以2了

            # 判断Z轴正方向还是负方向
            slice_norm_mat = np.zeros((3, 3), dtype=float)
            slice_norm_mat[:, 0] = self.ImageOrientationPatient[:3]
            slice_norm_mat[:, 1] = self.ImageOrientationPatient[3:]
            slice_norm_mat[:, 2] = self.SliceNormalVector
            # 法向量相反，Z序需要翻转
            if np.linalg.det(slice_norm_mat) < 0:
                self.z_reversed = True  # Z轴递减


        elif self.dicom_image_type == DICOM_IMAGE_TYPE.DICOM_IMAGE_TYPE_2D:
            self.ImagePositionPatient = self[0].ImagePositionPatient
            # 一个序列可能包含多次重复扫描，根据SliceLocation分成多次扫描
            # dicom文件由两种排列方式
            # 第一种是每个完整的重复次数放在一起
            # 第二种是相同的层放在一起
            if len(self) < 2:
                return
            first_slice_location = self[0].SliceLocation
            second_slice_location = self[1].SliceLocation
            self.is_second_arrangement_mode = (first_slice_location == second_slice_location)
            # 是否为第二种排列方式, 第二种模式表示同一位置切片放在一起。
            # 第一种模式表示整个Volume切片放在一起

            if self.is_second_arrangement_mode:
                for i in range(1, len(self)):
                    if self[i].SliceLocation != first_slice_location:
                        self.Repetition = i
                        break
                # 未找到不同的层厚信息则层厚为1
                self.Repetition = 1 if self.Repetition == 0 else self.Repetition
                self.SliceNumber = len(self) / self.Repetition
            else:
                for i in range(1, len(self)):
                    if self[i].SliceLocation == first_slice_location:
                        self.SliceNumber = i
                        break
                # 未发现相同的，层数量等于图片数量
                self.SliceNumber = len(self) if self.SliceNumber == 0 else self.SliceNumber
                self.Repetition = len(self) / self.SliceNumber

            self.SliceNumber = int(self.SliceNumber)
            self.Repetition = int(self.Repetition)

            if self.is_second_arrangement_mode:
                second_slice_position = self[self.Repetition].ImagePositionPatient
            else:
                second_slice_position = self[1].ImagePositionPatient

            # 判断Z轴正方向还是负方向
            self.iSL, self.z_reversed = self.verify_slice_dir(second_slice_position)

        elif self.dicom_image_type == DICOM_IMAGE_TYPE.DICOM_IMAGE_TYPE_3D:
            self.ImagePositionPatientList = self[0].ImagePositionPatientList
            self.ImagePositionPatient = self[0].ImagePositionPatientList[0]

            # 查看图片相同定位的数量
            same_position = {}
            for i in self.ImagePositionPatientList:
                multiValue2tuple = tuple(i)
                if multiValue2tuple not in same_position:
                    same_position[multiValue2tuple] = 0
                same_position[multiValue2tuple] += 1

            self.SliceNumber = len(same_position)
            self.Repetition = list(same_position.values())[0]
            # 多个3D dicom文件
            self.Repetition *= len(self)

            first_slice_location = self.ImagePositionPatientList[0]
            second_slice_location = self.ImagePositionPatientList[1]
            self.is_second_arrangement_mode = (first_slice_location == second_slice_location)
            self.is_third_arrangement_mode = False
            # 有可能出现第三种情况：第三种模式表示 第二模式基础上将label与control像分开放。
            # 第二种模式表示同一位置（SliceLocation）切片放在一起。
            # 第一种模式表示整个Volume切片放在一起
            if self.is_second_arrangement_mode:
                if self.ImagePositionPatientList[self.Repetition // 2] != second_slice_location:
                    self.is_third_arrangement_mode = True
                    self.is_second_arrangement_mode = False

            self.ImagePositionPatientList = [[float(j) for j in i] for i in same_position]
            # 判断Z轴正方向还是负方向
            second_slice_location = list(same_position)[1]
            self.iSL, self.z_reversed = self.verify_slice_dir(second_slice_location)

        if self.z_reversed:
            logger.info(f'{self.SeriesDescription} reversed')

    def verify_slice_dir(self, second_slice_position):
        # return slice direction: 1 = sag, 2 = coronal, 3 = axial
        iSL = self.SliceDirection.iSL()

        second_slice_pos = second_slice_position[iSL - 1]
        m = self._calc_2d_affine()
        # 通过矩阵计算一下正方向的location与第二张图的location是否同向
        # 同向说明不需要反转，否则需要反转
        x = (0, 0, self.SliceNumber - 1, 1)

        posv = np.matmul(m, x)
        pos = posv[iSL - 1]
        return iSL, (second_slice_pos > m[iSL - 1][3]) != (pos > m[iSL - 1][3])

    def inference_data_type(self, manufacturer: MANUFACTURER, sequence_name: str = None,
                            series_description: str = None) -> (ASL_Type, MRI_Type):
        '''
        根据 sequence 或者 series_description 推断数据类型
        :param manufacturer:
        :param sequence_name:
        :param series_description:
        :return:
        '''
        if sequence_name is not None:
            sequence_name = sequence_name.lower()
        if series_description is not None:
            series_description = series_description.lower()
        ASL_type = ASL_Type.ASL_UnKnown
        data_type = MRI_Type.MRI_TYPE_UnKnown
        # 排除一些像截图这类的文件
        if series_description.find('[') > -1 and series_description.find(']') > -1:
            return ASL_type, data_type
        if manufacturer == MANUFACTURER.kMANUFACTURER_SIEMENS:
            if sequence_name is not None and sequence_name != '':
                if self.PulseSequenceName.find('tgse_pcasl') > -1:
                    ASL_type = ASL_Type.ASL_PCASL

                elif self.PulseSequenceName.find('tgse_pasl') > -1:
                    ASL_type, data_type = ASL_Type.ASL_PASL, MRI_Type.MRI_TYPE_3D_PASL_SIEMENS

            if series_description is not None and series_description != '':
                if data_type != MRI_Type.MRI_TYPE_UnKnown:
                    pass
                else:
                    if (series_description.startswith('tgse_pcasl_pld') and
                        not series_description.startswith('tgse_pcasl_pld5')) or \
                            series_description.startswith('tgse_pcasl_m0'):
                        ASL_type, data_type = ASL_Type.ASL_PCASL, MRI_Type.MRI_TYPE_1Delay_3D_PCASL_SIEMENS
                    elif series_description.startswith('tgse_pcasl') or series_description.startswith('pcasl_5delay'):
                        ASL_type, data_type = ASL_Type.ASL_PCASL, MRI_Type.MRI_TYPE_5Delay_3D_PCASL_SIEMENS
                    elif series_description.find('te00_ti') > -1:
                        ASL_type, data_type = ASL_Type.ASL_PCASL, MRI_Type.MRI_TYPE_4Delay_3D_PCASL_SIEMENS_Old
                    elif series_description.startswith('asl_3d') or series_description.find('m0') > -1 or \
                            series_description.startswith('pasl_3d'):
                        ASL_type, data_type = ASL_type.ASL_PASL, MRI_Type.MRI_TYPE_3D_PASL_SIEMENS
                    elif series_description.find('t1') > -1:
                        data_type = MRI_Type.MRI_TYPE_T1
                        # t1 放在t2 flair前面；避免t1 flair被认为是 t2 flair
                    elif series_description.find('flair') > -1 or series_description.find('fluid') > -1:
                        data_type = MRI_Type.MRI_TYPE_T2_FLAIR
                    elif series_description.find('t2') > -1:
                        data_type = MRI_Type.MRI_TYPE_T2
                    elif series_description.find('dwi') > -1 or series_description.find('adc') > -1 or \
                            series_description.find('apparent diffusion coefficient') > -1 or \
                            series_description.find('tracew') > -1:
                        data_type = MRI_Type.MRI_TYPE_DWI

        elif manufacturer == MANUFACTURER.kMANUFACTURER_PHILIPS:
            if sequence_name is not None and sequence_name != '':
                if sequence_name == 'grase':
                    ASL_type, data_type = ASL_Type.ASL_PCASL, MRI_Type.MRI_TYPE_3D_PCASL_PHILIPS
            if series_description is not None and series_description != '':
                if series_description.find('3d') > -1 and series_description.find('pcasl') > -1:
                    ASL_type, data_type = ASL_Type.ASL_PCASL, MRI_Type.MRI_TYPE_3D_PCASL_PHILIPS
                elif series_description.find('t1') > -1:
                    data_type = MRI_Type.MRI_TYPE_T1
                    # t1 放在t2 flair前面；避免t1 flair被认为是 t2 flair
                elif series_description.find('flair') > -1 or series_description.find('fluid') > -1:
                    data_type = MRI_Type.MRI_TYPE_T2_FLAIR
                elif series_description.find('t2') > -1:
                    data_type = MRI_Type.MRI_TYPE_T2
                elif series_description.find('dwi') > -1 or series_description.find('adc') > -1 or \
                        series_description.find('apparent diffusion coefficient') > -1:
                    data_type = MRI_Type.MRI_TYPE_DWI

        elif manufacturer == MANUFACTURER.kMANUFACTURER_GE:
            if series_description is not None and series_description != '':
                if series_description.find('easl') > -1:
                    ASL_type, data_type = ASL_Type.ASL_PCASL, MRI_Type.MRI_TYPE_eASL_PCASL_GE
                elif (series_description.find('3d') > -1 and series_description.find('asl') > -1) or \
                        series_description.find('cerebral blood flow') > -1 or series_description.find('cbf') > -1:
                    ASL_type, data_type = ASL_Type.ASL_PCASL, MRI_Type.MRI_TYPE_3D_PCASL_GE
                elif series_description.find('t1') > -1:
                    data_type = MRI_Type.MRI_TYPE_T1
                    # t1 放在t2 flair前面；避免t1 flair被认为是 t2 flair
                elif series_description.find('flair') > -1 or series_description.find('fluid') > -1:
                    data_type = MRI_Type.MRI_TYPE_T2_FLAIR
                elif series_description.find('t2') > -1:
                    data_type = MRI_Type.MRI_TYPE_T2
                elif series_description.find('dwi') > -1 or series_description.find('adc') > -1 or \
                        series_description.find('apparent diffusion coefficient') > -1:
                    data_type = MRI_Type.MRI_TYPE_DWI

        elif manufacturer == MANUFACTURER.kMANUFACTURER_UIH:
            if series_description is not None and series_description != '':
                if series_description.find('asl_3d') > -1 or series_description.find('att') > -1 or \
                        series_description.find('acbv') > -1 or series_description.find('cbf') > -1:
                    ASL_type, data_type = ASL_type, MRI_Type.MRI_TYPE_3D_PASL_UIH
                elif series_description.find('t1') > -1:
                    data_type = MRI_Type.MRI_TYPE_T1
                    # t1 放在t2 flair前面；避免t1 flair被认为是 t2 flair
                elif series_description.find('flair') > -1 or series_description.find('fluid') > -1:
                    data_type = MRI_Type.MRI_TYPE_T2_FLAIR
                elif series_description.find('t2') > -1:
                    data_type = MRI_Type.MRI_TYPE_T2
                elif series_description.find('dwi') > -1:
                    data_type = MRI_Type.MRI_TYPE_DWI

        return ASL_type, data_type

    def validate_series(self):
        '''
        验证数据的完整性以及正确性；计算出层厚、层数量、以及重复次数是否符合要求
        :return:
        '''
        # 检查是否缺少Slice
        if self.dicom_image_type in (DICOM_IMAGE_TYPE.DICOM_IMAGE_TYPE_3D, DICOM_IMAGE_TYPE.DICOM_IMAGE_TYPE_MOSAIC):
            for i, image in enumerate(self):
                if (image.InstanceNumber != self.SliceNumber * i + 1) and (image.InstanceNumber != i + 1):
                    raise MissingSliceError(i * self.SliceNumber + 1)

        elif self.dicom_image_type == DICOM_IMAGE_TYPE.DICOM_IMAGE_TYPE_2D:
            for r in range(self.Repetition):
                first_number = self[r * self.SliceNumber].InstanceNumber
                # 增量：为应对某些number是等差增长，而非+1。但前提是第一张和第二章是不缺损的,才能保证正确
                d = self[r * self.SliceNumber + 1].InstanceNumber - self[r * self.SliceNumber].InstanceNumber
                # 允许每个Volume不连续
                for n in range(self.SliceNumber):
                    no = r * self.SliceNumber + n
                    if self[no].InstanceNumber != first_number + d * n:
                        logger.info(
                            f'未验证通过序列：{self.SeriesDescription}；层数：{self.SliceNumber}，重复次数：{self.Repetition}，'
                            f'图像类型：{self.dicom_image_type.value}，剖面：{self.SliceDirection}')
                        raise MissingSliceError(first_number + d * n)

        logger.info(f'验证通过序列：{self.SeriesDescription}；层数：{self.SliceNumber}，重复次数：{self.Repetition}，'
                    f'图像类型：{self.dicom_image_type.value}，剖面：{self.SliceDirection}')

    def load(self, rescale=1):
        '''
        加载数序列的图像，4维图像：包含重复次数
        :return:
        '''
        image = None
        if self.dicom_image_type == DICOM_IMAGE_TYPE.DICOM_IMAGE_TYPE_MOSAIC:
            for idx, instance in enumerate(self):
                _3d_image = demosaic(instance.ImageMat, self.MosaicSliceNumber)
                if image is None:
                    # 4维矩阵
                    image = np.repeat(_3d_image[:, :, :, np.newaxis], len(self), 3)
                else:
                    if _3d_image.shape != image.shape[:-1]:
                        raise Exception('维度不一致')
                    image[:, :, :, idx] = _3d_image

        elif self.dicom_image_type == DICOM_IMAGE_TYPE.DICOM_IMAGE_TYPE_2D:
            image = np.zeros((self.Rows, self.Columns, self.SliceNumber, self.Repetition))
            if self.is_second_arrangement_mode:
                for r in range(self.Repetition):
                    for n in range(self.SliceNumber):
                        instance_number = n * self.Repetition + r
                        image[:, :, n, r] = self[instance_number].ImageMat
            else:
                for r in range(self.Repetition):
                    for n in range(self.SliceNumber):
                        instance_number = r * self.SliceNumber + n
                        image[:, :, n, r] = self[instance_number].ImageMat

        elif self.dicom_image_type == DICOM_IMAGE_TYPE.DICOM_IMAGE_TYPE_3D:
            image = np.zeros((self.Rows, self.Columns, self.SliceNumber, self.Repetition))
            for no, _3d_image in enumerate(self):
                if self.is_third_arrangement_mode:
                    # 将第三种模式转换成第二种模式
                    image_mat = np.zeros(_3d_image.ImageMat.shape, dtype=_3d_image.ImageMat.dtype)
                    single_group = self.Repetition // 2
                    for i in range(0, _3d_image.ImageMat.shape[-1], 2):
                        image_mat[..., i] = _3d_image.ImageMat[..., i // 2]
                        image_mat[..., i + 1] = _3d_image.ImageMat[..., single_group + i // 2]
                    _3d_image.ImageMat = image_mat
                    self.is_third_arrangement_mode = False
                    self.is_second_arrangement_mode = True

                repetition = self.Repetition // len(self)
                if self.is_second_arrangement_mode:
                    for r in range(repetition):
                        for n in range(self.SliceNumber):
                            instance_number = n * self.Repetition + r
                            image[:, :, n, no * repetition + r] = _3d_image.ImageMat[..., instance_number]
                else:
                    for r in range(repetition):
                        for n in range(self.SliceNumber):
                            instance_number = r * self.SliceNumber + n
                            image[:, :, n, no * repetition + r] = _3d_image.ImageMat[..., instance_number]
        # 数值转换
        return image if image is None else (image * self.RescaleSlope + self.RescaleIntercept) * rescale

    def merge(self, other):
        if not isinstance(other, SeriesModel):
            raise Exception("only merge SeriesModel")
        if other.StudyInstanceUID != self.StudyInstanceUID:
            raise Exception('无法合并并不属于同一Study的序列')
        self.extend(other)
        self.Repetition += other.Repetition

    def __add__(self, other):
        return self.merge(other)

    def _calc_2d_affine(self):
        # 原点与方向
        orientation = self.ImageOrientationPatient
        position = self.ImagePositionPatient

        # 分辨率
        z_space = self.SpacingBetweenSlices
        x_space, y_space = self.PixelSpacing

        m = np.zeros((3, 3), dtype=float)
        m[0] = orientation[:3]
        m[1] = orientation[3:]
        val = sum(np.power(m[0], 2))
        if val > 0:
            val = 1 / np.sqrt(val)
            m[0] *= val
        else:
            m[0] = [1, 0, 0]

        val = sum(np.power(m[1], 2))
        if val > 0:
            val = 1 / np.sqrt(val)
            m[1] *= val
        else:
            m[1] = [0, 1, 0]

        # /* row 3 is the cross product of rows 1 and 2*/
        m[2, 0] = m[0, 1] * m[1, 2] - m[0, 2] * m[1, 1]
        m[2, 1] = m[0, 2] * m[1, 0] - m[0, 0] * m[1, 2]
        m[2, 2] = m[0, 0] * m[1, 1] - m[0, 1] * m[1, 0]

        # 转置阵
        m = m.T

        if np.linalg.det(m) < 0:
            m[:2] *= -1

        # 乘以分辨率
        diag_vox = np.array([[x_space, 0, 0], [0, y_space, 0], [0, 0, z_space]])
        m = np.matmul(m, diag_vox)

        m = np.c_[m, position]
        m = np.r_[m, [[0, 0, 0, 1]]]

        return m

    def calc_affine(self):
        m = self._calc_2d_affine()

        # mosaic的坐标系，需要进一步转换成2D的坐标系
        if self.dicom_image_type == DICOM_IMAGE_TYPE.DICOM_IMAGE_TYPE_MOSAIC:
            factor_x = factor_y = (self.Rows - (self.Columns / int(np.ceil(np.sqrt(self.SliceNumber))))) / 2.0
            m[:, 3] += m[:, 0] * factor_x + m[:, 1] * factor_y

        # 要反转的是 slice direction todo：不一定是[2,2]???
        if self.z_reversed:
            Q = np.eye(4)
            Q[2, 2] *= -1
            m = np.matmul(m, Q)

        return m


def dicom_parse_series(dir: str, parse_after_hook=None) -> Dict[str, Dict[str, SeriesModel]]:
    study_list = {}
    for root, _, files in os.walk(dir):
        for fn in files:
            abs_fn = os.path.join(root, fn)
            try:
                ds = pydicom.read_file(abs_fn)
                ds_tags = InstanceModel(ds, abs_fn)

                if parse_after_hook != None:
                    # 执行hook
                    parse_after_hook(abs_fn, ds_tags)
            except InvalidDicomError:
                logger.debug(f'忽略文件：{abs_fn}')
                continue
            except PhotometricRGBError:
                logger.debug(f'忽略彩色图像：{abs_fn}')
                continue
            except Exception as e:
                logger.debug(f'{e}：{abs_fn}')
                continue
            if ds_tags.StudyInstanceUID not in study_list:
                study_list[ds_tags.StudyInstanceUID] = {}
            if ds_tags.SeriesInstanceUID not in study_list[ds_tags.StudyInstanceUID]:
                study_list[ds_tags.StudyInstanceUID][ds_tags.SeriesInstanceUID] = SeriesModel(ds_tags, ds)
            study_list[ds_tags.StudyInstanceUID][ds_tags.SeriesInstanceUID].append(ds_tags)

    for study in study_list.values():
        for series in study.values():
            series.finish_handle()
    return study_list
