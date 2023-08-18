from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfToDocConverter (SpireObject) :
    @dispatch
    def __init__(self):
        GetDllLibPdf().PdfToDocConverter_CreatePdfToDocConverter.restype = c_void_p
        intPtr = GetDllLibPdf().PdfToDocConverter_CreatePdfToDocConverter()
        super(PdfToDocConverter, self).__init__(intPtr)
    @dispatch
    def __init__(self, filePath:str):
        GetDllLibPdf().PdfToDocConverter_CreatePdfToDocConverterF.argtypes=[c_wchar_p]
        GetDllLibPdf().PdfToDocConverter_CreatePdfToDocConverterF.restype = c_void_p
        intPtr = GetDllLibPdf().PdfToDocConverter_CreatePdfToDocConverterF(filePath)
        super(PdfToDocConverter, self).__init__(intPtr)

    @dispatch
    def __init__(self, stream:Stream):
        ptrStream:c_void_p = stream.Ptr
        GetDllLibPdf().PdfToDocConverter_CreatePdfToDocConverterS.argtypes=[c_void_p]
        GetDllLibPdf().PdfToDocConverter_CreatePdfToDocConverterS.restype = c_void_p
        intPtr = GetDllLibPdf().PdfToDocConverter_CreatePdfToDocConverterS(ptrStream)
        super(PdfToDocConverter, self).__init__(intPtr)
    """
    <summary>
        This class provides support for converting PDF into an XPS Document.
    </summary>
    """
    @property

    def DocxOptions(self)->'DocxOptions':
        """

        """
        GetDllLibPdf().PdfToDocConverter_get_DocxOptions.argtypes=[c_void_p]
        GetDllLibPdf().PdfToDocConverter_get_DocxOptions.restype=c_void_p
        intPtr = GetDllLibPdf().PdfToDocConverter_get_DocxOptions(self.Ptr)
        ret = None if intPtr==None else DocxOptions(intPtr)
        return ret


    @DocxOptions.setter
    def DocxOptions(self, value:'DocxOptions'):
        GetDllLibPdf().PdfToDocConverter_set_DocxOptions.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfToDocConverter_set_DocxOptions(self.Ptr, value.Ptr)

    @dispatch

    def SaveToDocx(self ,fileStream:Stream):
        """
    <summary>
        Convert to doc/docx document.
    </summary>
    <param name="fileStream">The out file stream.</param>
        """
        intPtrfileStream:c_void_p = fileStream.Ptr

        GetDllLibPdf().PdfToDocConverter_SaveToDocx.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfToDocConverter_SaveToDocx(self.Ptr, intPtrfileStream)

    @dispatch

    def SaveToDocx(self ,fileStream:Stream,isDocx:bool):
        """
    <summary>
        Convert to doc/docx document.
    </summary>
    <param name="fileStream">The out file stream.</param>
    <param name="isDocx">Is docs or doc.</param>
        """
        intPtrfileStream:c_void_p = fileStream.Ptr

        GetDllLibPdf().PdfToDocConverter_SaveToDocxFI.argtypes=[c_void_p ,c_void_p,c_bool]
        GetDllLibPdf().PdfToDocConverter_SaveToDocxFI(self.Ptr, intPtrfileStream,isDocx)

    @dispatch

    def SaveToDocx(self ,filename:str):
        """
    <summary>
        Convert to doc/docx document.
    </summary>
    <param name="filename">The out file name.</param>
        """
        
        GetDllLibPdf().PdfToDocConverter_SaveToDocxF.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfToDocConverter_SaveToDocxF(self.Ptr, filename)

    @dispatch

    def SaveToDocx(self ,filename:str,isDocx:bool):
        """
    <summary>
        Convert to doc/docx document.
    </summary>
    <param name="filename">The out file name.</param>
    <param name="isDocx">Is docs or doc.</param>
        """
        
        GetDllLibPdf().PdfToDocConverter_SaveToDocxFI1.argtypes=[c_void_p ,c_wchar_p,c_bool]
        GetDllLibPdf().PdfToDocConverter_SaveToDocxFI1(self.Ptr, filename,isDocx)

