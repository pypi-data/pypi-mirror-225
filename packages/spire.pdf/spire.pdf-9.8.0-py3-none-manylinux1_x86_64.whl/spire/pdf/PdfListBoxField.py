from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfListBoxField (  PdfListField) :
    """
    <summary>
        Represents list box field of the PDF form.
    </summary>
    """
    @property
    def MultiSelect(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether the field is multiselectable.
    </summary>
<value>
  <c>true</c> if multiselectable; otherwise, <c>false</c>.</value>
        """
        GetDllLibPdf().PdfListBoxField_get_MultiSelect.argtypes=[c_void_p]
        GetDllLibPdf().PdfListBoxField_get_MultiSelect.restype=c_bool
        ret = GetDllLibPdf().PdfListBoxField_get_MultiSelect(self.Ptr)
        return ret

    @MultiSelect.setter
    def MultiSelect(self, value:bool):
        GetDllLibPdf().PdfListBoxField_set_MultiSelect.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfListBoxField_set_MultiSelect(self.Ptr, value)

