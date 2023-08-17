import numpy as np
import os
import datetime
from pydicom.dataset import FileMetaDataset
import SimpleITK as sitk
import pydicom as pd
import dicom2nifti
import hashlib


## 杂项
def demosaic(input_image, data_array, dcm_tag, save_name, intermediate_folder, formatpack):
    ## formatpack0=slice_num
    #  formatpack1=sn
    #  formatpack2=dmrow
    #  formatpack3=siemensst
    #  formatpack4=siemenssl
    #  formatpack5=siemensipp
    #  formatpack6=siemensiop
    a = 0
    v = np.zeros((formatpack[0], formatpack[2], formatpack[2]))
    sid3 = input_image[0x0008, 0x0008].value
    sid4 = []
    for i in sid3:
        if i != 'MOSAIC':
            sid4.append(i)

    bitsStored = len(bin(int(data_array.max()))) - 2
    for i in np.vsplit(data_array, formatpack[1]):
        for j in np.hsplit(i, formatpack[1]):
            if a >= formatpack[0]:
                break
            jf = np.squeeze(j)
            v[a, :, :] = jf
            input_image[0x0028, 0x0101].value = bitsStored
            input_image[0x0028, 0x0102].value = bitsStored - 1

            input_image.Columns, input_image.Rows = formatpack[2], formatpack[2]
            input_image = get_and_set_bytetype(input_image, jf)
            input_image[0x0020, 0x0013].value = a + 1
            input_image[0x0020, 0x1041].value = formatpack[4] + a * formatpack[3]
            tempipp = formatpack[5]
            tempipp[2] = '{:.4f}'.format(input_image[0x0020, 0x1041].value)
            input_image[0x0020, 0x0032].value = tempipp
            input_image[0x0008, 0x0070].value = 'SIEMENS'
            input_image[0x0020, 0x0037].value = formatpack[6]
            input_image.AcquisitionNumber = a + 1
            sid = str(input_image.SourceImageSequence[a].ReferencedSOPInstanceUID)
            # print(input_image.file_meta)
            input_image[0x0008, 0x0008].value = sid4
            input_image[0x0008, 0x0018].value = sid
            input_image = add_AnImage_tag(input_image, dcm_tag)
            input_image.file_meta.MediaStorageSOPInstanceUID = sid
            modify_series_uid(input_image, 'm0', False)
            input_image.save_as(os.path.join(intermediate_folder, 'asl', save_name, '{:04d}.dcm'.format(a + 1)),
                                write_like_original=False)
            a += 1

    dicom2nifti.dicom_series_to_nifti(os.path.join(intermediate_folder,
                                                   'asl', save_name),
                                      os.path.join(intermediate_folder,
                                                   'asl', save_name + '.nii.gz'), reorient_nifti=False)


def to_mosaic(array_3d):
    [a,b,c] = np.shape(array_3d)
    factor = np.ceil(np.sqrt(c))
    array_2d = np.zeros((int(a * factor), int(b * factor)))
    for slice_idx in range(c):
        a_idx = int(np.floor(slice_idx / factor)) * a
        b_idx = int(np.remainder(slice_idx, factor)) * b
        array_2d[a_idx:a_idx+a, b_idx:b_idx+b] = array_3d[:, :, slice_idx]
    return array_2d


