from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfGrayConverter (SpireObject) :
    @dispatch
    def __init__(self, filePath:str):
        GetDllLibPdf().PdfGrayConverter_CreatePdfGrayConverterF.argtypes=[c_wchar_p]
        GetDllLibPdf().PdfGrayConverter_CreatePdfGrayConverterF.restype = c_void_p
        intPtr = GetDllLibPdf().PdfGrayConverter_CreatePdfGrayConverterF(filePath)
        super(PdfGrayConverter, self).__init__(intPtr)

    @dispatch
    def __init__(self, stream:Stream):
        ptrStream:c_void_p = stream.Ptr
        GetDllLibPdf().PdfGrayConverter_CreatePdfGrayConverterS.argtypes=[c_void_p]
        GetDllLibPdf().PdfGrayConverter_CreatePdfGrayConverterS.restype = c_void_p
        intPtr = GetDllLibPdf().PdfGrayConverter_CreatePdfGrayConverterS(ptrStream)
        super(PdfGrayConverter, self).__init__(intPtr)
    """
    <summary>
        The gray pdf conveter.
    </summary>
    """
    @dispatch

    def ToGrayPdf(self ,filePath:str):
        """
    <summary>
        Convert to gray pdf document.
    </summary>
    <param name="filePath">The out file path.</param>
        """
        
        GetDllLibPdf().PdfGrayConverter_ToGrayPdf.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfGrayConverter_ToGrayPdf(self.Ptr, filePath)

    @dispatch

    def ToGrayPdf(self ,stream:Stream):
        """
    <summary>
        Convert to gray pdf document.
    </summary>
    <param name="stream">The out stream.</param>
        """
        intPtrstream:c_void_p = stream.Ptr

        GetDllLibPdf().PdfGrayConverter_ToGrayPdfS.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfGrayConverter_ToGrayPdfS(self.Ptr, intPtrstream)

    def Dispose(self):
        """

        """
        GetDllLibPdf().PdfGrayConverter_Dispose.argtypes=[c_void_p]
        GetDllLibPdf().PdfGrayConverter_Dispose(self.Ptr)

