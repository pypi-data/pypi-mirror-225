"""
修改了-modify（ReScaleIntercept)为永久是-5，数据本身不稳定
读取的数据的负数都会变成0

21年06月29日
姚泽山
"""

import pydicom
import os
import numpy as np
from .AnImageASLUtility import AnImageASLUtility
from . import AnImageDCMUtility as DCMUtil


class AnImageDataSorterGE7:  # FIXME：需要整理代码，整体按照行号227-260的格式修改 [姚 06-14]
    def __init__(self):
        self.ref_img = ''
        self.intr_fldr = ''
        self.n = 0
        self.mask = []
        self.cbf_ncorr = []
        self.raw_data_pwpd = []
        self.st = 0
        self.sl = 0
        self.ipp = []
        self.iop = []
        self.dmrow = 0
        self.folder_suffix = ''
        self.series_CORR = []
        self.series_STAN = []
        self.label_dur = []
        self.delay_time = []
        self.aslutil = AnImageASLUtility()

    def set_up_aslutil(self):
        image_data = pydicom.dcmread(self.ref_img)
        self.aslutil.set_vendor('ge')
        self.aslutil.set_series_type('7delay')
        self.aslutil.set_duration_list(self.label_dur)
        self.aslutil.set_delay_list(self.delay_time)
        self.aslutil.set_measure_list([1] * 7)
        self.aslutil.set_scan_parameter(image_data)

        if [0x0021, 0x104f] in image_data:
            self.n = image_data[0x0021, 0x104f].value
        else:
            raise Exception('slice number not find, will fix later')

        self.dmrow = image_data[0x0028, 0x0010].value
        self.st = image_data[0x0018, 0x0050].value
        self.sl = image_data[0x0020, 0x1041].value
        self.ipp = image_data[0x0020, 0x0032].value
        self.iop = image_data[0x0020, 0x0037].value

    def parse_m0_from_raw_folder(self, seriesm0):
        self.raw_data_pwpd = np.zeros((self.dmrow, self.dmrow, self.n, 9))
        for series_idx in range(9):
            for slice_idx in range(self.n):
                image_data = pydicom.dcmread(seriesm0[0][self.n * series_idx + slice_idx + 1])
                self.raw_data_pwpd[:, :, slice_idx, series_idx] = image_data.pixel_array

        self.raw_data_pwpd[self.raw_data_pwpd < 0] = 0
        self.aslutil.set_raw_data(self.raw_data_pwpd)
        self.aslutil.gen_m0()
        self.aslutil.gen_mask()

        output_array = self.aslutil.get_m0()[:, :, :, 0]
        os.makedirs(os.path.join(self.intr_fldr, 'asl-' + self.folder_suffix, 'm0'), exist_ok=True)
        series_param = [1, 1, 0]
        DCMUtil.create_dcm_series(output_array, self.ref_img, self.intr_fldr,
                                  'asl', 'm0', series_param, self.folder_suffix)
        DCMUtil.dcm_to_nii(self.intr_fldr, 'asl-' + self.folder_suffix, 'm0')

    def ge_calc_yao(self, seriesatt):
        att_array = 0 * self.aslutil.get_m0()[:, :, :, 0]
        for slice_idx in range(len(seriesatt[0]) - 1):
            image_data = pydicom.dcmread(seriesatt[0][slice_idx + 1])
            att_array[:, :, slice_idx] = image_data.pixel_array.astype(np.float32) / 1000

        self.aslutil.set_att(att_array)
        self.aslutil.gen_plds()
        self.aslutil.gen_cbfs_ge7delay(transit_correction=False)
        self.cbf_ncorr = self.aslutil.get_mcbf()
        self.aslutil.gen_cbfs_ge7delay(transit_correction=True)
        self.aslutil.gen_acbv()

    def generate_scbf(self):
        if self.series_CORR:
            if len(self.series_CORR[0]) > 100:
                output_array = np.zeros((self.dmrow, self.dmrow, self.n, 7))
                for series_idx in range(7):
                    for slice_idx in range(self.n):
                        image_data = pydicom.dcmread(self.series_CORR[0][self.n * series_idx + slice_idx + 1])
                        output_array[:, :, slice_idx, series_idx] = image_data.pixel_array
            else:
                output_array = self.aslutil.get_cbfs()
        else:
            output_array = self.aslutil.get_cbfs()
        output_array[output_array < 0] = 0

        for file_idx in range(7):
            os.makedirs(os.path.join(self.intr_fldr, 'asl-' + self.folder_suffix,
                                     'cbf{:d}'.format(file_idx+1)), exist_ok=True)
            series_param = [10 + file_idx + 1, 10, 0]
            DCMUtil.create_dcm_series(output_array[:, :, :, file_idx], self.ref_img, self.intr_fldr, 'asl',
                                      'cbf{:d}'.format(file_idx+1), series_param, self.folder_suffix)
            DCMUtil.dcm_to_nii(self.intr_fldr, 'asl-' + self.folder_suffix,
                               'cbf{:d}'.format(file_idx+1))

    def generate_mcbf_noncorr(self):
        target_files = ["mcbf", "att", "acbv", "nc_cbf"]
        scaling = [10, 1000, 1000, 10]

        for file_idx in range(len(target_files)):
            os.makedirs(os.path.join(self.intr_fldr, 'asl-' + self.folder_suffix,
                                     '{}'.format(target_files[file_idx])), exist_ok=True)
            if file_idx == 0:
                output_array = self._check_series_CORR()
            elif file_idx == 1:
                output_array = self.aslutil.get_att()
            elif file_idx == 2:
                output_array = self.aslutil.get_acbv()
            elif file_idx == 3:
                output_array = self._check_series_STAN()

            output_array[output_array < 0] = 0
            series_param = [20 + file_idx + 1, scaling[file_idx], 0]
            DCMUtil.create_dcm_series(output_array, self.ref_img, self.intr_fldr, 'asl',
                                      '{}'.format(target_files[file_idx]), series_param, self.folder_suffix)
            DCMUtil.dcm_to_nii(self.intr_fldr, 'asl-' + self.folder_suffix,
                               '{}'.format(target_files[file_idx]))

    def _check_series_CORR(self):
        if self.series_CORR:
            if 0 < len(self.series_CORR[0]) < 100:
                output_array = np.zeros((self.dmrow, self.dmrow, self.n))
                for slice_idx in range(self.n):
                    image_data = pydicom.dcmread(self.series_CORR[0][slice_idx + 1])
                    output_array[:, :, slice_idx] = image_data.pixel_array
            else:
                output_array = self.aslutil.get_mcbf()
        else:
            output_array = self.aslutil.get_mcbf()
        # output_array = self.aslutil.get_mcbf()
        return output_array

    def _check_series_STAN(self):
        if self.series_STAN:
            if 0 < len(self.series_STAN[0]) < 100:
                output_array = np.zeros((self.dmrow, self.dmrow, self.n))
                for slice_idx in range(self.n):
                    image_data = pydicom.dcmread(self.series_STAN[0][slice_idx + 1])
                    output_array[:, :, slice_idx] = image_data.pixel_array
            else:
                output_array = self.cbf_ncorr
        else:
            output_array = self.cbf_ncorr
        return output_array

        # imgs = aslutil.get_mcbf()
        # imgs[imgs < 0] = 0  # FIXME: 额外加的，可能对数值好一些，需要查看
        # self.mcbf = imgs
        # modify = 0
        # mcbf_factor = 1
        # if np.min(imgs) < 0:
        #     if (int(abs(np.min(imgs))) // 10 + 1) * 10 > modify:
        #         modify = (int(abs(np.min(imgs))) // 10 + 1) * 10
        # imgs[self.mask[:, :, :, 0] == 0] = -modify * mcbf_factor
        # for slice_idx in range(imgs.shape[2]):
        #     img_mcbf = (imgs[:, :, slice_idx] + modify) * mcbf_factor
        #     if [0x0028, 0x1052] in test:
        #         test[0x0028, 0x1052].value = -modify * mcbf_factor
        #     else:
        #         test.add_new([0x0028, 0x1052], 'DS', -modify * mcbf_factor)
        #     # if [0x0028, 0x1053] in test:
        #     #     test[0x0028, 0x1053].value = 0.1
        #     # else:
        #     #     test.add_new([0x0028, 0x1053], 'DS', 0.1)
        #     test[0x0020, 0x0013].value = slice_idx + 1
        #     test[0x0020, 0x1041].value = self.sl + slice_idx * self.st
        #     self.ipp[2] = '{:.4f}'.format(test[0x0020, 0x1041].value)
        #     test[0x0020, 0x0032].value = self.ipp
        #     test[0x0020, 0x0037].value = self.iop
        #     test = SorterUtil.modify_series_uid(test, 'asl-mcbf')
        #     test = SorterUtil.add_AnImage_tag(test, 'asl-mcbf')
        #     test = SorterUtil.get_and_set_bytetype(test, img_mcbf)
        #     test.save_as(os.path.join(self.intr_fldr, 'asl-' + i,
        #                               'mcbf',
        #                               '{:04d}.dcm'.format(slice_idx + 1)))
        #
        # make_nifti(os.path.join(self.intr_fldr, 'asl-' + i), 'mcbf')

    def Sorter(self, intermediate_folder, folder_suffix, seriesdic, delay_time, label_dur):
        # print(json.dumps(seriesdic, sort_keys=True, indent=4))
        if "ATT" in seriesdic and "RAW" in seriesdic:
            os.makedirs(os.path.join(self.intr_fldr, 'asl-' + folder_suffix), exist_ok=True)
            self.intr_fldr = intermediate_folder
            self.folder_suffix = folder_suffix
            self.ref_img = seriesdic["RAW"][0][1]

            self.label_dur = label_dur
            self.delay_time = delay_time

            self.set_up_aslutil()
            self.parse_m0_from_raw_folder(seriesdic['RAW'])
            self.ge_calc_yao(seriesdic["ATT"])
            if "CORR_CBF" in seriesdic.keys():
                self.series_CORR = seriesdic["CORR_CBF"]
            if "STAN_CBF" in seriesdic.keys():
                self.series_STAN= seriesdic["STAN_CBF"]

            self.generate_scbf()
            self.generate_mcbf_noncorr()

        else:
            raise Exception('ATT and/or RAW instance not found!')
