from ._dicom import *
from ._dicom_util import write_dicom_series
from .data_sorter_base import DataSorterASLBase
from .errors import *


class DataSorterPhilipsPCASL(DataSorterASLBase):
    def __init__(self, data_type, output_root, delay_time, delay_rep, label_dur, series_list, calc_c_cbf):
        DataSorterASLBase.__init__(self, data_type, output_root, delay_time, delay_rep, label_dur, series_list, calc_c_cbf)
        self.M0:SeriesModel
        self.PWPD = [] # 灌注图
        self.CBF = [] # CBF参数图

        # 区别M0与灌注图
        for series in self.series_list:
            if not isinstance(series, SeriesModel):
                continue
            elif series.SeriesDescription.lower().find('source') > -1:
                self.PWPD.append(series)
            elif series.SeriesDescription.lower().find('3d') > -1 and series.SeriesDescription.lower().find('pcasl') > -1:
                self.CBF.append(series)

    def Sorter(self):
        super(DataSorterPhilipsPCASL, self).Sorter()

        delay_count = len(self.delay_time)
        cbf_count = len(self.CBF)
        pwpd_count = len(self.PWPD)
        if cbf_count == 0 and pwpd_count == 0:
            raise NotFoundSeriesError()
        elif cbf_count == 0:
            logger.error('未发现CBF图')
            raise MissingSequenceError('ASL')
        elif pwpd_count == 0:
            logger.warning('未发现PWPD，可能影响配准的效果')

        if cbf_count != delay_count:
            # raise DelayNotEqualSeriesNumberError(delay_count, cbf_count)
            logger.warning(f'输入的PLD长度与实际CBF数量不符, 将补齐/裁切')
            if delay_count < cbf_count:
                self.delay_time += ['undefined'] * (cbf_count - delay_count)

        logger.info(f'使用的PLD为{self.delay_time}')
        logger.info(f'飞利浦{delay_count}延迟数据')

        # 检测多延迟还是单延迟的多次重复
        self.PWPD.sort(key=lambda x: x.SeriesNumber)
        if pwpd_count > cbf_count:
            merge_PWPD = []
            # NumberOfTemporalPositions 此字段为飞利浦重复次数
            NumberOfTemporalPositions = self.PWPD[0].get_tag((0x0020, 0x0105))
            cur_number = -1
            for i, p in enumerate(self.PWPD):

                # TemporalPositionIdentifier 此字段为飞利浦重复第一次，校验是否缺失
                TemporalPositionIdentifier = p.get_tag((0x0020, 0x0100))
                if TemporalPositionIdentifier == 1:
                    merge_PWPD.append([p])
                    cur_number += 1
                else:
                    if i % NumberOfTemporalPositions + 1 != TemporalPositionIdentifier:
                        raise MissingSequenceError(f'NumberOfTemporalPositions {i + 1}')
                    merge_PWPD[cur_number].append(p)
            self.PWPD = merge_PWPD

        if len(self.PWPD) == 0:
            self.M0 = self.CBF
        elif len(self.PWPD) != cbf_count:
            raise DelayNotEqualSeriesNumberError(delay_count, len(self.PWPD))
        else:
            if type(self.PWPD[0]) != SeriesModel:
                self.M0 = self.PWPD[0]
            else:
                self.M0 = self.PWPD
        self.generate_cbf_3d_pcasl()

    def generate_cbf_3d_pcasl(self):
        m0_image = np.concatenate([i.load() for i in self.M0], axis=3)
        m0_image = m0_image[...,0]      # todo 第一个并不一定是M0，不过M0不参与计算，不影响配准

        cbf_image = np.concatenate([i.load() for i in self.CBF], axis=3)
        cur_series_number = SeriesNumberStartWith.ASL
        write_dicom_series(m0_image, self.M0[0], 'asl-m0', cur_series_number, os.path.join(self.output_root, 'asl', 'm0'))

        for i in range(len(self.CBF)):
            cur_series_number += 1

            write_dicom_series(cbf_image[...,i], self.CBF[0], f'asl-cbf{i+1}', cur_series_number,
                               os.path.join(self.output_root, 'asl', f'cbf{i+1}'))

        super().calc_correct_CBF(cbf_image, self.M0[0], cur_series_number + 1)

    def _gen_mask(self, input_image):
        threshold = 0.5 * np.sum(np.multiply(input_image, input_image)) / np.sum(input_image)
        output_image = np.zeros(np.shape(input_image))
        output_image[input_image >= threshold] = 1
        return output_image