from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfToLinearizedPdfConverter (SpireObject) :
    @dispatch
    def __init__(self, filePath:str):
        GetDllLibPdf().PdfToLinearizedPdfConverter_CreatePdfToLinearizedPdfConverterF.argtypes=[c_wchar_p]
        GetDllLibPdf().PdfToLinearizedPdfConverter_CreatePdfToLinearizedPdfConverterF.restype = c_void_p
        intPtr = GetDllLibPdf().PdfToLinearizedPdfConverter_CreatePdfToLinearizedPdfConverterF(filePath)
        super(PdfToLinearizedPdfConverter, self).__init__(intPtr)

    @dispatch
    def __init__(self, stream:Stream):
        ptrStream:c_void_p = stream.Ptr
        GetDllLibPdf().PdfToLinearizedPdfConverter_CreatePdfToLinearizedPdfConverterS.argtypes=[c_void_p]
        GetDllLibPdf().PdfToLinearizedPdfConverter_CreatePdfToLinearizedPdfConverterS.restype = c_void_p
        intPtr = GetDllLibPdf().PdfToLinearizedPdfConverter_CreatePdfToLinearizedPdfConverterS(ptrStream)
        super(PdfToLinearizedPdfConverter, self).__init__(intPtr)
    """

    """
    @dispatch

    def ToLinearizedPdf(self ,filePath:str):
        """
    <summary>
        Convert to linearized pdf document.
    </summary>
    <param name="filePath">The out file path.</param>
        """
        
        GetDllLibPdf().PdfToLinearizedPdfConverter_ToLinearizedPdf.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfToLinearizedPdfConverter_ToLinearizedPdf(self.Ptr, filePath)

    @dispatch

    def ToLinearizedPdf(self ,stream:Stream):
        """
    <summary>
        Convert to linearized pdf document.
    </summary>
    <param name="stream">The out stream.</param>
        """
        intPtrstream:c_void_p = stream.Ptr

        GetDllLibPdf().PdfToLinearizedPdfConverter_ToLinearizedPdfS.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfToLinearizedPdfConverter_ToLinearizedPdfS(self.Ptr, intPtrstream)

    def Dispose(self):
        """

        """
        GetDllLibPdf().PdfToLinearizedPdfConverter_Dispose.argtypes=[c_void_p]
        GetDllLibPdf().PdfToLinearizedPdfConverter_Dispose(self.Ptr)

