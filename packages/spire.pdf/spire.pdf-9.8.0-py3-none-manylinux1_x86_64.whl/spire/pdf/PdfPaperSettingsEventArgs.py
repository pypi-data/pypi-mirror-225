from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfPaperSettingsEventArgs (SpireObject) :
    """
    <summary>
        Provides data for paper setting event.
    </summary>
    """
    @property
    def CurrentPaper(self)->int:
        """
    <summary>
        Get current paper index,from 1.
    </summary>
        """
        GetDllLibPdf().PdfPaperSettingsEventArgs_get_CurrentPaper.argtypes=[c_void_p]
        GetDllLibPdf().PdfPaperSettingsEventArgs_get_CurrentPaper.restype=c_int
        ret = GetDllLibPdf().PdfPaperSettingsEventArgs_get_CurrentPaper(self.Ptr)
        return ret

#    @property
#
#    def PaperSources(self)->List['PaperSource']:
#        """
#    <summary>
#         Gets the paper source trays that are available on the printer.
#    </summary>
#        """
#        GetDllLibPdf().PdfPaperSettingsEventArgs_get_PaperSources.argtypes=[c_void_p]
#        GetDllLibPdf().PdfPaperSettingsEventArgs_get_PaperSources.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().PdfPaperSettingsEventArgs_get_PaperSources(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, PaperSource)
#        return ret


#    @property
#
#    def CurrentPaperSource(self)->'PaperSource':
#        """
#    <summary>
#        Get or set current paper source on the printer.
#    </summary>
#        """
#        GetDllLibPdf().PdfPaperSettingsEventArgs_get_CurrentPaperSource.argtypes=[c_void_p]
#        GetDllLibPdf().PdfPaperSettingsEventArgs_get_CurrentPaperSource.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPaperSettingsEventArgs_get_CurrentPaperSource(self.Ptr)
#        ret = None if intPtr==None else PaperSource(intPtr)
#        return ret
#


#    @CurrentPaperSource.setter
#    def CurrentPaperSource(self, value:'PaperSource'):
#        GetDllLibPdf().PdfPaperSettingsEventArgs_set_CurrentPaperSource.argtypes=[c_void_p, c_void_p]
#        GetDllLibPdf().PdfPaperSettingsEventArgs_set_CurrentPaperSource(self.Ptr, value.Ptr)


