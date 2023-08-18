from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PageAddedEventHandler (SpireObject) :
    """
    <summary>
        Represents the  method that executes on a PdfNewDocument when a new page is created.
    </summary>
    <param name="sender">The source of the event.</param>
    <param name="args">A  that contains the event data.</param>
    """

    def Invoke(self ,sender:'SpireObject',args:'PageAddedEventArgs'):
        """

        """
        intPtrsender:c_void_p = sender.Ptr
        intPtrargs:c_void_p = args.Ptr

        GetDllLibPdf().PageAddedEventHandler_Invoke.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().PageAddedEventHandler_Invoke(self.Ptr, intPtrsender,intPtrargs)

#
#    def BeginInvoke(self ,sender:'SpireObject',args:'PageAddedEventArgs',callback:'AsyncCallback',object:'SpireObject')->'IAsyncResult':
#        """
#
#        """
#        intPtrsender:c_void_p = sender.Ptr
#        intPtrargs:c_void_p = args.Ptr
#        intPtrcallback:c_void_p = callback.Ptr
#        intPtrobject:c_void_p = object.Ptr
#
#        GetDllLibPdf().PageAddedEventHandler_BeginInvoke.argtypes=[c_void_p ,c_void_p,c_void_p,c_void_p,c_void_p]
#        GetDllLibPdf().PageAddedEventHandler_BeginInvoke.restype=c_void_p
#        intPtr = GetDllLibPdf().PageAddedEventHandler_BeginInvoke(self.Ptr, intPtrsender,intPtrargs,intPtrcallback,intPtrobject)
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
#        GetDllLibPdf().PageAddedEventHandler_EndInvoke.argtypes=[c_void_p ,c_void_p]
#        GetDllLibPdf().PageAddedEventHandler_EndInvoke(self.Ptr, intPtrresult)


