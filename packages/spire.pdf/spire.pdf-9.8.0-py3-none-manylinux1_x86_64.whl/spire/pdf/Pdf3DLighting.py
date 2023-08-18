from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Pdf3DLighting (SpireObject) :
    @dispatch
    def __init__(self):
        GetDllLibPdf().Pdf3DLighting_CreatePdf3DLighting.restype = c_void_p
        intPtr = GetDllLibPdf().Pdf3DLighting_CreatePdf3DLighting()
        super(Pdf3DLighting, self).__init__(intPtr)
    @dispatch
    def __init__(self, style:Pdf3DLightingStyle):
        enumStyle:c_int = style.value
        GetDllLibPdf().Pdf3DLighting_CreatePdf3DLightingS.argtypes=[c_int]
        GetDllLibPdf().Pdf3DLighting_CreatePdf3DLightingS.restype = c_void_p
        intPtr = GetDllLibPdf().Pdf3DLighting_CreatePdf3DLightingS(enumStyle)
        super(Pdf3DLighting, self).__init__(intPtr)
    """
    <summary>
        Represents the lighting scheme for the 3D artwork.
    </summary>
    """
    @property

    def Style(self)->'Pdf3DLightingStyle':
        """
    <summary>
        Gets or sets the Lighting style of the 3D artwork.
    </summary>
        """
        GetDllLibPdf().Pdf3DLighting_get_Style.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DLighting_get_Style.restype=c_int
        ret = GetDllLibPdf().Pdf3DLighting_get_Style(self.Ptr)
        objwraped = Pdf3DLightingStyle(ret)
        return objwraped

    @Style.setter
    def Style(self, value:'Pdf3DLightingStyle'):
        GetDllLibPdf().Pdf3DLighting_set_Style.argtypes=[c_void_p, c_int]
        GetDllLibPdf().Pdf3DLighting_set_Style(self.Ptr, value.value)

