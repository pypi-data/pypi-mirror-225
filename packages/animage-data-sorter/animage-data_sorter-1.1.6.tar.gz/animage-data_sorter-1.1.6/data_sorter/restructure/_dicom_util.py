import copy
import os.path
import subprocess

import SimpleITK as sitk
import nibabel
from pydicom._storage_sopclass_uids import SecondaryCaptureImageStorage, RLELossless
from pydicom.uid import generate_uid

from ._dicom import *


# todo: 2023-05-16: 3D格式的 dicom文件有些问题
# todo: 有时间查看dcm2niix源码



def g_slice_location(first_slice_location, z_space, slice_num):
    for i in range(slice_num):
        yield first_slice_location + i * z_space

def g_position(m, slice_num):
    for i in range(slice_num):
        yield m[:3, 3] + i * m[:3, 2]

def cmd_dcm2niix(src, out, format):
    cmd = f'"D:\Program Files\MRIcron\Resources\dcm2niix.exe" -o "{out}" -z y -f "{format}" -b n -w 1 "{src}"'
    c = subprocess.Popen(cmd)
    c.wait()
    return c.returncode

def save_dicom(dicom_path: str, ds: pydicom.Dataset):
    ds_copy = copy.deepcopy(ds)
    ds_copy.compress(RLELossless)
    ds_copy.file_meta.TransferSyntaxUID = RLELossless
    ds_copy.save_as(dicom_path, write_like_original=False)

def write_dicom_series(image_data:np.ndarray, series_model:SeriesModel, tag:str, series_number:int, output_path:str,
                       slope:float=1, intercept: float=0, replace_lambda=None, dtype=None):
    '''
    将3D图像按照每个切片保存为单个DICOM文件
    :param image_data:
    :param series_model: 大部分标签所参考的对象
    :param tag:
    :param output_path:
    :param slope: 原始数值倍数
    :param intercept:
    :param replace_lambda: 需要额外替换的标签
    :return:
    '''
    # 每个切片保存为一个DICOM文件
    if replace_lambda is None:
        replace_lambda = lambda x: x
    os.makedirs(output_path, exist_ok=True)

    dicom_affine = series_model.calc_affine()
    if series_model.dicom_image_type == DICOM_IMAGE_TYPE.DICOM_IMAGE_TYPE_MOSAIC:
        # 只考虑了 Axial 的mosaic图像
        normal_direction = dicom_affine[2, 2] / abs(dicom_affine[2, 2]) # 切片方向
        for i in range (series_model.SliceNumber):
            position = (dicom_affine[:3, 3] + i * dicom_affine[:3, 2]).tolist()
            slice_location =  series_model.SliceLocation + normal_direction * series_model.SliceThickness * i
            slice_image = image_data[:,:,i]

            dataset = create_dicom_forpydicom(slice_image, position, series_model.ImageOrientationPatient, slice_location,
                                              series_model, series_number, tag, slope, intercept)
            dataset.InstanceNumber = i + 1
            replace_lambda(dataset)
            save_dicom(os.path.join(output_path, 'MR%06d.dcm'%(i+1)), dataset)

    elif series_model.dicom_image_type == DICOM_IMAGE_TYPE.DICOM_IMAGE_TYPE_2D:
        # slice_location 增加
        for i in range(series_model.SliceNumber):
            slice_image = image_data[:, :, i]
            if series_model.is_second_arrangement_mode:
                position = series_model[i * series_model.Repetition].ImagePositionPatient
                slice_location = series_model[i * series_model.Repetition].SliceLocation
            else:
                position = series_model[i].ImagePositionPatient
                slice_location = series_model[i].SliceLocation

            dataset = create_dicom_forpydicom(slice_image, position, series_model.ImageOrientationPatient, slice_location,
                                              series_model, series_number, tag, slope, intercept)
            dataset.InstanceNumber = i + 1
            replace_lambda(dataset)
            save_dicom(os.path.join(output_path, 'MR%06d.dcm'%(i+1)), dataset)

    elif series_model.dicom_image_type == DICOM_IMAGE_TYPE.DICOM_IMAGE_TYPE_3D:
        first_z_position = series_model.ImagePositionPatientList[0][2]
        second_z_position = series_model.ImagePositionPatientList[1][2]
        normal_direction = 1 if first_z_position < second_z_position else -1
        for i in range(series_model.SliceNumber):
            slice_image = image_data[:, :, i]
            slice_location = series_model.SliceLocation + normal_direction * series_model.SliceThickness * i
            dataset = create_dicom_forpydicom(slice_image, series_model.ImagePositionPatientList[i], series_model.ImageOrientationPatient,
                                              slice_location, series_model, series_number, tag, slope, intercept)
            dataset.InstanceNumber = i + 1
            replace_lambda(dataset)
            save_dicom(os.path.join(output_path, 'MR%06d.dcm'%(i+1)), dataset)

    else:
        raise UnidentifiedDicomImageTypeError()

    nifti_affine = dicom_affine.copy()
    # nifti 与 dicom 方向不一样 dicom: LPS -> nifti: RAS
    nifti_affine[:2] *= -1
    # todo：
    # 自己写的转换nifti，需要大量验证；速度最快；其中转换代码从dcm2niix源码中而来
    image_data_swap = (image_data.swapaxes(0, 1) * slope + intercept)
    if dtype is not None:
        image_data_swap = image_data_swap.astype(dtype)
    elif ('asl' not in tag) or 'm0' in tag:
        image_data_swap = image_data_swap.astype(np.int16)
    else:
        image_data_swap = image_data_swap.astype(np.float32)

    filename = os.path.join(os.path.dirname(output_path), tag + '.nii.gz')
    nibabel.Nifti1Image(image_data_swap, nifti_affine).to_filename(filename)

    # todo 利用sitk修复 nifti文件，自己写的nifti头部可能有些错误，会对后续步骤造成影响
    reader = sitk.ImageFileReader()
    reader.SetImageIO("NiftiImageIO")
    reader.SetFileName(filename)
    new_image = reader.Execute()

    writer = sitk.ImageFileWriter()
    writer.SetFileName(filename)
    writer.Execute(new_image)

    return filename

    # 用的开源dcm2niix，依赖dcm2niix.exe；最完善的转换插件
    # cmd_dcm2niix(output_path, os.path.dirname(output_path), tag)

    # python库，效率较低，但是无需依赖；也存在些问题
    # dicom2nifti.dicom_series_to_nifti(output_path, output_path + '.nii.gz', reorient_nifti=True)

