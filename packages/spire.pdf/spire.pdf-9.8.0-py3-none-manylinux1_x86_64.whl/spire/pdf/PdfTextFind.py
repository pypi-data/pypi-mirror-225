from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfTextFind (SpireObject) :
    """
    <summary>
        The class representing a result of searching designated text from PDF page.
    </summary>
    """
    @property

    def FontName(self)->str:
        """
    <summary>
        Get the actual font name
    </summary>
        """
        GetDllLibPdf().PdfTextFind_get_FontName.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextFind_get_FontName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfTextFind_get_FontName(self.Ptr))
        return ret


    @property

    def OriginalFontName(self)->str:
        """
    <summary>
        Get the original font name
    </summary>
        """
        GetDllLibPdf().PdfTextFind_get_OriginalFontName.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextFind_get_OriginalFontName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfTextFind_get_OriginalFontName(self.Ptr))
        return ret


    @property

    def SearchText(self)->str:
        """
    <summary>
         Gets  search text of this System.String structure.
    </summary>
        """
        GetDllLibPdf().PdfTextFind_get_SearchText.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextFind_get_SearchText.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfTextFind_get_SearchText(self.Ptr))
        return ret


    @property

    def MatchText(self)->str:
        """
    <summary>
        Gets  match text of this System.String structure.
    </summary>
        """
        GetDllLibPdf().PdfTextFind_get_MatchText.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextFind_get_MatchText.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfTextFind_get_MatchText(self.Ptr))
        return ret


    @property

    def OuterText(self)->str:
        """
    <summary>
        Gets  text which is including the searched text of this System.String structure.
    </summary>
        """
        GetDllLibPdf().PdfTextFind_get_OuterText.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextFind_get_OuterText.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfTextFind_get_OuterText(self.Ptr))
        return ret


    @property

    def LineText(self)->str:
        """
    <summary>
        Gets all the text of the line where covers the searched text of this System.String structure .
    </summary>
        """
        GetDllLibPdf().PdfTextFind_get_LineText.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextFind_get_LineText.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfTextFind_get_LineText(self.Ptr))
        return ret


    @property

    def SearchPage(self)->'PdfPageBase':
        """
    <summary>
        Gets page which is including the searched text of this Spire.Pdf.PdfPageBase structure.
    </summary>
        """
        GetDllLibPdf().PdfTextFind_get_SearchPage.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextFind_get_SearchPage.restype=c_void_p
        intPtr = GetDllLibPdf().PdfTextFind_get_SearchPage(self.Ptr)
        ret = None if intPtr==None else PdfPageBase(intPtr)
        return ret


    @property
    def SearchPageIndex(self)->int:
        """
    <summary>
        Gets index of page which is including the searched text of this System.Int32 structure.
    </summary>
        """
        GetDllLibPdf().PdfTextFind_get_SearchPageIndex.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextFind_get_SearchPageIndex.restype=c_int
        ret = GetDllLibPdf().PdfTextFind_get_SearchPageIndex(self.Ptr)
        return ret

    @property

    def Position(self)->'PointF':
        """
    <summary>
         Gets the position of the searched text of this System.Drawing.PointF structure.
    </summary>
        """
        GetDllLibPdf().PdfTextFind_get_Position.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextFind_get_Position.restype=c_void_p
        intPtr = GetDllLibPdf().PdfTextFind_get_Position(self.Ptr)
        ret = None if intPtr==None else PointF(intPtr)
        return ret


#    @property
#
#    def Positions(self)->'List1':
#        """
#    <summary>
#        Used by find text cross line
#            if the MatchText in more lines( &gt;=2 ),the results can not contain by one Rectangle.
#            So we need a list to save data.
#            Gets the positions of the searched text of this System.Drawing.PointF structure.
#    </summary>
#        """
#        GetDllLibPdf().PdfTextFind_get_Positions.argtypes=[c_void_p]
#        GetDllLibPdf().PdfTextFind_get_Positions.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfTextFind_get_Positions(self.Ptr)
#        ret = None if intPtr==None else List1(intPtr)
#        return ret
#


    @property

    def Size(self)->'SizeF':
        """
    <summary>
        if the MatchText in more lines( &gt;=2 ),the results can not contain by one Rectangle.
            So we need a list to save data.
             Gets the size of the searched text of this System.Drawing SizeF structure.
    </summary>
        """
        GetDllLibPdf().PdfTextFind_get_Size.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextFind_get_Size.restype=c_void_p
        intPtr = GetDllLibPdf().PdfTextFind_get_Size(self.Ptr)
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


