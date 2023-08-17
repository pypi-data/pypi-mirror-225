"""
梳理上传过来的DICOM数据为各种ASL数据和其他数据
Version 2.03.04

2022-02-01：1.03.04 => 2.03.04：修改逻辑，T1、T2、DWI、CTP、ASL作为第一层
2021-11-19，增加了接受后延迟标记重复的参数
2021-11-14，替换了原理应用UCLA输出到自己编译的java的JAR包，时间缩短了狠很多
姚泽山
"""

import pydicom
import sys
import os
import shutil
from .AnImageDataSorterSiemens5 import AnImageDataSorterSiemens5
from .AnImageDataSorterSiemens4 import AnImageDataSorterSiemens4
from .AnImageDataSorterSiemensPASL import AnImageDataSorterSiemensPASL
from .AnImageDataSorterGEeASL7 import AnImageDataSorterGE7
from .AnImageDataSorterGEpCASL13 import AnImageDataSorterGE13
from .AnImageDataSorterPhilips13 import AnImageDataSorterPhilips13
from data_sorter.old import AnImageDataSorterMISC
import json


class AnImageDataSorter:

    def __init__(self):

        self.raw_folder = os.path.join(os.getcwd(), '输入', 'Siemens-5delay-raw')
        self.archive_folder = os.path.join(os.getcwd(), '输入', 'Siemens-5delay-archive')
        self.intermediate_folder = os.path.join(os.getcwd(), 'md')
        self.output_path = os.path.join(os.getcwd(), 'AnImage输出')

        self.archive_bottom_folder = ''
        self.data_type = ''
        self.slice_num = 0
        self.raw_data_dict = {}
        self.ge7 = False
        self.asl_type = ''
        self.asl_institution = ''
        self.seriesdelay = 5
        self.delay_time = []
        self.delay_rep = []
        self.label_dur = []
        self.debugMode = False
        self.nonzip = True
        self.series_group_asl = {}
        self.seriesdic = {}
        self.seriesm0 = []
        self.seriesm02 = []
        self.seriescbf = []
        self.seriesadc = []
        self.seriesacbv = []
        self.seriesatt = []
        self.seriesmcbf = []
        self.seriesdwi = []
        self.seriest1 = []
        self.seriest2 = []
        self.seriesatt = []
        self.seriessuv = []
        self.pasl_extra_factor = None
        self.modify = 0

    def set_path(self):
        self.raw_folder = sys.argv[1]
        self.output_path = sys.argv[2]
        try:
            self.archive_bottom_folder = sys.argv[3]
        except:
            self.archive_bottom_folder = ''

    def DebugmodeOn(self):
        self.debugMode = True

    def DebugmodeOff(self):
        self.debugMode = False

    def ZipOff(self):
        self.nonzip = True

    def ZipOn(self):
        self.nonzip = False

    def perform_sorting(self):
        if self.seriessuv:
            AnImageDataSorterMISC.parse_suv_from_archive_folder(self.intermediate_folder, self.seriessuv)

        if self.seriesdwi:
            AnImageDataSorterMISC.parse_dwi_from_archive_folder(self.intermediate_folder, self.seriesdwi,
                                                                self.data_type)

        if self.seriesadc:
            AnImageDataSorterMISC.parse_adc_from_archive_folder(self.intermediate_folder, self.seriesadc)

        if self.seriest1:
            AnImageDataSorterMISC.parse_t1_from_archive_folder(self.intermediate_folder, self.seriest1)

        if self.seriest2:
            AnImageDataSorterMISC.parse_t2_from_archive_folder(self.intermediate_folder, self.seriest2)

        for dict_key in self.series_group_asl.keys():  # 不同序列
            print(dict_key)

            for series_time_key in self.series_group_asl[dict_key].keys():  # 多延迟eASL若多次出现
                if dict_key == "GE_7_eASL":
                    aids = AnImageDataSorterGE7()
                    aids.Sorter(self.intermediate_folder, folder_suffix = str(series_time_key),
                                seriesdic=self.series_group_asl[dict_key][series_time_key],
                                delay_time=self.delay_time, label_dur=self.label_dur)

                if dict_key == "GE_1_pCASL":
                    aids = AnImageDataSorterGE13()
                    aids.Sorter(self.intermediate_folder,
                                series=self.series_group_asl[dict_key][series_time_key])

                if dict_key == "WangJJ_pCASL":
                    aids = AnImageDataSorterSiemens5()
                    aids.Sorter(self.intermediate_folder, self.series_group_asl[dict_key][series_time_key]["RAW"],
                                delay_time=self.delay_time, delay_rep=self.delay_rep)

                if dict_key == "WangJJ_pCASL_old":
                    aids = AnImageDataSorterSiemens4()
                    aids.Sorter(self.intermediate_folder, series_dic=self.series_group_asl[dict_key][series_time_key],
                                delay_time=self.delay_time, delay_rep=self.delay_rep)

                if dict_key == "SI_1_PASL":
                    aids = AnImageDataSorterSiemensPASL()
                    print("启动PASL分析程序")
                    aids.Sorter(self.intermediate_folder, self.series_group_asl[dict_key][series_time_key],
                                delay_time=self.delay_time, delay_rep=self.delay_rep, label_dur=self.label_dur,
                                extra_factor=self.pasl_extra_factor)

                if dict_key == "PH_1_pCASL":
                    aids = AnImageDataSorterPhilips13()
                    aids.Sorter(self.intermediate_folder, series=self.series_group_asl[dict_key][series_time_key])

                # TODO 需要梳理
                # elif self.data_type == 'SIEMENS':
                #     # 若采用了美国的以前的代码的输出，这里会有不同的灌注文件
                #     if series_group[0] == 'UCLA':
                #         aids = AnImageDataSorterSiemens_UCLA()
                #         aids.Sorter(self.intermediate_folder, self.seriesm0, self.seriesdelay,
                #                     init_delay=self.delay_time, seriescbf=self.seriescbf,
                #                     seriesacbv=self.seriesacbv, seriesatt=self.seriesatt, seriesmcbf=self.seriesmcbf)
                #     elif 1 <= series_group[0] <= 3:
                #         aids = AnImageDataSorterSiemens13()
                #         aids.Sorter(self.intermediate_folder, self.seriesm0, self.seriesdelay,
                #                     init_delay=self.delay_time, delay_rep=self.delay_rep)
                #     elif series_group[0] == 'PASL':
                #         aids = AnImageDataSorterSiemensPASL()
                #         aids.Sorter(self.intermediate_folder, self.seriesm0, self.seriesdelay,
                #                     init_delay=self.delay_time, delay_rep=self.delay_rep)
                #

        if not self.nonzip:
            shutil.make_archive(self.output_path, 'zip', self.intermediate_folder)
            self.delete_intermediate()

    def check_zipped(self):
        if self.archive_bottom_folder == 'nonzip':
            self.nonzip = True
        self.create_intermediate()

    def create_intermediate(self):
        if self.nonzip:
            self.intermediate_folder = self.output_path
        os.makedirs(self.intermediate_folder, exist_ok=True)

    def delete_intermediate(self):
        shutil.rmtree(self.intermediate_folder)

    def validate_series(self, input_series_list):
        series_list = input_series_list
        output_series = []
        # 查看每一个series
        for series_idx in series_list:
            detected_asl_type = []
            recognize_flag = False
            target_series = self.raw_data_dict[series_idx]
            temp = self._from_dict_read_dicom_meta(series_idx)
            print('序列名称: ' + temp[0x0008, 0x103e].value)

            # 排除彩色图和图片数少于15的
            try:
                slice_number = temp[0x0019, 0x100A].value
            except:
                slice_number = len(target_series)
            if 'MONOCHROME' not in (temp[(0x0028, 0x0004)].value if (0x0028, 0x0004) in temp else ''):
                print('series is not grayscale, not included ' + temp[0x0008, 0x103e].value)
            elif slice_number < 11:
                print('series has less than 15 slices, not included')

            else:
                # 检查ASL之外的
                if 'T1' in target_series[0].upper() or 'FSPGR' in target_series[0].upper() or \
                        ("AA" in target_series[0].upper() and "SCOUT" in target_series[0].upper()):
                    recognize_flag = True
                    self.seriest1.append(target_series)

                elif 'T2' in target_series[0].upper() and '3' not in target_series[0]:
                    recognize_flag = True
                    self.seriest2.append(target_series)

                elif 'ADC' in target_series[0] and 'eADC' not in target_series[0]:
                    recognize_flag = True
                    detected_asl_type = "ADC"
                    self.seriesadc.append(target_series)

                elif 'Apparent Diffusion Coefficient' in target_series[0] and 'Exponential' not in target_series[0]:
                    recognize_flag = True
                    detected_asl_type = "ADC"
                    self.seriesadc.append(target_series)

                elif 'DWI' in target_series[0] or 'TRACEW' in target_series[0]:
                    recognize_flag = True
                    self.seriesdwi.append(target_series)

                elif [0x0054, 0x0016] in temp and 'FDG' in temp[0x0054, 0x0016][0]:
                    recognize_flag = True
                    self.seriessuv.append(target_series)

                # 检查飞利浦的ASL
                if self.data_type == 'Philips':
                    if 'SOURCE' in target_series[0]:
                        recognize_flag = True
                        self._dictionary_helper_function("PH_1_pCASL", "M0", target_series)

                    elif '3D_pCASL' in target_series[0]:
                        recognize_flag = True
                        self._dictionary_helper_function("PH_1_pCASL", "CBF", target_series)

                # 检查通用电气的ASL
                elif self.data_type == 'GE MEDICAL SYSTEMS':

                    # GE 多延迟
                    if 'eASL' in target_series[0]:

                        try:
                            series_time = int(temp[0x0008, 0x0031].value)
                        except:
                            series_time = 0
                        if series_time not in self.seriesdic.keys():
                            self.seriesdic[series_time] = {}

                        if 'Raw' in target_series[0]:
                            recognize_flag = True
                            detected_asl_type = "eASL_RAW"
                            self._dictionary_helper_function("GE_7_eASL", "RAW", target_series, series_time)

                        elif 'Transit delay' in target_series[0]:
                            recognize_flag = True
                            detected_asl_type = "eASL_ATT"
                            self._dictionary_helper_function("GE_7_eASL", "ATT", target_series, series_time)

                        elif 'Transit corrected' in target_series[0].replace('-', ' '):
                            recognize_flag = True
                            detected_asl_type = "eASL_CBF"
                            self._dictionary_helper_function("GE_7_eASL", "CORR_CBF", target_series, series_time)
                        elif 'CBF' in target_series[0].replace('Flow', 'CBF'):
                            recognize_flag = True
                            detected_asl_type = "eASL_CBF"
                            self._dictionary_helper_function("GE_7_eASL", "STAN_CBF", target_series, series_time)

                    # GE 单延迟
                    else:
                        if 'ASL' in target_series[0] or '3D ASL' in target_series[0]:
                            recognize_flag = True
                            target_series[0] = [target_series[0], temp[0x0018, 0x0082].value]  # 增加后延迟时间的标识
                            self._dictionary_helper_function("GE_1_pCASL", "PWPD", target_series)

                        elif 'CBF' in target_series[0] or 'Cerebral Blood Flow' in target_series[0]:
                            recognize_flag = True
                            detected_asl_type = "3DASL_CBF"
                            target_series[0] = [target_series[0], temp[0x0018, 0x0082].value]  # 增加后延迟时间的标识
                            self._dictionary_helper_function("GE_1_pCASL", "CBF", target_series)

                elif self.data_type == 'SIEMENS':
                    if "parameter_fit" in target_series[0].lower():
                        detected_asl_type = "PASL"
                        recognize_flag = True
                        self._dictionary_helper_function("SI_1_PASL", "PARAMETER_FIT", target_series)

                    elif "pd_tse" in target_series[0].lower() or \
                            ("m0" in target_series[0].lower() and "tgse" not in target_series[0].lower()):
                        detected_asl_type = "PASL"
                        recognize_flag = True
                        self._dictionary_helper_function("SI_1_PASL", "3DPASL_M0", target_series)
                    elif "asl_3d_tra" in target_series[0].lower():
                        detected_asl_type = "PASL"
                        recognize_flag = True
                        self._dictionary_helper_function("SI_1_PASL", "3DPASL_PERF", target_series)
                    elif "asl_2d_tra" in target_series[0].lower():
                        detected_asl_type = "PASL"
                        recognize_flag = True
                        self._dictionary_helper_function("SI_1_PASL", "2DPASL_RAW", target_series)

                    elif "tgse_pcasl" in target_series[0].lower():
                        detected_asl_type = "WangJJ_pCASL"
                        recognize_flag = True
                        self._dictionary_helper_function("WangJJ_pCASL", "RAW", target_series)

                    elif "_te00" in target_series[0].lower():
                        if "_ti4000" in target_series[0].lower():
                            if "ss" in target_series[0].lower():
                                self._dictionary_helper_function("WangJJ_pCASL_old", "M0", target_series)
                                detected_asl_type = "WangJJ_pCASL_old"
                                recognize_flag = True
                        else:
                            delay_time = int(target_series[0].lower().split("ti")[1])
                            if "ns" in target_series[0].lower():
                                target_series[0] = [target_series[0], delay_time]  # 增加后延迟时间的标识
                                self._dictionary_helper_function("WangJJ_pCASL_old", "Control", target_series)
                                detected_asl_type = "WangJJ_pCASL_old"
                                recognize_flag = True
                            elif "ss" in target_series[0].lower():
                                target_series[0] = [target_series[0], delay_time]  # 增加后延迟时间的标识
                                self._dictionary_helper_function("WangJJ_pCASL_old", "Label", target_series)
                                detected_asl_type = "WangJJ_pCASL_old"
                                recognize_flag = True

            # 数据是否被识别
            if not recognize_flag:
                print('文件被排除')

            # 若被识别查看图片数量
            else:
                print("文件识别成功")
                expected_num = [len(self.raw_data_dict[series_idx]) - 1]

                if detected_asl_type == "3DASL_CBF":
                    expected_num = [expected_num[0] * 2]
                elif detected_asl_type == "eASL_CBF":
                    expected_num = [expected_num[0] * 10, expected_num[0] / 7 * 10]
                elif detected_asl_type == "eASL_ATT":
                    expected_num = [expected_num[0] * 10]
                elif detected_asl_type == "eASL_RAW":
                    expected_num = [expected_num[0] / 9 * 10]
                elif detected_asl_type == "ADC":
                    expected_num = [expected_num[0] * 2]

                try:
                    slice_num = temp[0x0020, 0x1002].value
                except:
                    print("slice number not found, assume complete")
                    slice_num = expected_num[0]

                if slice_num not in expected_num:
                    raise Exception('slice missing!')

                output_series.append(target_series[0])

        # TODO 这里需要修改，应该不需要了
        for key in list(self.seriesdic.keys()):
            if not self.seriesdic.get(key):
                del self.seriesdic[key]

        self.seriesdelay = len(self.seriesm0)

        return output_series

        # if self.data_type == 'SIEMENS':
        #     for series_idx in series_list:
        #
        #         if self.raw_data_dict[series_idx][0].lower().startswith('tgse_pcasl') or self.raw_data_dict[series_idx][
        #             0] == 'Parameter_Fit':
        #             self.seriesm0 = self.raw_data_dict[series_idx]
        #
        #         elif self.raw_data_dict[series_idx][0] == 'MoCoSeries':  # 针对友谊医院的2DPASL+M0，头动校正后的数据
        #             self.seriesm0 = self.raw_data_dict[series_idx]
        #
        #         elif 'acbv' in self.raw_data_dict[series_idx][0] and (
        #                 'NonMosaic' in self.raw_data_dict[series_idx][0] or 'asl-' in self.raw_data_dict[series_idx][
        #             0]):
        #             self.seriesacbv = self.raw_data_dict[series_idx]
        #
        #         elif 'att' in self.raw_data_dict[series_idx][0] and (
        #                 'NonMosaic' in self.raw_data_dict[series_idx][0] or 'asl-' in self.raw_data_dict[series_idx][
        #             0]):
        #             self.seriesatt = self.raw_data_dict[series_idx]
        #
        #         elif 'mcbf' in self.raw_data_dict[series_idx][0] and (
        #                 'NonMosaic' in self.raw_data_dict[series_idx][0] or 'asl-' in self.raw_data_dict[series_idx][
        #             0]):
        #             self.seriesmcbf = self.raw_data_dict[series_idx]
        #
        #         elif 'cbf' in self.raw_data_dict[series_idx][0] and (
        #                 'NonMosaic' in self.raw_data_dict[series_idx][0] or 'asl-' in self.raw_data_dict[series_idx][
        #             0]):
        #             self.seriescbf.append(self.raw_data_dict[series_idx])
        #
        #     if len(self.seriesm0) == 27:
        #         self.seriesdelay = 5
        #     elif len(self.seriesm0) == 23 or len(self.seriesm0) == 17:
        #         self.seriesdelay = 1
        #     elif len(self.seriesm0) == 10 and self.seriesm0[0] == 'Parameter_Fit':
        #         self.seriesdelay = 2
        #     elif len(self.seriesm0) == 92 and self.seriesm0[0] == "MoCoSeries":
        #         print("察觉到了友谊医院2DPASL单延迟")
        #         self.seriesdelay = 1
        #     else:
        #         raise Exception("Invalid Number of Siemens Files!")

    def sort_files_and_check_patient(self):
        input_path = self.raw_folder
        file_list = [os.path.join(dp, f) for dp, dn, filenames in os.walk(input_path) for f in filenames]
        patientdate = 0
        patienttime = 0
        PatientInfo = {}
        PatientInfo['PatientName'] = ''
        PatientInfo['PatientBirthDate'] = ''
        PatientInfo['PatientSex'] = ''
        PatientInfo['PatientAge'] = ''
        PatientInfo['PatientWeight'] = ''
        PatientInfo['SeriesDate'] = ''
        PatientInfo['SeriesTime'] = ''
        for file_idx in range(len(file_list)):
            try:
                image_data = pydicom.dcmread(file_list[file_idx], stop_before_pixels=True)
            except:
                continue
            try:
                if patientdate == 0 or patientdate > image_data[0x0008, 0x0021].value:
                    patientdate = image_data[0x0008, 0x0021].value
                    patienttime = image_data[0x0008, 0x0032].value
                elif patientdate == image_data[0x0008, 0x0021].value:
                    if patienttime == 0 or patienttime > image_data[0x0008, 0x0032].value:
                        patienttime = image_data[0x0008, 0x0032].value
            except:
                patientdate = 0
                patienttime = 0
            if not PatientInfo['PatientName']:
                try:
                    PatientInfo['PatientName'] = str(image_data.PatientName)
                except:
                    PatientInfo['PatientName'] = ''
            if not PatientInfo['PatientBirthDate']:
                try:
                    PatientInfo['PatientBirthDate'] = str(image_data.PatientBirthDate)
                except:
                    PatientInfo['PatientBirthDate'] = ''
            if not PatientInfo['PatientSex']:
                try:
                    PatientInfo['PatientSex'] = str(image_data.PatientSex)
                except:
                    PatientInfo['PatientSex'] = ''
            if not PatientInfo['PatientAge']:
                try:
                    PatientInfo['PatientAge'] = str(image_data.PatientAge)
                except:
                    PatientInfo['PatientAge'] = ''
            if not PatientInfo['PatientWeight']:
                try:
                    PatientInfo['PatientWeight'] = str(image_data.PatientWeight)
                except:
                    PatientInfo['PatientWeight'] = ''
            if not PatientInfo['SeriesDate'] and patientdate != 0:
                try:
                    PatientInfo['SeriesDate'] = str(patientdate)
                except:
                    PatientInfo['SeriesDate'] = ''
            if not PatientInfo['SeriesTime'] and patienttime != 0:
                try:
                    PatientInfo['SeriesTime'] = str(patienttime)
                except:
                    PatientInfo['SeriesTime'] = ''

            if self.data_type == '':
                try:
                    self.data_type = image_data[0x0008, 0x0070].value
                except:
                    self.data_type = ''
            else:
                if [0x0008, 0x0070] in image_data and image_data[0x0008, 0x0070].value != self.data_type:
                    raise Exception("Multi-Manufacturer	in One Series!")

            if [0x0020, 0x0013] in image_data and (self.data_type != 'Philips' or (
                    self.data_type == 'Philips' and image_data[0x0020, 0x0100].value == 1)):
                try:
                    series_desc = str(image_data[0x0008, 0x103E].value)
                except:
                    series_desc = 'temp1234567890'
                series_uid = str(image_data[0x0020, 0x000E].value)
                try:
                    instance_num = int(image_data[0x0020, 0x0013].value)
                except:
                    instance_num = 1
                if series_desc != 'temp1234567890':
                    if series_uid not in self.raw_data_dict.keys():
                        self.raw_data_dict[series_uid] = {}
                        self.raw_data_dict[series_uid][int(0)] = series_desc
                    if 'MoCo_' in series_desc or 'asl-' in series_desc:
                        self.raw_data_dict[series_uid][instance_num + 1] = file_list[file_idx]
                    else:
                        self.raw_data_dict[series_uid][instance_num] = file_list[file_idx]

        json_str = json.dumps(PatientInfo)
        with open(os.path.join(self.intermediate_folder, 'patient.json'), 'w') as json_file:
            json_file.write(json_str)

        series_list = list(self.raw_data_dict.keys())
        return series_list

    def _from_dict_read_dicom_meta(self, series_idx):
        try:
            temp = pydicom.dcmread(self.raw_data_dict[series_idx][1],
                                   stop_before_pixels=True)
        except:
            temp = pydicom.dcmread([i for i in self.raw_data_dict[series_idx].values()][1],
                                   stop_before_pixels=True)
        return temp

    def _dictionary_helper_function(self, asl_type, input_string, target_series, series_time=9999):
        if asl_type not in self.series_group_asl.keys():
            self.series_group_asl[asl_type] = {}
        if series_time not in self.series_group_asl[asl_type].keys():
            self.series_group_asl[asl_type][series_time] = {}
        if input_string not in self.series_group_asl[asl_type][series_time].keys():
            self.series_group_asl[asl_type][series_time][input_string] = []
        self.series_group_asl[asl_type][series_time][input_string].append(target_series)


