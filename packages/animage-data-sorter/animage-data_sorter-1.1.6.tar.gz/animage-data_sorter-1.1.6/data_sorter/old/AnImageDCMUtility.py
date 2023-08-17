import SimpleITK as sitk
import pydicom as pd
import numpy as np
import dicom2nifti
import os
import time
import hashlib
import datetime


def create_dcm_series(pixel_array, ref_dcm, save_path, data_type, perfusion_type, series_param, folder_suffix=''):
    input_int = series_param[0]
    slope_adj = series_param[1]
    inter_adj = series_param[2]
    series_tag = data_type+'-'+perfusion_type
    if folder_suffix != '':
        save_folder = data_type + '-' + folder_suffix
    else:
        save_folder = data_type

    reader = sitk.ImageFileReader()
    reader.SetFileName(ref_dcm)
    ref_image = reader.Execute()

    mod_time = time.strftime("%H%M%S")
    mod_date = time.strftime("%Y%m%d")

    writer = sitk.ImageFileWriter()
    writer.KeepOriginalImageUIDOn()

    pixel_array = ((pixel_array + inter_adj) * slope_adj).astype(np.int16)
    for slice_idx in range(np.shape(pixel_array)[2]):
        image = sitk.GetImageFromArray(pixel_array[:, :, slice_idx])
        image = _copy_tags(image, reader, slice_idx+1, mod_time, mod_date, series_tag)
        image = _modify_series_uid(image, reader, series_tag, input_int)
        image = _modify_sop_uid(image, reader, series_tag, slice_idx+1)

        file_target = os.path.join(save_path, save_folder, perfusion_type, "{:04d}.dcm".format(slice_idx))
        writer.SetFileName(file_target)
        writer.Execute(image)
        pd_image = pd.dcmread(file_target)  # TODO, 最好脱离Pydicom的依赖，目前Sitk搞不清楚这一块
        pd_image[0x0028, 0x1052].value = -inter_adj
        pd_image[0x0028, 0x1053].value = 1 / slope_adj
        pd_image = _add_anImage_tag(pd_image, series_tag)
        pd_image.save_as(file_target)


def copy_dcm_slice(image_data, save_path, data_type, perfusion_type, slice_num, override_series_desc=False):
    series_tag = data_type + '-' + perfusion_type
    if override_series_desc:
        image_data[0x0008, 0x103E].value = series_tag
    image_data = _add_anImage_tag(image_data, series_tag)
    image_data = _modify_series_uid(image_data, None, series_tag, None)
    image_data = _modify_sop_uid(image_data, None, series_tag, None)
    image_data.save_as(os.path.join(save_path, data_type, perfusion_type, '{:04d}.dcm'.format(slice_num)))


def _add_anImage_tag(pd_image, series_tag):
    block = pd_image.private_block(0x0099, 'ANIMAGE HEADER', create=True)
    block2 = pd_image.private_block(0x0099, 'Created through AnImageDataSorter', create=True)
    block3 = pd_image.private_block(0x0099, 'Version 1.03.03', create=True)
    block4 = pd_image.private_block(0x0099, datetime.datetime.now().strftime('%c'), create=True)
    block5 = pd_image.private_block(0x0099, series_tag, create=True)
    return pd_image


def _copy_tags(image, reader, instance, mod_time, mod_date, series_desc):
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
    ]
    for tag_idx in copy_list:
        try:
            image.SetMetaData(tag_idx, reader.GetMetaData(tag_idx))
        except:
            pass

    pixel_spacing = float(reader.GetMetaData("0028|0030").split('\\')[0])
    slice_spacing = float(reader.GetMetaData("0018|0088"))
    image.SetSpacing([pixel_spacing, pixel_spacing, slice_spacing])

    image.SetMetaData("0008|103e", series_desc)
    image.SetMetaData("0008|0031", mod_time)
    image.SetMetaData("0008|0021", mod_date)
    image.SetMetaData("0008|0008", "DERIVED\\SECONDARY\\PROCESSED")
    image.SetMetaData("0020|000e", "1.2.826.0.1.3680043.2.1125." + mod_date + ".1" + mod_time)
    image.SetMetaData("0020|0013", str(instance))
    image.SetMetaData("0020|0032", '0\\0\\'+str(instance * slice_spacing))
    image.SetMetaData("0020|1041", str(instance * slice_spacing))

    return image


