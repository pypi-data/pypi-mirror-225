from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class OCSPResponseGenerateHandler (SpireObject) :
    """
    <summary>
        The handler which generate OCSP response.
    </summary>
    <param name="checkedCertificate">certificate to checked</param>
    <param name="issuerCertificate">certificate of the issuer</param>
    <returns>OCSP response which must conform to RFC 2560</returns>
    """
#
#    def Invoke(self ,checkedCertificate:'X509Certificate2',issuerCertificate:'X509Certificate2')->List['Byte']:
#        """
#
#        """
#        intPtrcheckedCertificate:c_void_p = checkedCertificate.Ptr
#        intPtrissuerCertificate:c_void_p = issuerCertificate.Ptr
#
#        GetDllLibPdf().OCSPResponseGenerateHandler_Invoke.argtypes=[c_void_p ,c_void_p,c_void_p]
#        GetDllLibPdf().OCSPResponseGenerateHandler_Invoke.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().OCSPResponseGenerateHandler_Invoke(self.Ptr, intPtrcheckedCertificate,intPtrissuerCertificate)
#        ret = GetObjVectorFromArray(intPtrArray, Byte)
#        return ret


#
#    def BeginInvoke(self ,checkedCertificate:'X509Certificate2',issuerCertificate:'X509Certificate2',callback:'AsyncCallback',object:'SpireObject')->'IAsyncResult':
#        """
#
#        """
#        intPtrcheckedCertificate:c_void_p = checkedCertificate.Ptr
#        intPtrissuerCertificate:c_void_p = issuerCertificate.Ptr
#        intPtrcallback:c_void_p = callback.Ptr
#        intPtrobject:c_void_p = object.Ptr
#
#        GetDllLibPdf().OCSPResponseGenerateHandler_BeginInvoke.argtypes=[c_void_p ,c_void_p,c_void_p,c_void_p,c_void_p]
#        GetDllLibPdf().OCSPResponseGenerateHandler_BeginInvoke.restype=c_void_p
#        intPtr = GetDllLibPdf().OCSPResponseGenerateHandler_BeginInvoke(self.Ptr, intPtrcheckedCertificate,intPtrissuerCertificate,intPtrcallback,intPtrobject)
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
#        GetDllLibPdf().OCSPResponseGenerateHandler_EndInvoke.argtypes=[c_void_p ,c_void_p]
#        GetDllLibPdf().OCSPResponseGenerateHandler_EndInvoke.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().OCSPResponseGenerateHandler_EndInvoke(self.Ptr, intPtrresult)
#        ret = GetObjVectorFromArray(intPtrArray, Byte)
#        return ret


