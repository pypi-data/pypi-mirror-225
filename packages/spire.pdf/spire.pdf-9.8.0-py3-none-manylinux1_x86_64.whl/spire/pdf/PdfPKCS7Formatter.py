from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfPKCS7Formatter (  IPdfSignatureFormatter, Security_IPdfSignatureFormatter) :
    """
    <summary>
        Pdf pkcs7 signature implementation.
    </summary>
    """
    @property

    def Properties(self)->'PdfSignatureProperties':
        """
    <summary>
        The signature properties.
    </summary>
        """
        GetDllLibPdf().PdfPKCS7Formatter_get_Properties.argtypes=[c_void_p]
        GetDllLibPdf().PdfPKCS7Formatter_get_Properties.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPKCS7Formatter_get_Properties(self.Ptr)
        ret = None if intPtr==None else PdfSignatureProperties(intPtr)
        return ret


#    @property
#
#    def Parameters(self)->'Dictionary2':
#        """
#    <summary>
#        Parameters for the encoding of the signature.
#    </summary>
#        """
#        GetDllLibPdf().PdfPKCS7Formatter_get_Parameters.argtypes=[c_void_p]
#        GetDllLibPdf().PdfPKCS7Formatter_get_Parameters.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPKCS7Formatter_get_Parameters(self.Ptr)
#        ret = None if intPtr==None else Dictionary2(intPtr)
#        return ret
#


    @property

    def OCSPService(self)->'IOCSPService':
        """
    <summary>
        The service which generate OCSP response.
    </summary>
        """
        GetDllLibPdf().PdfPKCS7Formatter_get_OCSPService.argtypes=[c_void_p]
        GetDllLibPdf().PdfPKCS7Formatter_get_OCSPService.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPKCS7Formatter_get_OCSPService(self.Ptr)
        ret = None if intPtr==None else IOCSPService(intPtr)
        return ret


    @OCSPService.setter
    def OCSPService(self, value:'IOCSPService'):
        GetDllLibPdf().PdfPKCS7Formatter_set_OCSPService.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfPKCS7Formatter_set_OCSPService(self.Ptr, value.Ptr)

    @property

    def TimestampService(self)->'ITSAService':
        """
    <summary>
        The provider which generate timestamp token.
    </summary>
        """
        GetDllLibPdf().PdfPKCS7Formatter_get_TimestampService.argtypes=[c_void_p]
        GetDllLibPdf().PdfPKCS7Formatter_get_TimestampService.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPKCS7Formatter_get_TimestampService(self.Ptr)
        ret = None if intPtr==None else ITSAService(intPtr)
        return ret


    @TimestampService.setter
    def TimestampService(self, value:'ITSAService'):
        GetDllLibPdf().PdfPKCS7Formatter_set_TimestampService.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfPKCS7Formatter_set_TimestampService(self.Ptr, value.Ptr)

#    @property
#
#    def ExtraCertificateStore(self)->'X509Certificate2Collection':
#        """
#    <summary>
#        Represents an additional collection of certificates that can be searched
#            by the chaining engine when validating a certificate chain.
#    </summary>
#        """
#        GetDllLibPdf().PdfPKCS7Formatter_get_ExtraCertificateStore.argtypes=[c_void_p]
#        GetDllLibPdf().PdfPKCS7Formatter_get_ExtraCertificateStore.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPKCS7Formatter_get_ExtraCertificateStore(self.Ptr)
#        ret = None if intPtr==None else X509Certificate2Collection(intPtr)
#        return ret
#


#    @ExtraCertificateStore.setter
#    def ExtraCertificateStore(self, value:'X509Certificate2Collection'):
#        GetDllLibPdf().PdfPKCS7Formatter_set_ExtraCertificateStore.argtypes=[c_void_p, c_void_p]
#        GetDllLibPdf().PdfPKCS7Formatter_set_ExtraCertificateStore(self.Ptr, value.Ptr)


#
#    def Sign(self ,content:'Byte[]')->List['Byte']:
#        """
#    <summary>
#        Sign.
#    </summary>
#    <param name="content">The data to be signed.</param>
#    <returns>The signature.</returns>
#        """
#        #arraycontent:ArrayTypecontent = ""
#        countcontent = len(content)
#        ArrayTypecontent = c_void_p * countcontent
#        arraycontent = ArrayTypecontent()
#        for i in range(0, countcontent):
#            arraycontent[i] = content[i].Ptr
#
#
#        GetDllLibPdf().PdfPKCS7Formatter_Sign.argtypes=[c_void_p ,ArrayTypecontent]
#        GetDllLibPdf().PdfPKCS7Formatter_Sign.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().PdfPKCS7Formatter_Sign(self.Ptr, arraycontent)
#        ret = GetObjVectorFromArray(intPtrArray, Byte)
#        return ret


