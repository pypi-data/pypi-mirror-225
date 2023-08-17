
import json
import shutil
import subprocess

from ._dicom import *
from ._dicom_util import write_dicom_series
from .data_sorter_base import DataSorterASLBase


class DataSorterSiemensPCASL_old(DataSorterASLBase):
    def __init__(self, data_type, output_root, delay_time, delay_rep, label_dur, series_list, calc_c_cbf):
        DataSorterASLBase.__init__(self, data_type, output_root, delay_time, delay_rep, label_dur, series_list, calc_c_cbf)
        self.delay_time = delay_time # 需要与识别到的TI做对比，所以先使用ms单位
        self.M0: SeriesModel
        self.Control: List[SeriesModel] = []
        self.Label: List[SeriesModel] = []

        for series in self.series_list:
            series_description = series.SeriesDescription.lower()
            if '_ti4000' in series_description:
                if 'ss' in series_description:
                    self.M0 = series
            elif 'ns' in series_description:
                self.Control.append(series)
            elif 'ss' in series_description:
                self.Label.append(series)

    def validate_series(self):
        if not hasattr(self, 'M0'):
            raise MissingSequenceError('M0[ss_TE00_TI4000]')
        if len(self.Control) != len(self.Label):
            raise ControlNotEqualLabelError(len(self.Control), len(self.Label))

        # 序列名后四位是否为数字
        def parse_ti(desc: str):
            split_ti = desc.split('ti')
            try:
                return int(split_ti[1])
            except:
                return 0
        control_delay_map = { parse_ti(s.SeriesDescription.lower()): s for s in self.Control}
        label_delay_map = { parse_ti(s.SeriesDescription.lower()): s for s in self.Label}

        def split_key_value(d):
            keys = []
            values = []
            for k, v in d:
                keys.append(k)
                values.append(v)
            return keys, values
        control_key, control_value = split_key_value(sorted(control_delay_map.items(), key=lambda x:x[0]))
        label_key, label_value = split_key_value(sorted(label_delay_map.items(), key=lambda x:x[0]))

        if len(control_key) != len(control_key):
            raise SeriesError('序列名称不规范')
        if control_key != label_key:
            raise SeriesError(f'Control{control_key}与Label{label_value}的TI不一致')
        if control_key != self.delay_time:
            logger.warning(f'识别到到TI{control_key}与所指定的delay_time{self.delay_time}不一致；将使用识别到的TI进行计算')
            self.delay_time = control_key
        self.delay_time = [i/1000 for i in self.delay_time]
        # 使用排序后的结果
        self.Control = control_value
        self.Label = label_value

        control_delay_rep = [s.Repetition for s in self.Control]
        label_delay_rep = [s.Repetition for s in self.Label]
        if control_delay_rep != label_delay_rep:
            raise SeriesError(f'Control{control_delay_rep}与Label{label_delay_rep}的重复次数不一致')
        if control_delay_rep != self.delay_rep:
            logger.warning(f'识别到到rep{control_delay_rep}与所指定的delay_rep{self.delay_rep}不一致；将使用识别到的结果')
            self.delay_rep = control_delay_rep


    def Sorter(self):
        # super(DataSorterSiemensPCASL_old, self).Sorter()
        self.validate_series()

        java_temp = os.path.join(self.output_root, 'java_temp')
        try:
            reconstructed_dir = self.generate_from_raw_folder(java_temp)

            # 计算完后，得到的2D增强Dicom文件，将其重整为2D Dicom；重写方向，位置标签
            def lambda_load_dicom(name):
                mat = pydicom.read_file(os.path.join(reconstructed_dir, name+'.dcm')).pixel_array
                mat = mat.swapaxes(0, 2)
                return mat.swapaxes(0, 1)

            cur_series_number = SeriesNumberStartWith.ASL
            file_list = ["m0", "mcbf", "att", "acbv", "cbf1", "cbf2", "cbf3", "cbf4"]
            scaling_list = [1, 0.1, 0.01, 0.001, 0.1, 0.1, 0.1, 0.1]
            for f, s in zip(file_list, scaling_list):
                # 防止溢出
                image = lambda_load_dicom(f.upper())
                write_dicom_series(image, self.M0, f'asl-{f}', cur_series_number,
                                   os.path.join(self.output_root, 'asl', f), slope=s)
                cur_series_number += 1
        except Exception as e:
            logger.error(e)
            raise e
        finally:
            shutil.rmtree(java_temp)

    def generate_from_raw_folder(self, temp_dir):
        # print("层数 = {:d}".format(self.slice_num))
        out_put = os.path.join(temp_dir, "reconstructed")
        os.makedirs(os.path.join(temp_dir, "reordered"), exist_ok=True)
        os.makedirs(os.path.join(temp_dir, "reconstructed"), exist_ok=True)
        self._make_json()

        for i, instance in enumerate(self.M0):
            instance.save_as(os.path.join(temp_dir, "reordered", "temp_m0_dcm_{:04d}.dcm".format(i)))

        number = 0
        for ctrl in self.Control:
            for instance in ctrl:
                instance.save_as(os.path.join(temp_dir, "reordered", "temp_ctrl_dcm_{:04d}.dcm".format(number)))
                number += 1

        number = 0
        for label in self.Label:
            for instance in label:
                instance.save_as(os.path.join(temp_dir, "reordered", "temp_lbl_dcm_{:04d}.dcm".format(number)))
                number += 1

        jar_folder = os.path.join(os.getcwd(), "UCLA_java_jar")

        print(jar_folder)
        response = subprocess.run(
            [
                "java", "-jar",
                "-Djava.library.path={}".format(os.path.join(jar_folder, "lib")),
                os.path.join(jar_folder, "ASL_yao_JAVA-master.jar"),
                os.path.join(temp_dir, "param.json")
            ]
        )
        if response.returncode != 0:
            raise Exception("Java程序运行失败，编号: {:d}".format(response.returncode))

        if os.path.isfile(os.path.join(self.output_root, "java_temp", "reconstructed", "finished.txt")):
            logger.debug("完成用Java的图像重建，开始用Python来调整标签")

        return os.path.join(temp_dir, "reconstructed")

    def _make_json(self):
        delay_num = len(self.delay_time)
        if delay_num == 0:
            raise Exception('delay_time is null')
        if delay_num != len(self.delay_rep):
            raise DelayNotEqualRepetitionError(delay_num, len(self.delay_rep))

        param_json_dict = {
            "data_type": '5delay_mosaic' if self.data_type in [MRI_Type.MRI_TYPE_5Delay_3D_PCASL_SIEMENS,
                                                               MRI_Type.MRI_TYPE_1Delay_3D_PCASL_SIEMENS] else '4delay_3d',
            "slice_order": '',
            "slice_num": self.M0.SliceNumber,
            "init_delay": self.delay_time[0],
            "delay_num": delay_num,
            "interval": self.delay_time[1] - self.delay_time[0] if delay_num >= 2 else 0.0,
            "delay_rep": self.delay_rep,
            "load_path": os.path.join(self.output_root, "java_temp", "reordered"),
            "save_path": os.path.join(self.output_root, "java_temp", "reconstructed")}

        with open(os.path.join(self.output_root, "java_temp", "param.json"), "w") as fp:
            json.dump(param_json_dict, fp, indent=4)
        print("json文件保存")

    @staticmethod
    def _3D_to_mosaic(array: np.ndarray):
        width = height = int(np.ceil(array.shape[2]))
        def get_slice(array: np.ndarray, slice: int):
            # 超出范围用 0值填充
            if array.shape[2] > slice:
                return array[:, :, slice]
            else:
                return np.zeros(array[:, :, 0].shape, dtype=array.dtype)

        row_img_vector = []
        for offset in range(width):
            col_index = tuple([i * width + offset for i in range(height)])
            col_img = np.vstack([get_slice(array, c) for c in col_index])
            row_img_vector.append(col_img)

        return np.hstack(row_img_vector)

