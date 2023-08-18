from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class BeginRowLayoutEventHandler (SpireObject) :
    """
    <summary>
        Delegate for handling StartRowLayoutEvent.
    </summary>
    <param name="sender">The sender of the event.</param>
    <param name="args">The arguments of the event.</param>
<remarks>This event is raised when starting a row in a layout.</remarks>
    """

    def Invoke(self ,sender:'SpireObject',args:'BeginRowLayoutEventArgs'):
        """

        """
        intPtrsender:c_void_p = sender.Ptr
        intPtrargs:c_void_p = args.Ptr

        GetDllLibPdf().BeginRowLayoutEventHandler_Invoke.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().BeginRowLayoutEventHandler_Invoke(self.Ptr, intPtrsender,intPtrargs)

#
#    def BeginInvoke(self ,sender:'SpireObject',args:'BeginRowLayoutEventArgs',callback:'AsyncCallback',object:'SpireObject')->'IAsyncResult':
#        """
#
#        """
#        intPtrsender:c_void_p = sender.Ptr
#        intPtrargs:c_void_p = args.Ptr
#        intPtrcallback:c_void_p = callback.Ptr
#        intPtrobject:c_void_p = object.Ptr
#
#        GetDllLibPdf().BeginRowLayoutEventHandler_BeginInvoke.argtypes=[c_void_p ,c_void_p,c_void_p,c_void_p,c_void_p]
#        GetDllLibPdf().BeginRowLayoutEventHandler_BeginInvoke.restype=c_void_p
#        intPtr = GetDllLibPdf().BeginRowLayoutEventHandler_BeginInvoke(self.Ptr, intPtrsender,intPtrargs,intPtrcallback,intPtrobject)
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
#        GetDllLibPdf().BeginRowLayoutEventHandler_EndInvoke.argtypes=[c_void_p ,c_void_p]
#        GetDllLibPdf().BeginRowLayoutEventHandler_EndInvoke(self.Ptr, intPtrresult)


