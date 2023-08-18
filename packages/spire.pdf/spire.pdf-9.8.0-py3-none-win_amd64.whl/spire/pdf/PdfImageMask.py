from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfImageMask (  PdfMask) :
    """
    <summary>
        Represents the image mask object for bitmaps.
    </summary>
    """
    @property

    def Mask(self)->'PdfBitmap':
        """
    <summary>
        Gets the image mask.
    </summary>
<value>The image mask.</value>
        """
        GetDllLibPdf().PdfImageMask_get_Mask.argtypes=[c_void_p]
        GetDllLibPdf().PdfImageMask_get_Mask.restype=c_void_p
        intPtr = GetDllLibPdf().PdfImageMask_get_Mask(self.Ptr)
        ret = None if intPtr==None else PdfBitmap(intPtr)
        return ret


    @property
    def SoftMask(self)->bool:
        """
    <summary>
        Gets the mask type.
    </summary>
<value>
  <c>true</c> if soft mask; otherwise, hard mask <c>false</c>.</value>
        """
        GetDllLibPdf().PdfImageMask_get_SoftMask.argtypes=[c_void_p]
        GetDllLibPdf().PdfImageMask_get_SoftMask.restype=c_bool
        ret = GetDllLibPdf().PdfImageMask_get_SoftMask(self.Ptr)
        return ret

