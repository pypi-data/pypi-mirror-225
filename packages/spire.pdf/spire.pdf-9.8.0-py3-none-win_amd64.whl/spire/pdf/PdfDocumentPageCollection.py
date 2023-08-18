from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfDocumentPageCollection (  IEnumerable) :
    """
    <summary>
        Implements a virtual collection of all pages in the document.
    </summary>
    """
    @property
    def Count(self)->int:
        """
    <summary>
        Gets the total number of the pages.
    </summary>
        """
        GetDllLibPdf().PdfDocumentPageCollection_get_Count.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocumentPageCollection_get_Count.restype=c_int
        ret = GetDllLibPdf().PdfDocumentPageCollection_get_Count(self.Ptr)
        return ret


    def get_Item(self ,index:int)->'PdfNewPage':
        """
    <summary>
        Gets a page by its index in the document.
    </summary>
        """
        
        GetDllLibPdf().PdfDocumentPageCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfDocumentPageCollection_get_Item.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocumentPageCollection_get_Item(self.Ptr, index)
        ret = None if intPtr==None else PdfNewPage(intPtr)
        return ret



    def add_PageAdded(self ,value:'PageAddedEventHandler'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().PdfDocumentPageCollection_add_PageAdded.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfDocumentPageCollection_add_PageAdded(self.Ptr, intPtrvalue)


    def remove_PageAdded(self ,value:'PageAddedEventHandler'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().PdfDocumentPageCollection_remove_PageAdded.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfDocumentPageCollection_remove_PageAdded(self.Ptr, intPtrvalue)


    def Add(self)->'PdfNewPage':
        """
    <summary>
        Creates a page and adds it to the last section in the document.
    </summary>
    <returns>Created page object.</returns>
        """
        GetDllLibPdf().PdfDocumentPageCollection_Add.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocumentPageCollection_Add.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocumentPageCollection_Add(self.Ptr)
        ret = None if intPtr==None else PdfNewPage(intPtr)
        return ret



    def Insert(self ,index:int,page:'PdfNewPage'):
        """
    <summary>
        Inserts a page at the specified index to the last section in the document.
    </summary>
    <param name="index">The index of the page in the section.</param>
    <param name="page">The page.</param>
        """
        intPtrpage:c_void_p = page.Ptr

        GetDllLibPdf().PdfDocumentPageCollection_Insert.argtypes=[c_void_p ,c_int,c_void_p]
        GetDllLibPdf().PdfDocumentPageCollection_Insert(self.Ptr, index,intPtrpage)


    def IndexOf(self ,page:'PdfNewPage')->int:
        """
    <summary>
        Gets the index of the page in the document.
    </summary>
    <param name="page">The current page.</param>
    <returns>Index of the page in the document if exists, -1 otherwise.</returns>
        """
        intPtrpage:c_void_p = page.Ptr

        GetDllLibPdf().PdfDocumentPageCollection_IndexOf.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfDocumentPageCollection_IndexOf.restype=c_int
        ret = GetDllLibPdf().PdfDocumentPageCollection_IndexOf(self.Ptr, intPtrpage)
        return ret


    def GetEnumerator(self)->'IEnumerator':
        """

        """
        GetDllLibPdf().PdfDocumentPageCollection_GetEnumerator.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocumentPageCollection_GetEnumerator.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocumentPageCollection_GetEnumerator(self.Ptr)
        ret = None if intPtr==None else IEnumerator(intPtr)
        return ret


