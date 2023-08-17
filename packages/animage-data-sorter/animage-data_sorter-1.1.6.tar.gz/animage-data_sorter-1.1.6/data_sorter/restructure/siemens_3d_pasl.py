from scipy.ndimage import gaussian_filter

from ._dicom import *
from ._dicom_util import write_dicom_series
from .data_sorter_base import DataSorterASLBase
from .errors import *


class DataSorterSiemensPASL(DataSorterASLBase):
    def __init__(self, data_type, output_root, delay_time, delay_rep, label_dur, series_list, extra_factor, calc_c_cbf):
        DataSorterASLBase.__init__(self, data_type, output_root, delay_time, delay_rep, label_dur, series_list, calc_c_cbf)
        if extra_factor is None or extra_factor == 0:
            raise Exception('extra_factor 未设置')
        self.extra_factor = 32 / extra_factor
        self.M0 = None
        self.PWPD = [] # 灌注图
        self.CBF = None # CBF参数图

        # 区别M0与灌注图
        for series in self.series_list:
            series_description = series.SeriesDescription.lower()
            if not isinstance(series, SeriesModel):
                continue
            if series_description.find('m0') > -1 or series_description.find('mo') > -1:
                self.M0 = series
            elif series_description.find('asl_3d_tra') > -1 or series_description.find('asl_pasl') > -1 or  \
                series_description.find('pasl_3d') > -1:
                self.PWPD.append(series)

        delay_count = len(self.delay_time)
        pwpd_count = len(self.PWPD)

        # 判断是否缺少某些序列
        if pwpd_count == 0:
            logger.error('未发现灌注图')
            raise MissingSequenceError('ASL')
        elif delay_count != pwpd_count:
            raise DelayNotEqualSeriesNumberError(delay_count, pwpd_count)
        if self.M0 is None:
            logger.warning('未发现M0，可能影像数值计算的准确性')
            self.M0 = self.PWPD[0]

        # 不同的重复次数存在于不同序列需要重新排序
        self.PWPD.sort(key=lambda x: (x.SeriesNumber, x[0].InstanceNumber))

    def Sorter(self):
        super(DataSorterSiemensPASL, self).Sorter()
        if self.PWPD[0].SeriesDescription.lower().find('asl_3d_tra_p2') > -1:
            self.generate_cbf_3d_pcasl()
        else:
            self.generate_cbf_3d_pasl()

    def generate_cbf_3d_pcasl(self):
        self.M0: SeriesModel
        m0_image = self.M0.load()
        # 多张M0只有第一张有效
        if len(m0_image.shape) == 4:
            m0_image = m0_image[:,:,:,0]
        m0_image *= self.extra_factor

        cur_series_number = SeriesNumberStartWith.ASL
        write_dicom_series(m0_image, self.M0, 'asl-m0', cur_series_number, os.path.join(self.output_root, 'asl', 'm0'))

        for i, pwpd in enumerate(self.PWPD):
            cbf_pcasl_calc = self.pcasl_calc_cbf(pwpd.load(), m0_image, self.delay_time[i], self.label_dur[i])
            cur_series_number += 1
            write_dicom_series(cbf_pcasl_calc * 10, pwpd, f'asl-cbf{i+1}', cur_series_number,
                               os.path.join(self.output_root, 'asl', f'cbf{i+1}'), slope=0.1)

    def pcasl_calc_cbf(self, pwpd_image: np.ndarray, m0_image: np.ndarray, delay_time, label_dur):
        control = pwpd_image[: ,: ,: ,0::2] # 控制像
        label = pwpd_image[:, :, :, 1::2] # 标记像
        repetitions = control.shape[-1]
        pwi = np.zeros(m0_image.shape)
        sub = control - label
        for i in range(repetitions):
            pwi += sub[:,:,:,i]
        pwi /= repetitions

        m0_image[m0_image < 1] = 1
        mask = self._gen_mask(m0_image)

        # calculating using simple model
        u_cnv = 6000  # units conversion from mL/g/s to mL/100g/min
        bb_p = 0.9  # mL/g, blood-brain partition coefficient
        t_inv = delay_time  # sec, post-labeling delay
        t1_b = 1.65  # sec, relaxation of blood at 3.0T
        lab_eff = 0.85  # labeling efficiency for pCASL
        l_dur = label_dur  # sec, labeling duration
        NEX = 32
        upper_param = u_cnv * bb_p * np.exp(t_inv / t1_b)
        lower_param = 2 * lab_eff * t1_b * (1 - np.exp(-l_dur / t1_b))
        cbf_pcasl_calc = np.divide(pwi, m0_image) / NEX * upper_param / lower_param

        cbf_pcasl_calc[pwi < 8] = 0
        cbf_pcasl_calc = np.multiply(cbf_pcasl_calc, mask)
        cbf_pcasl_calc = cbf_pcasl_calc.astype(np.int16)
        return cbf_pcasl_calc

    def generate_cbf_3d_pasl(self):
        self.M0: SeriesModel
        m0_image = self.M0.load()
        # 多张M0只有第一张有效
        m0_image = m0_image[:,:,:,0]
        m0_image *= self.extra_factor
        cur_series_number = SeriesNumberStartWith.ASL
        write_dicom_series(m0_image, self.M0, 'asl-m0', cur_series_number, os.path.join(self.output_root, 'asl', 'm0'))

        for i, pwpd in enumerate(self.PWPD):
            cbf_pasl_calc = self.pasl_calc_cbf(pwpd.load(), m0_image, self.delay_time[i], self.label_dur[i])
            cur_series_number += 1
            write_dicom_series(cbf_pasl_calc * 10, pwpd, f'asl-cbf{i+1}', cur_series_number,
                               os.path.join(self.output_root, 'asl', f'cbf{i+1}'), slope=0.1)

    def pasl_calc_cbf(self, pwpd_image: np.ndarray, m0_image: np.ndarray, delay_time, label_dur):
        control = pwpd_image[:, :, :, 0::2]  # 控制像
        label = pwpd_image[:, :, :, 1::2]  # 标记像
        repetitions = control.shape[-1]
        pwi = np.zeros(m0_image.shape)
        sub = control - label
        for i in range(repetitions):
            pwi += sub[:, :, :, i]
        pwi /= repetitions

        # calculating using simple model
        u_cnv = 6000  # units conversion from mL/g/s to mL/100g/min
        bb_p = 0.9  # mL/g, blood-brain partition coefficient
        t_inv = delay_time  # sec, inversion time
        t1_b = 1.65  # sec, relaxation of blood at 3.0T
        lab_eff = 0.98  # labeling efficiency for PASL
        l_dur = label_dur  # sec, labeling duration

        m0_image[m0_image < 1] = 1
        mask = self._gen_mask(m0_image)

        check = np.multiply(mask, pwi)

        if sum(check.flatten()) < 0:
            pwi = -pwi
        pwi[pwi < 0] = 0
        upper_param = u_cnv * bb_p * np.exp(t_inv / t1_b)
        lower_param = 2 * lab_eff * l_dur
        cbf_pasl_calc = pwi / m0_image * upper_param / lower_param
        cbf_pasl_calc = np.multiply(cbf_pasl_calc, mask)
        cbf_pasl_calc = gaussian_filter(cbf_pasl_calc, 0.7)
        cbf_pasl_calc = cbf_pasl_calc.astype(np.int16)
        return cbf_pasl_calc

    def _gen_mask(self, input_image):
        threshold = 0.5 * np.sum(np.multiply(input_image, input_image)) / np.sum(input_image)
        output_image = np.zeros(np.shape(input_image))
        output_image[input_image >= threshold] = 1
        return output_image