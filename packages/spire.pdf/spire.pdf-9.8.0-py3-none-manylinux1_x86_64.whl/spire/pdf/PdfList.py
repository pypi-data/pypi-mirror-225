from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfList (  PdfListBase) :
    @dispatch
    def __init__(self):
        GetDllLibPdf().PdfList_CreatePdfList.restype = c_void_p
        intPtr = GetDllLibPdf().PdfList_CreatePdfList()
        super(PdfList, self).__init__(intPtr)
    @dispatch
    def __init__(self, items:PdfListItemCollection):
        ptrItem:c_void_p = items.Ptr
        GetDllLibPdf().PdfList_CreatePdfListI.argtypes=[c_void_p]
        GetDllLibPdf().PdfList_CreatePdfListI.restype = c_void_p
        intPtr = GetDllLibPdf().PdfList_CreatePdfListI(ptrItem)
        super(PdfList, self).__init__(intPtr)
    @dispatch
    def __init__(self, font:PdfFontBase):
        ptrFont:c_void_p = font.Ptr
        GetDllLibPdf().PdfList_CreatePdfListF.argtypes=[c_void_p]
        GetDllLibPdf().PdfList_CreatePdfListF.restype = c_void_p
        intPtr = GetDllLibPdf().PdfList_CreatePdfListF(ptrFont)
        super(PdfList, self).__init__(intPtr)
    @dispatch
    def __init__(self, marker:PdfMarker):
        ptrMarker:c_void_p = marker.Ptr
        GetDllLibPdf().PdfList_CreatePdfListM.argtypes=[c_void_p]
        GetDllLibPdf().PdfList_CreatePdfListM.restype = c_void_p
        intPtr = GetDllLibPdf().PdfList_CreatePdfListM(ptrMarker)
        super(PdfList, self).__init__(intPtr)
    @dispatch
    def __init__(self, items:PdfListItemCollection,marker:PdfMarker):
        ptrItem:c_void_p = items.Ptr
        ptrMarker:c_void_p = marker.Ptr
        GetDllLibPdf().PdfList_CreatePdfListIM.argtypes=[c_void_p,c_void_p]
        GetDllLibPdf().PdfList_CreatePdfListIM.restype = c_void_p
        intPtr = GetDllLibPdf().PdfList_CreatePdfListIM(ptrItem,ptrMarker)
        super(PdfList, self).__init__(intPtr)
    @dispatch
    def __init__(self, text:str):
        GetDllLibPdf().PdfList_CreatePdfListT.argtypes=[c_wchar_p]
        GetDllLibPdf().PdfList_CreatePdfListT.restype = c_void_p
        intPtr = GetDllLibPdf().PdfList_CreatePdfListT(text)
        super(PdfList, self).__init__(intPtr)
    @dispatch
    def __init__(self, text:str,marker:PdfMarker):
        ptrMarker:c_void_p = marker.Ptr
        GetDllLibPdf().PdfList_CreatePdfListTM.argtypes=[c_wchar_p,c_void_p]
        GetDllLibPdf().PdfList_CreatePdfListTM.restype = c_void_p
        intPtr = GetDllLibPdf().PdfList_CreatePdfListTM(text,ptrMarker)
        super(PdfList, self).__init__(intPtr)
    """
    <summary>
        Represents unordered list.
    </summary>
    """
    @property

    def Marker(self)->'PdfMarker':
        """
    <summary>
        Gets or sets the marker.
    </summary>
        """
        GetDllLibPdf().PdfList_get_Marker.argtypes=[c_void_p]
        GetDllLibPdf().PdfList_get_Marker.restype=c_void_p
        intPtr = GetDllLibPdf().PdfList_get_Marker(self.Ptr)
        ret = None if intPtr==None else PdfMarker(intPtr)
        return ret


    @Marker.setter
    def Marker(self, value:'PdfMarker'):
        GetDllLibPdf().PdfList_set_Marker.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfList_set_Marker(self.Ptr, value.Ptr)

