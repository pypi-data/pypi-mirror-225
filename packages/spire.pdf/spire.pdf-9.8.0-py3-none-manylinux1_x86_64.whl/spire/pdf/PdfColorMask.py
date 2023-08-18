from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfColorMask (  PdfMask) :
    """
    <summary>
        Represents the color mask for bitmaps.
    </summary>
    """
    @property

    def StartColor(self)->'PdfRGBColor':
        """
    <summary>
        Gets or sets the start color.
    </summary>
<value>The start color.</value>
        """
        GetDllLibPdf().PdfColorMask_get_StartColor.argtypes=[c_void_p]
        GetDllLibPdf().PdfColorMask_get_StartColor.restype=c_void_p
        intPtr = GetDllLibPdf().PdfColorMask_get_StartColor(self.Ptr)
        ret = None if intPtr==None else PdfRGBColor(intPtr)
        return ret


    @StartColor.setter
    def StartColor(self, value:'PdfRGBColor'):
        GetDllLibPdf().PdfColorMask_set_StartColor.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfColorMask_set_StartColor(self.Ptr, value.Ptr)

    @property

    def EndColor(self)->'PdfRGBColor':
        """
    <summary>
        Gets or sets the end color.
    </summary>
<value>The end color.</value>
        """
        GetDllLibPdf().PdfColorMask_get_EndColor.argtypes=[c_void_p]
        GetDllLibPdf().PdfColorMask_get_EndColor.restype=c_void_p
        intPtr = GetDllLibPdf().PdfColorMask_get_EndColor(self.Ptr)
        ret = None if intPtr==None else PdfRGBColor(intPtr)
        return ret


    @EndColor.setter
    def EndColor(self, value:'PdfRGBColor'):
        GetDllLibPdf().PdfColorMask_set_EndColor.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfColorMask_set_EndColor(self.Ptr, value.Ptr)

