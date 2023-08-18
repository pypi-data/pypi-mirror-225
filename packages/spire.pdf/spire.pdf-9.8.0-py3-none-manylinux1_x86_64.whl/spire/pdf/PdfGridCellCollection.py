from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfGridCellCollection (  IEnumerable) :
    """

    """

    def get_Item(self ,index:int)->'PdfGridCell':
        """
    <summary>
        Gets the  at the specified index.
    </summary>
<value></value>
        """
        
        GetDllLibPdf().PdfGridCellCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfGridCellCollection_get_Item.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGridCellCollection_get_Item(self.Ptr, index)
        ret = None if intPtr==None else PdfGridCell(intPtr)
        return ret


    @property
    def Count(self)->int:
        """
    <summary>
        Gets the count.
    </summary>
<value>The count.</value>
        """
        GetDllLibPdf().PdfGridCellCollection_get_Count.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridCellCollection_get_Count.restype=c_int
        ret = GetDllLibPdf().PdfGridCellCollection_get_Count(self.Ptr)
        return ret


    def IndexOf(self ,cell:'PdfGridCell')->int:
        """
    <summary>
        Returns the index of a particular cell in the collection.
    </summary>
    <param name="cell">The cell.</param>
    <returns></returns>
        """
        intPtrcell:c_void_p = cell.Ptr

        GetDllLibPdf().PdfGridCellCollection_IndexOf.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfGridCellCollection_IndexOf.restype=c_int
        ret = GetDllLibPdf().PdfGridCellCollection_IndexOf(self.Ptr, intPtrcell)
        return ret


    def GetEnumerator(self)->'IEnumerator':
        """

        """
        GetDllLibPdf().PdfGridCellCollection_GetEnumerator.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridCellCollection_GetEnumerator.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGridCellCollection_GetEnumerator(self.Ptr)
        ret = None if intPtr==None else IEnumerator(intPtr)
        return ret


