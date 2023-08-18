from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class TSAHttpService (  ITSAService) :
    """
    <summary>
        Time Stamp service implementation which must conform to RFC 3161.
    </summary>
    """
#
#    def Generate(self ,signature:'Byte[]')->List['Byte']:
#        """
#    <summary>
#        Generate timestamp token.
#    </summary>
#    <param name="signature">
#            The value of signature field within SignerInfo.
#            The value of messageImprint field within TimeStampToken shall be the hash of signature.
#            Refrence RFC 3161 APPENDIX A.
#    </param>
#    <returns>timestamp which must conform to RFC 3161</returns>
#        """
#        #arraysignature:ArrayTypesignature = ""
#        countsignature = len(signature)
#        ArrayTypesignature = c_void_p * countsignature
#        arraysignature = ArrayTypesignature()
#        for i in range(0, countsignature):
#            arraysignature[i] = signature[i].Ptr
#
#
#        GetDllLibPdf().TSAHttpService_Generate.argtypes=[c_void_p ,ArrayTypesignature]
#        GetDllLibPdf().TSAHttpService_Generate.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().TSAHttpService_Generate(self.Ptr, arraysignature)
#        ret = GetObjVectorFromArray(intPtrArray, Byte)
#        return ret


