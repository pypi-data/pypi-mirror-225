import os
import time

import SimpleITK as sitk
import nibabel
import numpy as np
import pydicom
from nibabel.nicom import csareader
from pydicom._storage_sopclass_uids import SecondaryCaptureImageStorage
from pydicom.uid import generate_uid

'''
本文件为测试demo
'''

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
    image.SetMetaData('0028|0030', '\\'.join([str(i) for i in ref.PixelSpacing]))
    image.SetMetaData('0018|2010', '\\'.join([str(i) for i in ref.PixelSpacing]))
    image.SetMetaData('0018|0088', str(ref.SpacingBetweenSlices))
    # image.SetMetaData('0028|1052', str(-1))
    # image.SetMetaData('0028|1053', str(0.1))
    return image


def demosaic(mosaic_mat: np.ndarray, slice_num: int):
    n_rows = n_cols = int(np.ceil(np.sqrt(slice_num)))
    img_width, img_height = mosaic_mat.shape[1], mosaic_mat.shape[0]
    img_width //= n_cols
    img_height //= n_rows

    _3d_mat = np.zeros((img_height, img_width, slice_num))
    for i in range(slice_num):
        x_start = i % n_cols * img_width
        y_start = i // n_cols * img_height
        _3d_mat[::,:,i] = mosaic_mat[y_start:y_start+img_height, x_start:x_start+img_width]

    return _3d_mat


def nii_flipX(img: np.ndarray, affine: np.ndarray):
    s = affine[:3,:3]

    # 翻转后的偏移量
    v = [img.shape[0]-1, 0, 0, 1]
    v = np.matmul(affine, v)

    # 翻转后的方向
    mFlipZ = np.eye(3)
    mFlipZ[0,0] *= -1
    s = np.matmul(s, mFlipZ)

    # 切片方向与偏移量组合在一起
    s = np.c_[s, v[:3]]
    s = np.r_[s, [affine[3]]]
    return s

def nii_flipY(img: np.ndarray, affine: np.ndarray):
    s = affine[:3,:3]

    # 翻转后的偏移量
    v = [0, img.shape[1]-1, 0, 1]
    v = np.matmul(affine, v)

    # 翻转后的方向
    mFlipY = np.eye(3)
    mFlipY[1,1] *= -1
    s = np.matmul(s, mFlipY)

    # 切片方向与偏移量组合在一起
    s = np.c_[s, v[:3]]
    s = np.r_[s, [affine[3]]]
    return s

def nii_flipZ(img: np.ndarray, affine: np.ndarray):
    s = affine[:3,:3]

    # 翻转后的偏移量
    v = [0, 0, img.shape[2]-1, 1]
    v = np.matmul(affine, v)

    # 翻转后的方向
    mFlipZ = np.eye(3)
    mFlipZ[2,2] *= -1
    s = np.matmul(s, mFlipZ)

    # 切片方向与偏移量组合在一起
    s = np.c_[s, v[:3]]
    s = np.r_[s, [affine[3]]]
    return s


def siemens_affine(dataset):
    # 原点与方向
    orientation = dataset[0x0020, 0x0037].value
    position = dataset[0x0020, 0x0032].value

    # 分辨率
    z_space = dataset[0x0018, 0x0050].value
    x_space, y_space = dataset[0x0028, 0x0030].value

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


def siemens_mosaic_affine(dataset):
    m = siemens_affine(dataset)

    orientation = dataset[0x0020, 0x0037].value


    # mosaic图像尺寸
    row = dataset[0x0028, 0x0010].value
    col = dataset[0x0028, 0x0011].value

    _3d_slice_img = demosaic(dataset.pixel_array, slice_num)

    # 读取西门子CSA头
    csa_image = csareader.get_csa_header(dataset, 'image')
    sliceNormV = csa_image['tags']['SliceNormalVector']['items']

    factor_x = factor_y = (row - (row / int(np.ceil(np.sqrt(slice_num))))) / 2.0

    m[:,3] += m[:,0] * factor_x + m[:,1] * factor_y
    m[:2] *= -1

    slice_norm_mat = np.zeros((3, 3), dtype=float)
    slice_norm_mat[:, 0] = orientation[:3]
    slice_norm_mat[:, 1] = orientation[3:]
    slice_norm_mat[:, 2] = sliceNormV

    # 法向量相反，Z序需要翻转
    if np.linalg.det(slice_norm_mat) < 0:
        print('reversed')
        Q = np.eye(4)
        Q[2, 2] *= -1
        m = np.matmul(m, Q)



    return _3d_slice_img, m

def siemens_2d_affine(dataset):
    m = siemens_affine(dataset)
    m[:2] *= -1

    return None, m

def g_slice_location(first_slice_location, z_space, slice_num):
    cur_slice_location = first_slice_location
    for i in range(slice_num):
        yield cur_slice_location
        cur_slice_location += z_space

def g_position(m, slice_num):
    for i in range(slice_num):
        yield m[:3, 3] + i * m[:3, 2]

if __name__ == '__main__':
    dcm_fn = r'D:\WorkDir\cloud\dicom_normalization\dicom_demo\Mosaic\reverse\452.dcm'
    # dcm_fn = r'.\dicom_demo\Mosaic\reverse\M0\452.dcm'

    # dcm_fn = os.path.join(dcm_fn, '3179cb6b-b7e1e17c-6daa556e-fba45da6-86b5dbc0.dcm')

    dataset = pydicom.read_file(dcm_fn)
    slice_num = dataset[0x0019, 0x100a].value
    if slice_num > 0:
        _3d_img, affine = siemens_mosaic_affine(dataset)
        affine[:2] *= -1
        first_slice_location = dataset[0x0020, 0x1041].value
        normal_direction = affine[2,2] / abs(affine[2,2])
        ori = dataset[0x0020, 0x0037].value
        z_space = dataset[0x0018, 0x0050].value

        # plt.imshow(_3D_to_2D(_3d_img, 6, 6))
        # plt.show()

        writer = sitk.ImageFileWriter()
        writer.KeepOriginalImageUIDOn()

        i = 0
        start = time.time()
        for position, slice_location in zip(g_position(affine, _3d_img.shape[2]), g_slice_location(first_slice_location, normal_direction * z_space, _3d_img.shape[2])):



            image = create_dicom_forsitk(_3d_img[:, :, i], position, ori, slice_location, dataset)
            image.SetMetaData('0020|0013', str(i + 1))
            writer.SetFileName(os.path.join(r'D:\WorkDir\cloud\dicom_normalization\dicom_demo\Mosaic\reverse\split', 'MR%06d.dcm' % (i)))
            writer.Execute(image)

            i+=1
        print(time.time() - start)

    else:
        _3d_img, affine = siemens_2d_affine(dataset)

    _3d_img = _3d_img.swapaxes(0, 1)
    nibabel.Nifti1Image(_3d_img, affine).to_filename(r'D:\WorkDir\cloud\dicom_normalization\dicom_demo\Mosaic\reverse\a.nii.gz')

    #
    # print(nibabel.aff2axcodes(affine))
    # print(affine)



