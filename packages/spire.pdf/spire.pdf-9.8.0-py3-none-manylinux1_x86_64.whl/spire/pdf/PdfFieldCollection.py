from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfFieldCollection (  PdfCollection) :
    """
    <summary>
        Represents collection of the Pdf fields.
    </summary>
    """
    @dispatch

    def get_Item(self ,index:int)->PdfField:
        """
    <summary>
        Gets the  at the specified index.
    </summary>
        """
        
        GetDllLibPdf().PdfFieldCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfFieldCollection_get_Item.restype=c_void_p
        intPtr = GetDllLibPdf().PdfFieldCollection_get_Item(self.Ptr, index)
        ret = None if intPtr==None else PdfField(intPtr)
        return ret


    @dispatch

    def get_Item(self ,name:str)->PdfField:
        """
    <summary>
        Gets the  with thier field name.
    </summary>
        """
        
        GetDllLibPdf().PdfFieldCollection_get_ItemN.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfFieldCollection_get_ItemN.restype=c_void_p
        intPtr = GetDllLibPdf().PdfFieldCollection_get_ItemN(self.Ptr, name)
        ret = None if intPtr==None else PdfField(intPtr)
        return ret



    def Add(self ,field:'PdfField')->int:
        """
    <summary>
        Adds the specified field.
    </summary>
    <param name="field">The field item which is added in the PDF form.</param>
    <returns>The field to be added on the page. </returns>
        """
        intPtrfield:c_void_p = field.Ptr

        GetDllLibPdf().PdfFieldCollection_Add.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfFieldCollection_Add.restype=c_int
        ret = GetDllLibPdf().PdfFieldCollection_Add(self.Ptr, intPtrfield)
        return ret


    def Insert(self ,index:int,field:'PdfField'):
        """
    <summary>
        Inserts the the field at the specified index.
    </summary>
    <param name="index">The index of the field.</param>
    <param name="field">The field which should be inserted at the specified index.</param>
        """
        intPtrfield:c_void_p = field.Ptr

        GetDllLibPdf().PdfFieldCollection_Insert.argtypes=[c_void_p ,c_int,c_void_p]
        GetDllLibPdf().PdfFieldCollection_Insert(self.Ptr, index,intPtrfield)


    def Contains(self ,field:'PdfField')->bool:
        """
    <summary>
        Determines whether field is contained within the collection.
    </summary>
    <param name="field">Check whether  object is present in the field collection or not.</param>
    <returns>
  <c>true</c> if field is present in the collection, otherwise, <c>false</c>.
            </returns>
        """
        intPtrfield:c_void_p = field.Ptr

        GetDllLibPdf().PdfFieldCollection_Contains.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfFieldCollection_Contains.restype=c_bool
        ret = GetDllLibPdf().PdfFieldCollection_Contains(self.Ptr, intPtrfield)
        return ret


    def IndexOf(self ,field:'PdfField')->int:
        """
    <summary>
        Gets the index of the field.
    </summary>
    <param name="field">The  object whose index is requested.</param>
    <returns>Index of the field in collection.</returns>
        """
        intPtrfield:c_void_p = field.Ptr

        GetDllLibPdf().PdfFieldCollection_IndexOf.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfFieldCollection_IndexOf.restype=c_int
        ret = GetDllLibPdf().PdfFieldCollection_IndexOf(self.Ptr, intPtrfield)
        return ret


    def Remove(self ,field:'PdfField'):
        """
    <summary>
        Removes the specified field in the collection.
    </summary>
    <param name="field">The  object to be removed from collection.</param>
        """
        intPtrfield:c_void_p = field.Ptr

        GetDllLibPdf().PdfFieldCollection_Remove.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfFieldCollection_Remove(self.Ptr, intPtrfield)


    def RemoveAt(self ,index:int):
        """
    <summary>
        Removes field at the specified position.
    </summary>
    <param name="index">The index where to remove the item.</param>
        """
        
        GetDllLibPdf().PdfFieldCollection_RemoveAt.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfFieldCollection_RemoveAt(self.Ptr, index)

    def Clear(self):
        """
    <summary>
        Clears the form field collection.
    </summary>
        """
        GetDllLibPdf().PdfFieldCollection_Clear.argtypes=[c_void_p]
        GetDllLibPdf().PdfFieldCollection_Clear(self.Ptr)

