from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfListFieldItemCollection (  PdfCollection) :
    """
    <summary>
        Represents list field item collection.
    </summary>
    """

    def get_Item(self ,index:int)->'PdfListFieldItem':
        """
    <summary>
        Gets the  at the specified index.
    </summary>
<value>The  object.</value>
        """
        
        GetDllLibPdf().PdfListFieldItemCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfListFieldItemCollection_get_Item.restype=c_void_p
        intPtr = GetDllLibPdf().PdfListFieldItemCollection_get_Item(self.Ptr, index)
        ret = None if intPtr==None else PdfListFieldItem(intPtr)
        return ret



    def Add(self ,item:'PdfListFieldItem')->int:
        """
    <summary>
        Adds the specified item in the collection.
    </summary>
    <param name="item">The  object which to be added in the collection.</param>
    <returns>item</returns>
        """
        intPtritem:c_void_p = item.Ptr

        GetDllLibPdf().PdfListFieldItemCollection_Add.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfListFieldItemCollection_Add.restype=c_int
        ret = GetDllLibPdf().PdfListFieldItemCollection_Add(self.Ptr, intPtritem)
        return ret


    def Insert(self ,index:int,item:'PdfListFieldItem'):
        """
    <summary>
        Inserts the list item field at the specified index.
    </summary>
    <param name="index">The index where to insert the new item.</param>
    <param name="item">The  object to be added to collection.</param>
        """
        intPtritem:c_void_p = item.Ptr

        GetDllLibPdf().PdfListFieldItemCollection_Insert.argtypes=[c_void_p ,c_int,c_void_p]
        GetDllLibPdf().PdfListFieldItemCollection_Insert(self.Ptr, index,intPtritem)


    def Remove(self ,item:'PdfListFieldItem'):
        """
    <summary>
        Removes the specified item.
    </summary>
    <param name="item">The  object which to be removed in the collection.</param>
        """
        intPtritem:c_void_p = item.Ptr

        GetDllLibPdf().PdfListFieldItemCollection_Remove.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfListFieldItemCollection_Remove(self.Ptr, intPtritem)


    def RemoveAt(self ,index:int):
        """
    <summary>
        Removes the item at the specified position.
    </summary>
    <param name="index">The index where to remove the item.</param>
        """
        
        GetDllLibPdf().PdfListFieldItemCollection_RemoveAt.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfListFieldItemCollection_RemoveAt(self.Ptr, index)


    def Contains(self ,item:'PdfListFieldItem')->bool:
        """
    <summary>
        Determines whether the item is contained by the collection.
    </summary>
    <param name="item">Check whether  object is exists in the collection or not.</param>
    <returns>
  <c>true</c> if the item is contained within the collection; otherwise, <c>false</c>.
            </returns>
        """
        intPtritem:c_void_p = item.Ptr

        GetDllLibPdf().PdfListFieldItemCollection_Contains.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfListFieldItemCollection_Contains.restype=c_bool
        ret = GetDllLibPdf().PdfListFieldItemCollection_Contains(self.Ptr, intPtritem)
        return ret


    def IndexOf(self ,item:'PdfListFieldItem')->int:
        """
    <summary>
        Gets the index of the specified item.
    </summary>
    <param name="item">A  object whose index is requested.</param>
    <returns>The index of the given item, -1 if the item does not exist.</returns>
        """
        intPtritem:c_void_p = item.Ptr

        GetDllLibPdf().PdfListFieldItemCollection_IndexOf.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfListFieldItemCollection_IndexOf.restype=c_int
        ret = GetDllLibPdf().PdfListFieldItemCollection_IndexOf(self.Ptr, intPtritem)
        return ret

    def Clear(self):
        """
    <summary>
        Clears the collection.
    </summary>
        """
        GetDllLibPdf().PdfListFieldItemCollection_Clear.argtypes=[c_void_p]
        GetDllLibPdf().PdfListFieldItemCollection_Clear(self.Ptr)