def create_dicom_forpydicom(image:np.ndarray, position, orientation, slice_location, series_model: SeriesModel,
                            series_number: int, tag: str, slope: float=1, intercept: float=0):
    ds = pydicom.Dataset()
    ds.SOPClassUID = SecondaryCaptureImageStorage
    ds.SOPInstanceUID = generate_uid()
    ds.is_implicit_VR = True
    ds.is_little_endian = True
    ds.fix_meta_info()
    ds.file_meta.FileMetaInformationGroupLength = 1

    ds.PatientName = series_model.PatientName
    ds.PatientID = series_model.PatientID
    ds.PatientBirthDate = series_model.PatientBirthDate
    ds.PatientSex = series_model.PatientSex
    ds.PatientAge = series_model.PatientAge
    ds.PatientSize = series_model.PatientSize
    ds.PatientWeight = series_model.PatientWeight
    ds.PatientPosition = series_model.PatientPosition

    ds.StudyInstanceUID = series_model.StudyInstanceUID
    ds.StudyDescription = series_model.StudyDescription
    ds.StudyDate = series_model.StudyDate
    ds.StudyTime = series_model.StudyTime
    ds.StudyID = series_model.StudyID

    ds.SeriesInstanceUID = series_model.SeriesInstanceUID + '.1'
    ds.SeriesDate = series_model.SeriesDate
    ds.SeriesTime = series_model.SeriesTime
    ds.SeriesNumber = series_number

    ds.Manufacturer = series_model.Manufacturer.value
    ds.ManufacturerModelName = series_model.ManufacturerModelName
    ds.Modality = series_model.Modality.value
    ds.InstitutionName = series_model.InstitutionName

    ds.BitsAllocated = 16
    ds.BitsStored = 16
    ds.HighBit = 16
    ds.SliceThickness = series_model.SliceThickness
    ds.PixelSpacing = series_model.PixelSpacing
    ds.PixelRepresentation = 1
    ds.SpacingBetweenSlices = series_model.SpacingBetweenSlices
    ds.PhotometricInterpretation = series_model.PhotometricInterpretation

    ds.ProtocolName = tag
    ds.SeriesDescription = tag
    ds.SamplesPerPixel = 1
    ds.Rows = image.shape[0]
    ds.Columns = image.shape[1]
    ds.RescaleSlope = slope
    ds.RescaleIntercept = intercept


    # t = datetime.now()
    # ds.InstanceCreationDate = t.strftime('%Y%m%d')
    # ds.InstanceCreationTime = t.strftime('%H%M%S')

    ds.ImagePositionPatient = position
    ds.ImageOrientationPatient = orientation
    ds.SliceLocation = slice_location

    # 溢出的数值警告
    if image.max() > 32767:
        logger.warning('图像数值有溢出，> 32767 将使用32767代替')
        image[image > 32767] = 32767
    if image.min() < -32768:
        logger.warning('图像数值有溢出，< -32768 将使用-32768代替')
        image[image < -32768] = -32768

    ds.PixelData = image.astype(np.int16).tobytes()

    return ds

