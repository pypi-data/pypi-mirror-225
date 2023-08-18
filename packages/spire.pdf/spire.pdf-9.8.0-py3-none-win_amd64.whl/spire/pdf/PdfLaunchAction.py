from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfLaunchAction (  PdfAction) :
    @dispatch
    def __init__(self, filename:str):
        GetDllLibPdf().PdfLaunchAction_CreatePdfLaunchActionF.argtypes=[c_wchar_p]
        GetDllLibPdf().PdfLaunchAction_CreatePdfLaunchActionF.restype = c_void_p
        intPtr = GetDllLibPdf().PdfLaunchAction_CreatePdfLaunchActionF(filename)
        super(PdfLaunchAction, self).__init__(intPtr)
    @dispatch
    def __init__(self, filename:str,path:PdfFilePathType):
        enumType:c_int = path.value
        GetDllLibPdf().PdfLaunchAction_CreatePdfLaunchActionFP.argtypes=[c_wchar_p,c_int]
        GetDllLibPdf().PdfLaunchAction_CreatePdfLaunchActionFP.restype = c_void_p
        intPtr = GetDllLibPdf().PdfLaunchAction_CreatePdfLaunchActionFP(filename,enumType)
        super(PdfLaunchAction, self).__init__(intPtr)
    """
    <summary>
        Represents an action which launches an application or opens or prints a document.
    </summary>
    """
    @property

    def FileName(self)->str:
        """
    <summary>
        Gets or sets file to be launched.
    </summary>
        """
        GetDllLibPdf().PdfLaunchAction_get_FileName.argtypes=[c_void_p]
        GetDllLibPdf().PdfLaunchAction_get_FileName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfLaunchAction_get_FileName(self.Ptr))
        return ret


    @FileName.setter
    def FileName(self, value:str):
        GetDllLibPdf().PdfLaunchAction_set_FileName.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfLaunchAction_set_FileName(self.Ptr, value)

    @property
    def IsNewWindow(self)->bool:
        """
    <summary>
        Indicates the target document should be opened in a new window or not.
    </summary>
        """
        GetDllLibPdf().PdfLaunchAction_get_IsNewWindow.argtypes=[c_void_p]
        GetDllLibPdf().PdfLaunchAction_get_IsNewWindow.restype=c_bool
        ret = GetDllLibPdf().PdfLaunchAction_get_IsNewWindow(self.Ptr)
        return ret

    @IsNewWindow.setter
    def IsNewWindow(self, value:bool):
        GetDllLibPdf().PdfLaunchAction_set_IsNewWindow.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfLaunchAction_set_IsNewWindow(self.Ptr, value)

