from ._dicom import *
from .errors import DataQuantityTooManyError
from .ge_3d_pcasl import DataSorterGEPCASL
from .ge_easl import DataSorterGEeASL
from .noASL_MRI import *
from .philips_3d_pcasl import DataSorterPhilipsPCASL
from .siemens_3d_pasl import DataSorterSiemensPASL
from .siemens_3d_pcasl import DataSorterSiemensPCASL
from .siemens_3d_pcasl_old import DataSorterSiemensPCASL_old
from .uih_3d_pasl import DataSorterUIHPASL


def AnImageDataSorter(output_root: str, data_type, series_list, delay_time, delay_rep, label_dur, extra_factor=None,
                      default_value_lambda=None, calc_c_cbf=False):
    if default_value_lambda is None:
        default_value_lambda = lambda k, m: []
    try:
        if len(delay_time) == 0:
            delay_time = default_value_lambda(data_type, 0)
        if len(label_dur) == 0:
            label_dur = default_value_lambda(data_type, 1)
        if len(delay_rep) == 0:
            delay_rep = default_value_lambda(data_type, 2)
    except Exception as e:
        if data_type in [MRI_Type.MRI_TYPE_3D_PASL_SIEMENS,
                         MRI_Type.MRI_TYPE_5Delay_3D_PCASL_SIEMENS,
                         MRI_Type.MRI_TYPE_1Delay_3D_PCASL_SIEMENS,
                         MRI_Type.MRI_TYPE_4Delay_3D_PCASL_SIEMENS_Old,
                         MRI_Type.MRI_TYPE_3D_PCASL_PHILIPS,
                         MRI_Type.MRI_TYPE_3D_PCASL_GE,
                         MRI_Type.MRI_TYPE_eASL_PCASL_GE,
                         MRI_Type.MRI_TYPE_3D_PASL_UIH]:
            logger.warning(f'{data_type} 获取ASL参数失败 => {str(e)}')
    if data_type == MRI_Type.MRI_TYPE_3D_PASL_SIEMENS:
        return DataSorterSiemensPASL(data_type, output_root, delay_time, delay_rep, label_dur, series_list, extra_factor, calc_c_cbf)
    elif data_type in [MRI_Type.MRI_TYPE_5Delay_3D_PCASL_SIEMENS, MRI_Type.MRI_TYPE_1Delay_3D_PCASL_SIEMENS]:
        return DataSorterSiemensPCASL(data_type, output_root, delay_time, delay_rep, label_dur, series_list, calc_c_cbf)
    elif data_type == MRI_Type.MRI_TYPE_4Delay_3D_PCASL_SIEMENS_Old:
        return DataSorterSiemensPCASL_old(data_type, output_root, delay_time, delay_rep, label_dur, series_list, calc_c_cbf)
    elif data_type == MRI_Type.MRI_TYPE_3D_PCASL_PHILIPS:
        return DataSorterPhilipsPCASL(data_type, output_root, delay_time, delay_rep, label_dur, series_list, calc_c_cbf)
    elif data_type == MRI_Type.MRI_TYPE_3D_PCASL_GE:
        return DataSorterGEPCASL(data_type, output_root, delay_time, delay_rep, label_dur, series_list, calc_c_cbf)
    elif data_type == MRI_Type.MRI_TYPE_eASL_PCASL_GE:
        return DataSorterGEeASL(data_type, output_root, delay_time, delay_rep, label_dur, series_list, calc_c_cbf)
    elif data_type == MRI_Type.MRI_TYPE_3D_PASL_UIH:
        return DataSorterUIHPASL(data_type, output_root, delay_time, delay_rep, label_dur, series_list, 4, calc_c_cbf)
    elif data_type == MRI_Type.MRI_TYPE_T1:
        return DataSorterT1(data_type, output_root, series_list)
    elif data_type == MRI_Type.MRI_TYPE_T2:
        return DataSorterT2(data_type, output_root, series_list)
    elif data_type == MRI_Type.MRI_TYPE_T2_FLAIR:
        return DataSorterT2FLAIR(data_type, output_root, series_list)
    elif data_type == MRI_Type.MRI_TYPE_DWI:
        return DataSorterDWI(data_type, output_root, series_list)
    else:
        raise UnSupportDataTypeError(data_type)


def check_study_series(series_group_map: Dict[MRI_Type, List[SeriesModel]]):
    count = len(series_group_map)
    if MRI_Type.MRI_TYPE_UnKnown in series_group_map:
        count -= 1
    if MRI_Type.MRI_TYPE_T1 in series_group_map:
        count -= 1
    if MRI_Type.MRI_TYPE_T2 in series_group_map:
        count -= 1
    if MRI_Type.MRI_TYPE_T2_FLAIR in series_group_map:
        count -= 1
    if MRI_Type.MRI_TYPE_DWI in series_group_map:
        count -= 1
    if count > 1:
        raise DataQuantityTooManyError(count)
    # if count == 0:
    #     raise MissingSequenceError('ASL')

def ImageDataSort(src, out, delay_time, delay_rep, label_dur, extra_factor=None, default_value_lambda=None, calc_c_cbf=False):
    sorter_obj = []
    all_study_list = dicom_parse_series(src)

    # 只允许最多一个数据处理
    if len(all_study_list) > 1:
        raise DataQuantityTooManyError(len(all_study_list))

    # 划分可处理单元，每个study包含N个series_group
    for all_series_list in all_study_list.values():
        series_group_map = {}
        for series in all_series_list.values():
            if series.data_type not in series_group_map:
                series_group_map[series.data_type] = []
            series_group_map[series.data_type].append(series)

        # 检查数据中是否符合要求：只包含一组ASL数据
        check_study_series(series_group_map)

        for data_type, series_list in series_group_map.items():
            if data_type == MRI_Type.MRI_TYPE_UnKnown:
                continue
            try:
                sorter = AnImageDataSorter(out, data_type, series_list, delay_time, delay_rep, label_dur, extra_factor,
                                           default_value_lambda=default_value_lambda, calc_c_cbf=calc_c_cbf)
                logger.debug(f'{sorter.data_type} 开始清洗数据')
                sorter.Sorter()
                sorter_obj.append(sorter)
                logger.debug(f'{sorter.data_type} 清洗数据完成')
            except Exception as e:
                logger.error(f'{data_type} 清洗错误=> {e}')
                raise e

    return sorter_obj

if __name__ == '__main__':
    pass

