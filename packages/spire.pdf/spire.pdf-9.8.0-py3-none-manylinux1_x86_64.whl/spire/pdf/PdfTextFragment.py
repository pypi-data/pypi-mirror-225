from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfTextFragment (SpireObject) :
    """
    <summary>
        The class representing a result of searching designated text from PDF page.
    </summary>
    """
    @property

    def Text(self)->str:
        """
    <summary>
        Gets the text.
    </summary>
        """
        GetDllLibPdf().PdfTextFragment_get_Text.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextFragment_get_Text.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfTextFragment_get_Text(self.Ptr))
        return ret


    @property

    def LineText(self)->str:
        """
    <summary>
        Gets all text of the line which covers the target text.
    </summary>
        """
        GetDllLibPdf().PdfTextFragment_get_LineText.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextFragment_get_LineText.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfTextFragment_get_LineText(self.Ptr))
        return ret


    @property

    def Page(self)->'PdfPageBase':
        """
    <summary>
        Gets the page where the text is located.
    </summary>
        """
        GetDllLibPdf().PdfTextFragment_get_Page.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextFragment_get_Page.restype=c_void_p
        intPtr = GetDllLibPdf().PdfTextFragment_get_Page(self.Ptr)
        ret = None if intPtr==None else PdfPageBase(intPtr)
        return ret


#    @property
#
#    def Positions(self)->List['PointF']:
#        """
#    <summary>
#        Used by find text cross line
#            if the MatchText in more lines( &gt;=2 ),the results can not contain by one Rectangle.
#            So we need a list to save data.
#            Gets the positions of the searched text of this System.Drawing.PointF structure.
#    </summary>
#        """
#        GetDllLibPdf().PdfTextFragment_get_Positions.argtypes=[c_void_p]
#        GetDllLibPdf().PdfTextFragment_get_Positions.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().PdfTextFragment_get_Positions(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, PointF)
#        return ret


#    @property
#
#    def Bounds(self)->List['RectangleF']:
#        """
#    <summary>
#        if the MatchText in more lines( &gt;=2 ),the results can not contain by one Rectangle.
#            So we need a list to save data.
#            Gets the bounds of the searched text of this System.Drawing RectangleF structure.
#    </summary>
#        """
#        GetDllLibPdf().PdfTextFragment_get_Bounds.argtypes=[c_void_p]
#        GetDllLibPdf().PdfTextFragment_get_Bounds.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().PdfTextFragment_get_Bounds(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, RectangleF)
#        return ret


#    @property
#
#    def Sizes(self)->List['SizeF']:
#        """
#    <summary>
#        Used by find text cross line
#            if the MatchText in more lines( &gt;=2 ),the results can not contain by one Rectangle.
#            So we need a list to save data.
#            Gets the sizes of the searched text of this System.Drawing SizeF structure.
#    </summary>
#        """
#        GetDllLibPdf().PdfTextFragment_get_Sizes.argtypes=[c_void_p]
#        GetDllLibPdf().PdfTextFragment_get_Sizes.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().PdfTextFragment_get_Sizes(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, SizeF)
#        return ret


    @dispatch
    def HighLight(self):
        """
    <summary>
        Highlight the target text.
    </summary>
        """
        GetDllLibPdf().PdfTextFragment_HighLight.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextFragment_HighLight(self.Ptr)

    @dispatch

    def HighLight(self ,color:Color):
        """
    <summary>
        Highlight the target text.
    </summary>
    <param name="color">The hight light color.</param>
        """
        intPtrcolor:c_void_p = color.Ptr

        GetDllLibPdf().PdfTextFragment_HighLightC.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfTextFragment_HighLightC(self.Ptr, intPtrcolor)

