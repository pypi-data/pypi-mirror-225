
import json
import subprocess

import matplotlib
import matplotlib.pyplot as plt

from ._dicom import *
from ._dicom_util import write_dicom_series
from .data_sorter_base import DataSorterASLBase


class DataSorterSiemensPCASL(DataSorterASLBase):
    def __init__(self, data_type, output_root, delay_time, delay_rep, label_dur, series_list, calc_c_cbf):
        DataSorterASLBase.__init__(self, data_type, output_root, delay_time, delay_rep, label_dur, series_list, calc_c_cbf)

        delay_num = len(self.delay_time)
        rep_num = len(self.delay_rep)
        if delay_num != rep_num:
            raise DelayNotEqualRepetitionError(delay_num, rep_num)

        if self.data_type == MRI_Type.MRI_TYPE_5Delay_3D_PCASL_SIEMENS and delay_num != 5:
            raise DelayNotEqualSeriesNumberError(delay_num, 5)
        if self.data_type == MRI_Type.MRI_TYPE_1Delay_3D_PCASL_SIEMENS and delay_num != 1:
            raise DelayNotEqualSeriesNumberError(delay_num, 1)


        # PWI图如果被包含进来，排除掉
        self.raw_series = sorted(series_list, key=lambda x: len(x), reverse=True)[0]

    def Sorter(self):
        super(DataSorterSiemensPCASL, self).Sorter()

        # 单延迟PCASL重新计算重复次数
        if self.data_type == MRI_Type.MRI_TYPE_1Delay_3D_PCASL_SIEMENS:
            self.delay_rep = [self.raw_series.load().shape[-1] // 2 - 1]

        java_temp = os.path.join(self.output_root, 'java_temp')
        try:
            reconstructed_dir = self.generate_from_raw_folder(java_temp)
            self._save_head_motion_graph()

            # 计算完后，得到的2D增强Dicom文件，将其重整为2D Dicom；重写方向，位置标签
            def lambda_load_dicom(name):
                mat = pydicom.read_file(os.path.join(reconstructed_dir, name+'.dcm')).pixel_array
                mat = mat.swapaxes(0, 2)
                return mat.swapaxes(0, 1)

            cur_series_number = SeriesNumberStartWith.ASL
            if len(self.delay_time) == 5:
                param_array = None

                file_list = ["m0", "mcbf", "att", "acbv", "cbf1", "cbf2", "cbf3", "cbf4", "cbf5"]
                scaling_list = [1, 0.1, 0.01, 0.001, 0.1, 0.1, 0.1, 0.1, 0.1]
                for f, s, idx in zip(file_list, scaling_list, range(len(file_list))):
                    image = lambda_load_dicom(f.upper())
                    write_dicom_series(image, self.raw_series, f'asl-{f}', cur_series_number,
                                       os.path.join(self.output_root, 'asl', f), slope=s)
                    cur_series_number += 1

                    if param_array is None:
                        param_array = np.zeros(list(image.shape) + [9])
                    param_array[..., idx] = image

                # 后5个是CBF1-5，第3个是ATT
                super().calc_correct_CBF(param_array[...,-5:] * 0.1, self.raw_series, cur_series_number)

            elif len(self.delay_time) == 1:
                image = lambda_load_dicom('M0')
                write_dicom_series(image, self.raw_series, f'asl-m0', cur_series_number,
                                   os.path.join(self.output_root, 'asl', 'm0'), slope=1)
                cur_series_number += 1

                image = lambda_load_dicom('CBF')
                write_dicom_series(image, self.raw_series, f'asl-cbf1', cur_series_number,
                                   os.path.join(self.output_root, 'asl', 'cbf1'), slope=0.1)

                super().calc_correct_CBF(image * 0.1, self.raw_series, cur_series_number + 1)

        except Exception as e:
            logger.error(e)
            raise e
        finally:
            pass
            # shutil.rmtree(java_temp)

    def generate_from_raw_folder(self, temp_dir):
        if not os.path.exists(temp_dir):
            # print("层数 = {:d}".format(self.slice_num))
            os.makedirs(os.path.join(temp_dir, "reordered"), exist_ok=True)
            os.makedirs(os.path.join(temp_dir, "reconstructed"), exist_ok=True)
            self._make_json()

            for i, instance in enumerate(self.raw_series):
                instance.save_as(os.path.join(temp_dir, "reordered", "temp_dcm_{:04d}.dcm".format(i)))
            jar_folder = os.path.join(os.getcwd(), "UCLA_java_jar")

            print(jar_folder)
            response = subprocess.run(
                [
                    "java", "-jar",
                    "-Djava.library.path={}".format(os.path.join(jar_folder, "lib")),
                    os.path.join(jar_folder, "ASL_yao_JAVA-master.jar"),
                    os.path.join(temp_dir, "param.json")
                ],
                shell=True
            )
            if response.returncode != 0:
                raise Exception("Java程序运行失败，编号: {:d}".format(response.returncode))

            if os.path.isfile(os.path.join(self.output_root, "java_temp", "reconstructed", "finished.txt")):
                logger.debug("完成用Java的图像重建，开始用Python来调整标签")
        else:
            logger.debug('使用已存在的Java临时目录')

        return os.path.join(temp_dir, "reconstructed")

    def _save_head_motion_graph(self):
        file_path = os.path.join(self.output_root, "java_temp", "reconstructed", "headMotion.json")
        save_path = os.path.join(self.output_root, "headMotion.png")
        with open(file_path, 'r') as f:
            data = json.load(f)
        # print(data)
        fig = plt.figure()
        matplotlib.rcParams['font.family'] = "simsun"
        fig.set_size_inches(6, 2)
        xdata = np.linspace(1, len(data["controlFD"]), len(data["controlFD"]))
        plt.plot(xdata, data["controlFD"], 'bo-', label='无标记像')
        plt.plot(xdata, data["labelFD"], 'ro-', label='标记像')
        plt.xticks(xdata)
        plt.xlabel("图片序号")
        plt.ylabel("头动(mm)")
        plt.legend()
        plt.tight_layout()
        plt.savefig(save_path, dpi=200)
        plt.figure().clear()
        plt.close()
        plt.cla()
        plt.clf()

    def _make_json(self):
        self.raw_series: SeriesModel
        delay_num = len(self.delay_time)
        if delay_num == 0:
            raise Exception('delay_time is null')
        if delay_num != len(self.delay_rep):
            raise DelayNotEqualRepetitionError(delay_num, len(self.delay_rep))

        param_json_dict = {
            "data_type": '5delay_mosaic' if self.data_type in [MRI_Type.MRI_TYPE_5Delay_3D_PCASL_SIEMENS,
                                                               MRI_Type.MRI_TYPE_1Delay_3D_PCASL_SIEMENS] else '4delay_3d',
            "slice_order": 'ascending', # 此参数已不重要
            "slice_num": self.raw_series.SliceNumber,
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

