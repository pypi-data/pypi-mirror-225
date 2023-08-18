from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class ProgressEventHandler (SpireObject) :
    """
    <summary>
        Delegate for the  event.
    </summary>
    <param name="sender">The sender.</param>
    <param name="arguments">The arguments.</param>
    """

    def Invoke(self ,sender:'SpireObject',arguments:'ProgressEventArgs'):
        """

        """
        intPtrsender:c_void_p = sender.Ptr
        intPtrarguments:c_void_p = arguments.Ptr

        GetDllLibPdf().ProgressEventHandler_Invoke.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().ProgressEventHandler_Invoke(self.Ptr, intPtrsender,intPtrarguments)

#
#    def BeginInvoke(self ,sender:'SpireObject',arguments:'ProgressEventArgs',callback:'AsyncCallback',object:'SpireObject')->'IAsyncResult':
#        """
#
#        """
#        intPtrsender:c_void_p = sender.Ptr
#        intPtrarguments:c_void_p = arguments.Ptr
#        intPtrcallback:c_void_p = callback.Ptr
#        intPtrobject:c_void_p = object.Ptr
#
#        GetDllLibPdf().ProgressEventHandler_BeginInvoke.argtypes=[c_void_p ,c_void_p,c_void_p,c_void_p,c_void_p]
#        GetDllLibPdf().ProgressEventHandler_BeginInvoke.restype=c_void_p
#        intPtr = GetDllLibPdf().ProgressEventHandler_BeginInvoke(self.Ptr, intPtrsender,intPtrarguments,intPtrcallback,intPtrobject)
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
#        GetDllLibPdf().ProgressEventHandler_EndInvoke.argtypes=[c_void_p ,c_void_p]
#        GetDllLibPdf().ProgressEventHandler_EndInvoke(self.Ptr, intPtrresult)


