from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfSortedList (  PdfListBase) :
    @dispatch
    def __init__(self):
        GetDllLibPdf().PdfSortedList_CreatePdfSortedList.restype = c_void_p
        intPtr = GetDllLibPdf().PdfSortedList_CreatePdfSortedList()
        super(PdfSortedList, self).__init__(intPtr)
    @dispatch
    def __init__(self, text:str):
        GetDllLibPdf().PdfSortedList_CreatePdfSortedListT.argtypes=[c_wchar_p]
        GetDllLibPdf().PdfSortedList_CreatePdfSortedListT.restype = c_void_p
        intPtr = GetDllLibPdf().PdfSortedList_CreatePdfSortedListT(text)
        super(PdfSortedList, self).__init__(intPtr)
    @dispatch
    def __init__(self, font:PdfFontBase):
        ptrFont:c_void_p = font.Ptr
        GetDllLibPdf().PdfSortedList_CreatePdfSortedListF.argtypes=[c_void_p]
        GetDllLibPdf().PdfSortedList_CreatePdfSortedListF.restype = c_void_p
        intPtr = GetDllLibPdf().PdfSortedList_CreatePdfSortedListF(ptrFont)
        super(PdfSortedList, self).__init__(intPtr)
    @dispatch
    def __init__(self, style:PdfNumberStyle):
        enumStyle:c_int = style.value
        GetDllLibPdf().PdfSortedList_CreatePdfSortedListS.argtypes=[c_int]
        GetDllLibPdf().PdfSortedList_CreatePdfSortedListS.restype = c_void_p
        intPtr = GetDllLibPdf().PdfSortedList_CreatePdfSortedListS(enumStyle)
        super(PdfSortedList, self).__init__(intPtr)
    @dispatch
    def __init__(self, items:PdfListItemCollection):
        ptrItem:c_void_p = items.Ptr
        GetDllLibPdf().PdfSortedList_CreatePdfSortedListI.argtypes=[c_void_p]
        GetDllLibPdf().PdfSortedList_CreatePdfSortedListI.restype = c_void_p
        intPtr = GetDllLibPdf().PdfSortedList_CreatePdfSortedListI(ptrItem)
        super(PdfSortedList, self).__init__(intPtr)
    @dispatch
    def __init__(self, marker:PdfOrderedMarker):
        ptrMarker:c_void_p = marker.Ptr
        GetDllLibPdf().PdfSortedList_CreatePdfSortedListI.argtypes=[c_void_p]
        GetDllLibPdf().PdfSortedList_CreatePdfSortedListI.restype = c_void_p
        intPtr = GetDllLibPdf().PdfSortedList_CreatePdfSortedListI(ptrMarker)
        super(PdfSortedList, self).__init__(intPtr)
    @dispatch
    def __init__(self, items:PdfListItemCollection,marker:PdfOrderedMarker):
        ptrItem:c_void_p = items.Ptr
        ptrMarker:c_void_p = marker.Ptr
        GetDllLibPdf().PdfSortedList_CreatePdfSortedListIM.argtypes=[c_void_p,c_void_p]
        GetDllLibPdf().PdfSortedList_CreatePdfSortedListIM.restype = c_void_p
        intPtr = GetDllLibPdf().PdfSortedList_CreatePdfSortedListIM(ptrItem,ptrMarker)
        super(PdfSortedList, self).__init__(intPtr)
    @dispatch
    def __init__(self, text:str,marker:PdfOrderedMarker):
        ptrMarker:c_void_p = marker.Ptr
        GetDllLibPdf().PdfSortedList_CreatePdfSortedListTM.argtypes=[c_wchar_p,c_void_p]
        GetDllLibPdf().PdfSortedList_CreatePdfSortedListTM.restype = c_void_p
        intPtr = GetDllLibPdf().PdfSortedList_CreatePdfSortedListTM(text,ptrMarker)
        super(PdfSortedList, self).__init__(intPtr)
    """
    <summary>
        Represents the ordered list.
    </summary>
    """
    @property

    def Marker(self)->'PdfOrderedMarker':
        """
    <summary>
        Gets or sets marker of the list items.
    </summary>
        """
        GetDllLibPdf().PdfSortedList_get_Marker.argtypes=[c_void_p]
        GetDllLibPdf().PdfSortedList_get_Marker.restype=c_void_p
        intPtr = GetDllLibPdf().PdfSortedList_get_Marker(self.Ptr)
        ret = None if intPtr==None else PdfOrderedMarker(intPtr)
        return ret


    @Marker.setter
    def Marker(self, value:'PdfOrderedMarker'):
        GetDllLibPdf().PdfSortedList_set_Marker.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfSortedList_set_Marker(self.Ptr, value.Ptr)

    @property
    def MarkerHierarchy(self)->bool:
        """
    <summary>
        True if user want to use numbering hierarchy, otherwise false.
    </summary>
        """
        GetDllLibPdf().PdfSortedList_get_MarkerHierarchy.argtypes=[c_void_p]
        GetDllLibPdf().PdfSortedList_get_MarkerHierarchy.restype=c_bool
        ret = GetDllLibPdf().PdfSortedList_get_MarkerHierarchy(self.Ptr)
        return ret

    @MarkerHierarchy.setter
    def MarkerHierarchy(self, value:bool):
        GetDllLibPdf().PdfSortedList_set_MarkerHierarchy.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfSortedList_set_MarkerHierarchy(self.Ptr, value)

