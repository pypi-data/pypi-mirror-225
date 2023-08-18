from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class GraphicsGenerateHandler (SpireObject) :
    """
    <summary>
        The handler which generate graphics.
    </summary>
    <param name="graphics">
            The graphics context.
            The visible region is (0,0,signature bounds width,signature bounds height).
    </param>
    """

    def Invoke(self ,g:'PdfCanvas'):
        """

        """
        intPtrg:c_void_p = g.Ptr

        GetDllLibPdf().GraphicsGenerateHandler_Invoke.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().GraphicsGenerateHandler_Invoke(self.Ptr, intPtrg)

#
#    def BeginInvoke(self ,g:'PdfCanvas',callback:'AsyncCallback',object:'SpireObject')->'IAsyncResult':
#        """
#
#        """
#        intPtrg:c_void_p = g.Ptr
#        intPtrcallback:c_void_p = callback.Ptr
#        intPtrobject:c_void_p = object.Ptr
#
#        GetDllLibPdf().GraphicsGenerateHandler_BeginInvoke.argtypes=[c_void_p ,c_void_p,c_void_p,c_void_p]
#        GetDllLibPdf().GraphicsGenerateHandler_BeginInvoke.restype=c_void_p
#        intPtr = GetDllLibPdf().GraphicsGenerateHandler_BeginInvoke(self.Ptr, intPtrg,intPtrcallback,intPtrobject)
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
#        GetDllLibPdf().GraphicsGenerateHandler_EndInvoke.argtypes=[c_void_p ,c_void_p]
#        GetDllLibPdf().GraphicsGenerateHandler_EndInvoke(self.Ptr, intPtrresult)


