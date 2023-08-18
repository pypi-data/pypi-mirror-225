from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfMargins (SpireObject) :
    @dispatch
    def __init__(self):
        GetDllLibPdf().PdfMargins_CreatePdfMargins.restype = c_void_p
        intPtr = GetDllLibPdf().PdfMargins_CreatePdfMargins()
        super(PdfMargins, self).__init__(intPtr)
    @dispatch
    def __init__(self, margin:float):
        GetDllLibPdf().PdfMargins_CreatePdfMarginsM.argtypes=[c_float]
        GetDllLibPdf().PdfMargins_CreatePdfMarginsM.restype = c_void_p
        intPtr = GetDllLibPdf().PdfMargins_CreatePdfMarginsM(margin)
        super(PdfMargins, self).__init__(intPtr)

    @dispatch
    def __init__(self, leftRight:float,topBottom:float):
        GetDllLibPdf().PdfMargins_CreatePdfMarginsLT.argtypes=[c_float,c_float]
        GetDllLibPdf().PdfMargins_CreatePdfMarginsLT.restype = c_void_p
        intPtr = GetDllLibPdf().PdfMargins_CreatePdfMarginsLT(leftRight,topBottom)
        super(PdfMargins, self).__init__(intPtr)

    @dispatch
    def __init__(self, left:float,top:float, right:float,bottom:float):
        GetDllLibPdf().PdfMargins_CreatePdfMarginsLTRB.argtypes=[c_float,c_float,c_float,c_float]
        GetDllLibPdf().PdfMargins_CreatePdfMarginsLTRB.restype = c_void_p
        intPtr = GetDllLibPdf().PdfMargins_CreatePdfMarginsLTRB(left,top,right,bottom)
        super(PdfMargins, self).__init__(intPtr)
    """
    <summary>
        A class representing page margins.
    </summary>
    """
    @property
    def Left(self)->float:
        """
    <summary>
        Gets or sets the left margin size.
    </summary>
        """
        GetDllLibPdf().PdfMargins_get_Left.argtypes=[c_void_p]
        GetDllLibPdf().PdfMargins_get_Left.restype=c_float
        ret = GetDllLibPdf().PdfMargins_get_Left(self.Ptr)
        return ret

    @Left.setter
    def Left(self, value:float):
        GetDllLibPdf().PdfMargins_set_Left.argtypes=[c_void_p, c_float]
        GetDllLibPdf().PdfMargins_set_Left(self.Ptr, value)

    @property
    def Top(self)->float:
        """
    <summary>
        Gets or sets the top margin size.
    </summary>
        """
        GetDllLibPdf().PdfMargins_get_Top.argtypes=[c_void_p]
        GetDllLibPdf().PdfMargins_get_Top.restype=c_float
        ret = GetDllLibPdf().PdfMargins_get_Top(self.Ptr)
        return ret

    @Top.setter
    def Top(self, value:float):
        GetDllLibPdf().PdfMargins_set_Top.argtypes=[c_void_p, c_float]
        GetDllLibPdf().PdfMargins_set_Top(self.Ptr, value)

    @property
    def Right(self)->float:
        """
    <summary>
        Gets or sets the right margin size.
    </summary>
        """
        GetDllLibPdf().PdfMargins_get_Right.argtypes=[c_void_p]
        GetDllLibPdf().PdfMargins_get_Right.restype=c_float
        ret = GetDllLibPdf().PdfMargins_get_Right(self.Ptr)
        return ret

    @Right.setter
    def Right(self, value:float):
        GetDllLibPdf().PdfMargins_set_Right.argtypes=[c_void_p, c_float]
        GetDllLibPdf().PdfMargins_set_Right(self.Ptr, value)

    @property
    def Bottom(self)->float:
        """
    <summary>
        Gets or sets the bottom margin size.
    </summary>
        """
        GetDllLibPdf().PdfMargins_get_Bottom.argtypes=[c_void_p]
        GetDllLibPdf().PdfMargins_get_Bottom.restype=c_float
        ret = GetDllLibPdf().PdfMargins_get_Bottom(self.Ptr)
        return ret

    @Bottom.setter
    def Bottom(self, value:float):
        GetDllLibPdf().PdfMargins_set_Bottom.argtypes=[c_void_p, c_float]
        GetDllLibPdf().PdfMargins_set_Bottom(self.Ptr, value)

    @property
    def All(self)->float:
        return 0

    @All.setter
    def All(self, value:float):
        GetDllLibPdf().PdfMargins_set_All.argtypes=[c_void_p, c_float]
        GetDllLibPdf().PdfMargins_set_All(self.Ptr, value)


    def Clone(self)->'SpireObject':
        """
    <summary>
        Clones the object.
    </summary>
    <returns>The cloned object.</returns>
        """
        GetDllLibPdf().PdfMargins_Clone.argtypes=[c_void_p]
        GetDllLibPdf().PdfMargins_Clone.restype=c_void_p
        intPtr = GetDllLibPdf().PdfMargins_Clone(self.Ptr)
        ret = None if intPtr==None else SpireObject(intPtr)
        return ret


