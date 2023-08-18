from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfRadioButtonItemCollection (  PdfCollection) :
    """
    <summary>
        Represents collection of radio buttons items.
    </summary>
    """

    def Add(self ,item:'PdfRadioButtonListItem')->int:
        """
    <summary>
        Adds the specified item.
    </summary>
    <param name="item">The  object to be added to collection.</param>
    <returns>The index of the added field.</returns>
        """
        intPtritem:c_void_p = item.Ptr

        GetDllLibPdf().PdfRadioButtonItemCollection_Add.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfRadioButtonItemCollection_Add.restype=c_int
        ret = GetDllLibPdf().PdfRadioButtonItemCollection_Add(self.Ptr, intPtritem)
        return ret


    def Insert(self ,index:int,item:'PdfRadioButtonListItem'):
        """
    <summary>
        Inserts an item at the specified index.
    </summary>
    <param name="index">The index where to insert the new item..</param>
    <param name="item">A  object to be added to collection.</param>
        """
        intPtritem:c_void_p = item.Ptr

        GetDllLibPdf().PdfRadioButtonItemCollection_Insert.argtypes=[c_void_p ,c_int,c_void_p]
        GetDllLibPdf().PdfRadioButtonItemCollection_Insert(self.Ptr, index,intPtritem)


    def Remove(self ,item:'PdfRadioButtonListItem'):
        """
    <summary>
        Removes the specified item from the collection.
    </summary>
    <param name="item">The  object which is to be removed from the collection.</param>
        """
        intPtritem:c_void_p = item.Ptr

        GetDllLibPdf().PdfRadioButtonItemCollection_Remove.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfRadioButtonItemCollection_Remove(self.Ptr, intPtritem)


    def RemoveAt(self ,index:int):
        """
    <summary>
        Removes the item at the specified position.
    </summary>
    <param name="index">The index where to remove the item.</param>
        """
        
        GetDllLibPdf().PdfRadioButtonItemCollection_RemoveAt.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfRadioButtonItemCollection_RemoveAt(self.Ptr, index)


    def IndexOf(self ,item:'PdfRadioButtonListItem')->int:
        """
    <summary>
        Gets the index of the item within the collection.
    </summary>
    <param name="item">A  object whose index is requested.</param>
    <returns>Index of the item with the collection.</returns>
        """
        intPtritem:c_void_p = item.Ptr

        GetDllLibPdf().PdfRadioButtonItemCollection_IndexOf.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfRadioButtonItemCollection_IndexOf.restype=c_int
        ret = GetDllLibPdf().PdfRadioButtonItemCollection_IndexOf(self.Ptr, intPtritem)
        return ret


    def Contains(self ,item:'PdfRadioButtonListItem')->bool:
        """
    <summary>
        Determines whether the collection contains the specified item.
    </summary>
    <param name="item">Check whether  object is exists in the collection or not.</param>
    <returns>
  <c>true</c> if collection contains specified item; otherwise, <c>false</c>.
            </returns>
        """
        intPtritem:c_void_p = item.Ptr

        GetDllLibPdf().PdfRadioButtonItemCollection_Contains.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfRadioButtonItemCollection_Contains.restype=c_bool
        ret = GetDllLibPdf().PdfRadioButtonItemCollection_Contains(self.Ptr, intPtritem)
        return ret

    def Clear(self):
        """
    <summary>
        Clears the item collection.
    </summary>
        """
        GetDllLibPdf().PdfRadioButtonItemCollection_Clear.argtypes=[c_void_p]
        GetDllLibPdf().PdfRadioButtonItemCollection_Clear(self.Ptr)


    def get_Item(self ,index:int)->'PdfRadioButtonListItem':
        """
    <summary>
        Gets the  at the specified index.
    </summary>
<value>Returns item at the specified position.</value>
        """
        
        GetDllLibPdf().PdfRadioButtonItemCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfRadioButtonItemCollection_get_Item.restype=c_void_p
        intPtr = GetDllLibPdf().PdfRadioButtonItemCollection_get_Item(self.Ptr, index)
        ret = None if intPtr==None else PdfRadioButtonListItem(intPtr)
        return ret


