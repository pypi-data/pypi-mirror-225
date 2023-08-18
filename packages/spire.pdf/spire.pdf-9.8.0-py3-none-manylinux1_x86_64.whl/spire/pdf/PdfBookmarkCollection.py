from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfBookmarkCollection (  IEnumerable) :
    """
    <summary>
        This class plays two roles: it's a base class for all bookmarks
            and it's a root of a bookmarks tree.
    </summary>
    """
    @property
    def Count(self)->int:
        """
    <summary>
        Gets number of the elements in the collection.
    </summary>
        """
        GetDllLibPdf().PdfBookmarkCollection_get_Count.argtypes=[c_void_p]
        GetDllLibPdf().PdfBookmarkCollection_get_Count.restype=c_int
        ret = GetDllLibPdf().PdfBookmarkCollection_get_Count(self.Ptr)
        return ret


    def get_Item(self ,index:int)->'PdfBookmark':
        """
    <summary>
        Gets the  at the specified index.
    </summary>
<value>index</value>
        """
        
        GetDllLibPdf().PdfBookmarkCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfBookmarkCollection_get_Item.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBookmarkCollection_get_Item(self.Ptr, index)
        ret = None if intPtr==None else PdfBookmark(intPtr)
        return ret



    def Add(self ,title:str)->'PdfBookmark':
        """
    <summary>
        Creates and adds an outline.
    </summary>
    <param name="title">The title of the new outline.</param>
    <returns>The outline created.</returns>
        """
        
        GetDllLibPdf().PdfBookmarkCollection_Add.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfBookmarkCollection_Add.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBookmarkCollection_Add(self.Ptr, title)
        ret = None if intPtr==None else PdfBookmark(intPtr)
        return ret



    def Contains(self ,outline:'PdfBookmark')->bool:
        """
    <summary>
        Determines whether the specified outline is a direct descendant of the outline base.
    </summary>
    <param name="outline">The outline.</param>
    <returns>
  <c>true</c> if the specified outline is a direct descendant of the outline base;
            otherwise, <c>false</c>.
            </returns>
        """
        intPtroutline:c_void_p = outline.Ptr

        GetDllLibPdf().PdfBookmarkCollection_Contains.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfBookmarkCollection_Contains.restype=c_bool
        ret = GetDllLibPdf().PdfBookmarkCollection_Contains(self.Ptr, intPtroutline)
        return ret


    def Remove(self ,title:str):
        """
    <summary>
        Removes the specified bookmark from the document.
    </summary>
    <param name="title">The title of the outline.</param>
        """
        
        GetDllLibPdf().PdfBookmarkCollection_Remove.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfBookmarkCollection_Remove(self.Ptr, title)


    def RemoveAt(self ,index:int):
        """
    <summary>
        Removes the specified bookmark from the document at the specified index.
    </summary>
    <param name="index">The index.</param>
        """
        
        GetDllLibPdf().PdfBookmarkCollection_RemoveAt.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfBookmarkCollection_RemoveAt(self.Ptr, index)

    def Clear(self):
        """
    <summary>
        Removes all the bookmark from the document.
    </summary>
        """
        GetDllLibPdf().PdfBookmarkCollection_Clear.argtypes=[c_void_p]
        GetDllLibPdf().PdfBookmarkCollection_Clear(self.Ptr)


    def Insert(self ,index:int,title:str)->'PdfBookmark':
        """
    <summary>
        Inserts a new outline at the specified index.
    </summary>
    <param name="index">The index.</param>
    <param name="title">The title of the new outline.</param>
    <returns>The new outline.</returns>
        """
        
        GetDllLibPdf().PdfBookmarkCollection_Insert.argtypes=[c_void_p ,c_int,c_wchar_p]
        GetDllLibPdf().PdfBookmarkCollection_Insert.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBookmarkCollection_Insert(self.Ptr, index,title)
        ret = None if intPtr==None else PdfBookmark(intPtr)
        return ret


