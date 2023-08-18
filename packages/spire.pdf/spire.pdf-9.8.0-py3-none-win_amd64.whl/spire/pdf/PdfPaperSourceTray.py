from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfPaperSourceTray (SpireObject) :
    """
    <summary>
        Specifies the paper tray when the document is printed.
    </summary>
    """
    @property
    def StartPage(self)->int:
        """
    <summary>
        Gets or sets the page number (non zero-based) of the first page to print.
    </summary>
        """
        GetDllLibPdf().PdfPaperSourceTray_get_StartPage.argtypes=[c_void_p]
        GetDllLibPdf().PdfPaperSourceTray_get_StartPage.restype=c_int
        ret = GetDllLibPdf().PdfPaperSourceTray_get_StartPage(self.Ptr)
        return ret

    @StartPage.setter
    def StartPage(self, value:int):
        GetDllLibPdf().PdfPaperSourceTray_set_StartPage.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfPaperSourceTray_set_StartPage(self.Ptr, value)

    @property
    def EndPage(self)->int:
        """
    <summary>
        Gets or sets the page number (non zero-based) of the last page to print.
    </summary>
        """
        GetDllLibPdf().PdfPaperSourceTray_get_EndPage.argtypes=[c_void_p]
        GetDllLibPdf().PdfPaperSourceTray_get_EndPage.restype=c_int
        ret = GetDllLibPdf().PdfPaperSourceTray_get_EndPage(self.Ptr)
        return ret

    @EndPage.setter
    def EndPage(self, value:int):
        GetDllLibPdf().PdfPaperSourceTray_set_EndPage.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfPaperSourceTray_set_EndPage(self.Ptr, value)

#    @property
#
#    def PrintPaperSource(self)->'PaperSource':
#        """
#    <summary>
#        Specifies the paper tray from which the printer gets paper.
#    </summary>
#        """
#        GetDllLibPdf().PdfPaperSourceTray_get_PrintPaperSource.argtypes=[c_void_p]
#        GetDllLibPdf().PdfPaperSourceTray_get_PrintPaperSource.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPaperSourceTray_get_PrintPaperSource(self.Ptr)
#        ret = None if intPtr==None else PaperSource(intPtr)
#        return ret
#


#    @PrintPaperSource.setter
#    def PrintPaperSource(self, value:'PaperSource'):
#        GetDllLibPdf().PdfPaperSourceTray_set_PrintPaperSource.argtypes=[c_void_p, c_void_p]
#        GetDllLibPdf().PdfPaperSourceTray_set_PrintPaperSource(self.Ptr, value.Ptr)


