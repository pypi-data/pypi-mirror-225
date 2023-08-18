from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Utilities_PdfImageInfo (SpireObject) :
    """

    """
    @property

    def Bounds(self)->'RectangleF':
        """
    <summary>
        Gets the Image Boundary location.
    </summary>
        """
        GetDllLibPdf().Utilities_PdfImageInfo_get_Bounds.argtypes=[c_void_p]
        GetDllLibPdf().Utilities_PdfImageInfo_get_Bounds.restype=c_void_p
        intPtr = GetDllLibPdf().Utilities_PdfImageInfo_get_Bounds(self.Ptr)
        ret = None if intPtr==None else RectangleF(intPtr)
        return ret


    @property

    def Image(self)->'Image':
        """
    <summary>
        Gets the Image,save to stream.
    </summary>
        """
        GetDllLibPdf().Utilities_PdfImageInfo_get_Image.argtypes=[c_void_p]
        GetDllLibPdf().Utilities_PdfImageInfo_get_Image.restype=c_void_p
        intPtr = GetDllLibPdf().Utilities_PdfImageInfo_get_Image(self.Ptr)
        ret = None if intPtr==None else Image(intPtr)
        return ret


