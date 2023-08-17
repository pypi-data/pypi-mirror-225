from ._dicom import *
from ._dicom_util import write_dicom_series
from .data_sorter_base import DataSorterASLBase
from .errors import *


class DataSorterGEeASL(DataSorterASLBase):
    def __init__(self, data_type, output_root, delay_time, delay_rep, label_dur, series_list, calc_c_cbf):
        DataSorterASLBase.__init__(self, data_type, output_root, delay_time, delay_rep, label_dur, series_list, calc_c_cbf)
        self.output_root = output_root

        self.RAW = None
        self.ATT = None
        self.CORR_CBF = None
        self.STAN_CBF = None

        # 区别PWPD与CBF图
        for series in self.series_list:
            if not isinstance(series, SeriesModel):
                continue
            seriesDescription = series.SeriesDescription.lower().replace('-', ' ')
            if seriesDescription.find('raw') > -1:
                self.RAW = series
            elif seriesDescription.find('transit delay') > -1:
                self.ATT = series
            elif seriesDescription.find('transit corrected flow') > -1 or seriesDescription.find('transit corrected cbf') > -1:
                self.CORR_CBF = series
            elif seriesDescription.find('cbf') > -1 or seriesDescription.find('flow') > -1:
                self.STAN_CBF = series
            # todo 这里如果出现多组灌注图将只使用最后一个: 需要完善

    def validate_series(self):
        if self.RAW is None or self.ATT is None:
            raise MissingSequenceError('ATT and/or RAW')

    def Sorter(self):
        super(DataSorterGEeASL, self).Sorter()
        self.validate_series()

        raw_data_pwpd = self.RAW.load()
        raw_data_pwpd[raw_data_pwpd < 0] = 0

        # M0
        cur_series_number = SeriesNumberStartWith.ASL
        m0_image = raw_data_pwpd[...,-1]
        write_dicom_series(m0_image, self.RAW, 'asl-m0', cur_series_number, os.path.join(self.output_root, 'asl', 'm0'))

        # mask
        mask_image = self._gen_mask(m0_image)

        # PLD
        plds_image = raw_data_pwpd[...,:-1]

        att_image, (cbfs_image_corr, mcbf_image_corr, cbfs_image_ncorr, mcbf_image_ncorr), acbv_image = self.ge_calc_yao(plds_image, m0_image, mask_image)

        use_self_calc = False  # todo 是否使用自己计算的CBF
        is_use_ge_corr = True
        if is_use_ge_corr:
            # CORR_CBF 有可能是MCBF，也有可能是CBF1-7
            if (not use_self_calc) and (self.CORR_CBF is not None) and (self.CORR_CBF.Repetition == 1):
                # 使用提供的MCBF
                mcbf_image_corr = self.CORR_CBF.load()[..., 0]
            mcbf_image_corr[mcbf_image_corr < 0] = 0
            cur_series_number += 1
            write_dicom_series(mcbf_image_corr * 10, self.RAW, 'asl-mcbf', cur_series_number,
                               os.path.join(self.output_root, 'asl', 'mcbf'), slope=0.1)

            if (not use_self_calc) and (self.CORR_CBF is not None) and (self.CORR_CBF.Repetition == 7):
                # 使用已提供的结果
                cbfs_image_corr = self.CORR_CBF.load()
            cbfs_image_corr[cbfs_image_corr < 0] = 0
            for i in range(cbfs_image_corr.shape[3]):
                cur_series_number += 1
                write_dicom_series(cbfs_image_corr[...,i] * 10, self.RAW, 'asl-cbf%d'%(i+1), cur_series_number,
                                   os.path.join(self.output_root, 'asl', 'cbf%d'%(i+1)), 0.1)
            # super().calc_correct_CBF(cbfs_image_corr, self.RAW, cur_series_number + 1)

        else:
            # STAN_CBF 同样有可能是MCBF，也有可能是CBF1-7
            if (not use_self_calc) and (self.STAN_CBF is not None) and (self.STAN_CBF.Repetition == 1):
                # 使用提供的MCBF
                mcbf_image_ncorr = self.STAN_CBF.load()[..., 0]
            mcbf_image_ncorr[mcbf_image_ncorr < 0] = 0
            cur_series_number += 1
            write_dicom_series(mcbf_image_ncorr * 10, self.RAW, 'asl-mcbf', cur_series_number,
                               os.path.join(self.output_root, 'asl', 'mcbf'), slope=0.1)

            if (not use_self_calc) and (self.STAN_CBF is not None) and (self.STAN_CBF.Repetition == 7):
                # 使用已提供的结果
                cbfs_image_ncorr = self.STAN_CBF.load()
            cbfs_image_ncorr[cbfs_image_ncorr < 0] = 0
            for i in range(cbfs_image_ncorr.shape[3]):
                cur_series_number += 1
                write_dicom_series(cbfs_image_ncorr[..., i] * 10, self.RAW, 'asl-cbf%d' % (i + 1), cur_series_number,
                                   os.path.join(self.output_root, 'asl', 'cbf%d' % (i + 1)), 0.1)

            # super().calc_correct_CBF(cbfs_image_ncorr, self.RAW, cur_series_number + 1)

        # ATT
        cur_series_number += 1
        write_dicom_series(att_image * 1000, self.RAW, 'asl-att', cur_series_number, os.path.join(self.output_root, 'asl', 'att'), 0.001)

        # ACBV
        cur_series_number += 1
        write_dicom_series(acbv_image * 1000, self.RAW, 'asl-acbv', cur_series_number, os.path.join(self.output_root, 'asl', 'acbv'), 0.001)


    def set_up_aslutil(self):
        pass

    def set_scan_parameter(self, series_model: SeriesModel):
        self.number_of_averages = series_model.get_tag((0x0018, 0x0083), 1)
        self.magnetic_field_strength = series_model.get_tag((0x0018, 0x0087), 1)
        self.labeling_duration = series_model.get_tag((0x0043, 0x10A5), 1500) / 1000

    def ge_calc_yao(self, plds_image: np.ndarray, m0_image: np.ndarray, mask_image: np.ndarray):
        # ATT
        att_image = self.ATT.load()[..., -1]
        att_image /= 1000
        # 非校正CBF
        cbfs_image_ncorr, mcbf_image_ncorr = self.gen_cbfs_ge7delay(att_image, plds_image, m0_image, mask_image, False)

        # 校正后CBF
        cbfs_image_corr, mcbf_image_corr = self.gen_cbfs_ge7delay(att_image, plds_image, m0_image, mask_image, True)

        acbv_image = self.gen_acbv(att_image, mcbf_image_corr)
        return att_image, (cbfs_image_corr, mcbf_image_corr, cbfs_image_ncorr, mcbf_image_ncorr), acbv_image

    def gen_cbfs_ge7delay(self, att_image: np.ndarray, plds_image: np.ndarray, m0_image: np.ndarray, mask_image: np.ndarray, transit_correction=True):
        extra_factor = 0.88  # 额外的系数

        c_lambda = 0.73
        c_t1t = 1.2
        c_t1b = 1.6  # 3.0T磁场的参数
        c_epsilon = 0.6375
        plds = self.delay_time
        lds = self.label_dur

        cbfs_image = np.zeros(list(m0_image.shape) + [7])
        m0_image[m0_image < 1] = 1
        # 计算每一个CBF
        for cbf_ind in range(7):
            lower_mat1 = np.exp(- plds[cbf_ind] / c_t1t)
            lower_mat2 = np.exp(- (plds[cbf_ind] + lds[cbf_ind]) / c_t1t)
            constant_matrix = 6000 / 2 / (lower_mat1 - lower_mat2) * c_lambda / c_t1b / c_epsilon / 32
            cbf = np.multiply(np.divide(plds_image[:, :, :, cbf_ind], m0_image), constant_matrix) * extra_factor
            if transit_correction:
                att_factor = 1 + np.power(abs(att_image - plds[cbf_ind] + lds[cbf_ind] + 0.3) * 2, 6) / 2
                cbf = np.divide(cbf, att_factor)
            cbf[mask_image == 0] = 0
            cbfs_image[:, :, :, cbf_ind] = cbf


        # 计算mCBF
        upper_mat = np.exp(att_image * transit_correction / c_t1b)
        lower_mat1 = np.exp(- np.maximum(plds[0] - att_image * transit_correction, 0) / c_t1t)
        lower_mat2 = np.exp(- np.maximum(plds[6] + lds[6] - att_image * transit_correction, 0) / c_t1t)

        constant_matrix = 6000 / 2 * np.divide(upper_mat, lower_mat1 - lower_mat2) * c_lambda / c_t1b / c_epsilon / 32
        mcbf_image = np.multiply(np.divide(plds_image[:, :, :, -1], m0_image), constant_matrix) * extra_factor ** (
                    1 - transit_correction)
        mcbf_image[mask_image == 0] = 0

        return cbfs_image, mcbf_image

    def gen_acbv(self, att_image: np.ndarray, cbf_image: np.ndarray):
        sec_to_min = 60
        acbv_image = np.multiply(att_image, cbf_image) / sec_to_min
        return acbv_image

    def _gen_mask(self, input_image):
        threshold = 0.5 * np.sum(np.multiply(input_image, input_image)) / np.sum(input_image)
        output_image = np.zeros(np.shape(input_image))
        output_image[input_image >= threshold] = 1
        return output_image
