from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfCalGrayColor (  PdfComplexColor) :
    """
    <summary>
        Represents a calibrated gray color, based on a CalGray colorspace. 
    </summary>
    """
    @property
    def Gray(self)->float:
        """
    <summary>
        Gets or sets the gray level for this color. 
    </summary>
<value>The gray level of this color.</value>
<remarks>The acceptable range for this value is [0.0 1.0]. 
            0.0 means the darkest color that can be achieved, and 1.0 means the lightest color. </remarks>
        """
        GetDllLibPdf().PdfCalGrayColor_get_Gray.argtypes=[c_void_p]
        GetDllLibPdf().PdfCalGrayColor_get_Gray.restype=c_double
        ret = GetDllLibPdf().PdfCalGrayColor_get_Gray(self.Ptr)
        return ret

    @Gray.setter
    def Gray(self, value:float):
        GetDllLibPdf().PdfCalGrayColor_set_Gray.argtypes=[c_void_p, c_double]
        GetDllLibPdf().PdfCalGrayColor_set_Gray(self.Ptr, value)

