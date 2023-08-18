from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfJavaScript (SpireObject) :
    """
    <summary>
        The Adobe Built-in JavaScript
    </summary>
    """
    @staticmethod

    def GetNumberFormatString(nDec:int,sepStyle:int,negStyle:int,currStyle:int,strCurrency:str,bCurrencyPrepend:bool)->str:
        """
    <summary>
        Get a AFNumber_Format string
    </summary>
    <param name="nDec">The number of places after the decimal point</param>
    <param name="sepStyle">The integer denoting whether to use a separator or not. If sepStyle=0, use commas. If sepStyle=1, do not separate.</param>
    <param name="negStyle">The formatting used for negative numbers: 0 = MinusBlack, 1 = Red, 2 = ParensBlack, 3 = ParensRed</param>
    <param name="currStyle">The currency style - not used</param>
    <param name="strCurrency">The currency symbol</param>
    <param name="bCurrencyPrepend">True to prepend the currency symbol; false to display on the end of the number</param>
        """
        
        GetDllLibPdf().PdfJavaScript_GetNumberFormatString.argtypes=[ c_void_p,c_int,c_int,c_int,c_int,c_wchar_p,c_bool]
        GetDllLibPdf().PdfJavaScript_GetNumberFormatString.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfJavaScript_GetNumberFormatString( None, nDec,sepStyle,negStyle,currStyle,strCurrency,bCurrencyPrepend))
        return ret


    @staticmethod

    def GetNumberKeystrokeString(nDec:int,sepStyle:int,negStyle:int,currStyle:int,strCurrency:str,bCurrencyPrepend:bool)->str:
        """
    <summary>
        Get a AFNumber_Keystroke string
    </summary>
    <param name="nDec">The number of places after the decimal point</param>
    <param name="sepStyle">The integer denoting whether to use a separator or not. If sepStyle=0, use commas. If sepStyle=1, do not separate.</param>
    <param name="negStyle">The formatting used for negative numbers: 0 = MinusBlack, 1 = Red, 2 = ParensBlack, 3 = ParensRed</param>
    <param name="currStyle">The currency style - not used</param>
    <param name="strCurrency">The currency symbol</param>
    <param name="bCurrencyPrepend">True to prepend the currency symbol; false to display on the end of the number</param>
        """
        
        GetDllLibPdf().PdfJavaScript_GetNumberKeystrokeString.argtypes=[ c_void_p,c_int,c_int,c_int,c_int,c_wchar_p,c_bool]
        GetDllLibPdf().PdfJavaScript_GetNumberKeystrokeString.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfJavaScript_GetNumberKeystrokeString(None, nDec,sepStyle,negStyle,currStyle,strCurrency,bCurrencyPrepend))
        return ret


    @staticmethod

    def GetRangeValidateString(bGreaterThan:bool,nGreaterThan:float,bLessThan:bool,nLessThan:float)->str:
        """
    <summary>
        Get a AFRange_Validate string
    </summary>
    <param name="bGreaterThan">Indicate the use of the greater than comparison</param>
    <param name="nGreaterThan">The value to be used in the greater than comparison</param>
    <param name="bLessThan">Indicate the use of the less than comparison</param>
    <param name="nLessThan">The value to be used in the less than comparison</param>
        """
        
        GetDllLibPdf().PdfJavaScript_GetRangeValidateString.argtypes=[ c_void_p,c_bool,c_float,c_bool,c_float]
        GetDllLibPdf().PdfJavaScript_GetRangeValidateString.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfJavaScript_GetRangeValidateString( None, bGreaterThan,nGreaterThan,bLessThan,nLessThan))
        return ret


    @staticmethod

    def GetPercentFormatString(nDec:int,sepStyle:int)->str:
        """
    <summary>
        Get a AFPercent_Format string
    </summary>
    <param name="nDec">The number of places after the decimal point</param>
    <param name="sepStyle">The integer denoting whether to use a separator or not. If sepStyle=0, use commas. If sepStyle=1, do not separate</param>
        """
        
        GetDllLibPdf().PdfJavaScript_GetPercentFormatString.argtypes=[ c_void_p,c_int,c_int]
        GetDllLibPdf().PdfJavaScript_GetPercentFormatString.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfJavaScript_GetPercentFormatString(None, nDec,sepStyle))
        return ret


    @staticmethod

    def GetPercentKeystrokeString(nDec:int,sepStyle:int)->str:
        """
    <summary>
        Get a AFPercent_Keystroke string
    </summary>
    <param name="nDec">The number of places after the decimal point</param>
    <param name="sepStyle">The integer denoting whether to use a separator or not. If sepStyle=0, use commas. If sepStyle=1, do not separate</param>
        """
        
        GetDllLibPdf().PdfJavaScript_GetPercentKeystrokeString.argtypes=[ c_void_p,c_int,c_int]
        GetDllLibPdf().PdfJavaScript_GetPercentKeystrokeString.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfJavaScript_GetPercentKeystrokeString(None, nDec,sepStyle))
        return ret


    @staticmethod

    def GetDateFormatString(cFormat:str)->str:
        """
    <summary>
        Get a AFDate_FormatEx string
    </summary>
    <param name="cFormat">Must be one of: "m/d", "m/d/yy", "mm/dd/yy", "mm/yy", "d-mmm", "d-mmm-yy", "dd-mmm-yy", "yymm-dd", "mmm-yy", "mmmm-yy", "mmm d, yyyy", "mmmm d, yyyy", "m/d/yy h:MM tt", "m/d/yy HH:MM"</param>
        """
        
        GetDllLibPdf().PdfJavaScript_GetDateFormatString.argtypes=[ c_void_p,c_wchar_p]
        GetDllLibPdf().PdfJavaScript_GetDateFormatString.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfJavaScript_GetDateFormatString( None,cFormat))
        return ret


    @staticmethod

    def GetDateKeystrokeString(cFormat:str)->str:
        """
    <summary>
        Get a AFDate_KeystrokeEx string
    </summary>
    <param name="cFormat">Must be one of: "m/d", "m/d/yy", "mm/dd/yy", "mm/yy", "d-mmm", "d-mmm-yy", "dd-mmm-yy", "yymm-dd", "mmm-yy", "mmmm-yy", "mmm d, yyyy", "mmmm d, yyyy", "m/d/yy h:MM tt", "m/d/yy HH:MM"</param>
        """
        
        GetDllLibPdf().PdfJavaScript_GetDateKeystrokeString.argtypes=[ c_void_p,c_wchar_p]
        GetDllLibPdf().PdfJavaScript_GetDateKeystrokeString.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfJavaScript_GetDateKeystrokeString(None, cFormat))
        return ret


    @staticmethod

    def GetTimeFormatString(ptf:int)->str:
        """
    <summary>
        Get a AFTime_Format string
    </summary>
    <param name="ptf">The time format: 0 = 24HR_MM [ 14:30 ], 1 = 12HR_MM [ 2:30 PM ], 2 = 24HR_MM_SS [ 14:30:15 ], 3 = 12HR_MM_SS [ 2:30:15 PM ]</param>
        """
        
        GetDllLibPdf().PdfJavaScript_GetTimeFormatString.argtypes=[ c_void_p,c_int]
        GetDllLibPdf().PdfJavaScript_GetTimeFormatString.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfJavaScript_GetTimeFormatString(None, ptf))
        return ret


    @staticmethod

    def GetTimeKeystrokeString(ptf:int)->str:
        """
    <summary>
        Get a AFTime_Keystroke string
    </summary>
    <param name="ptf">The time format: 0 = 24HR_MM [ 14:30 ], 1 = 12HR_MM [ 2:30 PM ], 2 = 24HR_MM_SS [ 14:30:15 ], 3 = 12HR_MM_SS [ 2:30:15 PM ]</param>
        """
        
        GetDllLibPdf().PdfJavaScript_GetTimeKeystrokeString.argtypes=[ c_void_p,c_int]
        GetDllLibPdf().PdfJavaScript_GetTimeKeystrokeString.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfJavaScript_GetTimeKeystrokeString(None, ptf))
        return ret


    @staticmethod

    def GetSpecialFormatString(psf:int)->str:
        """
    <summary>
        Get a AFSpecial_Format string
    </summary>
    <param name="psf">The type of formatting to use:0 = zip code, 1 = zip + 4, 2 = phone, 3 = SSN</param>
        """
        
        GetDllLibPdf().PdfJavaScript_GetSpecialFormatString.argtypes=[ c_void_p,c_int]
        GetDllLibPdf().PdfJavaScript_GetSpecialFormatString.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfJavaScript_GetSpecialFormatString(None, psf))
        return ret


    @staticmethod

    def GetSpecialKeystrokeString(psf:int)->str:
        """
    <summary>
        Get a AFSpecial_Format string
    </summary>
    <param name="psf">The type of formatting to use:0 = zip code, 1 = zip + 4, 2 = phone, 3 = SSN</param>
        """
        
        GetDllLibPdf().PdfJavaScript_GetSpecialKeystrokeString.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfJavaScript_GetSpecialKeystrokeString.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfJavaScript_GetSpecialKeystrokeString(None, psf))
        return ret


    @staticmethod

    def GetSimpleCalculateString(cFunction:str,cFields:List[str])->str:
        """
    <summary>
        Get a AFSimple_Calculate string
    </summary>
    <param name="cFunction">Must be one of "AVG", "SUM", "PRD", "MIN", "MAX"</param>
    <param name="cFields">The name list of the fields to use in the calculation</param>
        """
        #arraycFields:ArrayTypecFields = ""
        countcFields = len(cFields)
        ArrayTypecFields = c_wchar_p * countcFields
        arraycFields = ArrayTypecFields()
        for i in range(0, countcFields):
            arraycFields[i] = cFields[i]


        GetDllLibPdf().PdfJavaScript_GetSimpleCalculateString.argtypes=[ c_void_p,c_wchar_p,ArrayTypecFields,c_int]
        GetDllLibPdf().PdfJavaScript_GetSimpleCalculateString.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfJavaScript_GetSimpleCalculateString(None, cFunction,arraycFields,countcFields))
        return ret


