from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfBookmark (  SpireObject) :
    """
    <summary>
        Each instance of this class represents
            an bookmark node in the bookmark tree.
    </summary>
    """
    @property

    def Destination(self)->'PdfDestination':
        """
    <summary>
        Gets or sets the outline destination.
    </summary>
        """
        GetDllLibPdf().PdfBookmark_get_Destination.argtypes=[c_void_p]
        GetDllLibPdf().PdfBookmark_get_Destination.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBookmark_get_Destination(self.Ptr)
        ret = None if intPtr==None else PdfDestination(intPtr)
        return ret


    @Destination.setter
    def Destination(self, value:'PdfDestination'):
        GetDllLibPdf().PdfBookmark_set_Destination.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfBookmark_set_Destination(self.Ptr, value.Ptr)

    @property

    def Title(self)->str:
        """
    <summary>
        Gets or sets the outline title.
    </summary>
<remarks>The outline title is the text,
            which appears in the outline tree as a tree node.</remarks>
        """
        GetDllLibPdf().PdfBookmark_get_Title.argtypes=[c_void_p]
        GetDllLibPdf().PdfBookmark_get_Title.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfBookmark_get_Title(self.Ptr))
        return ret


    @Title.setter
    def Title(self, value:str):
        GetDllLibPdf().PdfBookmark_set_Title.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfBookmark_set_Title(self.Ptr, value)

    @property

    def Color(self)->'PdfRGBColor':
        """
    <summary>
        Gets or sets the color.
    </summary>
        """
        GetDllLibPdf().PdfBookmark_get_Color.argtypes=[c_void_p]
        GetDllLibPdf().PdfBookmark_get_Color.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBookmark_get_Color(self.Ptr)
        ret = None if intPtr==None else PdfRGBColor(intPtr)
        return ret


    @Color.setter
    def Color(self, value:'PdfRGBColor'):
        GetDllLibPdf().PdfBookmark_set_Color.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfBookmark_set_Color(self.Ptr, value.Ptr)

    @property

    def DisplayStyle(self)->'PdfTextStyle':
        """
    <summary>
        Gets or sets the text style.
    </summary>
        """
        GetDllLibPdf().PdfBookmark_get_DisplayStyle.argtypes=[c_void_p]
        GetDllLibPdf().PdfBookmark_get_DisplayStyle.restype=c_int
        ret = GetDllLibPdf().PdfBookmark_get_DisplayStyle(self.Ptr)
        objwraped = PdfTextStyle(ret)
        return objwraped

    @DisplayStyle.setter
    def DisplayStyle(self, value:'PdfTextStyle'):
        GetDllLibPdf().PdfBookmark_set_DisplayStyle.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfBookmark_set_DisplayStyle(self.Ptr, value.value)

    @property
    def ExpandBookmark(self)->bool:
        """
    <summary>
        It's true,expand node
            It's false,collapse node
    </summary>
        """
        GetDllLibPdf().PdfBookmark_get_ExpandBookmark.argtypes=[c_void_p]
        GetDllLibPdf().PdfBookmark_get_ExpandBookmark.restype=c_bool
        ret = GetDllLibPdf().PdfBookmark_get_ExpandBookmark(self.Ptr)
        return ret

    @ExpandBookmark.setter
    def ExpandBookmark(self, value:bool):
        GetDllLibPdf().PdfBookmark_set_ExpandBookmark.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfBookmark_set_ExpandBookmark(self.Ptr, value)



    @property

    def Action(self)->'PdfAction':
        """
    <summary>
        Gets or sets the Action for the Outline.
    </summary>
        """
        GetDllLibPdf().PdfBookmark_get_Action.argtypes=[c_void_p]
        GetDllLibPdf().PdfBookmark_get_Action.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBookmark_get_Action(self.Ptr)
        ret = None if intPtr==None else PdfAction(intPtr)
        return ret


    @Action.setter
    def Action(self, value:'PdfAction'):
        GetDllLibPdf().PdfBookmark_set_Action.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfBookmark_set_Action(self.Ptr, value.Ptr)

    def ConvertToBookmarkCollection(self)->'PdfBookmarkCollection':
        from spire.pdf.PdfBookmarkCollection import PdfBookmarkCollection
        GetDllLibPdf().PdfBookmark_ConvertToBookmarkCollection.argtypes=[c_void_p]
        GetDllLibPdf().PdfBookmark_ConvertToBookmarkCollection.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBookmark_ConvertToBookmarkCollection(self.Ptr)
        ret = None if intPtr==None else PdfBookmarkCollection(intPtr)
        return ret