from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfSectionCollection (  IEnumerable) :
    """
    <summary>
        The collection of the sections.
    </summary>
    """

    def get_Item(self ,index:int)->'PdfSection':
        """
    <summary>
        Gets the  at the specified index.
    </summary>
<value></value>
        """
        
        GetDllLibPdf().PdfSectionCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfSectionCollection_get_Item.restype=c_void_p
        intPtr = GetDllLibPdf().PdfSectionCollection_get_Item(self.Ptr, index)
        ret = None if intPtr==None else PdfSection(intPtr)
        return ret


    @property
    def Count(self)->int:
        """
    <summary>
        Gets the count.
    </summary>
<value>The count.</value>
        """
        GetDllLibPdf().PdfSectionCollection_get_Count.argtypes=[c_void_p]
        GetDllLibPdf().PdfSectionCollection_get_Count.restype=c_int
        ret = GetDllLibPdf().PdfSectionCollection_get_Count(self.Ptr)
        return ret

    @dispatch

    def Add(self ,pageSettings:PdfPageSettings)->PdfSection:
        """
    <summary>
        Creates a section and adds it to the collection.
    </summary>
    <returns>Created section object.</returns>
        """
        intPtrpageSettings:c_void_p = pageSettings.Ptr

        GetDllLibPdf().PdfSectionCollection_Add.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfSectionCollection_Add.restype=c_void_p
        intPtr = GetDllLibPdf().PdfSectionCollection_Add(self.Ptr, intPtrpageSettings)
        ret = None if intPtr==None else PdfSection(intPtr)
        return ret


    @dispatch

    def Add(self)->PdfSection:
        """

        """
        GetDllLibPdf().PdfSectionCollection_Add1.argtypes=[c_void_p]
        GetDllLibPdf().PdfSectionCollection_Add1.restype=c_void_p
        intPtr = GetDllLibPdf().PdfSectionCollection_Add1(self.Ptr)
        ret = None if intPtr==None else PdfSection(intPtr)
        return ret



    def IndexOf(self ,section:'PdfSection')->int:
        """
    <summary>
        Determines the index of the section.
    </summary>
    <param name="section">The section.</param>
    <returns>The index of the section.</returns>
        """
        intPtrsection:c_void_p = section.Ptr

        GetDllLibPdf().PdfSectionCollection_IndexOf.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfSectionCollection_IndexOf.restype=c_int
        ret = GetDllLibPdf().PdfSectionCollection_IndexOf(self.Ptr, intPtrsection)
        return ret


    def Insert(self ,index:int,section:'PdfSection'):
        """
    <summary>
        Inserts the section at the specified index.
    </summary>
    <param name="index">The index.</param>
    <param name="section">The section.</param>
        """
        intPtrsection:c_void_p = section.Ptr

        GetDllLibPdf().PdfSectionCollection_Insert.argtypes=[c_void_p ,c_int,c_void_p]
        GetDllLibPdf().PdfSectionCollection_Insert(self.Ptr, index,intPtrsection)


    def Contains(self ,section:'PdfSection')->bool:
        """
    <summary>
        Checks whether the collection contains the section.
    </summary>
    <param name="section">The section object.</param>
    <returns>True - if the sections belongs to the collection, False otherwise.</returns>
        """
        intPtrsection:c_void_p = section.Ptr

        GetDllLibPdf().PdfSectionCollection_Contains.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfSectionCollection_Contains.restype=c_bool
        ret = GetDllLibPdf().PdfSectionCollection_Contains(self.Ptr, intPtrsection)
        return ret


    def GetEnumerator(self)->'IEnumerator':
        """

        """
        GetDllLibPdf().PdfSectionCollection_GetEnumerator.argtypes=[c_void_p]
        GetDllLibPdf().PdfSectionCollection_GetEnumerator.restype=c_void_p
        intPtr = GetDllLibPdf().PdfSectionCollection_GetEnumerator(self.Ptr)
        ret = None if intPtr==None else IEnumerator(intPtr)
        return ret


