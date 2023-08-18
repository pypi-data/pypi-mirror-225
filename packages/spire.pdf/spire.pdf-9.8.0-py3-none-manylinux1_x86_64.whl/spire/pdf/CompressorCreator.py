from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class CompressorCreator (SpireObject) :
    """

    """

    def Invoke(self ,outputStream:'Stream')->'Stream':
        """

        """
        intPtroutputStream:c_void_p = outputStream.Ptr

        GetDllLibPdf().CompressorCreator_Invoke.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().CompressorCreator_Invoke.restype=c_void_p
        intPtr = GetDllLibPdf().CompressorCreator_Invoke(self.Ptr, intPtroutputStream)
        ret = None if intPtr==None else Stream(intPtr)
        return ret


#
#    def BeginInvoke(self ,outputStream:'Stream',callback:'AsyncCallback',object:'SpireObject')->'IAsyncResult':
#        """
#
#        """
#        intPtroutputStream:c_void_p = outputStream.Ptr
#        intPtrcallback:c_void_p = callback.Ptr
#        intPtrobject:c_void_p = object.Ptr
#
#        GetDllLibPdf().CompressorCreator_BeginInvoke.argtypes=[c_void_p ,c_void_p,c_void_p,c_void_p]
#        GetDllLibPdf().CompressorCreator_BeginInvoke.restype=c_void_p
#        intPtr = GetDllLibPdf().CompressorCreator_BeginInvoke(self.Ptr, intPtroutputStream,intPtrcallback,intPtrobject)
#        ret = None if intPtr==None else IAsyncResult(intPtr)
#        return ret
#


#
#    def EndInvoke(self ,result:'IAsyncResult')->'Stream':
#        """
#
#        """
#        intPtrresult:c_void_p = result.Ptr
#
#        GetDllLibPdf().CompressorCreator_EndInvoke.argtypes=[c_void_p ,c_void_p]
#        GetDllLibPdf().CompressorCreator_EndInvoke.restype=c_void_p
#        intPtr = GetDllLibPdf().CompressorCreator_EndInvoke(self.Ptr, intPtrresult)
#        ret = None if intPtr==None else Stream(intPtr)
#        return ret
#


