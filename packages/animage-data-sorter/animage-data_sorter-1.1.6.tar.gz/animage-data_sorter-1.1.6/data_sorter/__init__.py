
from .old.AnImageDataSorter import ImageDataSort as ImageDataSort1
from .restructure import ImageDataSort as ImageDataSort2

def ImageDataSort(raw_folder, output_path, delay_time, delay_rep, label_dur, pasl_extra_factor, is_restructure=False,
                  calc_c_cbf=False):
    if is_restructure:
        return ImageDataSort2(raw_folder, output_path, delay_time, delay_rep, label_dur, pasl_extra_factor, calc_c_cbf=calc_c_cbf)
    else:
        return ImageDataSort1(raw_folder, output_path, delay_time, delay_rep, label_dur, pasl_extra_factor, zip=False,
                              debugmode=False, modify=0)