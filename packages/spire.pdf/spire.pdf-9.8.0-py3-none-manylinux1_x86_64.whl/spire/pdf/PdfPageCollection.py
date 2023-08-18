from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfPageCollection (  IEnumerable) :
    """
    <summary>
        Implements routines for manipulation with loaded pages.
    </summary>
    """

    def add_PageAdded(self ,value:'PageAddedEventHandler'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().PdfPageCollection_add_PageAdded.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfPageCollection_add_PageAdded(self.Ptr, intPtrvalue)


    def remove_PageAdded(self ,value:'PageAddedEventHandler'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().PdfPageCollection_remove_PageAdded.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfPageCollection_remove_PageAdded(self.Ptr, intPtrvalue)

    @property
    def SectionCount(self)->int:
        """
    <summary>
        Get the Section Count.
    </summary>
        """
        GetDllLibPdf().PdfPageCollection_get_SectionCount.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageCollection_get_SectionCount.restype=c_int
        ret = GetDllLibPdf().PdfPageCollection_get_SectionCount(self.Ptr)
        return ret


    def get_Item(self ,index:int)->'PdfPageBase':
        """
    <summary>
        Gets the  at the specified index.
    </summary>
        """
        
        GetDllLibPdf().PdfPageCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfPageCollection_get_Item.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageCollection_get_Item(self.Ptr, index)
        ret = None if intPtr==None else PdfPageBase(intPtr)
        return ret


    @property
    def Count(self)->int:
        """
    <summary>
        Gets the count.
    </summary>
        """
        GetDllLibPdf().PdfPageCollection_get_Count.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageCollection_get_Count.restype=c_int
        ret = GetDllLibPdf().PdfPageCollection_get_Count(self.Ptr)
        return ret

    @dispatch

    def Add(self)->PdfPageBase:
        """
    <summary>
        Creates a new page and adds it to the collection.
    </summary>
    <returns>The created page.</returns>
        """
        GetDllLibPdf().PdfPageCollection_Add.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageCollection_Add.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageCollection_Add(self.Ptr)
        ret = None if intPtr==None else PdfPageBase(intPtr)
        return ret


    @dispatch

    def Add(self ,size:SizeF)->PdfPageBase:
        """
    <summary>
        Creates a new page of the specified size and adds it to the collection.
    </summary>
    <param name="size">The size of the new page.</param>
    <returns>The created page.</returns>
        """
        intPtrsize:c_void_p = size.Ptr

        GetDllLibPdf().PdfPageCollection_AddS.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfPageCollection_AddS.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageCollection_AddS(self.Ptr, intPtrsize)
        ret = None if intPtr==None else PdfPageBase(intPtr)
        return ret


    @dispatch

    def Add(self ,size:SizeF,margins:PdfMargins)->PdfPageBase:
        """
    <summary>
        Creates a new page of the specified size and with the specified margins
            and adds it to the collection.
    </summary>
    <param name="size">The size of the new page.</param>
    <param name="margins">The margins of the new page.</param>
    <returns>The created page.</returns>
        """
        intPtrsize:c_void_p = size.Ptr
        intPtrmargins:c_void_p = margins.Ptr

        GetDllLibPdf().PdfPageCollection_AddSM.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().PdfPageCollection_AddSM.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageCollection_AddSM(self.Ptr, intPtrsize,intPtrmargins)
        ret = None if intPtr==None else PdfPageBase(intPtr)
        return ret


    @dispatch

    def Add(self ,size:SizeF,margins:PdfMargins,rotation:PdfPageRotateAngle)->PdfPageBase:
        """
    <summary>
        Creates a new page of the specified size and with the specified margins
            and adds it to the collection.
    </summary>
    <param name="size">The size of the new page.</param>
    <param name="margins">The margins of the new page.</param>
    <param name="rotation">The rotation of the new page.</param>
    <returns>The created page.</returns>
        """
        intPtrsize:c_void_p = size.Ptr
        intPtrmargins:c_void_p = margins.Ptr
        enumrotation:c_int = rotation.value

        GetDllLibPdf().PdfPageCollection_AddSMR.argtypes=[c_void_p ,c_void_p,c_void_p,c_int]
        GetDllLibPdf().PdfPageCollection_AddSMR.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageCollection_AddSMR(self.Ptr, intPtrsize,intPtrmargins,enumrotation)
        ret = None if intPtr==None else PdfPageBase(intPtr)
        return ret


    @dispatch

    def Add(self ,size:SizeF,margins:PdfMargins,rotation:PdfPageRotateAngle,orientation:PdfPageOrientation)->PdfPageBase:
        """
    <summary>
        Creates a new page of the specified size and with the specified margins
            and adds it to the collection.
    </summary>
    <param name="size">The size of the page.</param>
    <param name="margins">The margins of the page.</param>
    <param name="rotation">The rotation of the new page.</param>
    <param name="orientation">The orientation of the new page.</param>
    <returns>The created page.</returns>
        """
        intPtrsize:c_void_p = size.Ptr
        intPtrmargins:c_void_p = margins.Ptr
        enumrotation:c_int = rotation.value
        enumorientation:c_int = orientation.value

        GetDllLibPdf().PdfPageCollection_AddSMRO.argtypes=[c_void_p ,c_void_p,c_void_p,c_int,c_int]
        GetDllLibPdf().PdfPageCollection_AddSMRO.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageCollection_AddSMRO(self.Ptr, intPtrsize,intPtrmargins,enumrotation,enumorientation)
        ret = None if intPtr==None else PdfPageBase(intPtr)
        return ret


    @dispatch

    def Insert(self ,index:int)->PdfPageBase:
        """
    <summary>
        Creates a new page and inserts it at the specified index.
    </summary>
    <param name="index">The index.</param>
    <returns>The created page.</returns>
        """
        
        GetDllLibPdf().PdfPageCollection_Insert.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfPageCollection_Insert.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageCollection_Insert(self.Ptr, index)
        ret = None if intPtr==None else PdfPageBase(intPtr)
        return ret


    @dispatch

    def Insert(self ,index:int,size:SizeF)->PdfPageBase:
        """
    <summary>
        Creates a new page and inserts it at the specified index.
    </summary>
    <param name="index">The index.</param>
    <param name="size">The size of the page.</param>
    <returns>The created page.</returns>
        """
        intPtrsize:c_void_p = size.Ptr

        GetDllLibPdf().PdfPageCollection_InsertIS.argtypes=[c_void_p ,c_int,c_void_p]
        GetDllLibPdf().PdfPageCollection_InsertIS.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageCollection_InsertIS(self.Ptr, index,intPtrsize)
        ret = None if intPtr==None else PdfPageBase(intPtr)
        return ret


    @dispatch

    def Insert(self ,index:int,size:SizeF,margins:PdfMargins)->PdfPageBase:
        """
    <summary>
        Creates a new page and inserts it at the specified index.
    </summary>
    <param name="index">The index.</param>
    <param name="size">The size of the page.</param>
    <param name="margins">The margins of the page.</param>
    <returns>The created page.</returns>
        """
        intPtrsize:c_void_p = size.Ptr
        intPtrmargins:c_void_p = margins.Ptr

        GetDllLibPdf().PdfPageCollection_InsertISM.argtypes=[c_void_p ,c_int,c_void_p,c_void_p]
        GetDllLibPdf().PdfPageCollection_InsertISM.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageCollection_InsertISM(self.Ptr, index,intPtrsize,intPtrmargins)
        ret = None if intPtr==None else PdfPageBase(intPtr)
        return ret


    @dispatch

    def Insert(self ,index:int,size:SizeF,margins:PdfMargins,rotation:PdfPageRotateAngle)->PdfPageBase:
        """
    <summary>
        Creates a new page and inserts it at the specified index.
    </summary>
    <param name="index">The index.</param>
    <param name="size">The size of the page.</param>
    <param name="margins">The margins of the page.</param>
    <param name="rotation">The rotation of the new page.</param>
    <returns>The created page.</returns>
        """
        intPtrsize:c_void_p = size.Ptr
        intPtrmargins:c_void_p = margins.Ptr
        enumrotation:c_int = rotation.value

        GetDllLibPdf().PdfPageCollection_InsertISMR.argtypes=[c_void_p ,c_int,c_void_p,c_void_p,c_int]
        GetDllLibPdf().PdfPageCollection_InsertISMR.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageCollection_InsertISMR(self.Ptr, index,intPtrsize,intPtrmargins,enumrotation)
        ret = None if intPtr==None else PdfPageBase(intPtr)
        return ret



    def RemoveAt(self ,index:int):
        """
    <summary>
        Removes the page at the given specified index.
    </summary>
    <param name="index"> Index of the page.</param>
        """
        
        GetDllLibPdf().PdfPageCollection_RemoveAt.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfPageCollection_RemoveAt(self.Ptr, index)


    def Remove(self ,page:'PdfPageBase'):
        """
    <summary>
        Removes the specified page.
    </summary>
    <param name="page">The page to be remove.</param>
        """
        intPtrpage:c_void_p = page.Ptr

        GetDllLibPdf().PdfPageCollection_Remove.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfPageCollection_Remove(self.Ptr, intPtrpage)


    def ReArrange(self ,orderArray:List[int]):
        """
    <summary>
        ReArrange the Pages in the Loaded Document.
    </summary>
    <param name="orderArray">The page sequence to arrange the pages.</param>
        """
        #arrayorderArray:ArrayTypeorderArray = ""
        countorderArray = len(orderArray)
        ArrayTypeorderArray = c_int * countorderArray
        arrayorderArray = ArrayTypeorderArray()
        for i in range(0, countorderArray):
            arrayorderArray[i] = orderArray[i]


        GetDllLibPdf().PdfPageCollection_ReArrange.argtypes=[c_void_p ,ArrayTypeorderArray]
        GetDllLibPdf().PdfPageCollection_ReArrange(self.Ptr, arrayorderArray,countorderArray)

    @dispatch

    def Insert(self ,index:int,size:SizeF,margins:PdfMargins,rotation:PdfPageRotateAngle,orientation:PdfPageOrientation,existsPage:bool)->PdfPageBase:
        """
    <summary>
        Creates a new page and inserts it at the specified index.
    </summary>
    <param name="index">The index.</param>
    <param name="size">The size of the page.</param>
    <param name="margins">The margins of the page.</param>
    <param name="rotation">The rotation of the new page.</param>
    <param name="orientation">The orientation of the new page.</param>
    <returns>The created page.</returns>
        """
        intPtrsize:c_void_p = size.Ptr
        intPtrmargins:c_void_p = margins.Ptr
        enumrotation:c_int = rotation.value
        enumorientation:c_int = orientation.value

        GetDllLibPdf().PdfPageCollection_InsertISMROE.argtypes=[c_void_p ,c_int,c_void_p,c_void_p,c_int,c_int,c_bool]
        GetDllLibPdf().PdfPageCollection_InsertISMROE.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageCollection_InsertISMROE(self.Ptr, index,intPtrsize,intPtrmargins,enumrotation,enumorientation,existsPage)
        ret = None if intPtr==None else PdfPageBase(intPtr)
        return ret


    @dispatch

    def Insert(self ,index:int,newPage,settings:PdfPageSettings,existsPage:bool)->PdfPageBase:
        """

        """
        intPtrpage:c_void_p = newPage.Ptr
        intPtrsettings:c_void_p = settings.Ptr

        GetDllLibPdf().PdfPageCollection_InsertIPSE.argtypes=[c_void_p ,c_int,c_void_p,c_void_p,c_bool]
        GetDllLibPdf().PdfPageCollection_InsertIPSE.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageCollection_InsertIPSE(self.Ptr, index,intPtrpage,intPtrsettings,existsPage)
        ret = None if intPtr==None else PdfPageBase(intPtr)
        return ret


    @dispatch

    def Insert(self ,index:int,settings:PdfPageSettings,existsPage:bool)->PdfPageBase:
        """

        """
        intPtrsettings:c_void_p = settings.Ptr

        GetDllLibPdf().PdfPageCollection_InsertISE.argtypes=[c_void_p ,c_int,c_void_p,c_bool]
        GetDllLibPdf().PdfPageCollection_InsertISE.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageCollection_InsertISE(self.Ptr, index,intPtrsettings,existsPage)
        ret = None if intPtr==None else PdfPageBase(intPtr)
        return ret



    def IndexOf(self ,page:'PdfPageBase')->int:
        """
    <summary>
        Gets the index of the page in the document.
    </summary>
    <param name="page">The current page.</param>
    <returns>Index of the page in the document if exists, -1 otherwise.</returns>
        """
        intPtrpage:c_void_p = page.Ptr

        GetDllLibPdf().PdfPageCollection_IndexOf.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfPageCollection_IndexOf.restype=c_int
        ret = GetDllLibPdf().PdfPageCollection_IndexOf(self.Ptr, intPtrpage)
        return ret


    def GetEnumerator(self)->'IEnumerator':
        """

        """
        GetDllLibPdf().PdfPageCollection_GetEnumerator.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageCollection_GetEnumerator.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageCollection_GetEnumerator(self.Ptr)
        ret = None if intPtr==None else IEnumerator(intPtr)
        return ret


