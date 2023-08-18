from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfFontBase (SpireObject) :
    """
    <summary>
        Represents the font.
    </summary>
    """
    def Dispose(self):
        """

        """
        GetDllLibPdf().PdfFontBase_Dispose.argtypes=[c_void_p]
        GetDllLibPdf().PdfFontBase_Dispose(self.Ptr)

    @property

    def Name(self)->str:
        """
    <summary>
        Gets the name.
    </summary>
<value>The name.</value>
        """
        GetDllLibPdf().PdfFontBase_get_Name.argtypes=[c_void_p]
        GetDllLibPdf().PdfFontBase_get_Name.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfFontBase_get_Name(self.Ptr))
        return ret


    @property
    def Size(self)->float:
        """
    <summary>
        Gets the size.
    </summary>
<value>The size.</value>
        """
        GetDllLibPdf().PdfFontBase_get_Size.argtypes=[c_void_p]
        GetDllLibPdf().PdfFontBase_get_Size.restype=c_float
        ret = GetDllLibPdf().PdfFontBase_get_Size(self.Ptr)
        return ret

    @property
    def Height(self)->float:
        """
    <summary>
        Gets the height of the font in points.
    </summary>
        """
        GetDllLibPdf().PdfFontBase_get_Height.argtypes=[c_void_p]
        GetDllLibPdf().PdfFontBase_get_Height.restype=c_float
        ret = GetDllLibPdf().PdfFontBase_get_Height(self.Ptr)
        return ret

    @property
    def Descent(self)->float:
        """
    <summary>
        Gets the descent of the font in points.
    </summary>
        """
        GetDllLibPdf().PdfFontBase_get_Descent.argtypes=[c_void_p]
        GetDllLibPdf().PdfFontBase_get_Descent.restype=c_float
        ret = GetDllLibPdf().PdfFontBase_get_Descent(self.Ptr)
        return ret

    @property

    def Style(self)->'PdfFontStyle':
        """
    <summary>
        Gets the style information for this font.
    </summary>
        """
        GetDllLibPdf().PdfFontBase_get_Style.argtypes=[c_void_p]
        GetDllLibPdf().PdfFontBase_get_Style.restype=c_int
        ret = GetDllLibPdf().PdfFontBase_get_Style(self.Ptr)
        objwraped = PdfFontStyle(ret)
        return objwraped

    @property
    def Bold(self)->bool:
        """
    <summary>
        Gets a value indicating whether this  is bold.
    </summary>
<value>
  <c>true</c> if bold; otherwise, <c>false</c>.</value>
        """
        GetDllLibPdf().PdfFontBase_get_Bold.argtypes=[c_void_p]
        GetDllLibPdf().PdfFontBase_get_Bold.restype=c_bool
        ret = GetDllLibPdf().PdfFontBase_get_Bold(self.Ptr)
        return ret

    @property
    def Italic(self)->bool:
        """
    <summary>
        Gets a value indicating whether this  is italic.
    </summary>
<value>
  <c>true</c> if italic; otherwise, <c>false</c>.</value>
        """
        GetDllLibPdf().PdfFontBase_get_Italic.argtypes=[c_void_p]
        GetDllLibPdf().PdfFontBase_get_Italic.restype=c_bool
        ret = GetDllLibPdf().PdfFontBase_get_Italic(self.Ptr)
        return ret

    @property
    def Strikeout(self)->bool:
        """
    <summary>
        Gets a value indicating whether this  is strikeout.
    </summary>
<value>
  <c>true</c> if strikeout; otherwise, <c>false</c>.</value>
        """
        GetDllLibPdf().PdfFontBase_get_Strikeout.argtypes=[c_void_p]
        GetDllLibPdf().PdfFontBase_get_Strikeout.restype=c_bool
        ret = GetDllLibPdf().PdfFontBase_get_Strikeout(self.Ptr)
        return ret

    @property
    def Underline(self)->bool:
        """
    <summary>
        Gets a value indicating whether this  is underline.
    </summary>
<value>
  <c>true</c> if underline; otherwise, <c>false</c>.</value>
        """
        GetDllLibPdf().PdfFontBase_get_Underline.argtypes=[c_void_p]
        GetDllLibPdf().PdfFontBase_get_Underline.restype=c_bool
        ret = GetDllLibPdf().PdfFontBase_get_Underline(self.Ptr)
        return ret

    @dispatch

    def MeasureString(self ,text:str)->SizeF:
        """
    <summary>
        Measures a string by using this font.
    </summary>
    <param name="text">Text to be measured.</param>
    <returns>Size of the text.</returns>
        """
        
        GetDllLibPdf().PdfFontBase_MeasureString.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfFontBase_MeasureString.restype=c_void_p
        intPtr = GetDllLibPdf().PdfFontBase_MeasureString(self.Ptr, text)
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @dispatch

    def MeasureString(self ,text:str,format:PdfStringFormat)->SizeF:
        """
    <summary>
        Measures a string by using this font.
    </summary>
    <param name="text">Text to be measured.</param>
    <param name="format">PdfStringFormat that represents formatting information, such as line spacing, for the string.</param>
    <returns>Size of the text.</returns>
        """
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfFontBase_MeasureStringTF.argtypes=[c_void_p ,c_wchar_p,c_void_p]
        GetDllLibPdf().PdfFontBase_MeasureStringTF.restype=c_void_p
        intPtr = GetDllLibPdf().PdfFontBase_MeasureStringTF(self.Ptr, text,intPtrformat)
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


