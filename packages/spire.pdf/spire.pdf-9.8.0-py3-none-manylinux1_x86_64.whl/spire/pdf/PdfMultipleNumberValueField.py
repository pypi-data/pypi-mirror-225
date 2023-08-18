from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfMultipleNumberValueField (  PdfMultipleValueField) :
    """
    <summary>
        Represents automatic field which has the same value within the 
    </summary>
    """
    @property

    def NumberStyle(self)->'PdfNumberStyle':
        """
    <summary>
        Gets or sets the number style.
    </summary>
<value>The number style.</value>
        """
        GetDllLibPdf().PdfMultipleNumberValueField_get_NumberStyle.argtypes=[c_void_p]
        GetDllLibPdf().PdfMultipleNumberValueField_get_NumberStyle.restype=c_int
        ret = GetDllLibPdf().PdfMultipleNumberValueField_get_NumberStyle(self.Ptr)
        objwraped = PdfNumberStyle(ret)
        return objwraped

    @NumberStyle.setter
    def NumberStyle(self, value:'PdfNumberStyle'):
        GetDllLibPdf().PdfMultipleNumberValueField_set_NumberStyle.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfMultipleNumberValueField_set_NumberStyle(self.Ptr, value.value)

