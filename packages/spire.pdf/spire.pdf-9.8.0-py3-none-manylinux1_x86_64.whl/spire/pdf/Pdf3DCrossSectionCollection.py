from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Pdf3DCrossSectionCollection (SpireObject) :
    """
    <summary>
        Represents the collection of  objects. 
    </summary>
    """

    def Add(self ,value:'Pdf3DCrossSection')->int:
        """
    <summary>
        Adds the specified value.
    </summary>
    <param name="value">The value.</param>
    <returns></returns>
        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().Pdf3DCrossSectionCollection_Add.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().Pdf3DCrossSectionCollection_Add.restype=c_int
        ret = GetDllLibPdf().Pdf3DCrossSectionCollection_Add(self.Ptr, intPtrvalue)
        return ret


    def Contains(self ,value:'Pdf3DCrossSection')->bool:
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

        GetDllLibPdf().Pdf3DCrossSectionCollection_Contains.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().Pdf3DCrossSectionCollection_Contains.restype=c_bool
        ret = GetDllLibPdf().Pdf3DCrossSectionCollection_Contains(self.Ptr, intPtrvalue)
        return ret


    def IndexOf(self ,value:'Pdf3DCrossSection')->int:
        """
    <summary>
        Indexes the of.
    </summary>
    <param name="value">The value.</param>
    <returns></returns>
        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().Pdf3DCrossSectionCollection_IndexOf.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().Pdf3DCrossSectionCollection_IndexOf.restype=c_int
        ret = GetDllLibPdf().Pdf3DCrossSectionCollection_IndexOf(self.Ptr, intPtrvalue)
        return ret


    def Insert(self ,index:int,value:'Pdf3DCrossSection'):
        """
    <summary>
        Inserts the specified index.
    </summary>
    <param name="index">The index.</param>
    <param name="value">The value.</param>
        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().Pdf3DCrossSectionCollection_Insert.argtypes=[c_void_p ,c_int,c_void_p]
        GetDllLibPdf().Pdf3DCrossSectionCollection_Insert(self.Ptr, index,intPtrvalue)


    def Remove(self ,value:'Pdf3DCrossSection'):
        """
    <summary>
        Removes the specified value.
    </summary>
    <param name="value">The value.</param>
        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().Pdf3DCrossSectionCollection_Remove.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().Pdf3DCrossSectionCollection_Remove(self.Ptr, intPtrvalue)


    def get_Item(self ,index:int)->'Pdf3DCrossSection':
        """
    <summary>
        Gets or sets the  at the specified index.
    </summary>
        """
        
        GetDllLibPdf().Pdf3DCrossSectionCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().Pdf3DCrossSectionCollection_get_Item.restype=c_void_p
        intPtr = GetDllLibPdf().Pdf3DCrossSectionCollection_get_Item(self.Ptr, index)
        ret = None if intPtr==None else Pdf3DCrossSection(intPtr)
        return ret



    def set_Item(self ,index:int,value:'Pdf3DCrossSection'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().Pdf3DCrossSectionCollection_set_Item.argtypes=[c_void_p ,c_int,c_void_p]
        GetDllLibPdf().Pdf3DCrossSectionCollection_set_Item(self.Ptr, index,intPtrvalue)

