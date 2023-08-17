import os
import pydicom
import numpy as np
import math
from . import AnImageDataSorterUtility as SorterUtil
import dicom2nifti
from .AnImageASLUtility import AnImageASLUtility


def create_path(target_path):
    if not os.path.exists(target_path):
        os.mkdir(target_path)


def make_nifti(pre_path, input_name):
    dicom2nifti.dicom_series_to_nifti(os.path.join(pre_path, input_name),
                                      os.path.join(pre_path, input_name, input_name + '.nii.gz'), reorient_nifti=True)


# 西门子1，5延迟处理
class AnImageDataSorterSiemens_UCLA:

    def __init__(self):
        self.intermediate_folder = ''
        self.seriesdelay = 0
        self.debugMode = False
        self.formatpack = []
        self.row = 0
        self.col = 0

    def parse_m0_from_raw_folder(self, seriesm0):
        create_path(os.path.join(self.intermediate_folder, 'asl', 'm0'))
        try:
            image_data = pydicom.dcmread(seriesm0[1])
        except:
            image_data = pydicom.dcmread([i for i in seriesm0.values()][1])
        # m0 = image_data.pixel_array
        self.row = image_data[0x0028, 0x0010].value
        self.col = image_data[0x0028, 0x0011].value
        # mask = np.zeros((self.row, self.col))
        # threshold = 0.15
        # mask[m0 < m0.max() * threshold] = 1
        slice_num = image_data[0x0019, 0x100A].value
        sn = math.ceil(np.sqrt(slice_num))
        dmrow = image_data[0x0028, 0x0010].value // sn
        siemensst = image_data[0x0018, 0x0050].value
        siemenssl = image_data[0x0020, 0x1041].value
        siemensipp = image_data[0x0020, 0x0032].value
        siemensiop = [1, 0, 0, 0, 1, 0]
        self.formatpack = [slice_num, sn, dmrow, siemensst, siemenssl, siemensipp, siemensiop]
        SorterUtil.demosaic(image_data, image_data.pixel_array, 'm0', self.intermediate_folder, self.formatpack)

    def parse_cbf_from_archive_folder(self, seriesmcbf, seriesatt, seriesacbv, seriescbf):
        # acbv_factor=1.65
        # att_factor=9
        # mcbf_factor=0.56
        acbv_factor = 1
        att_factor = 1
        mcbf_factor = 1
        # mcbf_factor=1
        if self.seriesdelay == 5:
            create_path(os.path.join(self.intermediate_folder, 'asl', 'mcbf'))
            create_path(os.path.join(self.intermediate_folder, 'asl', 'att'))
            create_path(os.path.join(self.intermediate_folder, 'asl', 'acbv'))

            test = pydicom.dcmread(seriesmcbf[1])
            studytime = test[0x0008, 0x0030].value
            for file_idx in range(len(seriesmcbf) - 1):
                image_data = pydicom.dcmread((seriesmcbf[file_idx + 1]))
                image_data[0x0008, 0x0030].value = studytime
                array = image_data.pixel_array * mcbf_factor
                image_data.PixelData = array.astype(np.uint16)
                image_data[0x0020, 0x0013].value = image_data[0x0020, 0x0013].value + 1
                image_data.add_new([0x0020, 0x1041], 'DS', self.formatpack[4] + file_idx * self.formatpack[3])
                self.formatpack[5][2] = self.formatpack[4] + file_idx * self.formatpack[3]
                image_data.add_new([0x0020, 0x0032], 'DS', self.formatpack[5])
                image_data.add_new([0x0020, 0x0037], 'DS', self.formatpack[6])
                if [0x0028, 0x1053] in image_data:
                    image_data[0x0028, 0x1053].value = 0.1
                else:
                    image_data.add_new([0x0028, 0x1053], 'DS', 0.1)
                image_data = SorterUtil.add_AnImage_tag(image_data, 'asl-mcbf')
                image_data = SorterUtil.modify_series_uid(image_data, 'asl-mcbf')
                image_data.save_as(os.path.join(self.intermediate_folder, 'asl', 'mcbf',
                                                '{:04d}.dcm'.format(int(image_data[0x0020, 0x0013].value))))

            make_nifti(os.path.join(self.intermediate_folder, 'asl'), 'mcbf')

            test = pydicom.dcmread(seriesatt[1])
            studytime = test[0x0008, 0x0030].value
            for file_idx in range(len(seriesatt) - 1):
                image_data = pydicom.dcmread((seriesatt[file_idx + 1]))
                image_data[0x0008, 0x0030].value = studytime
                array = image_data.pixel_array * att_factor
                image_data[0x0020, 0x0013].value = image_data[0x0020, 0x0013].value + 1
                image_data.add_new([0x0020, 0x1041], 'DS', self.formatpack[4] + file_idx * self.formatpack[3])
                self.formatpack[5][2] = self.formatpack[4] + file_idx * self.formatpack[3]
                image_data.add_new([0x0020, 0x0032], 'DS', self.formatpack[5])
                image_data.add_new([0x0020, 0x0037], 'DS', self.formatpack[6])
                if [0x0028, 0x1053] in image_data:
                    image_data[0x0028, 0x1053].value = 0.01
                else:
                    image_data.add_new([0x0028, 0x1053], 'DS', 0.01)
                image_data.PixelData = array.astype(np.uint16)
                image_data = SorterUtil.add_AnImage_tag(image_data, 'asl-att')
                image_data = SorterUtil.modify_series_uid(image_data, 'asl-att')
                image_data.save_as(os.path.join(self.intermediate_folder, 'asl', 'att',
                                                '{:04d}.dcm'.format(int(image_data[0x0020, 0x0013].value))))

            make_nifti(os.path.join(self.intermediate_folder, 'asl'), 'att')

            test = pydicom.dcmread(seriesacbv[1])
            studytime = test[0x0008, 0x0030].value
            for file_idx in range(len(seriesacbv) - 1):
                image_data = pydicom.dcmread((seriesacbv[file_idx + 1]))
                image_data[0x0008, 0x0030].value = studytime
                image_data[0x0020, 0x0013].value = image_data[0x0020, 0x0013].value + 1
                image_data.add_new([0x0020, 0x1041], 'DS', self.formatpack[4] + file_idx * self.formatpack[3])
                self.formatpack[5][2] = self.formatpack[4] + file_idx * self.formatpack[3]
                image_data.add_new([0x0020, 0x0032], 'DS', self.formatpack[5])
                image_data.add_new([0x0020, 0x0037], 'DS', self.formatpack[6])
                if [0x0028, 0x1053] in image_data:
                    image_data[0x0028, 0x1053].value = 0.001
                else:
                    image_data.add_new([0x0028, 0x1053], 'DS', 0.001)
                array = image_data.pixel_array * acbv_factor
                image_data.PixelData = array.astype(np.uint16)
                image_data = SorterUtil.add_AnImage_tag(image_data, 'asl-acbv')
                image_data = SorterUtil.modify_series_uid(image_data, 'asl-acbv')
                image_data.save_as(os.path.join(self.intermediate_folder, 'asl', 'acbv',
                                                '{:04d}.dcm'.format(int(image_data[0x0020, 0x0013].value))))

            make_nifti(os.path.join(self.intermediate_folder, 'asl'), 'acbv')

        for series_idx in range(self.seriesdelay):
            create_path(os.path.join(self.intermediate_folder, 'asl', 'cbf{:d}'.format(series_idx + 1)))
            if series_idx != 0:
                create_path(
                    os.path.join(self.intermediate_folder, 'asl', 'cbf{:d}-{:d}'.format(series_idx + 1, series_idx)))

            test = pydicom.dcmread(seriescbf[series_idx][1])
            studytime = test[0x0008, 0x0030].value
            series = np.zeros((len(seriescbf[series_idx]) - 1, test[0x0028, 0x0010].value, test[0x0028, 0x0011].value))
            for slice_idx in range(len(seriescbf[series_idx]) - 1):
                image_data = pydicom.dcmread(seriescbf[series_idx][slice_idx + 1])
                image_data[0x0008, 0x0030].value = studytime
                array = image_data.pixel_array
                array2 = image_data.pixel_array
                image_data[0x0020, 0x0013].value = image_data[0x0020, 0x0013].value + 1
                image_data.PixelData = array.astype(np.uint16)
                image_data.add_new([0x0020, 0x1041], 'DS', self.formatpack[4] + slice_idx * self.formatpack[3])
                self.formatpack[5][2] = self.formatpack[4] + slice_idx * self.formatpack[3]
                image_data.add_new([0x0020, 0x0032], 'DS', self.formatpack[5])
                image_data.add_new([0x0020, 0x0037], 'DS', self.formatpack[6])
                if [0x0028, 0x1053] in image_data:
                    image_data[0x0028, 0x1053].value = 0.1
                else:
                    image_data.add_new([0x0028, 0x1053], 'DS', 0.1)
                image_data = SorterUtil.add_AnImage_tag(image_data, 'asl-cbf{:d}'.format(series_idx + 1))
                image_data = SorterUtil.modify_series_uid(image_data, 'asl-cbf{:d}'.format(series_idx + 1))
                image_data.save_as(os.path.join(self.intermediate_folder, 'asl',
                                                'cbf{:d}'.format(series_idx + 1),
                                                '{:04d}.dcm'.format(int(image_data[0x0020, 0x0013].value))))
                series[image_data[0x0020, 0x0013].value - 1, :, :] = array2

                if series_idx != 0:
                    diffdata = array2 - series2[image_data[0x0020, 0x0013].value - 1, :, :]
                    image_data.remove_private_tags()
                    image_data.PixelData = diffdata.astype(np.uint16)
                    if [0x0028, 0x1053] in image_data:
                        image_data[0x0028, 0x1053].value = 0.1
                    else:
                        image_data.add_new([0x0028, 0x1053], 'DS', 0.1)
                    image_data = SorterUtil.add_AnImage_tag(image_data,
                                                            'asl-cbf{:d}-{:d}'.format(series_idx + 1, series_idx))
                    image_data = SorterUtil.modify_series_uid(image_data,
                                                              'asl-cbf{:d}-{:d}'.format(series_idx + 1, series_idx))
                    image_data.save_as(os.path.join(self.intermediate_folder, 'asl',
                                                    'cbf{:d}-{:d}'.format(series_idx + 1, series_idx),
                                                    '{:04d}.dcm'.format(int(image_data[0x0020, 0x0013].value))))

            series2 = series
            make_nifti(os.path.join(self.intermediate_folder, 'asl'), 'cbf{:d}'.format(series_idx + 1))

            if series_idx != 0:
                make_nifti(os.path.join(self.intermediate_folder, 'asl'),
                           'cbf{:d}-{:d}'.format(series_idx + 1, series_idx))

    def siemen_calc_yao(self, init_delay, seriesm0):
        scaling_pldcbf = 10
        scaling_wdatt = 100
        aslutil = AnImageASLUtility()
        aslutil.set_vendor('siemens')
        if self.seriesdelay == 5:
            pld_list = [2, 2, 2, 3, 3]
        elif self.seriesdelay == 1:
            pld_list = [10]
        threshold = 0.15
        raw_array = np.zeros((self.row, self.col, len(seriesm0) - 1))
        raw_list = list(seriesm0)
        for i in range(len(raw_list) - 1):
            ds = pydicom.dcmread(seriesm0[raw_list[i + 1]])
            acquisition_idx = ds[0x0020, 0x0012].value - 1
            raw_array[:, :, acquisition_idx] = ds.pixel_array

            # 创建raw_data, 这里可以改成set_raw_data(矩阵）
        raw_array = np.expand_dims(raw_array, axis=2)
        aslutil.set_raw_data(raw_array)

        # 设定参数、内部生成各图片
        aslutil.set_delay_list(init_delay)
        aslutil.set_measure_list(pld_list)

        aslutil.gen_m0()
        aslutil.gen_mask(threshold)
        aslutil.gen_plds()
        if self.seriesdelay == 5:
            aslutil.gen_wd()
            aslutil.gen_att_mcbf_fitting()  # 这个时间长，会显示当前的层序号
            aslutil.gen_cbfs('corrected')  # 这里可以用simple或corrected；simple是将ATT设定为0，跟单延迟一样
            aslutil.gen_acbv()
        elif self.seriesdelay == 1:
            aslutil.gen_cbfs('simple')  # 这里可以用simple或corrected；simple是将ATT设定为0，跟单延迟一样

        # 保存各图象
        if self.debugMode:
            img_plds = aslutil.get_plds()
            for idx in range(self.seriesdelay):
                out_array = img_plds[:, :, :, idx] * scaling_pldcbf
                out_array = np.squeeze(out_array)
                if not os.path.exists(
                        os.path.join(self.intermediate_folder, 'asl', 'pld{:d}'.format(idx + 1))):
                    os.mkdir(os.path.join(self.intermediate_folder, 'asl', 'pld{:d}'.format(idx + 1)))
                SorterUtil.demosaic(ds, out_array, 'pld{:d}'.format(idx + 1), self.intermediate_folder, self.formatpack)

        if self.seriesdelay == 5:
            if self.debugMode == True:
                out_wd = aslutil.get_wd() * scaling_wdatt
                if not os.path.exists(
                        os.path.join(self.intermediate_folder, 'asl', 'wd')):
                    os.mkdir(os.path.join(self.intermediate_folder, 'asl', 'wd'))
                SorterUtil.demosaic(ds, out_wd, 'wd', self.intermediate_folder, self.formatpack)

            out_att = aslutil.get_att() * scaling_wdatt * 10
            if [0x0028, 0x1053] in ds:
                ds[0x0028, 0x1053].value = 0.001
            else:
                ds.add_new([0x0028, 0x1053], 'DS', 0.001)
            if not os.path.exists(
                    os.path.join(self.intermediate_folder, 'asl', 'att')):
                os.mkdir(os.path.join(self.intermediate_folder, 'asl', 'att'))
            SorterUtil.demosaic(ds, out_att, 'att', self.intermediate_folder, self.formatpack)

            out_mcbf = aslutil.get_mcbf() * scaling_pldcbf
            if [0x0028, 0x1053] in ds:
                ds[0x0028, 0x1053].value = 0.1
            else:
                ds.add_new([0x0028, 0x1053], 'DS', 0.1)
            if not os.path.exists(
                    os.path.join(self.intermediate_folder, 'asl', 'mcbf')):
                os.mkdir(os.path.join(self.intermediate_folder, 'asl', 'mcbf'))
            SorterUtil.demosaic(ds, out_mcbf, 'mcbf', self.intermediate_folder, self.formatpack)

            out_acbv = aslutil.get_acbv() * scaling_pldcbf / 60
            if [0x0028, 0x1053] in ds:
                ds[0x0028, 0x1053].value = 0.001
            else:
                ds.add_new([0x0028, 0x1053], 'DS', 0.001)
            if not os.path.exists(
                    os.path.join(self.intermediate_folder, 'asl', 'acbv')):
                os.mkdir(os.path.join(self.intermediate_folder, 'asl', 'acbv'))
            SorterUtil.demosaic(ds, out_acbv, 'acbv', self.intermediate_folder, self.formatpack)

        img_cbfs = aslutil.get_cbfs()
        for idx in range(self.seriesdelay):
            out_cbfs = img_cbfs[:, :, :, idx] * scaling_pldcbf
            if [0x0028, 0x1053] in ds:
                ds[0x0028, 0x1053].value = 0.1
            else:
                ds.add_new([0x0028, 0x1053], 'DS', 0.1)
            if not os.path.exists(
                    os.path.join(self.intermediate_folder, 'asl', 'cbf{:d}'.format(idx + 1))):
                os.mkdir(os.path.join(self.intermediate_folder, 'asl', 'cbf{:d}'.format(idx + 1)))
            SorterUtil.demosaic(ds, out_cbfs, 'cbf{:d}'.format(idx + 1), self.intermediate_folder, self.formatpack)
            if idx != 0:
                out_cbfd = (img_cbfs[:, :, :, idx] - img_cbfs[:, :, :, idx - 1]) * scaling_pldcbf
                # mask=aslutil.get_mask()[:,:,:,idx-1]
                # if np.min(out_cbfd)<0:
                #     modify = (int(abs(np.min(out_cbfd))) // 10 + 1) * 10
                #     out_cbfd[mask==1]+=modify
                #     if [0x0028,0x1052] in ds:
                #         ds[0x0028,0x1052].value=-modify
                #     else:
                #         ds.add_new([0x0028,0x1052], 'DS', -modify)
                if not os.path.exists(
                        os.path.join(self.intermediate_folder, 'asl', 'cbf{:d}-{:d}'.format(idx + 1, idx))):
                    os.mkdir(os.path.join(self.intermediate_folder, 'asl', 'cbf{:d}-{:d}'.format(idx + 1, idx)))
                SorterUtil.demosaic(ds, out_cbfd, 'cbf{:d}-{:d}'.format(idx + 1, idx), self.intermediate_folder,
                                    self.formatpack)

    def parse_pasl_from_archive_folder(self, seriesm0):
        if not os.path.exists(os.path.join(self.intermediate_folder, 'asl', 'mcbf')):
            os.mkdir(os.path.join(self.intermediate_folder, 'asl', 'mcbf'))
        if not os.path.exists(os.path.join(self.intermediate_folder, 'asl', 'att')):
            os.mkdir(os.path.join(self.intermediate_folder, 'asl', 'att'))
        if not os.path.exists(os.path.join(self.intermediate_folder, 'asl', 'm0')):
            os.mkdir(os.path.join(self.intermediate_folder, 'asl', 'm0'))

        seriesm0.pop(0)
        for file_idx in list(seriesm0.values()):
            image_data = pydicom.dcmread(file_idx)
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
            if image_data[0x0020, 0x4000].value == 'M0 Image':
                SorterUtil.demosaic(image_data, image_data.pixel_array, 'm0', self.intermediate_folder,
                                    self.formatpack)
            elif image_data[0x0020, 0x4000].value == 'relCBF':
                SorterUtil.demosaic(image_data, image_data.pixel_array, 'mcbf',
                                    self.intermediate_folder,
                                    self.formatpack)
            elif image_data[0x0020, 0x4000].value == 'Bolus Arrival Time (BAT) Image':
                if [0x0028, 0x1053] in image_data:
                    image_data[0x0028, 0x1053].value = 0.001
                else:
                    image_data.add_new([0x0028, 0x1053], 'DS', 0.001)
                SorterUtil.demosaic(image_data, image_data.pixel_array, 'att',
                                    self.intermediate_folder,
                                    self.formatpack)

    def siemens_data_check(self, seriesm0, seriesacbv, seriesatt, seriesmcbf, seriescbf):
        try:
            image_data = pydicom.dcmread(seriesm0[1], stop_before_pixels=True)
        except:
            image_data = pydicom.dcmread([i for i in seriesm0.values()][1], stop_before_pixels=True)
        try:
            slice_num = image_data[0x0019, 0x100A].value
        except:
            raise Exception('slice number not found')
        if self.seriesdelay == 5:
            if len(seriesmcbf) == slice_num + 1:
                for slice_idx in range(slice_num + 1):
                    if slice_idx not in seriesmcbf:
                        raise Exception('missing mcbf slice ' + str(slice_idx))
            else:
                raise Exception('missing mcbf slice')
            if len(seriesatt) == slice_num + 1:
                for slice_idx in range(slice_num + 1):
                    if slice_idx not in seriesatt:
                        raise Exception('missing att slice ' + str(slice_idx))
            else:
                raise Exception('missing att slice')
            if len(seriesacbv) == slice_num + 1:
                for slice_idx in range(slice_num + 1):
                    if slice_idx not in seriesacbv:
                        raise Exception('missing acbv slice ' + str(slice_idx))
            else:
                raise Exception('missing acbv slice')

        if len(seriescbf) != self.seriesdelay:
            raise Exception('number of cbf not equal to series delay')

        for series_idx in range(len(seriescbf)):
            if len(seriescbf[series_idx]) == slice_num + 1:
                for slice_idx in range(slice_num + 1):
                    if slice_idx not in seriescbf[series_idx]:
                        raise Exception('missing cbf slice ' + str(slice_idx))
            else:
                raise Exception('missing slice?')

    def Sorter(self, intermediate_folder, seriesm0, seriesdelay, init_delay=[], seriescbf={}, seriesacbv=[],
               seriesatt=[], seriesmcbf=[], debugMode=False):
        self.intermediate_folder = intermediate_folder
        self.seriesdelay = seriesdelay
        self.debugMode = debugMode
        if not os.path.exists(os.path.join(self.intermediate_folder, 'asl')):
            os.mkdir(os.path.join(self.intermediate_folder, 'asl'))

        if self.seriesdelay == 2:
            self.parse_pasl_from_archive_folder(seriesm0)
        elif (self.seriesdelay == 5 and seriesacbv and seriesatt and seriesmcbf and seriescbf) \
                or (self.seriesdelay == 1 and seriescbf):
            self.siemens_data_check(seriesm0, seriesacbv, seriesatt, seriesmcbf, seriescbf)
            self.parse_m0_from_raw_folder(seriesm0)
            self.parse_cbf_from_archive_folder(seriesmcbf, seriesatt, seriesacbv, seriescbf)
        else:
            self.parse_m0_from_raw_folder(seriesm0)
            self.siemen_calc_yao(init_delay, seriesm0)
