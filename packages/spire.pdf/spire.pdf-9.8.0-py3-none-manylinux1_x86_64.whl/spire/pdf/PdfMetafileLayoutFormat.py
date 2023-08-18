from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfMetafileLayoutFormat (  PdfTextLayout) :
    """

    """
    @property
    def SplitTextLines(self)->bool:
        """

        """
        GetDllLibPdf().PdfMetafileLayoutFormat_get_SplitTextLines.argtypes=[c_void_p]
        GetDllLibPdf().PdfMetafileLayoutFormat_get_SplitTextLines.restype=c_bool
        ret = GetDllLibPdf().PdfMetafileLayoutFormat_get_SplitTextLines(self.Ptr)
        return ret

    @SplitTextLines.setter
    def SplitTextLines(self, value:bool):
        GetDllLibPdf().PdfMetafileLayoutFormat_set_SplitTextLines.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfMetafileLayoutFormat_set_SplitTextLines(self.Ptr, value)

    @property
    def SplitImages(self)->bool:
        """

        """
        GetDllLibPdf().PdfMetafileLayoutFormat_get_SplitImages.argtypes=[c_void_p]
        GetDllLibPdf().PdfMetafileLayoutFormat_get_SplitImages.restype=c_bool
        ret = GetDllLibPdf().PdfMetafileLayoutFormat_get_SplitImages(self.Ptr)
        return ret

    @SplitImages.setter
    def SplitImages(self, value:bool):
        GetDllLibPdf().PdfMetafileLayoutFormat_set_SplitImages.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfMetafileLayoutFormat_set_SplitImages(self.Ptr, value)

