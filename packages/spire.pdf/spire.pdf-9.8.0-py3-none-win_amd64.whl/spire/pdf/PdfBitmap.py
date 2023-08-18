from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfBitmap (  PdfImage) :
    """
    <summary>
        Represents the bitmap images.
    </summary>
    """
    @property
    def ActiveFrame(self)->int:
        """
    <summary>
        Gets or sets the active frame of the bitmap.
    </summary>
<value>The active frame index.</value>
        """
        GetDllLibPdf().PdfBitmap_get_ActiveFrame.argtypes=[c_void_p]
        GetDllLibPdf().PdfBitmap_get_ActiveFrame.restype=c_int
        ret = GetDllLibPdf().PdfBitmap_get_ActiveFrame(self.Ptr)
        return ret

    @ActiveFrame.setter
    def ActiveFrame(self, value:int):
        GetDllLibPdf().PdfBitmap_set_ActiveFrame.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfBitmap_set_ActiveFrame(self.Ptr, value)

    @property
    def FrameCount(self)->int:
        """
    <summary>
        Gets the number of frames in the bitmap.
    </summary>
<value>The frame count.</value>
        """
        GetDllLibPdf().PdfBitmap_get_FrameCount.argtypes=[c_void_p]
        GetDllLibPdf().PdfBitmap_get_FrameCount.restype=c_int
        ret = GetDllLibPdf().PdfBitmap_get_FrameCount(self.Ptr)
        return ret

    @property

    def Mask(self)->'PdfMask':
        """
    <summary>
        Gets or sets the mask of bitmap.
    </summary>
<value>New PdfMask.</value>
        """
        GetDllLibPdf().PdfBitmap_get_Mask.argtypes=[c_void_p]
        GetDllLibPdf().PdfBitmap_get_Mask.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBitmap_get_Mask(self.Ptr)
        ret = None if intPtr==None else PdfMask(intPtr)
        return ret


    @Mask.setter
    def Mask(self, value:'PdfMask'):
        GetDllLibPdf().PdfBitmap_set_Mask.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfBitmap_set_Mask(self.Ptr, value.Ptr)

    @property
    def Quality(self)->int:
        """
    <summary>
        Gets or sets the quality.
            The range is from 0 to 100, 100 is the best quality.
    </summary>
<remarks>
            When the image is stored into PDF not as a mask,
            you may reduce its quality, which saves the disk space.
            </remarks>
        """
        GetDllLibPdf().PdfBitmap_get_Quality.argtypes=[c_void_p]
        GetDllLibPdf().PdfBitmap_get_Quality.restype=c_long
        ret = GetDllLibPdf().PdfBitmap_get_Quality(self.Ptr)
        return ret

    @Quality.setter
    def Quality(self, value:int):
        GetDllLibPdf().PdfBitmap_set_Quality.argtypes=[c_void_p, c_long]
        GetDllLibPdf().PdfBitmap_set_Quality(self.Ptr, value)

    def Dispose(self):
        """
    <summary>
        Performs application-defined tasks associated with freeing,
            releasing, or resetting unmanaged resources.
    </summary>
        """
        GetDllLibPdf().PdfBitmap_Dispose.argtypes=[c_void_p]
        GetDllLibPdf().PdfBitmap_Dispose(self.Ptr)

