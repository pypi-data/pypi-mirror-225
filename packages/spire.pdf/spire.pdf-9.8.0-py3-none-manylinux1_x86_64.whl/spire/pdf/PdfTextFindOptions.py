from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfTextFindOptions (SpireObject) :
    """
    <summary>
         Represents text search options
    </summary>
    """
    @property
    def Area(self)->'RectangleF':
        return None

    @Area.setter
    def Area(self, value:'RectangleF'):
        GetDllLibPdf().PdfTextFindOptions_set_Area.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfTextFindOptions_set_Area(self.Ptr, value.Ptr)

    @property
    def IsShowHiddenText(self)->bool:
        """
    <summary>
        Whether is show hidden texts.
            default vale: false.
    </summary>
        """
        GetDllLibPdf().PdfTextFindOptions_get_IsShowHiddenText.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextFindOptions_get_IsShowHiddenText.restype=c_bool
        ret = GetDllLibPdf().PdfTextFindOptions_get_IsShowHiddenText(self.Ptr)
        return ret

    @IsShowHiddenText.setter
    def IsShowHiddenText(self, value:bool):
        GetDllLibPdf().PdfTextFindOptions_set_IsShowHiddenText.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfTextFindOptions_set_IsShowHiddenText(self.Ptr, value)

    @property

    def Parameter(self)->'TextFindParameter':
        """
    <summary>
        Specified the text find parameter. Default value : TextFindParameter.None
    </summary>
        """
        GetDllLibPdf().PdfTextFindOptions_get_Parameter.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextFindOptions_get_Parameter.restype=c_int
        ret = GetDllLibPdf().PdfTextFindOptions_get_Parameter(self.Ptr)
        objwraped = TextFindParameter(ret)
        return objwraped

    @Parameter.setter
    def Parameter(self, value:'TextFindParameter'):
        GetDllLibPdf().PdfTextFindOptions_set_Parameter.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfTextFindOptions_set_Parameter(self.Ptr, value.value)