def demosaic_sitk(orig_input_image, data_array, tag, intermediate_folder, formatpack):
    writer = sitk.ImageFileWriter()
    a = 0
    v = np.zeros((formatpack[0], formatpack[2], formatpack[2]))
    sid3 = orig_input_image[0x0008, 0x0008].value
    sid4 = []
    for i in sid3:
        if i != 'MOSAIC':
            sid4.append(i)
    for i in np.vsplit(data_array, formatpack[1]):
        for j in np.hsplit(i, formatpack[1]):
            if a >= formatpack[0]:
                break
            jf = np.squeeze(j)
            sitk_img = sitk.GetImageFromArray(jf.astype(np.uint16))
            writer.SetFileName("temp.dcm")
            writer.Execute(sitk_img)

            input_image = pd.dcmread("temp.dcm")
            for element in orig_input_image:
                if np.floor(int(element.tag) / 16 ** 4) in [0x8, 0x10, 0x18, 0x20, 0x28]:
                    if element.tag in input_image:
                        input_image[element.tag].value = element.value
                    else:
                        input_image.add_new(element.tag, element.VR, element.value)

            input_image.Columns, input_image.Rows = formatpack[2], formatpack[2]
            # input_image = get_and_set_bytetype(input_image, jf)
            input_image[0x0020, 0x0013].value = a + 1
            input_image[0x0020, 0x1041].value = formatpack[4] + a * formatpack[3]
            tempipp = formatpack[5]
            tempipp[2] = '{:.4f}'.format(input_image[0x0020, 0x1041].value)
            input_image[0x0020, 0x0032].value = tempipp
            input_image[0x0008, 0x0070].value = 'SIEMENS'
            input_image[0x0020, 0x0037].value = formatpack[6]
            input_image.AcquisitionNumber = a + 1
            sid = str(input_image.SourceImageSequence[a].ReferencedSOPInstanceUID)
            # print(input_image.file_meta)
            input_image[0x0008, 0x0008].value = sid4
            input_image[0x0008, 0x0018].value = sid
            input_image = add_AnImage_tag(input_image, "asl-"+tag)
            input_image.file_meta.MediaStorageSOPInstanceUID = sid
            modify_series_uid(input_image, tag, None)
            input_image.save_as(os.path.join(intermediate_folder, 'asl', tag, '{:04d}.dcm'.format(a + 1)),
                                write_like_original=False)
            a += 1

    dicom2nifti.dicom_series_to_nifti(os.path.join(intermediate_folder,
                                                   'asl', tag),
                                      os.path.join(intermediate_folder,
                                                   'asl', tag + '.nii.gz'), reorient_nifti=False)


def modify_uid_tag_AnImage(input_image, filetype, instance_num=None, input_int=None):
    input_image = modify_series_uid(input_image, filetype, input_int)
    input_image = modify_sop_uid(input_image, filetype, instance_num)
    input_image = add_AnImage_tag(input_image, filetype)
    return input_image


def modify_series_uid(input_image, filetype, input_int):
    suffix = str(int(hashlib.sha1(filetype.encode("utf-8")).hexdigest(), 16) % (10 ** 8))
    original_string = input_image[0x0020, 0x000E].value
    cut_length = len(original_string) - len(suffix) - 1
    input_image[0x0020, 0x000E].value = original_string[:cut_length] + '.' + suffix
    if input_int:
        input_image[0x0020, 0x0011].value = int(input_int)
    return input_image


def modify_sop_uid(input_image, filetype, instance_num):
    if not instance_num:
        instance_num = input_image[0x0020, 0x0013].value
    suffix = str(int(hashlib.sha1(filetype.encode("utf-8")).hexdigest(), 16) % (10 ** 8) + instance_num)
    original_string = input_image[0x0008, 0x0018].value
    cut_length = len(original_string) - len(suffix) - 1
    input_image.file_meta.MediaStorageSOPInstanceUID = original_string[:cut_length] + '.' + suffix
    input_image[0x0008, 0x0018].value = original_string[:cut_length] + '.' + suffix
    return input_image