def ImageDataSort(raw_folder, output_path, delay_time, delay_rep, label_dur, pasl_extra_factor, zip=True, debugmode=False, modify=0):
    ImageSorterClass = AnImageDataSorter()
    ImageSorterClass.modify = modify
    ImageSorterClass.nonzip = not zip
    ImageSorterClass.debugMode = debugmode
    ImageSorterClass.raw_folder = raw_folder
    ImageSorterClass.output_path = output_path
    for i in range(len(delay_time)):
        delay_time[i] = delay_time[i]/1000
    ImageSorterClass.delay_time = delay_time
    ImageSorterClass.delay_rep = delay_rep
    for i in range(len(label_dur)):
        label_dur[i] = label_dur[i]/1000
    ImageSorterClass.label_dur = label_dur
    ImageSorterClass.check_zipped()
    ImageSorterClass.pasl_extra_factor = pasl_extra_factor
    all_series_list = ImageSorterClass.sort_files_and_check_patient()
    # print(json.dumps(all_series_list, sort_keys=True, indent=4))
    valid_series_list = ImageSorterClass.validate_series(all_series_list)
    print(json.dumps(valid_series_list, sort_keys=True, indent=4))
    ImageSorterClass.perform_sorting()
    return 0


if __name__ == "__main__":
    raw_folder = r'D:\WorkDir\DataSet\Sorter_test\GE_1pld'
    output_path = r'D:\WorkDir\DataSet\Sorter_test\GE_1pld'
    delay_time = []
    delay_rep = []
    label_dur = []
    ImageDataSort(raw_folder, output_path, delay_time, delay_rep, label_dur, 8)
