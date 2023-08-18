from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfRowCollection (  PdfCollection) :
    """
    <summary>
        Represents the collection of the columns.
    </summary>
    """

    def get_Item(self ,index:int)->'PdfRow':
        """
    <summary>
        Gets the  at the specified index.
    </summary>
        """
        
        GetDllLibPdf().PdfRowCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfRowCollection_get_Item.restype=c_void_p
        intPtr = GetDllLibPdf().PdfRowCollection_get_Item(self.Ptr, index)
        ret = None if intPtr==None else PdfRow(intPtr)
        return ret


    @dispatch

    def Add(self ,row:PdfRow):
        """
    <summary>
        Adds the specified row.
    </summary>
    <param name="row">The row.</param>
        """
        intPtrrow:c_void_p = row.Ptr

        GetDllLibPdf().PdfRowCollection_Add.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfRowCollection_Add(self.Ptr, intPtrrow)

    @dispatch

    def Add(self ,values:List[SpireObject]):
        """
    <summary>
        The array of values that are used to create the new row.
    </summary>
        """
        #arrayvalues:ArrayTypevalues = ""
        countvalues = len(values)
        ArrayTypevalues = c_void_p * countvalues
        arrayvalues = ArrayTypevalues()
        for i in range(0, countvalues):
            arrayvalues[i] = values[i].Ptr


        GetDllLibPdf().PdfRowCollection_AddV.argtypes=[c_void_p ,ArrayTypevalues]
        GetDllLibPdf().PdfRowCollection_AddV(self.Ptr, arrayvalues)

