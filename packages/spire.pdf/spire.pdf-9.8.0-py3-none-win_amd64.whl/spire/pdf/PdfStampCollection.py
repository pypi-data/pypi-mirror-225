from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfStampCollection (  PdfCollection) :
    """
    <summary>
        A collection of stamps that are applied to the page templates.
    </summary>
    """

    def get_Item(self ,index:int)->'PdfPageTemplateElement':
        """
    <summary>
        Gets a stamp element by its index.
    </summary>
        """
        
        GetDllLibPdf().PdfStampCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfStampCollection_get_Item.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStampCollection_get_Item(self.Ptr, index)
        ret = None if intPtr==None else PdfPageTemplateElement(intPtr)
        return ret


    @dispatch

    def Add(self ,template:PdfPageTemplateElement)->int:
        """
    <summary>
        Adds a stamp element to the collection.
    </summary>
    <param name="template">The stamp element.</param>
    <returns>The index of the stamp element.</returns>
        """
        intPtrtemplate:c_void_p = template.Ptr

        GetDllLibPdf().PdfStampCollection_Add.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfStampCollection_Add.restype=c_int
        ret = GetDllLibPdf().PdfStampCollection_Add(self.Ptr, intPtrtemplate)
        return ret

    @dispatch

    def Add(self ,x:float,y:float,width:float,height:float)->PdfPageTemplateElement:
        """
    <summary>
        Creates a stamp element and adds it to the collection.
    </summary>
    <param name="x">X co-ordinate of the stamp.</param>
    <param name="y">Y co-ordinate of the stamp.</param>
    <param name="width">Width of the stamp.</param>
    <param name="height">Height of the stamp.</param>
    <returns>The created stamp element.</returns>
        """
        
        GetDllLibPdf().PdfStampCollection_AddXYWH.argtypes=[c_void_p ,c_float,c_float,c_float,c_float]
        GetDllLibPdf().PdfStampCollection_AddXYWH.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStampCollection_AddXYWH(self.Ptr, x,y,width,height)
        ret = None if intPtr==None else PdfPageTemplateElement(intPtr)
        return ret



    def Contains(self ,template:'PdfPageTemplateElement')->bool:
        """
    <summary>
        Checks whether the stamp element exists in the collection.
    </summary>
    <param name="template">Stamp element.</param>
    <returns>True - if stamp element exists in the collection, False otherwise.</returns>
        """
        intPtrtemplate:c_void_p = template.Ptr

        GetDllLibPdf().PdfStampCollection_Contains.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfStampCollection_Contains.restype=c_bool
        ret = GetDllLibPdf().PdfStampCollection_Contains(self.Ptr, intPtrtemplate)
        return ret


    def Insert(self ,index:int,template:'PdfPageTemplateElement'):
        """
    <summary>
        Inserts a stamp element to the collection at the specified position.
    </summary>
    <param name="index">The index of the stamp in the collection.</param>
    <param name="template">The stamp element.</param>
        """
        intPtrtemplate:c_void_p = template.Ptr

        GetDllLibPdf().PdfStampCollection_Insert.argtypes=[c_void_p ,c_int,c_void_p]
        GetDllLibPdf().PdfStampCollection_Insert(self.Ptr, index,intPtrtemplate)


    def Remove(self ,template:'PdfPageTemplateElement'):
        """
    <summary>
        Removes the stamp element from the collection.
    </summary>
    <param name="template">The stamp element.</param>
        """
        intPtrtemplate:c_void_p = template.Ptr

        GetDllLibPdf().PdfStampCollection_Remove.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfStampCollection_Remove(self.Ptr, intPtrtemplate)


    def RemoveAt(self ,index:int):
        """
    <summary>
        Removes a stamp element from the specified position in the collection.
    </summary>
    <param name="index">The index of the stamp in the collection.</param>
        """
        
        GetDllLibPdf().PdfStampCollection_RemoveAt.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfStampCollection_RemoveAt(self.Ptr, index)

    def Clear(self):
        """
    <summary>
        Cleares the collection.
    </summary>
        """
        GetDllLibPdf().PdfStampCollection_Clear.argtypes=[c_void_p]
        GetDllLibPdf().PdfStampCollection_Clear(self.Ptr)


    def GetEnumerator(self)->'IEnumerator':
        """

        """
        GetDllLibPdf().PdfStampCollection_GetEnumerator.argtypes=[c_void_p]
        GetDllLibPdf().PdfStampCollection_GetEnumerator.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStampCollection_GetEnumerator(self.Ptr)
        ret = None if intPtr==None else IEnumerator(intPtr)
        return ret


