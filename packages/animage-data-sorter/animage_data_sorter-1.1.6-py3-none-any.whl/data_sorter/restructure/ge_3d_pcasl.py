from ._dicom import *
from ._dicom_util import write_dicom_series
from .data_sorter_base import DataSorterASLBase
from .errors import *


class DataSorterGEPCASL(DataSorterASLBase):
    def __init__(self, data_type, output_root, delay_time, delay_rep, label_dur, series_list, calc_c_cbf):
        DataSorterASLBase.__init__(self, data_type, output_root, delay_time, delay_rep, label_dur, series_list, calc_c_cbf)
        self.PWPD = [] # 灌注图
        self.CBF = [] # CBF参数图

        # 区别PWPD与CBF图
        for series in self.series_list:
            series_description = series.SeriesDescription.lower()
            if not isinstance(series, SeriesModel):
                continue
            elif series_description.find('3d') > -1 and series_description.find('asl') > -1:
                self.PWPD.append(series)
            elif series_description.find('cerebral blood flow') > -1 or series_description.find('cbf') > -1:
                self.CBF.append(series)

    def Sorter(self):
        super(DataSorterGEPCASL, self).Sorter()

        # 验证序列
        self.validate_series()

        # 多延迟存在于不同序列需要重新排序
        self.PWPD.sort(key=lambda x: x.SeriesNumber)
        self.CBF.sort(key=lambda x: x.SeriesNumber)

        self.generate_cbf_3d_pcasl()

    def validate_series(self):
        delay_time = []
        for i in self.PWPD:
            delay_time.append(i.get_tag((0x0018, 0x0082)))
        if len(delay_time) > 0:
            self.delay_time = [float(i) / 1000 for i in delay_time]
        logger.info(f'3D ASL 使用PLD为：{self.delay_time}')

        delay_count = len(self.delay_time)
        cbf_count = len(self.CBF)
        pwpd_count = len(self.PWPD)
        if cbf_count == 0 and pwpd_count == 0:
            raise NotFoundSeriesError()
        elif cbf_count == 0:
            logger.info('未发现CBF图，将由3D ASL计算生成')
        elif pwpd_count == 0:
            logger.warning('未发现PWPD，可能影响配准的效果')
        else:
            # 两种序列都存在，PWPD数量应为CBF两倍
            for i, j in zip(self.PWPD, self.CBF):
                if i.Repetition != 2 * j.Repetition:
                    raise SliceLessError(i.SliceNumber)

        if cbf_count != delay_count and cbf_count != 0:
            raise DelayNotEqualSeriesNumberError(delay_count, cbf_count)
        if pwpd_count != delay_count and pwpd_count != 0:
            raise DelayNotEqualSeriesNumberError(delay_count, pwpd_count)

    def set_scan_parameter(self, series_model: SeriesModel):
        self.number_of_averages = series_model.get_tag((0x0018, 0x0083), 1)
        self.magnetic_field_strength = series_model.get_tag((0x0018, 0x0087), 1)
        self.labeling_duration = series_model.get_tag((0x0043, 0x10A5), 1500) / 1000

    def generate_cbf_3d_pcasl(self):
        m0_image = None
        pw_image = None
        ref_series = None

        cbf_image = None
        if len(self.CBF) != 0:
            cbf_image = np.concatenate([i.load() for i in self.CBF], axis=3)
            ref_series = self.CBF[0]

        if len(self.PWPD) != 0:
            pwpd_image = np.concatenate([i.load() for i in self.PWPD], axis=3)
            pwpd_image[pwpd_image < 0] = 0
            m0_image = pwpd_image[:, :, :, 1::2]
            pw_image = pwpd_image[:, :, :, 0::2]
            ref_series = self.PWPD[0]

        if cbf_image is None:
            cbf_image = np.zeros(pw_image.shape)
            self.set_scan_parameter(self.PWPD[0])
            mask = self._gen_mask(m0_image)
            # 计算 CBF
            for i in range(pw_image.shape[3]):
                c_lambda = 0.9
                c_st = 2
                c_t1t = 1.2
                pld = self.delay_time[i]
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
                m0 = m0_image[:, :, :, i]
                m0[m0 < 1] = 1
                cbf = np.divide(pw_image[:, :, :, i], m0) * constant
                cbf[mask[..., i] == 0] = 0
                cbf_image[..., i] = cbf

        elif m0_image is None:
            # 无M0使用CBF替代
            m0_image = cbf_image

        cur_series_number = SeriesNumberStartWith.ASL
        write_dicom_series(m0_image[...,0], ref_series, 'asl-m0', cur_series_number, os.path.join(self.output_root, 'asl', 'm0'))
        for i, d in enumerate(self.delay_time):
            cur_series_number += 1
            write_dicom_series(cbf_image[:,:,:,i] * 10, ref_series, f'asl-cbf{i+1}', cur_series_number,
                               os.path.join(self.output_root, 'asl', f'cbf{i+1}'), slope=0.1)

        super().calc_correct_CBF(cbf_image, ref_series, cur_series_number + 1)

    def _gen_mask(self, m0: np.ndarray):
        mask = np.zeros(m0.shape)
        for i in range(m0.shape[3]):
            pd_data = m0[:, :, :, i]
            threshold = 0.5 * np.sum(np.multiply(pd_data, pd_data)) / np.sum(pd_data)
            mask[:, :, :, i][pd_data >= threshold] = 1
        return mask
