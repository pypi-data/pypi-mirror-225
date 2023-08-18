from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class BeginPageLayoutEventHandler (SpireObject) :
    """
    <summary>
        Delegate. Defines a type of the event before lay outing on the page.
    </summary>
    """

    def Invoke(self ,sender:'SpireObject',e:'BeginPageLayoutEventArgs'):
        """

        """
        intPtrsender:c_void_p = sender.Ptr
        intPtre:c_void_p = e.Ptr

        GetDllLibPdf().BeginPageLayoutEventHandler_Invoke.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().BeginPageLayoutEventHandler_Invoke(self.Ptr, intPtrsender,intPtre)

#
#    def BeginInvoke(self ,sender:'SpireObject',e:'BeginPageLayoutEventArgs',callback:'AsyncCallback',object:'SpireObject')->'IAsyncResult':
#        """
#
#        """
#        intPtrsender:c_void_p = sender.Ptr
#        intPtre:c_void_p = e.Ptr
#        intPtrcallback:c_void_p = callback.Ptr
#        intPtrobject:c_void_p = object.Ptr
#
#        GetDllLibPdf().BeginPageLayoutEventHandler_BeginInvoke.argtypes=[c_void_p ,c_void_p,c_void_p,c_void_p,c_void_p]
#        GetDllLibPdf().BeginPageLayoutEventHandler_BeginInvoke.restype=c_void_p
#        intPtr = GetDllLibPdf().BeginPageLayoutEventHandler_BeginInvoke(self.Ptr, intPtrsender,intPtre,intPtrcallback,intPtrobject)
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
#        GetDllLibPdf().BeginPageLayoutEventHandler_EndInvoke.argtypes=[c_void_p ,c_void_p]
#        GetDllLibPdf().BeginPageLayoutEventHandler_EndInvoke(self.Ptr, intPtrresult)


