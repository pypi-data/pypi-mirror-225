from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class OCSPHttpService (  IOCSPService) :
    """
    <summary>
        Ocsp http service implementation.
     </summary>
    """
#
#    def Generate(self ,checkedCertificate:'X509Certificate2',issuerCertificate:'X509Certificate2')->List['Byte']:
#        """
#    <summary>
#        Generate OCSP response.
#    </summary>
#    <param name="checkedCertificate">certificate to checked</param>
#    <param name="issuerCertificate">certificate of the issuer</param>
#    <returns>OCSP response which must conform to RFC 2560</returns>
#        """
#        intPtrcheckedCertificate:c_void_p = checkedCertificate.Ptr
#        intPtrissuerCertificate:c_void_p = issuerCertificate.Ptr
#
#        GetDllLibPdf().OCSPHttpService_Generate.argtypes=[c_void_p ,c_void_p,c_void_p]
#        GetDllLibPdf().OCSPHttpService_Generate.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().OCSPHttpService_Generate(self.Ptr, intPtrcheckedCertificate,intPtrissuerCertificate)
#        ret = GetObjVectorFromArray(intPtrArray, Byte)
#        return ret


