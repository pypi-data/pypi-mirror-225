from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class TimestampGenerateHandler (SpireObject) :
    """
    <summary>
        The handler which generate timestamp token.
    </summary>
    <param name="signature">
            The value of signature field within SignerInfo.
            The value of messageImprint field within TimeStampToken shall be the hash of signature.
            Refrence RFC 3161 APPENDIX A.
    </param>
    <returns>timestamp which must conform to RFC 3161</returns>
    """
#
#    def Invoke(self ,signature:'Byte[]')->List['Byte']:
#        """
#
#        """
#        #arraysignature:ArrayTypesignature = ""
#        countsignature = len(signature)
#        ArrayTypesignature = c_void_p * countsignature
#        arraysignature = ArrayTypesignature()
#        for i in range(0, countsignature):
#            arraysignature[i] = signature[i].Ptr
#
#
#        GetDllLibPdf().TimestampGenerateHandler_Invoke.argtypes=[c_void_p ,ArrayTypesignature]
#        GetDllLibPdf().TimestampGenerateHandler_Invoke.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().TimestampGenerateHandler_Invoke(self.Ptr, arraysignature)
#        ret = GetObjVectorFromArray(intPtrArray, Byte)
#        return ret


#
#    def BeginInvoke(self ,signature:'Byte[]',callback:'AsyncCallback',object:'SpireObject')->'IAsyncResult':
#        """
#
#        """
#        #arraysignature:ArrayTypesignature = ""
#        countsignature = len(signature)
#        ArrayTypesignature = c_void_p * countsignature
#        arraysignature = ArrayTypesignature()
#        for i in range(0, countsignature):
#            arraysignature[i] = signature[i].Ptr
#
#        intPtrcallback:c_void_p = callback.Ptr
#        intPtrobject:c_void_p = object.Ptr
#
#        GetDllLibPdf().TimestampGenerateHandler_BeginInvoke.argtypes=[c_void_p ,ArrayTypesignature,c_void_p,c_void_p]
#        GetDllLibPdf().TimestampGenerateHandler_BeginInvoke.restype=c_void_p
#        intPtr = GetDllLibPdf().TimestampGenerateHandler_BeginInvoke(self.Ptr, arraysignature,intPtrcallback,intPtrobject)
#        ret = None if intPtr==None else IAsyncResult(intPtr)
#        return ret
#


#
#    def EndInvoke(self ,result:'IAsyncResult')->List['Byte']:
#        """
#
#        """
#        intPtrresult:c_void_p = result.Ptr
#
#        GetDllLibPdf().TimestampGenerateHandler_EndInvoke.argtypes=[c_void_p ,c_void_p]
#        GetDllLibPdf().TimestampGenerateHandler_EndInvoke.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().TimestampGenerateHandler_EndInvoke(self.Ptr, intPtrresult)
#        ret = GetObjVectorFromArray(intPtrArray, Byte)
#        return ret


