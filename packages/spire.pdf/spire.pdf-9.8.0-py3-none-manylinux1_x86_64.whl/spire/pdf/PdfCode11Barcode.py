from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfCode11Barcode (  PdfUnidimensionalBarcode) :
    @dispatch
    def __init__(self):
        GetDllLibPdf().PdfCode11Barcode_CreatePdfCode11Barcode.restype = c_void_p
        intPtr = GetDllLibPdf().PdfCode11Barcode_CreatePdfCode11Barcode()
        super(PdfCode11Barcode, self).__init__(intPtr)

    @dispatch
    def __init__(self, text:str):
        GetDllLibPdf().PdfCode11Barcode_CreatePdfCode11BarcodeT.argtypes=[c_wchar_p]
        GetDllLibPdf().PdfCode11Barcode_CreatePdfCode11BarcodeT.restype = c_void_p
        intPtr = GetDllLibPdf().PdfCode11Barcode_CreatePdfCode11BarcodeT(text)
        super(PdfCode11Barcode, self).__init__(intPtr)
    """
    <summary>
        Represents a Code11 barcode.
    </summary>
<remarks> Only the following symbols are allowed in a Code 11 barcode: 0 1 2 3 4 5 6 7 8 9 -</remarks>
    """
