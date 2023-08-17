
from enum import Enum
from typing import List

from .errors import UnSupportDataTypeError, UnidentifiedOrientationError

UnKnown = 'unknown'

class MANUFACTURER(Enum):
    kMANUFACTURER_SIEMENS = 'SIEMENS'
    kMANUFACTURER_PHILIPS = 'PHILIPS'
    kMANUFACTURER_GE = 'GE MEDICAL SYSTEMS'
    kMANUFACTURER_UIH = 'UIH'

    @staticmethod
    def str2MANUFACTURER(m):
        table = {
            MANUFACTURER.kMANUFACTURER_SIEMENS.value: MANUFACTURER.kMANUFACTURER_SIEMENS,
            MANUFACTURER.kMANUFACTURER_PHILIPS.value: MANUFACTURER.kMANUFACTURER_PHILIPS,
            MANUFACTURER.kMANUFACTURER_GE.value: MANUFACTURER.kMANUFACTURER_GE,
            MANUFACTURER.kMANUFACTURER_UIH.value: MANUFACTURER.kMANUFACTURER_UIH,
        }

        m = m.upper()
        for i in MANUFACTURER:
            if m.find(i.value) > -1:
                return i
        else:
            raise UnSupportDataTypeError(m)

class MODALITY(Enum):
    MODALITY_MR = 'MR'
    MODALITY_CT = 'CT'
    MODALITY_OT = 'OT'

    @staticmethod
    def str2MODALITY(s):
        table = {
            MODALITY.MODALITY_MR.value: MODALITY.MODALITY_MR,
            MODALITY.MODALITY_CT.value: MODALITY.MODALITY_CT,
            MODALITY.MODALITY_OT.value: MODALITY.MODALITY_OT,
        }
        if s in table:
            return table[s]
        else:
            raise UnSupportDataTypeError(s)

class ASL_Type(Enum):
    # MR->ASL
    ASL_PCASL = 'pcasl'
    ASL_PASL = 'pasl'
    ASL_UnKnown = UnKnown

    def startswith(self, s: str):
        self.value.startswith(s)

class DICOM_IMAGE_TYPE(Enum):
    DICOM_IMAGE_TYPE_MOSAIC = 'mosaic'
    DICOM_IMAGE_TYPE_3D = '3d'
    DICOM_IMAGE_TYPE_2D = '2d'
    DICOM_IMAGE_TYPE_UnKnown = UnKnown

class SeriesNumberStartWith():
    ASL = 10000
    T1 = 10010
    T2 = 10020
    T2FLAIR = 10030
    DWI = 10040
    AstrokeReport = 10090
    CereflowReport = 10095


class MRI_Type(Enum):
    # MR type: AnImage custom
    MRI_TYPE_5Delay_3D_PCASL_SIEMENS = '5delay_PCASL_Siemens'
    MRI_TYPE_1Delay_3D_PCASL_SIEMENS = '1delay_PCASL_Siemens'
    MRI_TYPE_4Delay_3D_PCASL_SIEMENS_Old = '4delay_PCASL_Siemens'
    MRI_TYPE_3D_PASL_SIEMENS = '1delay_PASL_Siemens'
    MRI_TYPE_3D_PCASL_GE = '3D_ASL_GE'
    MRI_TYPE_eASL_PCASL_GE = 'eASL_GE'
    MRI_TYPE_3D_PCASL_PHILIPS = 'PCASL_Philips'
    MRI_TYPE_3D_PASL_UIH = 'PASL_UIH'
    MRI_TYPE_UnKnown = 'Unknown'

    MRI_TYPE_T1 = 'T1'
    MRI_TYPE_T2 = 'T2'
    MRI_TYPE_T2_FLAIR = 'T2_FLAIR'
    MRI_TYPE_DWI = 'DWI'

    # MRI_TYPE_ADC = 'ADC'
    def SimpleName(self) -> str:
        if self in [
            MRI_Type.MRI_TYPE_5Delay_3D_PCASL_SIEMENS,
            MRI_Type.MRI_TYPE_1Delay_3D_PCASL_SIEMENS,
            MRI_Type.MRI_TYPE_4Delay_3D_PCASL_SIEMENS_Old,
            MRI_Type.MRI_TYPE_3D_PASL_SIEMENS,
            MRI_Type.MRI_TYPE_3D_PCASL_GE,
            MRI_Type.MRI_TYPE_3D_PCASL_PHILIPS,
            MRI_Type.MRI_TYPE_3D_PASL_UIH,
        ]:
            return 'ASL'
        else:
            return self.value

class SliceDirection(Enum):
    Axial = 'XY' # 轴状面
    Coronal = 'XZ'  # 冠状面
    Sagittal = 'YZ' # 矢状面

    def iSL(self):
        if self == SliceDirection.Axial:
            return 3
        elif self == SliceDirection.Coronal:
            return 2
        elif self == SliceDirection.Sagittal:
            return 1
        else:
            raise UnidentifiedOrientationError('to iSL')

def affine2Orientation(affine: List[float]) -> SliceDirection:
    if len(affine) != 6:
        raise UnidentifiedOrientationError(affine)
    abs_affine = [abs(i) for i in affine] # 忽略正负数（方向），只关注剖面
    first = abs_affine[:3]
    second = abs_affine[3:]
    a = first.index(max(first))
    b = second.index(max(second))
    if a == 0 and b == 1:
        # [ 1 0 0 ]
        # [ 0 1 0 ] 是轴状面
        return SliceDirection.Axial
    elif a == 0 and b == 2:
        # [ 1 0 0 ]
        # [ 0 0 1 ] 是冠状面
        return SliceDirection.Coronal
    elif a == 1 and b == 2:
        # [ 1 0 0 ]
        # [ 0 0 1 ] 是矢状面
        return SliceDirection.Sagittal
    else:
        raise UnidentifiedOrientationError(affine)


SERIES_TYPE_M0 = 'm0'
SERIES_TYPE_CBF = 'asl-cbf'