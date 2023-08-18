from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfPaddings (SpireObject) :
    """

    """
    @property
    def Left(self)->float:
        """
    <summary>
        Gets or sets the left.
    </summary>
<value>The left.</value>
        """
        GetDllLibPdf().PdfPaddings_get_Left.argtypes=[c_void_p]
        GetDllLibPdf().PdfPaddings_get_Left.restype=c_float
        ret = GetDllLibPdf().PdfPaddings_get_Left(self.Ptr)
        return ret

    @Left.setter
    def Left(self, value:float):
        GetDllLibPdf().PdfPaddings_set_Left.argtypes=[c_void_p, c_float]
        GetDllLibPdf().PdfPaddings_set_Left(self.Ptr, value)

    @property
    def Right(self)->float:
        """
    <summary>
        Gets or sets the right.
    </summary>
<value>The right.</value>
        """
        GetDllLibPdf().PdfPaddings_get_Right.argtypes=[c_void_p]
        GetDllLibPdf().PdfPaddings_get_Right.restype=c_float
        ret = GetDllLibPdf().PdfPaddings_get_Right(self.Ptr)
        return ret

    @Right.setter
    def Right(self, value:float):
        GetDllLibPdf().PdfPaddings_set_Right.argtypes=[c_void_p, c_float]
        GetDllLibPdf().PdfPaddings_set_Right(self.Ptr, value)

    @property
    def Top(self)->float:
        """
    <summary>
        Gets or sets the top.
    </summary>
<value>The top.</value>
        """
        GetDllLibPdf().PdfPaddings_get_Top.argtypes=[c_void_p]
        GetDllLibPdf().PdfPaddings_get_Top.restype=c_float
        ret = GetDllLibPdf().PdfPaddings_get_Top(self.Ptr)
        return ret

    @Top.setter
    def Top(self, value:float):
        GetDllLibPdf().PdfPaddings_set_Top.argtypes=[c_void_p, c_float]
        GetDllLibPdf().PdfPaddings_set_Top(self.Ptr, value)

    @property
    def Bottom(self)->float:
        """
    <summary>
        Gets or sets the bottom.
    </summary>
<value>The bottom.</value>
        """
        GetDllLibPdf().PdfPaddings_get_Bottom.argtypes=[c_void_p]
        GetDllLibPdf().PdfPaddings_get_Bottom.restype=c_float
        ret = GetDllLibPdf().PdfPaddings_get_Bottom(self.Ptr)
        return ret

    @Bottom.setter
    def Bottom(self, value:float):
        GetDllLibPdf().PdfPaddings_set_Bottom.argtypes=[c_void_p, c_float]
        GetDllLibPdf().PdfPaddings_set_Bottom(self.Ptr, value)

    @property
    def All(self)->float:
        return 0

    @All.setter
    def All(self, value:float):
        GetDllLibPdf().PdfPaddings_set_All.argtypes=[c_void_p, c_float]
        GetDllLibPdf().PdfPaddings_set_All(self.Ptr, value)

