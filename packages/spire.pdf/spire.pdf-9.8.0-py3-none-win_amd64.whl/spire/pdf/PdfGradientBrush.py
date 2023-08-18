from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfGradientBrush (  PdfBrush) :
    """
    <summary>
        Implements gradient brush capabilities.
    </summary>
    """
    @property

    def Background(self)->'PdfRGBColor':
        """
    <summary>
        Gets or sets the background color of the brush.
    </summary>
<remarks>This value is optional. If null is assigned to it,
            the associated entry is removed from the appropriate dictionary.</remarks>
        """
        GetDllLibPdf().PdfGradientBrush_get_Background.argtypes=[c_void_p]
        GetDllLibPdf().PdfGradientBrush_get_Background.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGradientBrush_get_Background(self.Ptr)
        ret = None if intPtr==None else PdfRGBColor(intPtr)
        return ret


    @Background.setter
    def Background(self, value:'PdfRGBColor'):
        GetDllLibPdf().PdfGradientBrush_set_Background.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfGradientBrush_set_Background(self.Ptr, value.Ptr)

    @property
    def AntiAlias(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether use anti aliasing algorithm.
    </summary>
        """
        GetDllLibPdf().PdfGradientBrush_get_AntiAlias.argtypes=[c_void_p]
        GetDllLibPdf().PdfGradientBrush_get_AntiAlias.restype=c_bool
        ret = GetDllLibPdf().PdfGradientBrush_get_AntiAlias(self.Ptr)
        return ret

    @AntiAlias.setter
    def AntiAlias(self, value:bool):
        GetDllLibPdf().PdfGradientBrush_set_AntiAlias.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfGradientBrush_set_AntiAlias(self.Ptr, value)

    def Dispose(self):
        """

        """
        GetDllLibPdf().PdfGradientBrush_Dispose.argtypes=[c_void_p]
        GetDllLibPdf().PdfGradientBrush_Dispose(self.Ptr)

