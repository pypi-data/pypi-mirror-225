from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfToHtmlParameter (SpireObject) :
    """
    <summary>
        Pdf to html Set Parameter
    </summary>
    """
    @property
    def SplitHtmlNumber(self)->int:
        """
    <summary>
        In 1000 The Split Page,default 1000
    </summary>
        """
        GetDllLibPdf().PdfToHtmlParameter_get_SplitHtmlNumber.argtypes=[c_void_p]
        GetDllLibPdf().PdfToHtmlParameter_get_SplitHtmlNumber.restype=c_int
        ret = GetDllLibPdf().PdfToHtmlParameter_get_SplitHtmlNumber(self.Ptr)
        return ret

    @SplitHtmlNumber.setter
    def SplitHtmlNumber(self, value:int):
        GetDllLibPdf().PdfToHtmlParameter_set_SplitHtmlNumber.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfToHtmlParameter_set_SplitHtmlNumber(self.Ptr, value)

    @property
    def IsEmbedImage(self)->bool:
        """
    <summary>
        wheather embedded image
    </summary>
        """
        GetDllLibPdf().PdfToHtmlParameter_get_IsEmbedImage.argtypes=[c_void_p]
        GetDllLibPdf().PdfToHtmlParameter_get_IsEmbedImage.restype=c_bool
        ret = GetDllLibPdf().PdfToHtmlParameter_get_IsEmbedImage(self.Ptr)
        return ret

    @IsEmbedImage.setter
    def IsEmbedImage(self, value:bool):
        GetDllLibPdf().PdfToHtmlParameter_set_IsEmbedImage.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfToHtmlParameter_set_IsEmbedImage(self.Ptr, value)

