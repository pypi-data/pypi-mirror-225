from ._dicom import *
from ._dicom_util import write_dicom_series, convert
from .data_sorter_base import DataSorterASLBase


class DataSorterUIHPASL(DataSorterASLBase):
    def __init__(self, data_type, output_root, delay_time, delay_rep, label_dur, series_list, extra_factor, calc_c_cbf):
        DataSorterASLBase.__init__(self, data_type, output_root, delay_time, delay_rep, label_dur, series_list, calc_c_cbf)
        if extra_factor is None or extra_factor == 0:
            logger.debug('extra_factor 未设置')
            # raise Exception('extra_factor 未设置')
        else:
            self.extra_factor = 32 / extra_factor
        self.M0 = []
        self.CBF = [] # CBF参数图
        self.ATT: SeriesModel = None
        self.ACBV: SeriesModel = None

        self.Control = []
        self.Label = []

        self.M0_count = 0
        self.CBF_count = 0
        # 区别M0与灌注图
        for series in self.series_list:
            if not isinstance(series, SeriesModel):
                continue
            seriesDescription = series.SeriesDescription.lower().replace('-', ' ')
            if seriesDescription.find('m0') > -1:
                self.M0_count += 1
                self.M0.append(series)
            elif seriesDescription.find('cbf') > -1:
                self.CBF_count += 1
                self.CBF.append(series)
            elif seriesDescription.find('att') > -1:
                self.ATT = series
            elif seriesDescription.find('acbv') > -1:
                self.ACBV = series
            elif seriesDescription.find('ctrl') > -1:
                self.Control.append(series)
            elif seriesDescription.find('tag') > -1:
                self.Label.append(series)

    def validate_series(self):
        if len(self.M0) == 0:
            raise MissingSequenceError('M0')
        if len(self.CBF) == 0:
            raise MissingSequenceError('CBF')

        # if self.M0_count > 1:
        #     raise SeriesTooMany(f'发现{self.M0_count}组M0图像，请保留一组再进行处理')
        # if self.CBF_count > 1:
        #     raise SeriesTooMany(f'发现{self.CBF_count}组CBF图像，请保留一组再进行处理')

    def Sorter(self):
        super(DataSorterUIHPASL, self).Sorter()

        self.validate_series()

        if self.ATT is not None and self.ACBV is not None:
            self.generate_multi_pld()

        else:
            # self.generate_calc_cbf_3d_pasl()
            self.generate_cbf_3d_pasl()

    def generate_multi_pld(self):
        self.M0: SeriesModel = self.M0[0]
        m0_image = self.M0.load()
        # 多张M0只有第一张有效
        m0_image = m0_image[..., 0]
        write_dicom_series(m0_image, self.M0, 'asl-m0', 1001, os.path.join(self.output_root, 'asl', 'm0'))

        cbf_image = self.CBF[0].load()[..., 0]
        write_dicom_series(cbf_image * 10, self.M0, 'asl-cbf', 1002, os.path.join(self.output_root, 'asl', 'cbf'), slope=0.1)

        # UIH的ATT 单位为ms，不再乘以1000
        att_image = self.ATT.load()[..., 0]
        write_dicom_series(att_image, self.M0, 'asl-att', 1003, os.path.join(self.output_root, 'asl', 'att'), slope=0.001)

        acbv_image = self.ACBV.load()[..., 0]
        write_dicom_series(acbv_image * 1000, self.M0, 'asl-acbv', 1004, os.path.join(self.output_root, 'asl', 'acbv'), slope=0.001)

    def generate_cbf_3d_pasl(self):
        self.M0: SeriesModel = self.M0[0]
        m0_image = self.M0.load()
        # 多张M0只有第一张有效
        m0_image = m0_image[...,0]
        m0_nii = write_dicom_series(m0_image, self.M0, 'asl-m0', 1001, os.path.join(self.output_root, 'asl', 'm0'))

        # 加载全部的CBF，空间如不一致抛异常
        cbf_mat_list = []
        space_resolution = None
        for i in self.CBF:
            mat = i.load()[..., 0]
            if space_resolution is None:
                space_resolution = mat.shape
            elif space_resolution != mat.shape:
                raise Exception(f'多个PLD图像分辨率不一致{mat.shape} 与 {space_resolution}')
            cbf_mat_list.append(mat)

        for i, (cbf_mat, cbf_series) in enumerate(zip(cbf_mat_list, self.CBF)):
            cbf_nii = write_dicom_series(cbf_mat * 10, cbf_series, f'asl-cbf{i+1}', 1002 + i,
                               os.path.join(self.output_root, 'asl', f'cbf{i+1}'), slope=0.1)

            # convert(cbf_nii, cbf_nii, m0_nii)

        super().calc_correct_CBF(np.concatenate([i.load() for i in self.CBF], axis=3), self.CBF[0], 1002+len(self.CBF))

    def generate_calc_cbf_3d_pasl(self):
        self.M0: SeriesModel
        m0_image = self.M0.load()
        # 多张M0只有第一张有效
        m0_image = m0_image[:,:,:,0]
        write_dicom_series(m0_image, self.M0, 'asl-m0', 1001, os.path.join(self.output_root, 'asl', 'm0'))

        control = self.Control.load()
        label = self.Label.load()
        repetitions = control.shape[-1]
        pwi = np.zeros(m0_image.shape)
        sub = control - label
        for i in range(repetitions):
            pwi += sub[:,:,:,i]
        pwi /= repetitions

        # calculate CBF
        t_inv = self.delay_time  # sec, inversion time
        l_dur = self.label_dur  # sec, labeling duration
        bb_p = 0.9  # mL/g, blood-brain partition coefficient
        t1_b = 1.65  # sec, relaxation of blood at 3.0T
        lab_eff = 0.98  # labeling efficiency for PASL
        u_cnv = 6000  # units conversion from mL/g/s to mL/100g/min

        upper_param = u_cnv * bb_p * np.exp(t_inv / t1_b)
        lower_param = 2 * lab_eff * l_dur
        calc_cbf = pwi / m0_image.astype(float) * upper_param / lower_param
        write_dicom_series(calc_cbf * 10, self.M0, 'asl-cbf1', 1002, os.path.join(self.output_root, 'asl', 'cbf1'),
                           slope=0.1)

    def _gen_mask(self, input_image):
        threshold = 0.5 * np.sum(np.multiply(input_image, input_image)) / np.sum(input_image)
        output_image = np.zeros(np.shape(input_image))
        output_image[input_image >= threshold] = 1
        return output_image