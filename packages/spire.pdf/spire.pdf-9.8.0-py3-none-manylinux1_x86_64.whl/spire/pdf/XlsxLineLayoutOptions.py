from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class XlsxLineLayoutOptions (  XlsxOptions) :
    @dispatch
    def __init__(self):
        GetDllLibPdf().XlsxLineLayoutOptions_CreateXlsxLineLayoutOptions.restype = c_void_p
        intPtr = GetDllLibPdf().XlsxLineLayoutOptions_CreateXlsxLineLayoutOptions()
        super(XlsxLineLayoutOptions, self).__init__(intPtr)
    @dispatch
    def __init__(self, convertToMultipleSheet:bool , rotatedText:bool , splitCell:bool ):
        GetDllLibPdf().XlsxLineLayoutOptions_CreateXlsxLineLayoutOptionsCRS.argtypes=[c_bool,c_bool,c_bool]
        GetDllLibPdf().XlsxLineLayoutOptions_CreateXlsxLineLayoutOptionsCRS.restype = c_void_p
        intPtr = GetDllLibPdf().XlsxLineLayoutOptions_CreateXlsxLineLayoutOptionsCRS(convertToMultipleSheet,rotatedText,splitCell)
        super(XlsxLineLayoutOptions, self).__init__(intPtr)
    @dispatch
    def __init__(self, convertToMultipleSheet:bool , rotatedText:bool , splitCell:bool ,wrapText:bool):
        GetDllLibPdf().XlsxLineLayoutOptions_CreateXlsxLineLayoutOptionsCRSW.argtypes=[c_bool,c_bool,c_bool,c_bool]
        GetDllLibPdf().XlsxLineLayoutOptions_CreateXlsxLineLayoutOptionsCRSW.restype = c_void_p
        intPtr = GetDllLibPdf().XlsxLineLayoutOptions_CreateXlsxLineLayoutOptionsCRSW(convertToMultipleSheet,rotatedText,splitCell,wrapText)
        super(XlsxLineLayoutOptions, self).__init__(intPtr)
    @dispatch
    def __init__(self, convertToMultipleSheet:bool , rotatedText:bool , splitCell:bool ,wrapText:bool,overlapText:bool):
        GetDllLibPdf().XlsxLineLayoutOptions_CreateXlsxLineLayoutOptionsCRSWO.argtypes=[c_bool,c_bool,c_bool,c_bool,c_bool]
        GetDllLibPdf().XlsxLineLayoutOptions_CreateXlsxLineLayoutOptionsCRSWO.restype = c_void_p
        intPtr = GetDllLibPdf().XlsxLineLayoutOptions_CreateXlsxLineLayoutOptionsCRSWO(convertToMultipleSheet,rotatedText,splitCell,wrapText,overlapText)
        super(XlsxLineLayoutOptions, self).__init__(intPtr)
    """
    <summary>
        Pdf to excel,the options use line layout
    </summary>
    """
