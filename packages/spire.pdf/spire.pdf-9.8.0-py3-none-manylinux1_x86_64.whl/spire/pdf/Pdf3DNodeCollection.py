from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Pdf3DNodeCollection (SpireObject) :
    """
    <summary>
        Represents a collection of  objects. 
    </summary>
    """

    def Add(self ,value:'Pdf3DNode')->int:
        """
    <summary>
        Adds the specified value.
                <param name="value">The value.</param></summary>
    <returns></returns>
        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().Pdf3DNodeCollection_Add.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().Pdf3DNodeCollection_Add.restype=c_int
        ret = GetDllLibPdf().Pdf3DNodeCollection_Add(self.Ptr, intPtrvalue)
        return ret


    def Contains(self ,value:'Pdf3DNode')->bool:
        """
    <summary>
        Determines whether [contains] [the specified value].
    </summary>
    <param name="value">The value.</param>
    <returns>
            if it contains the specified value, set to <c>true</c>.
            </returns>
        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().Pdf3DNodeCollection_Contains.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().Pdf3DNodeCollection_Contains.restype=c_bool
        ret = GetDllLibPdf().Pdf3DNodeCollection_Contains(self.Ptr, intPtrvalue)
        return ret


    def IndexOf(self ,value:'Pdf3DNode')->int:
        """
    <summary>
        Indexes the of.
    </summary>
    <param name="value">The value.</param>
    <returns></returns>
        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().Pdf3DNodeCollection_IndexOf.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().Pdf3DNodeCollection_IndexOf.restype=c_int
        ret = GetDllLibPdf().Pdf3DNodeCollection_IndexOf(self.Ptr, intPtrvalue)
        return ret


    def Insert(self ,index:int,value:'Pdf3DNode'):
        """
    <summary>
        Inserts the specified index.
    </summary>
    <param name="index">The index.</param>
    <param name="value">The value.</param>
        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().Pdf3DNodeCollection_Insert.argtypes=[c_void_p ,c_int,c_void_p]
        GetDllLibPdf().Pdf3DNodeCollection_Insert(self.Ptr, index,intPtrvalue)


    def Remove(self ,value:'Pdf3DNode'):
        """
    <summary>
        Removes the specified value.
    </summary>
    <param name="value">The value.</param>
        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().Pdf3DNodeCollection_Remove.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().Pdf3DNodeCollection_Remove(self.Ptr, intPtrvalue)


    def get_Item(self ,index:int)->'Pdf3DNode':
        """
    <summary>
        Gets or sets the  at the specified index.
    </summary>
        """
        
        GetDllLibPdf().Pdf3DNodeCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().Pdf3DNodeCollection_get_Item.restype=c_void_p
        intPtr = GetDllLibPdf().Pdf3DNodeCollection_get_Item(self.Ptr, index)
        ret = None if intPtr==None else Pdf3DNode(intPtr)
        return ret



    def set_Item(self ,index:int,value:'Pdf3DNode'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().Pdf3DNodeCollection_set_Item.argtypes=[c_void_p ,c_int,c_void_p]
        GetDllLibPdf().Pdf3DNodeCollection_set_Item(self.Ptr, index,intPtrvalue)