def add_AnImage_tag(input_image, filetype):
    if [0x0008, 0x0008] in input_image:
        input_image[0x0008, 0x0008].value = ['DERIVED', 'SECONDARY', 'PROCESSED']
    else:
        input_image.add_new([0x0008, 0x0008], 'CS', ['DERIVED', 'SECONDARY', 'PROCESSED'])
    input_image.remove_private_tags()
    tag = filetype.lower()
    block = input_image.private_block(0x0099, 'ANIMAGE HEADER', create=True)
    block2 = input_image.private_block(0x0099, 'Created through AnImageDataSorter', create=True)
    block3 = input_image.private_block(0x0099, 'Version 1.03.03', create=True)
    block4 = input_image.private_block(0x0099, datetime.datetime.now().strftime('%c'), create=True)
    block5 = input_image.private_block(0x0099, tag, create=True)
    if not ('t1' in filetype or 't2' in filetype):
        if [0x0018, 0x1030] in input_image:
            input_image[0x0018, 0x1030].value = tag
        else:
            input_image.add_new([0x0018, 0x1030], 'LO', tag)
        if [0x0008, 0x103e] in input_image:
            input_image[0x0008, 0x103e].value = tag
        else:
            input_image.add_new([0x0008, 0x103e], 'LO', tag)
    return input_image


def get_and_set_bytetype(dicom_image, num_data):
    bytetype = dicom_image[0x0028, 0x0100].value
    if dicom_image.is_little_endian == False:
        del dicom_image.file_meta
        file_meta = FileMetaDataset()
        file_meta.FileMetaInformationGroupLength = 180
        file_meta.FileMetaInformationVersion = b'\x00\x01'
        file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.4'
        file_meta.MediaStorageSOPInstanceUID = '1.2.840.113619.2.80.2406827568.2282.1597905292.45'
        file_meta.TransferSyntaxUID = '1.2.840.10008.1.2.1'
        file_meta.ImplementationClassUID = '1.2.40.0.13.1.1'
        file_meta.ImplementationVersionName = 'dcm4che-3.3.7'
        dicom_image.file_meta = file_meta
        dicom_image.is_implicit_VR = False
        dicom_image.is_little_endian = True

    if bytetype == 16:
        dicom_image.PixelData = num_data.astype(np.uint16)
    elif bytetype == 8:
        dicom_image.PixelData = num_data.astype(np.uint8)
    else:
        raise Exception('invalid bytetype!')
    return dicom_image


def parse_dcm_files_add_tag(series, folder, type, name, multiple):
    if multiple == 'no':
        os.makedirs(os.path.join(folder, type), exist_ok=True)
        if name == '':
            tag_name = type
            nifti_name = type
        else:
            os.makedirs(os.path.join(folder, type, name), exist_ok=True)
            tag_name = type+'-'+name
            nifti_name = name
        for slice_idx in range(len(series) - 1):
            image_data = pd.dcmread(series[slice_idx + 1])
            image_data = add_AnImage_tag(image_data, tag_name)
            image_data = modify_series_uid(image_data, tag_name)
            image_data.save_as(os.path.join(folder, type, name,
                                            '{:04d}.dcm'.format(slice_idx + 1)))
        if type == 't1' or type == 't2':
            type = ''
        dcm_to_nii(os.path.join(folder, type), nifti_name)

    elif multiple == 'type':
        for series_id in range(len(series)):
            os.makedirs(os.path.join(folder, type+'_{:d}'.format(series_id + 1)))
            for slice_idx in range(len(series[series_id]) - 1):
                image_data = pd.dcmread(series[series_id][slice_idx + 1])
                image_data = add_AnImage_tag(image_data, type)
                image_data.save_as(os.path.join(folder,
                                                type+'_{:d}'.format(series_id + 1),
                                                '{:04d}.dcm'.format(slice_idx + 1)))


def dcm_to_nii(save_path, data_type, perfusion_type=''):
    if perfusion_type == '':
        save_name = data_type
    else:
        save_name = perfusion_type

    print(os.path.join(save_path, data_type, perfusion_type, save_name + '.nii.gz'))
    dicom2nifti.dicom_series_to_nifti(os.path.join(save_path, data_type, perfusion_type),
                                      os.path.join(save_path, data_type, perfusion_type, save_name + '.nii.gz'),
                                      reorient_nifti=True)
