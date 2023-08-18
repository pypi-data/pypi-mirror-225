from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfTextExtractOptions (SpireObject) :
    """
    <summary>
        Represents text extraction options
    </summary>
    """
    @property
    def IsSimpleExtraction(self)->bool:
        return None
    @IsSimpleExtraction.setter
    def IsSimpleExtraction(self, value:bool):
        GetDllLibPdf().PdfTextExtractOptions_set_IsSimpleExtraction.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfTextExtractOptions_set_IsSimpleExtraction(self.Ptr, value)

    @property
    def IsExtractAllText(self)->bool:
        return None
    @IsExtractAllText.setter
    def IsExtractAllText(self, value:bool):
        GetDllLibPdf().PdfTextExtractOptions_set_IsExtractAllText.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfTextExtractOptions_set_IsExtractAllText(self.Ptr, value)

    @property
    def IsShowHiddenText(self)->bool:
        return None
    @IsShowHiddenText.setter
    def IsShowHiddenText(self, value:bool):
        GetDllLibPdf().PdfTextExtractOptions_set_IsShowHiddenText.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfTextExtractOptions_set_IsShowHiddenText(self.Ptr, value)

    @property
    def ExtractArea(self)->bool:
        return None
    @ExtractArea.setter
    def ExtractArea(self, value:'RectangleF'):
        GetDllLibPdf().PdfTextExtractOptions_set_ExtractArea.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfTextExtractOptions_set_ExtractArea(self.Ptr, value.Ptr)

