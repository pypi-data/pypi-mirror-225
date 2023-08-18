from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class EndPageLayoutEventHandler (SpireObject) :
    """
    <summary>
        Delegate. Defines a type of the event after lay outing on the page.
    </summary>
    """

    def Invoke(self ,sender:'SpireObject',e:'EndPageLayoutEventArgs'):
        """

        """
        intPtrsender:c_void_p = sender.Ptr
        intPtre:c_void_p = e.Ptr

        GetDllLibPdf().EndPageLayoutEventHandler_Invoke.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().EndPageLayoutEventHandler_Invoke(self.Ptr, intPtrsender,intPtre)

#
#    def BeginInvoke(self ,sender:'SpireObject',e:'EndPageLayoutEventArgs',callback:'AsyncCallback',object:'SpireObject')->'IAsyncResult':
#        """
#
#        """
#        intPtrsender:c_void_p = sender.Ptr
#        intPtre:c_void_p = e.Ptr
#        intPtrcallback:c_void_p = callback.Ptr
#        intPtrobject:c_void_p = object.Ptr
#
#        GetDllLibPdf().EndPageLayoutEventHandler_BeginInvoke.argtypes=[c_void_p ,c_void_p,c_void_p,c_void_p,c_void_p]
#        GetDllLibPdf().EndPageLayoutEventHandler_BeginInvoke.restype=c_void_p
#        intPtr = GetDllLibPdf().EndPageLayoutEventHandler_BeginInvoke(self.Ptr, intPtrsender,intPtre,intPtrcallback,intPtrobject)
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
#        GetDllLibPdf().EndPageLayoutEventHandler_EndInvoke.argtypes=[c_void_p ,c_void_p]
#        GetDllLibPdf().EndPageLayoutEventHandler_EndInvoke(self.Ptr, intPtrresult)


