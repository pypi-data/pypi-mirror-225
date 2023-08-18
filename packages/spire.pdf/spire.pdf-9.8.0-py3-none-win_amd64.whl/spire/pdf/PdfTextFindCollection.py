from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfTextFindCollection (SpireObject) :
    """
    <summary>
        The class representing all the resuls of searching designated text from PDF page
    </summary>
    """
    @property

    def Finds(self)->List['PdfTextFind']:
        """

        """
        GetDllLibPdf().PdfTextFindCollection_get_Finds.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextFindCollection_get_Finds.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().PdfTextFindCollection_get_Finds(self.Ptr)
        ret = GetObjVectorFromArray(intPtrArray, PdfTextFind)
        return ret


