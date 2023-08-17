"""
处理动脉自旋标记图像的矩阵用的工具包
兼容西门子多延迟、通用电气单延迟、飞利浦单延迟数据
可以计算GE7延迟的mCBF、corr-mCBF、CBF1-7、corr-CBF1-7的功能，需要导入eASL：raw和eASL：transit-delay
准确性：mCBF和CBF1-7没问题，corr-mCBF有点散但是拟合没问题，corr-CBF1-7猜的，建议不要用，用GE自己生成的

TODO：
加降噪功能、加头动矫正功能
王老师序列单延迟输出的确认、完善飞利浦的CBF计算、
完善ATT-mapping以及王老师序列生成每一个CBF的对比

版本：3.0
日期：2021-06-07
作者：姚泽山

2.0 -> 3.0: 增加计算通用电气7延迟的mCBF、CBF1~7
1.0 -> 2.0: 增加计算飞利浦和通用电气的CBF数据，以及Masking参数；现在需要输入核磁厂家信息
"""

import os
import numpy as np
import pydicom as pd
from scipy.optimize import curve_fit


def get_balloon_model_parameters():
    pul_dur = 1.5  # pulse duration
    blc = 0.9  # Blood Tissue Coefficient, lambda
    tag = 0.73  # Tagging Efficiency
    r1a = 0.61
    return pul_dur, blc, tag, r1a


def func(x, att, cbf):
    pul_dur, blc, tag, r1a = get_balloon_model_parameters()
    y = cbf * tag / 3000 / blc / r1a * np.piecewise(x, [x < att, x >= att],
                                                    [lambda x: np.exp(-att * r1a) - np.exp(-r1a * (pul_dur + x)),
                                                     lambda x: np.exp(-x * r1a) - np.exp(-r1a * (pul_dur + x))])
    return y


def binary_search(arr, x):
    n = len(arr)
    if x > arr[-1]:
        return n
    left, right = 0, n - 1
    while left <= right:
        mid = (left + right) // 2
        if x <= arr[mid]:
            right = mid - 1
        else:
            left = mid + 1
    return left


