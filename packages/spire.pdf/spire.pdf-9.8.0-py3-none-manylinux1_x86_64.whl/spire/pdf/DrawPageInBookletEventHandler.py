from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class DrawPageInBookletEventHandler (SpireObject) :
    """
    <summary>
        Delegate for handling event when drawing page in a booklet.
    </summary>
    <param name="sender">The sender of the event.</param>
    <param name="args">The arguments of the event.</param>
<remarks>This event is raised when starting/finished drawing a page of the source file in a booklet.</remarks>
    """

    def Invoke(self ,sender:'SpireObject',args:'DrawPageInBookletEventArgs'):
        """

        """
        intPtrsender:c_void_p = sender.Ptr
        intPtrargs:c_void_p = args.Ptr

        GetDllLibPdf().DrawPageInBookletEventHandler_Invoke.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().DrawPageInBookletEventHandler_Invoke(self.Ptr, intPtrsender,intPtrargs)

#
#    def BeginInvoke(self ,sender:'SpireObject',args:'DrawPageInBookletEventArgs',callback:'AsyncCallback',object:'SpireObject')->'IAsyncResult':
#        """
#
#        """
#        intPtrsender:c_void_p = sender.Ptr
#        intPtrargs:c_void_p = args.Ptr
#        intPtrcallback:c_void_p = callback.Ptr
#        intPtrobject:c_void_p = object.Ptr
#
#        GetDllLibPdf().DrawPageInBookletEventHandler_BeginInvoke.argtypes=[c_void_p ,c_void_p,c_void_p,c_void_p,c_void_p]
#        GetDllLibPdf().DrawPageInBookletEventHandler_BeginInvoke.restype=c_void_p
#        intPtr = GetDllLibPdf().DrawPageInBookletEventHandler_BeginInvoke(self.Ptr, intPtrsender,intPtrargs,intPtrcallback,intPtrobject)
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
#        GetDllLibPdf().DrawPageInBookletEventHandler_EndInvoke.argtypes=[c_void_p ,c_void_p]
#        GetDllLibPdf().DrawPageInBookletEventHandler_EndInvoke(self.Ptr, intPtrresult)


