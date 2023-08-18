from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfListWidgetItemCollection (  PdfCollection) :
    """
    <summary>
        Represents a collection of list box field items.
    </summary>
    """

    def get_Item(self ,index:int)->'PdfListWidgetItem':
        """
    <summary>
        Gets the  at the specified index.
    </summary>
        """
        
        GetDllLibPdf().PdfListWidgetItemCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfListWidgetItemCollection_get_Item.restype=c_void_p
        intPtr = GetDllLibPdf().PdfListWidgetItemCollection_get_Item(self.Ptr, index)
        ret = None if intPtr==None else PdfListWidgetItem(intPtr)
        return ret



    def Add(self ,widgetItem:'PdfListWidgetItem')->int:
        """
    <summary>
        Inserts an item at the end of the collection. 
    </summary>
    <param name="widgetItem">a object to be added to collection.</param>
    <returns>The index of item.</returns>
        """
        intPtrwidgetItem:c_void_p = widgetItem.Ptr

        GetDllLibPdf().PdfListWidgetItemCollection_Add.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfListWidgetItemCollection_Add.restype=c_int
        ret = GetDllLibPdf().PdfListWidgetItemCollection_Add(self.Ptr, intPtrwidgetItem)
        return ret


    def Insert(self ,index:int,widgetItem:'PdfListWidgetItem'):
        """
    <summary>
        Inserts the list item at the specified index.
    </summary>
    <param name="index">The index.</param>
    <param name="widgetItem">The item.</param>
        """
        intPtrwidgetItem:c_void_p = widgetItem.Ptr

        GetDllLibPdf().PdfListWidgetItemCollection_Insert.argtypes=[c_void_p ,c_int,c_void_p]
        GetDllLibPdf().PdfListWidgetItemCollection_Insert(self.Ptr, index,intPtrwidgetItem)


    def RemoveAt(self ,index:int):
        """
    <summary>
        Removes the element at the specified index.
    </summary>
    <param name="index">The index.</param>
<remarks>Throws IndexOutOfRange exception if the index is out of bounds.</remarks>
        """
        
        GetDllLibPdf().PdfListWidgetItemCollection_RemoveAt.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfListWidgetItemCollection_RemoveAt(self.Ptr, index)

    def Clear(self):
        """
    <summary>
        Clears the item collection.
    </summary>
        """
        GetDllLibPdf().PdfListWidgetItemCollection_Clear.argtypes=[c_void_p]
        GetDllLibPdf().PdfListWidgetItemCollection_Clear(self.Ptr)

