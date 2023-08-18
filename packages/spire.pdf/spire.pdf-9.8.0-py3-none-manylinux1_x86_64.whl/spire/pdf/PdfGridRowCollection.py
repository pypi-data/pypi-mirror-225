from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfGridRowCollection (SpireObject) :
    """

    """

    def Add(self)->'PdfGridRow':
        """
    <summary>
        Adds this instance.
    </summary>
    <returns></returns>
        """
        GetDllLibPdf().PdfGridRowCollection_Add.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridRowCollection_Add.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGridRowCollection_Add(self.Ptr)
        ret = None if intPtr==None else PdfGridRow(intPtr)
        return ret



    def SetSpan(self ,rowIndex:int,cellIndex:int,rowSpan:int,colSpan:int):
        """
    <summary>
        Sets the span.
    </summary>
    <param name="rowIndex">Index of the row.</param>
    <param name="cellIndex">Index of the cell.</param>
    <param name="rowSpan">The row span.</param>
    <param name="colSpan">The col span.</param>
        """
        
        GetDllLibPdf().PdfGridRowCollection_SetSpan.argtypes=[c_void_p ,c_int,c_int,c_int,c_int]
        GetDllLibPdf().PdfGridRowCollection_SetSpan(self.Ptr, rowIndex,cellIndex,rowSpan,colSpan)


    def ApplyStyle(self ,style:'PdfGridStyleBase'):
        """
    <summary>
        Applies the style.
    </summary>
    <param name="style">The style.</param>
        """
        intPtrstyle:c_void_p = style.Ptr

        GetDllLibPdf().PdfGridRowCollection_ApplyStyle.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfGridRowCollection_ApplyStyle(self.Ptr, intPtrstyle)

