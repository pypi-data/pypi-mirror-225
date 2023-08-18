from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfPageLabels (SpireObject) :
    @dispatch
    def __init__(self):
        GetDllLibPdf().PdfPageLabels_CreatePdfPageLabels.restype = c_void_p
        intPtr = GetDllLibPdf().PdfPageLabels_CreatePdfPageLabels()
        super(PdfPageLabels, self).__init__(intPtr)
    """
    <summary>
        The document’s labeling ranges.
    </summary>
    """
    @dispatch

    def AddRange(self ,indexOfFirstPage:int,numberStyle:str,prefix:str):
        """
    <summary>
        Add labeling range which is a series of consecutive pages using the same numbering system.
    </summary>
    <param name="indexOfFirstPage">
            the page index of the first page in the labeling range.
    </param>
    <param name="numberStyle">
            The numbering style to be used for the numeric portion of each page label.
            As follow:
            Decimal_Arabic_Numerals/Uppercase_Roman_Numerals/Lowercase_Roman_Numerals/Uppercase_Letters/Lowercase_Letters
    </param>
    <param name="prefix">
            The label prefix for page labels in the labeling range.
    </param>
        """
        
        GetDllLibPdf().PdfPageLabels_AddRange.argtypes=[c_void_p ,c_int,c_wchar_p,c_wchar_p]
        GetDllLibPdf().PdfPageLabels_AddRange(self.Ptr, indexOfFirstPage,numberStyle,prefix)

    @dispatch

    def AddRange(self ,indexOfFirstPage:int,numberStyle:str,prefix:str,numberOfFirstPage:int):
        """
    <summary>
        Add labeling range which is a series of consecutive pages using the same numbering system.
    </summary>
    <param name="indexOfFirstPage">
            the page index of the first page in the labeling range.
    </param>
    <param name="numberStyle">
            The numbering style to be used for the numeric portion of each page label.
            As follow:
            Decimal_Arabic_Numerals/Uppercase_Roman_Numerals/Lowercase_Roman_Numerals/Uppercase_Letters/Lowercase_Letters
    </param>
    <param name="prefix">
            The label prefix for page labels in the labeling range.
    </param>
    <param name="numberOfFirstPage">
            The value of the numeric portion for the first page label in the range. 
            Subsequent pages are numbered sequentially from this value, which must be greater than or equal to 1. Default value: 1.
    </param>
        """
        
        GetDllLibPdf().PdfPageLabels_AddRangeINPN.argtypes=[c_void_p ,c_int,c_wchar_p,c_wchar_p,c_int]
        GetDllLibPdf().PdfPageLabels_AddRangeINPN(self.Ptr, indexOfFirstPage,numberStyle,prefix,numberOfFirstPage)


    def GetPageLabel(self ,index:int)->str:
        """
    <summary>
        Get page label.
    </summary>
    <param name="index">The page index.</param>
    <returns>The page label.</returns>
        """
        
        GetDllLibPdf().PdfPageLabels_GetPageLabel.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfPageLabels_GetPageLabel.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfPageLabels_GetPageLabel(self.Ptr, index))
        return ret


    @staticmethod

    def Decimal_Arabic_Numerals_Style()->str:
        """
    <summary>
        Decimal arabic numerals style to be used for the numeric portion of each page label.
    </summary>
        """
        #GetDllLibPdf().PdfPageLabels_Decimal_Arabic_Numerals_Style.argtypes=[]
        GetDllLibPdf().PdfPageLabels_Decimal_Arabic_Numerals_Style.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfPageLabels_Decimal_Arabic_Numerals_Style())
        return ret


    @staticmethod

    def Uppercase_Roman_Numerals_Style()->str:
        """
    <summary>
        Uppercase roman numerals style to be used for the numeric portion of each page label.
    </summary>
        """
        #GetDllLibPdf().PdfPageLabels_Uppercase_Roman_Numerals_Style.argtypes=[]
        GetDllLibPdf().PdfPageLabels_Uppercase_Roman_Numerals_Style.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfPageLabels_Uppercase_Roman_Numerals_Style())
        return ret


    @staticmethod

    def Lowercase_Roman_Numerals_Style()->str:
        """
    <summary>
        Lowercase roman numerals style to be used for the numeric portion of each page label.
    </summary>
        """
        #GetDllLibPdf().PdfPageLabels_Lowercase_Roman_Numerals_Style.argtypes=[]
        GetDllLibPdf().PdfPageLabels_Lowercase_Roman_Numerals_Style.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfPageLabels_Lowercase_Roman_Numerals_Style())
        return ret


    @staticmethod

    def Uppercase_Letters_Style()->str:
        """
    <summary>
        Uppercase letters style to be used for the numeric portion of each page label.
    </summary>
        """
        #GetDllLibPdf().PdfPageLabels_Uppercase_Letters_Style.argtypes=[]
        GetDllLibPdf().PdfPageLabels_Uppercase_Letters_Style.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfPageLabels_Uppercase_Letters_Style())
        return ret


    @staticmethod

    def Lowercase_Letters_Style()->str:
        """
    <summary>
        Lowercase letters style to be used for the numeric portion of each page label.
    </summary>
        """
        #GetDllLibPdf().PdfPageLabels_Lowercase_Letters_Style.argtypes=[]
        GetDllLibPdf().PdfPageLabels_Lowercase_Letters_Style.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfPageLabels_Lowercase_Letters_Style())
        return ret


