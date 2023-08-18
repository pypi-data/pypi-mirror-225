from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfLabColor (  PdfComplexColor) :
    """
    <summary>
        Represents a calibrated Lab color, based on a Lab colorspace. 
    </summary>
    """
    @property
    def A(self)->float:
        """
    <summary>
        Gets or sets the a* component for this color. 
    </summary>
<value>The a* component of this color.</value>
<remarks>The range for this value is defined by the Range property of the underlying Lab colorspace. </remarks>
        """
        GetDllLibPdf().PdfLabColor_get_A.argtypes=[c_void_p]
        GetDllLibPdf().PdfLabColor_get_A.restype=c_double
        ret = GetDllLibPdf().PdfLabColor_get_A(self.Ptr)
        return ret

    @A.setter
    def A(self, value:float):
        GetDllLibPdf().PdfLabColor_set_A.argtypes=[c_void_p, c_double]
        GetDllLibPdf().PdfLabColor_set_A(self.Ptr, value)

    @property
    def B(self)->float:
        """
    <summary>
        Gets or sets the b* component for this color. 
    </summary>
<value>The b* component of this color.</value>
<remarks>The range for this value is defined by the Range property of the underlying Lab colorspace. </remarks>
        """
        GetDllLibPdf().PdfLabColor_get_B.argtypes=[c_void_p]
        GetDllLibPdf().PdfLabColor_get_B.restype=c_double
        ret = GetDllLibPdf().PdfLabColor_get_B(self.Ptr)
        return ret

    @B.setter
    def B(self, value:float):
        GetDllLibPdf().PdfLabColor_set_B.argtypes=[c_void_p, c_double]
        GetDllLibPdf().PdfLabColor_set_B(self.Ptr, value)

    @property
    def L(self)->float:
        """
    <summary>
        Gets or sets the l component for this color. 
    </summary>
<value>The l component of this color. </value>
<remarks>The acceptable range for this value is [0.0 100.0]. 0.0 means the darkest color that can be achieved, and 100.0 means the lightest color. </remarks>
        """
        GetDllLibPdf().PdfLabColor_get_L.argtypes=[c_void_p]
        GetDllLibPdf().PdfLabColor_get_L.restype=c_double
        ret = GetDllLibPdf().PdfLabColor_get_L(self.Ptr)
        return ret

    @L.setter
    def L(self, value:float):
        GetDllLibPdf().PdfLabColor_set_L.argtypes=[c_void_p, c_double]
        GetDllLibPdf().PdfLabColor_set_L(self.Ptr, value)

