from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfSignatureProperties (SpireObject) :
    """
    <summary>
        Signature properties.
    </summary>
    """

    def SetFilter(self ,filter:str):
        """
    <summary>
        Set the name of the preferred signature handler to use when validating this signature.
            (Required)
    </summary>
    <param name="filter">the name of the preferred signature handler.</param>
        """
        
        GetDllLibPdf().PdfSignatureProperties_SetFilter.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfSignatureProperties_SetFilter(self.Ptr, filter)


    def SetSubFilter(self ,subFilter:str):
        """
    <summary>
        Set a name that describes the encoding of the signature value.
            (Required)
    </summary>
    <param name="subFilter">a name that describes the encoding of the signature value.</param>
        """
        
        GetDllLibPdf().PdfSignatureProperties_SetSubFilter.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfSignatureProperties_SetSubFilter(self.Ptr, subFilter)

#    @dispatch
#
#    def SetCert(self ,cert:'X509Certificate2'):
#        """
#    <summary>
#        Set the X.509 certificate used when signing and verifying signatures that use public-key cryptography.
#            (Required when SubFilter is adbe.x509.rsa_sha1)
#    </summary>
#    <param name="cert">the X.509 certificate.</param>
#        """
#        intPtrcert:c_void_p = cert.Ptr
#
#        GetDllLibPdf().PdfSignatureProperties_SetCert.argtypes=[c_void_p ,c_void_p]
#        GetDllLibPdf().PdfSignatureProperties_SetCert(self.Ptr, intPtrcert)


#    @dispatch
#
#    def SetCert(self ,certs:'IList1'):
#        """
#    <summary>
#        Set the X.509 certificate chain used when signing and verifying signatures that use public-key cryptography.
#            (Required when SubFilter is adbe.x509.rsa_sha1)
#    </summary>
#    <param name="certs">the X.509 certificate chain.</param>
#        """
#        intPtrcerts:c_void_p = certs.Ptr
#
#        GetDllLibPdf().PdfSignatureProperties_SetCertC.argtypes=[c_void_p ,c_void_p]
#        GetDllLibPdf().PdfSignatureProperties_SetCertC(self.Ptr, intPtrcerts)



    def SetSignatureLength(self ,signatureLength:'UInt32'):
        """
    <summary>
        Set signature length.
            (Option)
            Default, signature need to call twice "Sign" method, one is to calculate signature length.
            If the signature length is known, avoid to calculate signature length by "Sign" method.
            The signature length.
    </summary>
    <param name="signatureLength">the signature length.</param>
        """
        intPtrsignatureLength:c_void_p = signatureLength.Ptr

        GetDllLibPdf().PdfSignatureProperties_SetSignatureLength.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfSignatureProperties_SetSignatureLength(self.Ptr, intPtrsignatureLength)


    def SetSoftwareModuleName(self ,softwareModuleName:str):
        """
    <summary>
        Set the name of the software module used to create the signature.
            (Option)
    </summary>
    <param name="softwareModuleName">the name of the software module.</param>
        """
        
        GetDllLibPdf().PdfSignatureProperties_SetSoftwareModuleName.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfSignatureProperties_SetSoftwareModuleName(self.Ptr, softwareModuleName)

