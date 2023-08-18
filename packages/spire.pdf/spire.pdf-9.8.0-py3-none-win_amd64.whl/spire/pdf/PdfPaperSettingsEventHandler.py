from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfPaperSettingsEventHandler (SpireObject) :
    """
    <summary>
        Represents the method that handles paper setting event.
    </summary>
    <param name="sender">The source of the event.</param>
    <param name="e">The event data</param>
    """

    def Invoke(self ,sender:'SpireObject',e:'PdfPaperSettingsEventArgs'):
        """

        """
        intPtrsender:c_void_p = sender.Ptr
        intPtre:c_void_p = e.Ptr

        GetDllLibPdf().PdfPaperSettingsEventHandler_Invoke.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().PdfPaperSettingsEventHandler_Invoke(self.Ptr, intPtrsender,intPtre)

#
#    def BeginInvoke(self ,sender:'SpireObject',e:'PdfPaperSettingsEventArgs',callback:'AsyncCallback',object:'SpireObject')->'IAsyncResult':
#        """
#
#        """
#        intPtrsender:c_void_p = sender.Ptr
#        intPtre:c_void_p = e.Ptr
#        intPtrcallback:c_void_p = callback.Ptr
#        intPtrobject:c_void_p = object.Ptr
#
#        GetDllLibPdf().PdfPaperSettingsEventHandler_BeginInvoke.argtypes=[c_void_p ,c_void_p,c_void_p,c_void_p,c_void_p]
#        GetDllLibPdf().PdfPaperSettingsEventHandler_BeginInvoke.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPaperSettingsEventHandler_BeginInvoke(self.Ptr, intPtrsender,intPtre,intPtrcallback,intPtrobject)
#        ret = None if intPtr==None else IAsyncResult(intPtr)
#        return ret
#


#
#    def EndInvoke(self ,result:'IAsyncResult'):
#        """
#
#        """
#        intPtrresult:c_void_p = result.Ptr
#
#        GetDllLibPdf().PdfPaperSettingsEventHandler_EndInvoke.argtypes=[c_void_p ,c_void_p]
#        GetDllLibPdf().PdfPaperSettingsEventHandler_EndInvoke(self.Ptr, intPtrresult)


