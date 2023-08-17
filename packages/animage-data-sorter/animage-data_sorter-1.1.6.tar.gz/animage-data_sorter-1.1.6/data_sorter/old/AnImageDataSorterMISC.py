import os
import pydicom as pd
from . import AnImageDCMUtility as DCMUtil


# adc
def parse_adc_from_archive_folder(intermediate_folder, series):
    os.makedirs(os.path.join(intermediate_folder, 'dwi'), exist_ok=True)
    os.makedirs(os.path.join(intermediate_folder, 'dwi', 'adc'), exist_ok=True)
    keys = sorted(list(series[0].keys()))
    for slice_idx in range(len(series[0]) - 1):
        image_data = pd.dcmread(series[0][keys[slice_idx + 1]])
        DCMUtil.copy_dcm_slice(image_data, intermediate_folder, 'dwi', 'adc', slice_idx,
                               override_series_desc=True)
    DCMUtil.dcm_to_nii(intermediate_folder, 'dwi', 'adc')


# dwi
def parse_dwi_from_archive_folder(intermediate_folder, series, data_type):
    os.makedirs(os.path.join(intermediate_folder, 'dwi'), exist_ok=True)
    nifti_flags = [['b0', False], ['trace1', False], ['trace2', False], ['trace3', False]]
    keys = sorted(list(series[0].keys()))
    for slice_idx in range(len(series[0]) - 1):
        image_data = pd.dcmread(series[0][keys[slice_idx + 1]])
        if data_type == 'GE MEDICAL SYSTEMS':
            b = image_data[0x0043, 0x1039]
            if b[0] == 0:
                series_type = 'b0'
                nifti_flags[0][1] = True
            elif b[0] == 1000:
                series_type = 'trace1'
                nifti_flags[1][1] = True
            else:
                raise Exception("tracew error")
        elif data_type == "Philips":
            b = image_data[0x0008, 0x103E].value.lower()
            if 'b1000' in b:
                series_type = 'trace1'
                nifti_flags[1][1] = True
        elif data_type == 'SIEMENS':
            b = image_data[0x0018, 0x0024].value.lower()
            if 'b10000' in b:
                series_type = 'trace3'
                nifti_flags[3][1] = True
            elif 'b5000' in b:
                series_type = 'trace2'
                nifti_flags[2][1] = True
            elif 'b1000' in b:
                series_type = 'trace1'
                nifti_flags[1][1] = True
            elif 'b0' in b:
                series_type = 'b0'
                nifti_flags[0][1] = True

        os.makedirs(os.path.join(intermediate_folder, 'dwi', series_type), exist_ok=True)
        DCMUtil.copy_dcm_slice(image_data, intermediate_folder, 'dwi', series_type, slice_idx,
                               override_series_desc=True)

    for nifti_idx in range(4):
        if nifti_flags[nifti_idx][1]:
            DCMUtil.dcm_to_nii(intermediate_folder, 'dwi', '{}'.format(nifti_flags[nifti_idx][0]))


def parse_t1_from_archive_folder(intermediate_folder, series):
    os.makedirs(os.path.join(intermediate_folder, 'struct'), exist_ok=True)
    os.makedirs(os.path.join(intermediate_folder, 'struct', 't1'), exist_ok=True)
    keys = sorted(list(series[0].keys()))
    for slice_idx in range(len(series[0]) - 1):
        image_data = pd.dcmread(series[0][keys[slice_idx + 1]])
        DCMUtil.copy_dcm_slice(image_data, intermediate_folder, 'struct', 't1', slice_idx)
    DCMUtil.dcm_to_nii(intermediate_folder, 'struct', 't1')


def parse_t2_from_archive_folder(intermediate_folder, seriest2):
    os.makedirs(os.path.join(intermediate_folder, 'struct'), exist_ok=True)
    for series_id in range(len(seriest2)):
        t2_name = 't2_{:d}'.format(series_id + 1)
        os.makedirs(os.path.join(intermediate_folder, 'struct', t2_name), exist_ok=True)
        for slice_idx in range(len(seriest2[series_id]) - 1):
            image_data = pd.dcmread(seriest2[series_id][slice_idx + 1])
            DCMUtil.copy_dcm_slice(image_data, intermediate_folder, 'struct', t2_name, slice_idx)
        DCMUtil.dcm_to_nii(intermediate_folder, 'struct', t2_name)


# fdg-suv
def parse_suv_from_archive_folder(intermediate_folder, series):
    os.makedirs(os.path.join(intermediate_folder, 'fdg'), exist_ok=True)
    os.makedirs(os.path.join(intermediate_folder, 'fdg', 'suv'), exist_ok=True)
    keys = sorted(list(series[0].keys()))
    for slice_idx in range(len(series[0]) - 1):
        image_data = pd.dcmread(series[0][keys[slice_idx + 1]])
        DCMUtil.copy_dcm_slice(image_data, intermediate_folder, 'fdg', 'suv', slice_idx,
                               override_series_desc=True)
