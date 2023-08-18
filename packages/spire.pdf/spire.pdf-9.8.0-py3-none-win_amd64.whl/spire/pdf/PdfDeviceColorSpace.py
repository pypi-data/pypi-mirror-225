from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfDeviceColorSpace (  PdfColorSpaces) :
    """
    <summary>
        Represents a device colorspace.
    </summary>
    """
    @property

    def DeviceColorSpaceType(self)->'PdfColorSpace':
        """
    <summary>
        Gets or sets the DeviceColorSpaceType
    </summary>
        """
        GetDllLibPdf().PdfDeviceColorSpace_get_DeviceColorSpaceType.argtypes=[c_void_p]
        GetDllLibPdf().PdfDeviceColorSpace_get_DeviceColorSpaceType.restype=c_int
        ret = GetDllLibPdf().PdfDeviceColorSpace_get_DeviceColorSpaceType(self.Ptr)
        objwraped = PdfColorSpace(ret)
        return objwraped

    @DeviceColorSpaceType.setter
    def DeviceColorSpaceType(self, value:'PdfColorSpace'):
        GetDllLibPdf().PdfDeviceColorSpace_set_DeviceColorSpaceType.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfDeviceColorSpace_set_DeviceColorSpaceType(self.Ptr, value.value)