class AnImageASLUtility:

    def __init__(self, vendor=[], series_type=[]):
        self.vendor = vendor
        self.series_type = series_type
        self.raw_data = []
        self.measure_list = []
        self.duration_list = []
        self.delay_list = []
        self.threshold = []

        self.img_m0 = []
        self.mask = []

        self.img_plds = []
        self.img_wd = []
        self.img_att = []
        self.img_cbfs = []
        self.img_diff_cbfs = []
        self.img_mcbf = []
        self.img_acbv = []

        self.number_of_averages = []
        self.magnetic_field_strength = []
        self.labeling_duration = []

        # TODO 额外加上的系数；只是不知为什么跟小彭输出有差异的部分，我猜是平滑导致的
        self.extra_pld_factor = 0.92
        self.extra_wds_factor = 0.90
        self.extra_att_factor = 0.90
        self.extra_cbf_factor = 0.88
        self.extra_cbv_factor = 1.80

    def set_vendor(self, vendor):
        self.vendor = vendor

    def set_series_type(self, series_type):
        self.series_type = series_type

    def set_scan_parameter(self, pydicom_image):
        img = pydicom_image
        self.number_of_averages = img[0x0018, 0x0083].value if [0x0018, 0x0083] in img else 1
        self.magnetic_field_strength = img[0x0018, 0x0087].value if [0x0018, 0x0087] in img else 1
        try:
            self.labeling_duration = img[0x0043, 0x10A5].value / 1000
        except:
            self.labeling_duration = 1.5

    def set_duration_list(self, input_list):
        self.duration_list = input_list

    def get_duration_list(self):
        return self.duration_list

    def set_delay_list(self, *argv):
        if len(argv) == 1:
            self.delay_list = argv[0]

        elif len(argv) == 3:
            init_delay = argv[0]
            delay_num = argv[1]
            delay_interval = argv[2]
            delays = []
            for delay_idx in range(delay_num):
                delays.append(init_delay + delay_idx * delay_interval)
            self.delay_list = delays

    def get_delay_list(self):
        return self.delay_list

    def set_measure_list(self, measure_list):
        self.measure_list = measure_list

    def get_measure_list(self):
        return self.measure_list

    def set_raw_data(self, input_data):
        self.raw_data = input_data

    def get_raw_data(self):
        return self.raw_data

    def data4d_from_siemens_mosaic_folder(self, input_path):
        dcm_image_list = os.listdir(input_path)
        acquisition_num = len(dcm_image_list)
        for file_idx in range(acquisition_num):
            dcm_img = pd.dcmread(os.path.join(input_path, dcm_image_list[file_idx]))
            acquisition_idx = dcm_img[0x0020, 0x0012].value - 1
            array_img = dcm_img.pixel_array

            if file_idx == 0:
                slice_num = dcm_img[0x0019, 0x100A].value
                side_num = np.ceil(np.sqrt(slice_num))
                a, b = array_img.shape
                row = int(a / side_num)
                col = int(b / side_num)
                array_4d = np.zeros((row, col, slice_num, acquisition_num))

            for slice_idx in range(slice_num):
                shift1 = np.floor(slice_idx / side_num)
                shift2 = int((slice_idx - shift1 * side_num) * row)
                shift1 = int(shift1 * col)
                array_4d[:, :, slice_idx, acquisition_idx] = array_img[shift1:row + shift1, shift2:col + shift2]

        array_4d = np.moveaxis(array_4d, [0, 1, 2, 3], [1, 0, 2, 3])
        self.raw_data = array_4d

    def data4d_from_multi_folder(self, input_path):
        file_list = []
        file_instance_list = []
        file_series_list = []
        for root, dirs, files in os.walk(input_path):
            for file in files:
                file_list.append(os.path.join(root, file))
                img = pd.dcmread(file_list[-1], stop_before_pixels=True)
                file_instance_list.append(int(img[0x0020, 0x0013].value))
                file_series_list.append(int(img[0x0020, 0x0011].value))

        a = int(img[0x0028, 0x0010].value)
        b = int(img[0x0028, 0x0011].value)
        c = np.unique(file_instance_list)
        d = np.unique(file_series_list)

        array_4d = np.zeros((a, b, len(c), len(d)))
        data3d = np.zeros((a, b, len(c)))

        for j in range(len(d)):
            for i in range(len(c)):
                img = pd.dcmread(file_list[i + len(c) * j])
                instance_idx = img[0x0020, 0x0013].value - 1
                data3d[:, :, instance_idx] = img.pixel_array

            array_4d[:, :, :, j] = data3d

        array_4d = np.moveaxis(array_4d, [0, 1, 2, 3], [1, 0, 2, 3])
        self.raw_data = array_4d

    def data4d_from_ge7_folder(self, input_path):
        dcm_image_list = os.listdir(input_path)
        acquisition_num = len(dcm_image_list)
        for file_idx in range(acquisition_num):
            dcm_img = pd.dcmread(os.path.join(input_path, dcm_image_list[file_idx]))
            instance_idx = dcm_img[0x0020, 0x0013].value - 1
            array_img = dcm_img.pixel_array

            if file_idx == 0:
                slice_num = int(dcm_img[0x0020, 0x1002].value / 10)
                images_num = 9
                row, col = array_img.shape
                array_4d = np.zeros((row, col, slice_num, images_num))

            array_4d[:, :, instance_idx % slice_num, int(np.floor(instance_idx / slice_num))] = array_img

        array_4d = np.moveaxis(array_4d, [0, 1, 2, 3], [1, 0, 2, 3])
        self.raw_data = array_4d

    def xydownsample_raw(self, down_sample):
        self.raw_data = self.raw_data[::down_sample, ::down_sample, :, :]

    def gen_m0(self):
        if self.vendor == 'siemens':
            img_m0 = self.raw_data[:, :, :, 0]
            self.img_m0 = np.tile(img_m0[:, :, :, np.newaxis], (1, 1, 1, len(self.delay_list)))
        elif self.vendor == 'ge':
            if self.series_type == '7delay':
                img_m0 = self.raw_data[:, :, :, -1]
                self.img_m0 = np.tile(img_m0[:, :, :, np.newaxis], (1, 1, 1, len(self.delay_list)))
            else:
                _, _, c, _ = self.raw_data.shape
                cutoff = int(c / 2)
                self.img_m0 = self.raw_data[:, :, cutoff:, :]
        elif self.vendor == 'philips':
            _, _, c, _ = self.raw_data.shape
            skip = int((self.measure_list[0] + 1) * 2)
            self.img_m0 = self.raw_data[:, :, ::skip, :]

    def get_m0(self):
        return self.img_m0

    def gen_mask(self, threshold=0):
        mask = np.zeros(self.img_m0.shape)
        if self.vendor == 'siemens':
            self.threshold = threshold
            mask[self.img_m0 >= np.percentile(self.img_m0, 99) * self.threshold] = 1
        elif self.vendor in ['ge', 'philips']:
            for i in range(self.img_m0.shape[3]):
                pd_data = self.img_m0[:, :, :, i]
                self.threshold = 0.5 * np.sum(np.multiply(pd_data, pd_data)) / np.sum(pd_data)
                temp = np.zeros(np.shape(pd_data))
                temp[pd_data >= self.threshold] = 1
                mask[:, :, :, i] = temp
        self.mask = mask

    def get_mask(self):
        return self.mask

    def gen_plds(self):
        if self.vendor == 'siemens':
            a, b, c, _ = self.raw_data.shape
            self.img_plds = np.zeros((a, b, c, len(self.delay_list)))
            cur_idx = 2
            for pld_idx in range(len(self.measure_list)):
                data3d = np.zeros((a, b, c))
                for rep_idx in range(self.measure_list[pld_idx]):
                    control_image = self.raw_data[:, :, :, cur_idx]
                    label_image = self.raw_data[:, :, :, cur_idx + 1]
                    data3d = data3d + label_image.astype(np.float) - control_image.astype(np.float)
                    cur_idx += 2

                data3d = data3d / self.measure_list[pld_idx]
                data3d[data3d < 0] = 0
                self.img_plds[:, :, :, pld_idx] = data3d * self.extra_pld_factor  # TODO check extra factor here

        elif self.vendor == 'ge':
            if self.series_type == '7delay':
                self.img_plds = self.raw_data[:, :, :, :-1]
            else:
                _, _, c, _ = self.raw_data.shape
                cutoff = int(c / 2)
                self.img_plds = self.raw_data[:, :, :cutoff, :]

        elif self.vendor == 'philips':
            a, b, c, d = self.raw_data.shape
            skip = int((self.measure_list[0] + 1) * 2)
            self.img_plds = np.zeros((a, b, int(c / skip), d))
            for rep_idx in range(2, self.measure_list[0], 2):
                control_image = self.raw_data[:, :, range(rep_idx + 1, c, skip), :]
                label_image = self.raw_data[:, :, range(rep_idx, c, skip), :]
                self.img_plds = self.img_plds + label_image.astype(np.single) - control_image.astype(np.single)
            self.img_plds = self.img_plds / self.measure_list[0]

    def get_plds(self):
        return self.img_plds

    def gen_wd(self):
        a, b, c = self.mask[:, :, :, 0].shape
        numerator = np.zeros((a, b, c))
        denominator = np.zeros((a, b, c))
        for i in range(len(self.delay_list)):
            numerator += self.img_plds[:, :, :, i] * self.delay_list[i]
            denominator += self.img_plds[:, :, :, i]

        denominator[denominator == 0] = 1000000
        wd_image = np.divide(numerator, denominator)
        wd_image[self.mask[:, :, :, 0] == 0] = 0
        self.img_wd = wd_image * self.extra_wds_factor

    def get_wd(self):
        return self.img_wd

    def set_att(self, input_img):
        self.img_att = input_img

    def att_from_ge7_folder(self, input_path):

        dcm_image_list = os.listdir(input_path)
        acquisition_num = len(dcm_image_list)
        for file_idx in range(acquisition_num):
            dcm_img = pd.dcmread(os.path.join(input_path, dcm_image_list[file_idx]))
            instance_idx = dcm_img[0x0020, 0x0013].value - 1
            array_img = dcm_img.pixel_array

            if file_idx == 0:
                slice_num = int(dcm_img[0x0020, 0x1002].value / 10)
                row, col = array_img.shape
                array = np.zeros((row, col, slice_num))

            array[:, :, instance_idx] = array_img.astype(np.float32) / 1000

        array = np.moveaxis(array, [0, 1, 2], [1, 0, 2])
        self.img_att = array

    def gen_att_mapping_DAI(self): # Dai (2012)'s method, estimated from graph, doi:10.1002/mrm.23103
        self.img_att = self.img_wd * 1.761 - 1.532
        self.img_att[self.img_att < 0.7] = 0.7
        self.img_att[self.img_att > 3.0] = 3.0
        self.img_att[self.mask[:,:,:,0] == 0] = 0

    def gen_att_mapping(self):
        att_precision = 0.01
        a, b, c = self.img_wd.shape
        attValues = self._generate_att_cache(att_precision)
        av = attValues.tolist()
        att = np.zeros((a, b, c))
        for a_idx in range(a):
            for b_idx in range(b):
                for c_idx in range(c):
                    if self.mask[a_idx][b_idx][c_idx][0] == 1:
                        wdValue = self.img_wd[a_idx][b_idx][c_idx]
                        if not wdValue in av:
                            index2 = binary_search(av, wdValue)
                        else:
                            index2 = av.index(wdValue)
                        att[a_idx][b_idx][c_idx] = self.delay_list[0] + att_precision * index2

        self.img_att = att

    def _generate_att_cache(self, att_precision):
        pul_dur, _, _, r1a = get_balloon_model_parameters()
        output = np.zeros(int((self.delay_list[-1] - self.delay_list[0]) / att_precision) + 1)
        for index in range(len(output)):
            att = self.delay_list[0] + att_precision * index
            plds = np.zeros(len(self.delay_list))
            for delay_idx in range(len(self.delay_list)):
                delay = self.delay_list[delay_idx]
                plds[delay_idx] = np.exp((min([att - delay, 0]) - att) * r1a) - np.exp(0 - (pul_dur + delay) * r1a)
            numerator = 0
            denominator = 0
            for i in range(len(self.delay_list)):
                denominator += plds[i]
                numerator += plds[i] * (self.delay_list[i])
            output[index] = numerator / denominator
        return output

    def gen_cbfs(self, att_correction):
        pul_dur, blc, tag, r1a = get_balloon_model_parameters()
        a, b, c, d = self.img_plds.shape
        cbf_image = np.zeros((a, b, c, d))

        if att_correction == 'corrected':
            att_image = self.img_att
        elif att_correction == 'simple':
            att_image = np.zeros((a, b, c))

        for a_idx in range(a):
            for b_idx in range(b):
                for c_idx in range(c):
                    for d_idx in range(d):
                        if self.mask[a_idx][b_idx][c_idx][d_idx] == 1:
                            m0_vxl = self.img_m0[a_idx][b_idx][c_idx][d_idx]
                            att_vxl = att_image[a_idx][b_idx][c_idx]
                            pld_vxl = self.img_plds[a_idx][b_idx][c_idx][d_idx]
                            cbf_image[a_idx][b_idx][c_idx][d_idx] = 6000 * pld_vxl / m0_vxl * blc * r1a / 2 / tag / (
                                    np.exp((min([0, att_vxl - self.delay_list[d_idx]]) - att_vxl) * r1a)
                                    - np.exp(- r1a * (pul_dur + self.delay_list[d_idx])))

        cbf_image[cbf_image == np.NAN] = 0
        self.img_cbfs = cbf_image

    def gen_cbfs_ge(self):
        self.img_cbfs = np.zeros(self.img_m0.shape)
        for i in range(self.img_m0.shape[3]):
            c_lambda = 0.9
            c_st = 2
            c_t1t = 1.2
            pld = self.delay_list[i]
            c_t1b = 1.4  # 1.5T磁场的参数
            if self.magnetic_field_strength == 3:
                c_t1b = 1.6  # 3.0T磁场的参数
            c_epsilon = 0.6
            c_tau = self.labeling_duration
            nex = self.number_of_averages
            sf = 32  # 在DicomTag里找不到这个信息

            physiology_related = (1 - np.exp(-c_st / c_t1t)) * np.exp(pld / c_t1b) / c_t1b / (
                    1 - np.exp(-c_tau / c_t1b))
            scan_parameter_related = c_lambda / c_epsilon / sf / nex
            constant = 6000 / 2 * physiology_related * scan_parameter_related
            m0 = self.img_m0[:, :, :, i]
            m0[m0 < 1] = 1
            cbf = np.divide(self.img_plds[:, :, :, i], m0) * constant
            cbf[self.mask[:, :, :, i] == 0] = 0
            self.img_cbfs[:, :, :, i] = cbf

    def gen_cbf_tcorr_ge(self):  # 需要已生成ATT图
        a, b, c, d = self.img_m0.shape
        self.img_mcbf = np.zeros([a,b,c])
        att = self.img_att
        for i in range(d):
            c_lambda = 0.9
            c_st = 2
            c_t1t = 1.2
            pld = self.delay_list[i]
            c_t1b = 1.4  # 1.5T磁场的参数
            if self.magnetic_field_strength == 3:
                c_t1b = 1.6  # 3.0T磁场的参数
            c_epsilon = 0.6
            c_tau = self.labeling_duration
            nex = self.number_of_averages
            sf = 32  # 在DicomTag里找不到这个信息

            # 从王老师那里转换过来的，pld = att时，会产生下一行的公式，就跟GE原始的一样了
            # pld_related = np.exp(pld / c_t1b) / (1 - np.exp(-c_tau / c_t1b))
            pld_related = np.exp(pld / c_t1b) / (np.exp(np.minimum(0, pld - att) / c_t1b) - np.exp(-c_tau / c_t1b))
            physio_related = (1 - np.exp(-c_st / c_t1t)) / c_t1b
            scan_param_related = c_lambda / c_epsilon / sf / nex
            constant = 6000 / 2.0 * physio_related * scan_param_related * pld_related
            m0 = self.img_m0[:, :, :, i]
            m0[m0 < 1] = 1
            cbf = np.divide(self.img_plds[:, :, :, i], m0) * constant
            cbf[self.mask[:, :, :, i] == 0] = 0
            self.img_mcbf += cbf
        self.img_mcbf = self.img_mcbf / d
        self.img_mcbf[self.img_mcbf < 0] = 0
        self.img_mcbf[self.img_mcbf > 400] = 0

    def gen_cbfs_ge7delay(self, transit_correction=True):
        self.img_cbfs = np.zeros(self.img_m0.shape)

        extra_factor = 0.88  # 额外的系数

        if len(self.duration_list) == 7:
            lds = self.duration_list
            plds = self.delay_list
        else:
            lds = [0.22, 0.26, 0.30, 0.37, 0.48, 0.68, 1.18]
            plds = [1.0, 1.22, 1.48, 1.78, 2.15, 2.62, 3.32]

        print("lds & plds")
        print(lds)
        print(plds)
        c_lambda = 0.73
        c_t1t = 1.2
        c_t1b = 1.6  # 3.0T磁场的参数
        c_epsilon = 0.6375

        # 计算每一个CBF
        for cbf_ind in range(7):
            lower_mat1 = np.exp(- plds[cbf_ind] / c_t1t)
            lower_mat2 = np.exp(- (plds[cbf_ind] + lds[cbf_ind]) / c_t1t)
            constant_matrix = 6000 / 2 / (lower_mat1 - lower_mat2) * c_lambda / c_t1b / c_epsilon / 32
            m0 = self.img_m0[:, :, :, cbf_ind]
            m0[m0 < 1] = 1
            cbf = np.multiply(np.divide(self.img_plds[:, :, :, cbf_ind], m0), constant_matrix) * extra_factor
            if transit_correction:
                att_factor = 1 + np.power(abs(self.img_att - plds[cbf_ind] + lds[cbf_ind] + 0.3) * 2, 6) / 2
                cbf = np.divide(cbf, att_factor)
            cbf[self.mask[:, :, :, cbf_ind] == 0] = 0
            self.img_cbfs[:, :, :, cbf_ind] = cbf

        # 计算mCBF
        upper_mat = np.exp(self.img_att * transit_correction / c_t1b)
        lower_mat1 = np.exp(- np.maximum(plds[0] - self.img_att * transit_correction, 0) / c_t1t)
        lower_mat2 = np.exp(- np.maximum(plds[6] + lds[6] - self.img_att * transit_correction, 0) / c_t1t)

        constant_matrix = 6000 / 2 * np.divide(upper_mat, lower_mat1 - lower_mat2) * c_lambda / c_t1b / c_epsilon / 32
        cbf = np.multiply(np.divide(self.img_plds[:, :, :, -1], m0), constant_matrix) * extra_factor ** (1 - transit_correction)
        cbf[self.mask[:, :, :, cbf_ind] == 0] = 0
        self.img_mcbf = cbf

    def gen_cbfs_philips(self):
        self.img_cbfs = np.zeros(self.img_m0.shape)
        for i in range(len(self.delay_list)):
            c_lambda = 0.9
            pld = self.delay_list[i]
            c_t1b = 1.35  # 1.5T磁场的参数
            if self.magnetic_field_strength == 3:
                c_t1b = 1.65  # 3.0T磁场的参数
            c_alpha = 0.85
            c_tau = self.labeling_duration

            physiology_related = np.exp(pld / c_t1b) / (1 - np.exp(-c_tau / c_t1b))
            scan_parameter_related = c_lambda / c_alpha
            constant = 6000 / 2 * physiology_related * scan_parameter_related
            m0 = self.img_m0[:, :, :, i]
            m0[m0 < 1] = 1
            cbf = np.divide(self.img_plds[:, :, :, i], m0) * constant
            cbf[self.mask[:, :, :, i] == 0] = 0
            self.img_cbfs[:, :, :, i] = cbf

    def get_cbfs(self):
        return self.img_cbfs

    def gen_diff_cbfs(self):
        self.img_diff_cbfs = self.img_cbfs[:, :, :, 1:] - self.img_cbfs[:, :, :, :-1]

    def get_diff_cbfs(self):
        return self.img_diff_cbfs

    def gen_att_mcbf_fitting(self):
        att_default = self.delay_list[0]
        cbf_default = 80
        fitting_shift = 0.05
        x_arr = self.delay_list
        a, b, c = self.img_m0[:, :, :, 0].shape
        att_image = np.zeros((a, b, c))
        mcbf_image = np.zeros((a, b, c))
        for c_idx in range(c):
            print([c_idx, c])
            for a_idx in range(a):
                for b_idx in range(b):
                    if self.mask[a_idx, b_idx, c_idx, 0] == 1:
                        y_arr = (self.img_plds[a_idx, b_idx, c_idx, :]).flatten() / self.img_m0[a_idx, b_idx, c_idx, 0]
                        try:
                            att_cbf, _ = curve_fit(func, x_arr, y_arr,
                                                   p0=(att_default + fitting_shift, cbf_default),
                                                   maxfev=100)
                        except Exception as e:
                            print(e)
                        else:
                            if att_cbf[0] < 0 or att_cbf[0] > 20:
                                pass
                            else:
                                att_image[a_idx, b_idx, c_idx] = att_cbf[0]
                                mcbf_image[a_idx, b_idx, c_idx] = att_cbf[1]

        self.img_att = att_image * self.extra_att_factor
        self.img_mcbf = mcbf_image * self.extra_cbf_factor

    def get_att(self):
        return self.img_att

    def get_mcbf(self):
        return self.img_mcbf

    def gen_acbv(self):
        sec_to_min = 60
        self.img_acbv = np.multiply(self.img_att, self.img_mcbf) / sec_to_min

    def get_acbv(self):
        return self.img_acbv
