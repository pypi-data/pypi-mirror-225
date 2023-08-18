from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfBorders (SpireObject) :
    """

    """
    @property

    def Left(self)->'PdfPen':
        """
    <summary>
        Gets or sets the left.
    </summary>
<value>The left.</value>
        """
        GetDllLibPdf().PdfBorders_get_Left.argtypes=[c_void_p]
        GetDllLibPdf().PdfBorders_get_Left.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBorders_get_Left(self.Ptr)
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @Left.setter
    def Left(self, value:'PdfPen'):
        GetDllLibPdf().PdfBorders_set_Left.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfBorders_set_Left(self.Ptr, value.Ptr)

    @property

    def Right(self)->'PdfPen':
        """
    <summary>
        Gets or sets the right.
    </summary>
<value>The right.</value>
        """
        GetDllLibPdf().PdfBorders_get_Right.argtypes=[c_void_p]
        GetDllLibPdf().PdfBorders_get_Right.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBorders_get_Right(self.Ptr)
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @Right.setter
    def Right(self, value:'PdfPen'):
        GetDllLibPdf().PdfBorders_set_Right.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfBorders_set_Right(self.Ptr, value.Ptr)

    @property

    def Top(self)->'PdfPen':
        """
    <summary>
        Gets or sets the top.
    </summary>
<value>The top.</value>
        """
        GetDllLibPdf().PdfBorders_get_Top.argtypes=[c_void_p]
        GetDllLibPdf().PdfBorders_get_Top.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBorders_get_Top(self.Ptr)
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @Top.setter
    def Top(self, value:'PdfPen'):
        GetDllLibPdf().PdfBorders_set_Top.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfBorders_set_Top(self.Ptr, value.Ptr)

    @property

    def Bottom(self)->'PdfPen':
        """
    <summary>
        Gets or sets the bottom.
    </summary>
<value>The bottom.</value>
        """
        GetDllLibPdf().PdfBorders_get_Bottom.argtypes=[c_void_p]
        GetDllLibPdf().PdfBorders_get_Bottom.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBorders_get_Bottom(self.Ptr)
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @Bottom.setter
    def Bottom(self, value:'PdfPen'):
        GetDllLibPdf().PdfBorders_set_Bottom.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfBorders_set_Bottom(self.Ptr, value.Ptr)

    @property
    def All(self)->'PdfPen':
        return None

    @All.setter
    def All(self, value:'PdfPen'):
        GetDllLibPdf().PdfBorders_set_All.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfBorders_set_All(self.Ptr, value.Ptr)

    @staticmethod

    def get_Default()->'PdfBorders':
        """
    <summary>
        Gets the default.
    </summary>
<value>The default.</value>
        """
        #GetDllLibPdf().PdfBorders_get_Default.argtypes=[]
        GetDllLibPdf().PdfBorders_get_Default.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBorders_get_Default()
        ret = None if intPtr==None else PdfBorders(intPtr)
        return ret


