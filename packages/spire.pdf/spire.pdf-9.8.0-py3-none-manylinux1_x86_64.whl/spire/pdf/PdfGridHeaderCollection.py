from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfGridHeaderCollection (  IEnumerable) :
    """

    """

    def get_Item(self ,index:int)->'PdfGridRow':
        """
    <summary>
        Gets the  at the specified index.
    </summary>
<value></value>
        """
        
        GetDllLibPdf().PdfGridHeaderCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfGridHeaderCollection_get_Item.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGridHeaderCollection_get_Item(self.Ptr, index)
        ret = None if intPtr==None else PdfGridRow(intPtr)
        return ret


    @property
    def Count(self)->int:
        """
    <summary>
        Gets the count.
    </summary>
<value>The count.</value>
        """
        GetDllLibPdf().PdfGridHeaderCollection_get_Count.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridHeaderCollection_get_Count.restype=c_int
        ret = GetDllLibPdf().PdfGridHeaderCollection_get_Count(self.Ptr)
        return ret

#
#    def Add(self ,count:int)->List['PdfGridRow']:
#        """
#    <summary>
#        Adds the specified count.
#    </summary>
#    <param name="count">The count.</param>
#        """
#        
#        GetDllLibPdf().PdfGridHeaderCollection_Add.argtypes=[c_void_p ,c_int]
#        GetDllLibPdf().PdfGridHeaderCollection_Add.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().PdfGridHeaderCollection_Add(self.Ptr, count)
#        ret = GetObjVectorFromArray(intPtrArray, PdfGridRow)
#        return ret


    def Clear(self):
        """
    <summary>
        Clears this instance.
    </summary>
        """
        GetDllLibPdf().PdfGridHeaderCollection_Clear.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridHeaderCollection_Clear(self.Ptr)


    def ApplyStyle(self ,style:'PdfGridStyleBase'):
        """
    <summary>
        Applies the style.
    </summary>
    <param name="style">The style.</param>
        """
        intPtrstyle:c_void_p = style.Ptr

        GetDllLibPdf().PdfGridHeaderCollection_ApplyStyle.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfGridHeaderCollection_ApplyStyle(self.Ptr, intPtrstyle)


    def GetEnumerator(self)->'IEnumerator':
        """

        """
        GetDllLibPdf().PdfGridHeaderCollection_GetEnumerator.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridHeaderCollection_GetEnumerator.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGridHeaderCollection_GetEnumerator(self.Ptr)
        ret = None if intPtr==None else IEnumerator(intPtr)
        return ret


