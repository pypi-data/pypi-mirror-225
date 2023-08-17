
class DataSortException(Exception):
    errno = 20000
    def __init__(self, msg):
        super().__init__(msg)

class DicomMissingTagError(DataSortException):
    errno = 20001
    def __init__(self, key: tuple) -> None:
        super().__init__('Dicom Missing Tag (0x%04x, 0x%04x)'%(key[0], key[1]))

class CsaHeaderMissingKeyError(DataSortException):
    errno = 20002
    def __init__(self, key) -> None:
        super().__init__(f'Siemens CSA Header Missing Key {key}')

class UnSupportDataTypeError(DataSortException):
    errno = 20003
    def __init__(self, data_type) -> None:
        super().__init__(f'UnSupport DataType {data_type}')

class PhotometricRGBError(DataSortException):
    errno = 20004
    def __init__(self) -> None:
        super().__init__(f'RGB ignore')

class MissingSequenceError(DataSortException):
    errno = 20005
    def __init__(self, sequence_name: str) -> None:
        super().__init__(f'Missing Sequence {sequence_name}')

class MissingSliceError(DataSortException):
    errno = 20006
    def __init__(self, missing_number: int) -> None:
        super().__init__(f'Missing Slice No.{missing_number}')

class SliceLessError(DataSortException):
    errno = 20007
    # 切片数量太少
    def __init__(self, slice_number: int) -> None:
        super().__init__(f'The layer number of too little {slice_number}')

class SpaceIsDifferentError(DataSortException):
    errno = 20008
    # 空间不一致
    def __init__(self, *args) -> None:
        super().__init__(f'{"、".join([str(i) for i in args])} In the same space')

class DiffusionBValueMissingError(DataSortException):
    errno = 20009
    def __init__(self) -> None:
        super().__init__(f'DiffusionBValue Missing')

class UnidentifiedDicomImageTypeError(DataSortException):
    errno = 20010
    # DICOM 图像类型未明确
    def __init__(self) -> None:
        super().__init__(f'Dicom image type is unidentified')

class UnidentifiedOrientationError(DataSortException):
    errno = 20011
    # 方位未明确
    def __init__(self, affine) -> None:
        super().__init__(f'Orientation is unidentified {affine}')

class NotFoundSeriesError(DataSortException):
    errno = 20012
    def __init__(self) -> None:
        super().__init__(f'Not found Series')

class DelayNotEqualSeriesNumberError(DataSortException):
    errno = 20013
    def __init__(self, delay_count: int, series_count) -> None:
        super().__init__(f'PLD输入数量错误，请输入{series_count}个时间点')

class DelayNotEqualRepetitionError(DataSortException):
    errno = 20014
    def __init__(self, delay_count: int, repetition):
        super().__init__(f'The delay must be equal to the number of repetitions：Delay[{delay_count}]，Repetition[{repetition}]')

class ControlNotEqualLabelError(DataSortException):
    errno = 20015
    def __init__(self, control_count: int, label_count: int):
        super().__init__(f'Not Equal：control_count[{control_count}]，label_count[{label_count}]')

class SeriesError(DataSortException):
    errno = 20016
    def __init__(self, msg):
        super().__init__(msg)

class DataQuantityTooManyError(DataSortException):
    errno = 20017
    def __init__(self, c: int):
        super().__init__(f'The amount of data should be less than 1, current[{c}]')

class SeriesTooMany(DataSortException):
    errno = 20018
    def __init__(self, msg):
        super().__init__(msg)

class NeedTwoBValueDWIError(DataSortException):
    errno = 20019
    def __init__(self):
        super().__init__('需要给出2个不同B值的DWI序列')