def _modify_series_uid(image, reader, filetype, input_int):
    suffix = str(int(hashlib.sha1(filetype.encode("utf-8")).hexdigest(), 16) % (10 ** 8))
    if isinstance(image, pd.Dataset):
        if input_int:
            image[0x0020, 0x0011].value = int(input_int)
        original_string = image[0x0020, 0x000E].value
        cut_length = len(original_string) - len(suffix) - 1
        image[0x0020, 0x000E].value = original_string[:cut_length] + '.' + suffix
    else:
        if input_int:
            image.SetMetaData("0020|0011", str(input_int))
        original_string = reader.GetMetaData("0020|000e")
        cut_length = len(original_string) - len(suffix) - 1
        image.SetMetaData("0020|000e", original_string[:cut_length] + '.' + suffix)

    return image


def _modify_sop_uid(image, reader, filetype, instance_num):
    if isinstance(image, pd.Dataset):
        if not instance_num:
            instance_num = image[0x0020, 0x0013].value
    else:
        if not instance_num:
            instance_num = reader.GetMetaData("0020|0013")
    suffix = str(int(hashlib.sha1(filetype.encode("utf-8")).hexdigest(), 16) % (10 ** 8) + instance_num)

    if isinstance(image, pd.Dataset):
        original_string = image[0x0008, 0x0018].value
        cut_length = len(original_string) - len(suffix) - 1
        image.file_meta.MediaStorageSOPInstanceUID = original_string[:cut_length] + '.' + suffix
        image[0x0008, 0x0018].value = original_string[:cut_length] + '.' + suffix
    else:
        original_string = reader.GetMetaData("0008|0018")
        cut_length = len(original_string) - len(suffix) - 1
        image.SetMetaData("0002|0003", original_string[:cut_length] + '.' + suffix)
        image.SetMetaData("0008|0018", original_string[:cut_length] + '.' + suffix)

    return image


def dcm_to_nii(save_path, data_type, perfusion_type):
    print(os.path.join(save_path, data_type, perfusion_type))
    dicom2nifti.dicom_series_to_nifti(os.path.join(save_path, data_type, perfusion_type),
                                      os.path.join(save_path, data_type, perfusion_type + '.nii.gz'),
                                      reorient_nifti=True)


def iterative_seq_tag_search(obj, tag, input_array):
    return_value = input_array
    if tag in obj:
        return_value.append(obj[tag].value)
    else:
        for elem in obj:
            if elem.VR == "SQ":
                for item in elem:
                    return_value = iterative_seq_tag_search(item, tag, return_value)
    return return_value


if __name__ == '__main__':
    folder_path = r'C:\Users\zeyao\Desktop\dicom test\input'
    folder_path2 = r'C:\Users\zeyao\Desktop\dicom test\output'
    ref_dicom = r'C:\Users\zeyao\Desktop\dicom test\input\MR000000.dcm'
    array = np.zeros((128, 128, 72))
    for slices in range(72):
        array[:, :, slices] = pd.dcmread(os.path.join(folder_path, 'MR{:06d}.dcm'.format(slices))).pixel_array

    os.makedirs(os.path.join(folder_path2, 'asl'), exist_ok=True)
    os.makedirs(os.path.join(folder_path2, 'asl', 'm0'), exist_ok=True)
    series_param = [1, 0.001, 50]
    create_dcm_series(array, ref_dicom, folder_path2, 'asl', 'm0', series_param)
    dcm_to_nii(folder_path2, 'asl', 'm0')
