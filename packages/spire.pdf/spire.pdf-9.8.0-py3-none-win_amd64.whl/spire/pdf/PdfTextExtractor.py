from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfTextExtractor (SpireObject) :
    """
    <summary>
        Represent the pdf text extractor.
    </summary>
    """

    def ExtractText(self ,options:'PdfTextExtractOptions')->str:
        """
    <summary>
        Extract text from the page.
    </summary>
    <param name="options">The options.</param>
    <returns>The Extracted Text.</returns>
        """
        intPtroptions:c_void_p = options.Ptr

        GetDllLibPdf().PdfTextExtractor_ExtractText.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfTextExtractor_ExtractText.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfTextExtractor_ExtractText(self.Ptr, intPtroptions))
        return ret


