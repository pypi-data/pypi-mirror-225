from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfListItemCollection (  PdfCollection) :
    """
    <summary>
        Represents collection of list items.
    </summary>
    """

    def get_Item(self ,index:int)->'PdfListItem':
        """
    <summary>
        Gets the PdfListItem from collection at the specified index.
    </summary>
        """
        
        GetDllLibPdf().PdfListItemCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfListItemCollection_get_Item.restype=c_void_p
        intPtr = GetDllLibPdf().PdfListItemCollection_get_Item(self.Ptr, index)
        ret = None if intPtr==None else PdfListItem(intPtr)
        return ret


    @dispatch

    def Add(self ,item:PdfListItem)->int:
        """
    <summary>
        Adds the specified item.
    </summary>
    <param name="item">The item.</param>
    <returns>The item index in collection.</returns>
        """
        intPtritem:c_void_p = item.Ptr

        GetDllLibPdf().PdfListItemCollection_Add.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfListItemCollection_Add.restype=c_int
        ret = GetDllLibPdf().PdfListItemCollection_Add(self.Ptr, intPtritem)
        return ret

    @dispatch

    def Add(self ,item:PdfListItem,itemIndent:float)->int:
        """
    <summary>
        Adds the specified item.
    </summary>
    <param name="item">The item.</param>
    <param name="itemIndent">The item indent.</param>
        """
        intPtritem:c_void_p = item.Ptr

        GetDllLibPdf().PdfListItemCollection_AddII.argtypes=[c_void_p ,c_void_p,c_float]
        GetDllLibPdf().PdfListItemCollection_AddII.restype=c_int
        ret = GetDllLibPdf().PdfListItemCollection_AddII(self.Ptr, intPtritem,itemIndent)
        return ret

    @dispatch

    def Add(self ,text:str)->PdfListItem:
        """
    <summary>
        Adds the item with a specified text.
    </summary>
    <param name="text">The text.</param>
    <returns></returns>
        """
        
        GetDllLibPdf().PdfListItemCollection_AddT.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfListItemCollection_AddT.restype=c_void_p
        intPtr = GetDllLibPdf().PdfListItemCollection_AddT(self.Ptr, text)
        ret = None if intPtr==None else PdfListItem(intPtr)
        return ret


    @dispatch

    def Add(self ,text:str,itemIndent:float)->PdfListItem:
        """
    <summary>
        Adds the specified text.
    </summary>
    <param name="text">The text.</param>
    <param name="itemIndent">The item indent.</param>
    <returns>List item.</returns>
        """
        
        GetDllLibPdf().PdfListItemCollection_AddTI.argtypes=[c_void_p ,c_wchar_p,c_float]
        GetDllLibPdf().PdfListItemCollection_AddTI.restype=c_void_p
        intPtr = GetDllLibPdf().PdfListItemCollection_AddTI(self.Ptr, text,itemIndent)
        ret = None if intPtr==None else PdfListItem(intPtr)
        return ret


    @dispatch

    def Add(self ,text:str,font:PdfFontBase)->PdfListItem:
        """
    <summary>
        Adds the specified text.
    </summary>
    <param name="text">The text.</param>
    <param name="font">The font.</param>
    <returns>The item index in collection.</returns>
        """
        intPtrfont:c_void_p = font.Ptr

        GetDllLibPdf().PdfListItemCollection_AddTF.argtypes=[c_void_p ,c_wchar_p,c_void_p]
        GetDllLibPdf().PdfListItemCollection_AddTF.restype=c_void_p
        intPtr = GetDllLibPdf().PdfListItemCollection_AddTF(self.Ptr, text,intPtrfont)
        ret = None if intPtr==None else PdfListItem(intPtr)
        return ret


    @dispatch

    def Add(self ,text:str,font:PdfFontBase,itemIndent:float)->PdfListItem:
        """
    <summary>
        Adds the specified text.
    </summary>
    <param name="text">The text.</param>
    <param name="font">The font.</param>
    <param name="itemIndent">The item indent.</param>
    <returns>List item.</returns>
        """
        intPtrfont:c_void_p = font.Ptr

        GetDllLibPdf().PdfListItemCollection_AddTFI.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_float]
        GetDllLibPdf().PdfListItemCollection_AddTFI.restype=c_void_p
        intPtr = GetDllLibPdf().PdfListItemCollection_AddTFI(self.Ptr, text,intPtrfont,itemIndent)
        ret = None if intPtr==None else PdfListItem(intPtr)
        return ret


    @dispatch

    def Insert(self ,index:int,item:PdfListItem):
        """
    <summary>
        Inserts item at the specified index.
    </summary>
    <param name="index">The specified index.</param>
    <param name="item">The item.</param>
    <returns>The item index </returns>
        """
        intPtritem:c_void_p = item.Ptr

        GetDllLibPdf().PdfListItemCollection_Insert.argtypes=[c_void_p ,c_int,c_void_p]
        GetDllLibPdf().PdfListItemCollection_Insert(self.Ptr, index,intPtritem)

    @dispatch

    def Insert(self ,index:int,item:PdfListItem,itemIndent:float):
        """
    <summary>
        Inserts the specified index.
    </summary>
    <param name="index">The index.</param>
    <param name="item">The item.</param>
    <param name="itemIndent">The item indent.</param>
        """
        intPtritem:c_void_p = item.Ptr

        GetDllLibPdf().PdfListItemCollection_InsertIII.argtypes=[c_void_p ,c_int,c_void_p,c_float]
        GetDllLibPdf().PdfListItemCollection_InsertIII(self.Ptr, index,intPtritem,itemIndent)


    def Remove(self ,item:'PdfListItem'):
        """
    <summary>
        Removes the specified item from the list.
    </summary>
    <param name="item">The specified item.</param>
        """
        intPtritem:c_void_p = item.Ptr

        GetDllLibPdf().PdfListItemCollection_Remove.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfListItemCollection_Remove(self.Ptr, intPtritem)


    def RemoveAt(self ,index:int):
        """
    <summary>
        Removes the item at the specified index from the list.
    </summary>
    <param name="index">he specified index.</param>
        """
        
        GetDllLibPdf().PdfListItemCollection_RemoveAt.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfListItemCollection_RemoveAt(self.Ptr, index)


    def IndexOf(self ,item:'PdfListItem')->int:
        """
    <summary>
        Determines the index of a specific item in the list.
    </summary>
    <param name="item">The item to locate in the list. </param>
    <returns>The index of item if found in the list; otherwise, -1. </returns>
        """
        intPtritem:c_void_p = item.Ptr

        GetDllLibPdf().PdfListItemCollection_IndexOf.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfListItemCollection_IndexOf.restype=c_int
        ret = GetDllLibPdf().PdfListItemCollection_IndexOf(self.Ptr, intPtritem)
        return ret

    def Clear(self):
        """
    <summary>
        Clears collection.
    </summary>
        """
        GetDllLibPdf().PdfListItemCollection_Clear.argtypes=[c_void_p]
        GetDllLibPdf().PdfListItemCollection_Clear(self.Ptr)

