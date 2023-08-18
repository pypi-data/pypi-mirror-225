from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfGoToAction (  PdfAction) :
    @dispatch
    def __init__(self, destination:PdfDestination):
        ptrDest:c_void_p = destination.Ptr
        GetDllLibPdf().PdfGoToAction_CreatePdfGoToActionD.argtypes=[c_void_p]
        GetDllLibPdf().PdfGoToAction_CreatePdfGoToActionD.restype = c_void_p
        intPtr = GetDllLibPdf().PdfGoToAction_CreatePdfGoToActionD(ptrDest)
        super(PdfGoToAction, self).__init__(intPtr)
    @dispatch
    def __init__(self, newPage):
        ptrPage:c_void_p = newPage.Ptr
        GetDllLibPdf().PdfGoToAction_CreatePdfGoToActionP.argtypes=[c_void_p]
        GetDllLibPdf().PdfGoToAction_CreatePdfGoToActionP.restype = c_void_p
        intPtr = GetDllLibPdf().PdfGoToAction_CreatePdfGoToActionP(ptrPage)
        super(PdfGoToAction, self).__init__(intPtr)
    """
    <summary>
        Represents an action which goes to a destination in the current document.
    </summary>
    """
    @property

    def Destination(self)->'PdfDestination':
        """
    <summary>
        Gets or sets the destination.
    </summary>
<value>The destination.</value>
        """
        GetDllLibPdf().PdfGoToAction_get_Destination.argtypes=[c_void_p]
        GetDllLibPdf().PdfGoToAction_get_Destination.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGoToAction_get_Destination(self.Ptr)
        ret = None if intPtr==None else PdfDestination(intPtr)
        return ret


    @Destination.setter
    def Destination(self, value:'PdfDestination'):
        GetDllLibPdf().PdfGoToAction_set_Destination.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfGoToAction_set_Destination(self.Ptr, value.Ptr)

