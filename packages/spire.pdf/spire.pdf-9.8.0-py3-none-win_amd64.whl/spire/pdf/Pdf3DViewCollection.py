from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Pdf3DViewCollection (SpireObject) :
    """
    <summary>
        Represents a collection of Pdf3DView objects. 
    </summary>
    """

    def Add(self ,value:'Pdf3DView')->int:
        """
    <summary>
        Adds the specified value.
    </summary>
    <param name="value">The value.</param>
    <returns>Pdf3DView</returns>
        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().Pdf3DViewCollection_Add.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().Pdf3DViewCollection_Add.restype=c_int
        ret = GetDllLibPdf().Pdf3DViewCollection_Add(self.Ptr, intPtrvalue)
        return ret


    def Contains(self ,value:'Pdf3DView')->bool:
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

        GetDllLibPdf().Pdf3DViewCollection_Contains.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().Pdf3DViewCollection_Contains.restype=c_bool
        ret = GetDllLibPdf().Pdf3DViewCollection_Contains(self.Ptr, intPtrvalue)
        return ret


    def IndexOf(self ,value:'Pdf3DView')->int:
        """
    <summary>
        Indexes the of the Pdf3DView object.
    </summary>
    <param name="value">The value.</param>
    <returns>Pdf3DView</returns>
        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().Pdf3DViewCollection_IndexOf.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().Pdf3DViewCollection_IndexOf.restype=c_int
        ret = GetDllLibPdf().Pdf3DViewCollection_IndexOf(self.Ptr, intPtrvalue)
        return ret


    def Insert(self ,index:int,value:'Pdf3DView'):
        """
    <summary>
        Inserts the specified index.
    </summary>
    <param name="index">The index.</param>
    <param name="value">The value.</param>
        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().Pdf3DViewCollection_Insert.argtypes=[c_void_p ,c_int,c_void_p]
        GetDllLibPdf().Pdf3DViewCollection_Insert(self.Ptr, index,intPtrvalue)


    def Remove(self ,value:'Pdf3DView'):
        """
    <summary>
        Removes the specified value.
    </summary>
    <param name="value">The Pdf3DView object.</param>
        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().Pdf3DViewCollection_Remove.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().Pdf3DViewCollection_Remove(self.Ptr, intPtrvalue)


    def get_Item(self ,index:int)->'Pdf3DView':
        """
    <summary>
        Gets or sets the  at the specified index.
    </summary>
<value>Pdf3DView</value>
        """
        
        GetDllLibPdf().Pdf3DViewCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().Pdf3DViewCollection_get_Item.restype=c_void_p
        intPtr = GetDllLibPdf().Pdf3DViewCollection_get_Item(self.Ptr, index)
        ret = None if intPtr==None else Pdf3DView(intPtr)
        return ret



    def set_Item(self ,index:int,value:'Pdf3DView'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().Pdf3DViewCollection_set_Item.argtypes=[c_void_p ,c_int,c_void_p]
        GetDllLibPdf().Pdf3DViewCollection_set_Item(self.Ptr, index,intPtrvalue)

