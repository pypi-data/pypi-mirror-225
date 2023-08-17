from ._dicom import *
from typing import Tuple, Optional
from ._dicom_util import write_dicom_series

class DataSorterBase:
    def __init__(self, data_type, output_root, series_list: List[SeriesModel]):
        self.output_root = output_root
        # 排个序
        self.series_list = sorted(series_list, key=lambda x: x.SeriesNumber)
        self.data_type = data_type
        logger.info(f'识别类型：{data_type}')

    def _validate_series_base(self):
        for i in range(len(self.series_list)):
            self.series_list[i].validate_series()

    def Sorter(self):
        # 清洗前需要基本验证：是否缺图像、是否完整、是否断层...
        self._validate_series_base()

class DataSorterASLBase(DataSorterBase):
    def __init__(self, data_type, output_root, delay_time, delay_rep, label_dur, series_list, calc_c_cbf):
        DataSorterBase.__init__(self, data_type, output_root, series_list)
        self.delay_time = [i / 1000 for i in delay_time]  # 外部单位毫秒， 内部单位秒
        self.delay_rep = delay_rep
        self.label_dur = [i / 1000 for i in label_dur]
        self.calc_c_cbf = calc_c_cbf

        logger.debug(f'[{data_type}] 延迟时间：{delay_time}')
        logger.debug(f'[{data_type}] 标记时长：{label_dur}')
        logger.debug(f'[{data_type}] 重复次数：{delay_rep}')

    def get_PLD_millisecond(self):
        '''
        获取PLD时间, 毫秒单位需要乘以1000
        :return:
        '''
        return [int(i * 1000) for i in self.delay_time]

    def calc_correct_CBF(self, CBF_array: np.ndarray, ref_series: SeriesModel, series_number:int,
                         ATT_array: Optional[np.ndarray] = None):
        '''
        拥有ATT的ASL使用ATT校准CBF，没有ATT的使用多CBF对应体素最大值校准ATT，并输出CBF_PLD图
        :param CBF_array:
        :param ref_series:
        :param series_number:
        :param ATT_array:
        :return:
        '''
        if not self.calc_c_cbf:
            return
        if len(CBF_array.shape) < 4 or CBF_array.shape[3] == 1:
            logger.warning('单PLD无需校正')
            return

        targets = np.array(self.delay_time, str)
        if ATT_array is None:
            # 寻找多个CBF最大的那个
            corr_CBF = np.maximum.reduce(CBF_array, 3)
            write_dicom_series(corr_CBF * 10, ref_series, f'asl-corr-cbf', series_number,
                               os.path.join(self.output_root, 'asl', 'corr-cbf'), slope=0.1)

            # CBF_pld_index = np.argmax(CBF_array, 3)
            # CBF_pld_map = targets[CBF_pld_index]

            # write_dicom_series(CBF_pld_map * 1000, ref_series, f'asl-corr-att', series_number,
            #                    os.path.join(self.output_root, 'asl', 'corr-att'), dtype=np.float32, slope=0.001)

        else:
            is_back = True
            def back_function(x):
                for idx, num in enumerate(self.delay_time):
                    if num >= x or (x - num) < 0.01:
                        return idx
                return len(self.delay_time) - 1
            def near_function(x):
                abs_diff = np.abs(targets - x)
                return int(np.argmin(abs_diff))


            # 使用 np.vectorize() 创建向量化函数
            vectorized_function = np.vectorize(back_function if is_back else near_function)
            CBF_pld_index = vectorized_function(ATT_array)

            corr_CBF = np.zeros(CBF_pld_index.shape, dtype=np.float32)
            for i in range(len(self.delay_time)):
                corr_CBF[CBF_pld_index == i] = CBF_array[...,i][CBF_pld_index == i]

            write_dicom_series(corr_CBF * 10, ref_series, f'asl-corr-cbf', series_number,
                               os.path.join(self.output_root, 'asl', 'corr-cbf'), slope=0.1)

            # 使用索引获取最接近的目标数组元素的值
            # CBF_pld_map = targets[CBF_pld_index]
            # write_dicom_series(CBF_pld_map * 1000, ref_series, f'asl-corr-att', series_number,
            #                    os.path.join(self.output_root, 'asl', 'corr-att'), dtype=np.float32, slope=0.001)