def create_dicom_forsitk(image:np.ndarray, position, orientation, slice_location, ref: pydicom.Dataset):
    image = sitk.GetImageFromArray(image.astype(np.uint16))
    image.SetMetaData('0020|0037', '\\'.join([str(i) for i in orientation]))
    image.SetMetaData('0020|0032', '\\'.join([str(i) for i in position]))
    image.SetMetaData('0020|1041', str(slice_location))


    image.SetMetaData('0020|000E', ref.SeriesInstanceUID)
    image.SetMetaData('0020|000d', ref.StudyInstanceUID)
    uid = generate_uid()
    image.SetMetaData('0002|0003', uid)
    image.SetMetaData('0008|0018', uid)
    image.SetMetaData('0002|0002', SecondaryCaptureImageStorage)
    image.SetMetaData('0008|0016', SecondaryCaptureImageStorage)
    image.SetMetaData('0008|0060', 'MR')
    image.SetMetaData('0008|0030', ref.StudyTime)
    image.SetMetaData('0008|0020', ref.StudyDate)
    # image.SetMetaData('0028|1052', str(-1))
    # image.SetMetaData('0028|1053', str(0.1))
    return image

def convert(input_path, output_path, ref_img_fn: str = None, dst_space=None, interpolation=None,
            default_pixel_nan=False):
    '''
    转换nifti空间信息
    :param input_path:
    :param output_path:
    :param ref_img_fn:
    :param dst_space: 俩参数二选一
    :param interpolation: 插值方式，ADC需要使用邻近插值
    :param default_pixel_nan: 灌注图背景需要填充nan，但只有浮点支持nan；所以此参数会改变原有的数据类型，其余情况不适用
    :return:
    '''
    if interpolation is None:
        interpolation = sitk.sitkBSpline
    reader = sitk.ImageFileReader()
    reader.SetImageIO("NiftiImageIO")
    reader.SetFileName(input_path)
    if default_pixel_nan:
        reader.SetOutputPixelType(sitk.sitkFloat32)
    image = reader.Execute()
    old_sizes = image.GetSize()
    old_spaces = image.GetSpacing()

    # dst_space[0] = min(dst_space[0], spaces[0])
    # dst_space[1] = min(dst_space[1], spaces[1])
    # dst_space[2] = min(dst_space[2], spaces[2])

    resample = sitk.ResampleImageFilter()
    if ref_img_fn is not None and ref_img_fn != '':
        reader.SetFileName(ref_img_fn)
        ref_img = reader.Execute()
        dst_space = ref_img.GetSpacing()
        resample.SetOutputSpacing(dst_space)
        resample.SetSize(ref_img.GetSize())
        resample.SetOutputOrigin(ref_img.GetOrigin())
        resample.SetOutputDirection(ref_img.GetDirection())
    elif dst_space is not None:
        size = [
            int(np.round(old_sizes[0] * old_spaces[0] / dst_space[0])),
            int(np.round(old_sizes[1] * old_spaces[1] / dst_space[1])),
            int(np.floor(old_sizes[2] * old_spaces[2] / dst_space[2]))
        ]
        resample.SetOutputSpacing(dst_space)
        resample.SetSize(size)

    resample.SetOutputOrigin(reader.GetOrigin())
    resample.SetOutputDirection(reader.GetDirection())

    resample.SetTransform(sitk.Transform())
    resample.SetDefaultPixelValue(np.nan)
    resample.SetInterpolator(interpolation)
    new_image = resample.Execute(image)

    sizes = new_image.GetSize()
    spaces = new_image.GetSpacing()

    logger.debug("原始尺寸 {:d}, {:d}, {:d} [{:0.2f}, {:0.2f}, {:0.2f}]；重建尺寸 {:d}, {:d}, {:d} [{:0.2f}, {:0.2f}, {:0.2f}]".
                 format(old_sizes[0], old_sizes[1], old_sizes[2], old_spaces[0], old_spaces[1], old_spaces[2],
                        sizes[0], sizes[1], sizes[2], spaces[0], spaces[1], spaces[2]))

    writer = sitk.ImageFileWriter()
    writer.SetFileName(output_path)
    writer.Execute(new_image)