#    @dispatch
#
#    def MeasureString(self ,text:str,format:PdfStringFormat,charactersFitted:'Int32&',linesFilled:'Int32&')->SizeF:
#        """
#
#        """
#        intPtrformat:c_void_p = format.Ptr
#        intPtrcharactersFitted:c_void_p = charactersFitted.Ptr
#        intPtrlinesFilled:c_void_p = linesFilled.Ptr
#
#        GetDllLibPdf().PdfFontBase_MeasureStringTFCL.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_void_p]
#        GetDllLibPdf().PdfFontBase_MeasureStringTFCL.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfFontBase_MeasureStringTFCL(self.Ptr, text,intPtrformat,intPtrcharactersFitted,intPtrlinesFilled)
#        ret = None if intPtr==None else SizeF(intPtr)
#        return ret
#


    @dispatch

    def MeasureString(self ,text:str,width:float)->SizeF:
        """
    <summary>
        Measures a string by using this font.
    </summary>
    <param name="text">Text to be measured.</param>
    <param name="width">Maximum width of the string in points.</param>
    <returns>Size of the text.</returns>
        """
        
        GetDllLibPdf().PdfFontBase_MeasureStringTW.argtypes=[c_void_p ,c_wchar_p,c_float]
        GetDllLibPdf().PdfFontBase_MeasureStringTW.restype=c_void_p
        intPtr = GetDllLibPdf().PdfFontBase_MeasureStringTW(self.Ptr, text,width)
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @dispatch

    def MeasureString(self ,text:str,width:float,format:PdfStringFormat)->SizeF:
        """
    <summary>
        Measures a string by using this font.
    </summary>
    <param name="text">Text to be measured.</param>
    <param name="width">Maximum width of the string in points.</param>
    <param name="format">PdfStringFormat that represents formatting information, such as line spacing, for the string.</param>
    <returns>Size of the text.</returns>
        """
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfFontBase_MeasureStringTWF.argtypes=[c_void_p ,c_wchar_p,c_float,c_void_p]
        GetDllLibPdf().PdfFontBase_MeasureStringTWF.restype=c_void_p
        intPtr = GetDllLibPdf().PdfFontBase_MeasureStringTWF(self.Ptr, text,width,intPtrformat)
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


#    @dispatch
#
#    def MeasureString(self ,text:str,width:float,format:PdfStringFormat,charactersFitted:'Int32&',linesFilled:'Int32&')->SizeF:
#        """
#
#        """
#        intPtrformat:c_void_p = format.Ptr
#        intPtrcharactersFitted:c_void_p = charactersFitted.Ptr
#        intPtrlinesFilled:c_void_p = linesFilled.Ptr
#
#        GetDllLibPdf().PdfFontBase_MeasureStringTWFCL.argtypes=[c_void_p ,c_wchar_p,c_float,c_void_p,c_void_p,c_void_p]
#        GetDllLibPdf().PdfFontBase_MeasureStringTWFCL.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfFontBase_MeasureStringTWFCL(self.Ptr, text,width,intPtrformat,intPtrcharactersFitted,intPtrlinesFilled)
#        ret = None if intPtr==None else SizeF(intPtr)
#        return ret
#


    @dispatch

    def MeasureString(self ,text:str,layoutArea:SizeF)->SizeF:
        """
    <summary>
        Measures a string by using this font.
    </summary>
    <param name="text">Text to be measured.</param>
    <param name="layoutArea">SizeF structure that specifies the maximum layout area for the text in points.</param>
    <returns>Size of the text.</returns>
        """
        intPtrlayoutArea:c_void_p = layoutArea.Ptr

        GetDllLibPdf().PdfFontBase_MeasureStringTL.argtypes=[c_void_p ,c_wchar_p,c_void_p]
        GetDllLibPdf().PdfFontBase_MeasureStringTL.restype=c_void_p
        intPtr = GetDllLibPdf().PdfFontBase_MeasureStringTL(self.Ptr, text,intPtrlayoutArea)
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @dispatch

    def MeasureString(self ,text:str,layoutArea:SizeF,format:PdfStringFormat)->SizeF:
        """
    <summary>
        Measures a string by using this font.
    </summary>
    <param name="text">Text to be measured.</param>
    <param name="layoutArea">SizeF structure that specifies the maximum layout area for the text in points.</param>
    <param name="format">PdfStringFormat that represents formatting information, such as line spacing, for the string.</param>
    <returns>Size of the text.</returns>
        """
        intPtrlayoutArea:c_void_p = layoutArea.Ptr
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfFontBase_MeasureStringTLF.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p]
        GetDllLibPdf().PdfFontBase_MeasureStringTLF.restype=c_void_p
        intPtr = GetDllLibPdf().PdfFontBase_MeasureStringTLF(self.Ptr, text,intPtrlayoutArea,intPtrformat)
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


#    @dispatch
#
#    def MeasureString(self ,text:str,layoutArea:SizeF,format:PdfStringFormat,charactersFitted:'Int32&',linesFilled:'Int32&')->SizeF:
#        """
#
#        """
#        intPtrlayoutArea:c_void_p = layoutArea.Ptr
#        intPtrformat:c_void_p = format.Ptr
#        intPtrcharactersFitted:c_void_p = charactersFitted.Ptr
#        intPtrlinesFilled:c_void_p = linesFilled.Ptr
#
#        GetDllLibPdf().PdfFontBase_MeasureStringTLFCL.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_void_p,c_void_p]
#        GetDllLibPdf().PdfFontBase_MeasureStringTLFCL.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfFontBase_MeasureStringTLFCL(self.Ptr, text,intPtrlayoutArea,intPtrformat,intPtrcharactersFitted,intPtrlinesFilled)
#        ret = None if intPtr==None else SizeF(intPtr)
#        return ret
#