#    @property
#
#    def Sizes(self)->'List1':
#        """
#    <summary>
#        Used by find text cross line
#            if the MatchText in more lines( &gt;=2 ),the results can not contain by one Rectangle.
#            So we need a list to save data.
#            Gets the sizes of the searched text of this System.Drawing SizeF structure.
#    </summary>
#        """
#        GetDllLibPdf().PdfTextFind_get_Sizes.argtypes=[c_void_p]
#        GetDllLibPdf().PdfTextFind_get_Sizes.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfTextFind_get_Sizes(self.Ptr)
#        ret = None if intPtr==None else List1(intPtr)
#        return ret
#


    @property

    def Bounds(self)->'RectangleF':
        """
    <summary>
        Gets the bounds of the searched text of this System.Drawing RectangleF structure.
    </summary>
        """
        GetDllLibPdf().PdfTextFind_get_Bounds.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextFind_get_Bounds.restype=c_void_p
        intPtr = GetDllLibPdf().PdfTextFind_get_Bounds(self.Ptr)
        ret = None if intPtr==None else RectangleF(intPtr)
        return ret


#    @property
#
#    def Boundses(self)->'List1':
#        """
#    <summary>
#        Used by find text cross line
#            if the MatchText in more lines( &gt;=2 ),the results can not contain by one Rectangle.
#            So we need a list to save data.
#            Gets the bounds of the searched text of this System.Drawing RectangleF structure.
#    </summary>
#        """
#        GetDllLibPdf().PdfTextFind_get_Boundses.argtypes=[c_void_p]
#        GetDllLibPdf().PdfTextFind_get_Boundses.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfTextFind_get_Boundses(self.Ptr)
#        ret = None if intPtr==None else List1(intPtr)
#        return ret
#


#    @property
#
#    def TextBounds(self)->'List1':
#        """
#    <summary>
#        if the MatchText in more lines( &gt;=2 ),the results can not contain by one Rectangle.
#            So we need a list to save data.
#            Gets the bounds of the searched text of this System.Drawing RectangleF structure.
#    </summary>
#        """
#        GetDllLibPdf().PdfTextFind_get_TextBounds.argtypes=[c_void_p]
#        GetDllLibPdf().PdfTextFind_get_TextBounds.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfTextFind_get_TextBounds(self.Ptr)
#        ret = None if intPtr==None else List1(intPtr)
#        return ret
#


    @dispatch
    def HighLight(self):
        """
    <summary>
        Highlight the seached text.
    </summary>
        """
        GetDllLibPdf().PdfTextFind_HighLight.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextFind_HighLight(self.Ptr)

    @dispatch

    def HighLight(self ,color:Color):
        """
    <summary>
        Highlight the seached text.
    </summary>
    <param name="color">The hight light color.</param>
        """
        intPtrcolor:c_void_p = color.Ptr

        GetDllLibPdf().PdfTextFind_HighLightC.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfTextFind_HighLightC(self.Ptr, intPtrcolor)

    @dispatch
    def ApplyHighLight(self):
        """
    <summary>
        apply hight light of the seached text
    </summary>
        """
        GetDllLibPdf().PdfTextFind_ApplyHighLight.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextFind_ApplyHighLight(self.Ptr)

    @dispatch

    def ApplyHighLight(self ,highlightColor:Color):
        """
    <summary>
        Apply hight light of the seached text
    </summary>
    <param name="highlightColor">Hight light color</param>
        """
        intPtrhighlightColor:c_void_p = highlightColor.Ptr

        GetDllLibPdf().PdfTextFind_ApplyHighLightH.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfTextFind_ApplyHighLightH(self.Ptr, intPtrhighlightColor)

    @dispatch

    def ApplyRecoverString(self ,newvalue:str):
        """
    <summary>
        apply hight light of the seached text
    </summary>
        """
        
        GetDllLibPdf().PdfTextFind_ApplyRecoverString.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfTextFind_ApplyRecoverString(self.Ptr, newvalue)

    @dispatch

    def ApplyRecoverString(self ,newvalue:str,unicode:bool):
        """
    <summary>
        apply hight light of the seached text,with unicode
    </summary>
    <param name="newvalue"></param>
    <param name="unicode"></param>
        """
        
        GetDllLibPdf().PdfTextFind_ApplyRecoverStringNU.argtypes=[c_void_p ,c_wchar_p,c_bool]
        GetDllLibPdf().PdfTextFind_ApplyRecoverStringNU(self.Ptr, newvalue,unicode)

    @dispatch

    def ApplyRecoverString(self ,newvalue:str,backColor:Color):
        """
    <summary>
        Apply hight light of the seached text
    </summary>
        """
        intPtrbackColor:c_void_p = backColor.Ptr

        GetDllLibPdf().PdfTextFind_ApplyRecoverStringNB.argtypes=[c_void_p ,c_wchar_p,c_void_p]
        GetDllLibPdf().PdfTextFind_ApplyRecoverStringNB(self.Ptr, newvalue,intPtrbackColor)

    @dispatch

    def ApplyRecoverString(self ,newvalue:str,backColor:Color,unicode:bool):
        """
    <summary>
        apply hight light of the seached text,with unicode
    </summary>
    <param name="newvalue"></param>
    <param name="backColor"></param>
        """
        intPtrbackColor:c_void_p = backColor.Ptr

        GetDllLibPdf().PdfTextFind_ApplyRecoverStringNBU.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_bool]
        GetDllLibPdf().PdfTextFind_ApplyRecoverStringNBU(self.Ptr, newvalue,intPtrbackColor,unicode)

