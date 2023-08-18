from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfGridColumnCollection (  IEnumerable) :
    """

    """

    def get_Item(self ,index:int)->'PdfGridColumn':
        """
    <summary>
        Gets the  at the specified index.
    </summary>
<value></value>
        """
        
        GetDllLibPdf().PdfGridColumnCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfGridColumnCollection_get_Item.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGridColumnCollection_get_Item(self.Ptr, index)
        ret = None if intPtr==None else PdfGridColumn(intPtr)
        return ret


    @property
    def Count(self)->int:
        """
    <summary>
        Gets the count.
    </summary>
<value>The count.</value>
        """
        GetDllLibPdf().PdfGridColumnCollection_get_Count.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridColumnCollection_get_Count.restype=c_int
        ret = GetDllLibPdf().PdfGridColumnCollection_get_Count(self.Ptr)
        return ret

    @dispatch

    def Add(self)->PdfGridColumn:
        """
    <summary>
        Adds this instance.
    </summary>
    <returns></returns>
        """
        GetDllLibPdf().PdfGridColumnCollection_Add.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridColumnCollection_Add.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGridColumnCollection_Add(self.Ptr)
        ret = None if intPtr==None else PdfGridColumn(intPtr)
        return ret


    @dispatch

    def Add(self ,count:int):
        """
    <summary>
        Adds the specified count.
    </summary>
    <param name="count">The count.</param>
        """
        
        GetDllLibPdf().PdfGridColumnCollection_AddC.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfGridColumnCollection_AddC(self.Ptr, count)

    @dispatch

    def Add(self ,column:PdfGridColumn):
        """
    <summary>
        Adds the specified column.
    </summary>
    <param name="column">The column.</param>
        """
        intPtrcolumn:c_void_p = column.Ptr

        GetDllLibPdf().PdfGridColumnCollection_AddC1.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfGridColumnCollection_AddC1(self.Ptr, intPtrcolumn)


    def Remove(self ,item:'PdfGridColumn')->bool:
        """
    <summary>
        Removes the first occurrence of a specific object from the PdfGridColumnCollection.
    </summary>
    <param name="item">The object to remove from the PdfGridColumnCollection.
    </param>
    <returns>true if item is successfully removed; otherwise, false</returns>
        """
        intPtritem:c_void_p = item.Ptr

        GetDllLibPdf().PdfGridColumnCollection_Remove.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfGridColumnCollection_Remove.restype=c_bool
        ret = GetDllLibPdf().PdfGridColumnCollection_Remove(self.Ptr, intPtritem)
        return ret


    def RemoveAt(self ,index:int):
        """
    <summary>
        Removes the element at the specified index of the PdfGridColumnCollection.
    </summary>
    <param name="index">The zero-based index of the element to remove.</param>
        """
        
        GetDllLibPdf().PdfGridColumnCollection_RemoveAt.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfGridColumnCollection_RemoveAt(self.Ptr, index)


    def GetEnumerator(self)->'IEnumerator':
        """

        """
        GetDllLibPdf().PdfGridColumnCollection_GetEnumerator.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridColumnCollection_GetEnumerator.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGridColumnCollection_GetEnumerator(self.Ptr)
        ret = None if intPtr==None else IEnumerator(intPtr)
        return ret


