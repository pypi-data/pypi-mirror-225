from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfImageInfo (SpireObject) :
    """
    <summary>
        Represents the utility class to store information about Images and its location.
    </summary>
    """
    @property

    def Bounds(self)->'RectangleF':
        """
    <summary>
        Gets the Image Boundary location.
    </summary>
        """
        GetDllLibPdf().PdfImageInfo_get_Bounds.argtypes=[c_void_p]
        GetDllLibPdf().PdfImageInfo_get_Bounds.restype=c_void_p
        intPtr = GetDllLibPdf().PdfImageInfo_get_Bounds(self.Ptr)
        ret = None if intPtr==None else RectangleF(intPtr)
        return ret


    @property

    def Image(self)->Stream:
        """
    <summary>
        Gets the Image,save to stream.
    </summary>
        """
        GetDllLibPdf().PdfImageInfo_get_Image.argtypes=[c_void_p]
        GetDllLibPdf().PdfImageInfo_get_Image.restype=c_void_p
        intPtr = GetDllLibPdf().PdfImageInfo_get_Image(self.Ptr)
        ret = None if intPtr==None else Stream(intPtr)
        return ret


    @property
    def Index(self)->int:
        """
    <summary>
        Gets the Image index.
    </summary>
        """
        GetDllLibPdf().PdfImageInfo_get_Index.argtypes=[c_void_p]
        GetDllLibPdf().PdfImageInfo_get_Index.restype=c_int
        ret = GetDllLibPdf().PdfImageInfo_get_Index(self.Ptr)
        return ret

    def Dispose(self):
        """
    <summary>
        dispose the image resources
    </summary>
        """
        GetDllLibPdf().PdfImageInfo_Dispose.argtypes=[c_void_p]
        GetDllLibPdf().PdfImageInfo_Dispose(self.Ptr)

