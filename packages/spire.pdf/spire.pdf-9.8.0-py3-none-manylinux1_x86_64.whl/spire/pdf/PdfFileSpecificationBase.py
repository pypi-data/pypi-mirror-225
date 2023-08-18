from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfFileSpecificationBase (SpireObject) :
    """
    <summary>
        Represents base class for file specification objects.
    </summary>
    """
    @property

    def FileName(self)->str:
        """
    <summary>
        Gets or sets the name of the file.
    </summary>
<value>The name of the file.</value>
        """
        GetDllLibPdf().PdfFileSpecificationBase_get_FileName.argtypes=[c_void_p]
        GetDllLibPdf().PdfFileSpecificationBase_get_FileName.restype=c_wchar_p
        ret = PtrToStr(GetDllLibPdf().PdfFileSpecificationBase_get_FileName(self.Ptr))
        return ret


    @FileName.setter
    def FileName(self, value:str):
        GetDllLibPdf().PdfFileSpecificationBase_set_FileName.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfFileSpecificationBase_set_FileName(self.Ptr, value)

