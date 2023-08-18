from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfCheckFieldBase (  PdfStyledField) :
    """
    <summary>
        Represents base class for field which can be in checked and unchecked states.
    </summary>
    """
    @property

    def Style(self)->'PdfCheckBoxStyle':
        """
    <summary>
        Gets or sets the style.
    </summary>
<value>The  object specifies the style of the check box field.</value>
        """
        GetDllLibPdf().PdfCheckFieldBase_get_Style.argtypes=[c_void_p]
        GetDllLibPdf().PdfCheckFieldBase_get_Style.restype=c_int
        ret = GetDllLibPdf().PdfCheckFieldBase_get_Style(self.Ptr)
        objwraped = PdfCheckBoxStyle(ret)
        return objwraped

    @Style.setter
    def Style(self, value:'PdfCheckBoxStyle'):
        GetDllLibPdf().PdfCheckFieldBase_set_Style.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfCheckFieldBase_set_Style(self.Ptr, value.value)

