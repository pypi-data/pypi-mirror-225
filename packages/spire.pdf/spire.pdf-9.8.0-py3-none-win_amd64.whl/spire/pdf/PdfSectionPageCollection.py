from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfSectionPageCollection (  IEnumerable) :
    """
    <summary>
        Manipulates pages within a section.
    </summary>
    """

    def get_Item(self ,index:int)->'PdfNewPage':
        """
    <summary>
        Gets the  at the specified index.
    </summary>
        """
        
        GetDllLibPdf().PdfSectionPageCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfSectionPageCollection_get_Item.restype=c_void_p
        intPtr = GetDllLibPdf().PdfSectionPageCollection_get_Item(self.Ptr, index)
        ret = None if intPtr==None else PdfNewPage(intPtr)
        return ret


    @property
    def Count(self)->int:
        """
    <summary>
        Gets the count of the pages.
    </summary>
        """
        GetDllLibPdf().PdfSectionPageCollection_get_Count.argtypes=[c_void_p]
        GetDllLibPdf().PdfSectionPageCollection_get_Count.restype=c_int
        ret = GetDllLibPdf().PdfSectionPageCollection_get_Count(self.Ptr)
        return ret

    @dispatch

    def Add(self)->PdfNewPage:
        """
    <summary>
        Creates a new page and adds it into the collection.
    </summary>
    <returns>The new page.</returns>
        """
        GetDllLibPdf().PdfSectionPageCollection_Add.argtypes=[c_void_p]
        GetDllLibPdf().PdfSectionPageCollection_Add.restype=c_void_p
        intPtr = GetDllLibPdf().PdfSectionPageCollection_Add(self.Ptr)
        ret = None if intPtr==None else PdfNewPage(intPtr)
        return ret


    @dispatch

    def Add(self ,page:PdfNewPage):
        """
    <summary>
        Adds a page into collection.
    </summary>
    <param name="page">The page.</param>
        """
        intPtrpage:c_void_p = page.Ptr

        GetDllLibPdf().PdfSectionPageCollection_AddP.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfSectionPageCollection_AddP(self.Ptr, intPtrpage)


    def Insert(self ,index:int,page:'PdfNewPage'):
        """
    <summary>
        Inserts a page at the specified index.
    </summary>
    <param name="index">The index.</param>
    <param name="page">The page.</param>
        """
        intPtrpage:c_void_p = page.Ptr

        GetDllLibPdf().PdfSectionPageCollection_Insert.argtypes=[c_void_p ,c_int,c_void_p]
        GetDllLibPdf().PdfSectionPageCollection_Insert(self.Ptr, index,intPtrpage)


    def IndexOf(self ,page:'PdfNewPage')->int:
        """
    <summary>
        Returns the index of the specified page.
    </summary>
    <param name="page">The page.</param>
    <returns>The index of the page.</returns>
        """
        intPtrpage:c_void_p = page.Ptr

        GetDllLibPdf().PdfSectionPageCollection_IndexOf.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfSectionPageCollection_IndexOf.restype=c_int
        ret = GetDllLibPdf().PdfSectionPageCollection_IndexOf(self.Ptr, intPtrpage)
        return ret


    def Contains(self ,page:'PdfNewPage')->bool:
        """
    <summary>
        Determines whether the specified page is within the collection.
    </summary>
    <param name="page">The page.</param>
    <returns>
  <c>true</c> if the collection contains the specified page; otherwise, <c>false</c>.
            </returns>
        """
        intPtrpage:c_void_p = page.Ptr

        GetDllLibPdf().PdfSectionPageCollection_Contains.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfSectionPageCollection_Contains.restype=c_bool
        ret = GetDllLibPdf().PdfSectionPageCollection_Contains(self.Ptr, intPtrpage)
        return ret


    def Remove(self ,page:'PdfNewPage'):
        """
    <summary>
        Removes the specified page.
    </summary>
    <param name="page">The page.</param>
        """
        intPtrpage:c_void_p = page.Ptr

        GetDllLibPdf().PdfSectionPageCollection_Remove.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfSectionPageCollection_Remove(self.Ptr, intPtrpage)


    def RemoveAt(self ,index:int):
        """
    <summary>
        Removes a page at the index specified.
    </summary>
    <param name="index">The index.</param>
        """
        
        GetDllLibPdf().PdfSectionPageCollection_RemoveAt.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfSectionPageCollection_RemoveAt(self.Ptr, index)

    def Clear(self):
        """
    <summary>
        Clears this collection.
    </summary>
        """
        GetDllLibPdf().PdfSectionPageCollection_Clear.argtypes=[c_void_p]
        GetDllLibPdf().PdfSectionPageCollection_Clear(self.Ptr)

