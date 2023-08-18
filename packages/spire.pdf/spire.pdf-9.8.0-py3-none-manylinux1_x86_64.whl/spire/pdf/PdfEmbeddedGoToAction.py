from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfEmbeddedGoToAction (  PdfAction) :
    @dispatch
    def __init__(self, filename:str,dest:PdfDestination,newWindow:bool):
        ptrDest:c_void_p = dest.Ptr

        GetDllLibPdf().PdfEmbeddedGoToAction_CreatePdfEmbeddedGoToActionFDN.argtypes=[c_wchar_p,c_void_p,c_bool]
        GetDllLibPdf().PdfEmbeddedGoToAction_CreatePdfEmbeddedGoToActionFDN.restype = c_void_p
        intPtr = GetDllLibPdf().PdfEmbeddedGoToAction_CreatePdfEmbeddedGoToActionFDN(filename,ptrDest,newWindow)
        super(PdfEmbeddedGoToAction, self).__init__(intPtr)
    """
    <summary>
        Represents an embedded go-to action which allows jumping to or from a PDF file that is embedded in another PDF file.
    </summary>
    """
    @property
    def IsNewWindow(self)->bool:
        """
    <summary>
        Indicates the target document should be opened in a new window or not.
    </summary>
        """
        GetDllLibPdf().PdfEmbeddedGoToAction_get_IsNewWindow.argtypes=[c_void_p]
        GetDllLibPdf().PdfEmbeddedGoToAction_get_IsNewWindow.restype=c_bool
        ret = GetDllLibPdf().PdfEmbeddedGoToAction_get_IsNewWindow(self.Ptr)
        return ret

    @IsNewWindow.setter
    def IsNewWindow(self, value:bool):
        GetDllLibPdf().PdfEmbeddedGoToAction_set_IsNewWindow.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfEmbeddedGoToAction_set_IsNewWindow(self.Ptr, value)

    @property

    def FileName(self)->str:
        """
    <summary>
        The target document name.
    </summary>
        """
        GetDllLibPdf().PdfEmbeddedGoToAction_get_FileName.argtypes=[c_void_p]
        GetDllLibPdf().PdfEmbeddedGoToAction_get_FileName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfEmbeddedGoToAction_get_FileName(self.Ptr))
        return ret


    @FileName.setter
    def FileName(self, value:str):
        GetDllLibPdf().PdfEmbeddedGoToAction_set_FileName.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfEmbeddedGoToAction_set_FileName(self.Ptr, value)

    @property

    def Destination(self)->'PdfDestination':
        """
    <summary>
        The destination in the target document to jump to.
    </summary>
        """
        GetDllLibPdf().PdfEmbeddedGoToAction_get_Destination.argtypes=[c_void_p]
        GetDllLibPdf().PdfEmbeddedGoToAction_get_Destination.restype=c_void_p
        intPtr = GetDllLibPdf().PdfEmbeddedGoToAction_get_Destination(self.Ptr)
        ret = None if intPtr==None else PdfDestination(intPtr)
        return ret


