from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfCertificate (SpireObject) :
    """
    <summary>
        Represents the Certificate object.
    </summary>
    """
#    @staticmethod
#
#    def GetCertificates()->List['PdfCertificate']:
#        """
#    <summary>
#        Gets the certificates in all storages.
#    </summary>
#    <returns>
#            PdfCertificate array.
#            </returns>
#        """
#        #GetDllLibPdf().PdfCertificate_GetCertificates.argtypes=[]
#        GetDllLibPdf().PdfCertificate_GetCertificates.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().PdfCertificate_GetCertificates()
#        ret = GetVectorFromArray(intPtrArray, PdfCertificate)
#        return ret


    @staticmethod

    def FindBySubject(storeName:'StoreType',subject:str)->'PdfCertificate':
        """
    <summary>
        Finds the certificate by subject.
    </summary>
    <param name="storeName">The store name.</param>
    <param name="subject">The certificate subject.</param>
    <returns>The certificate.</returns>
        """
        enumstoreName:c_int = storeName.value

        GetDllLibPdf().PdfCertificate_FindBySubject.argtypes=[ c_int,c_wchar_p]
        GetDllLibPdf().PdfCertificate_FindBySubject.restype=c_void_p
        intPtr = GetDllLibPdf().PdfCertificate_FindBySubject( enumstoreName,subject)
        ret = None if intPtr==None else PdfCertificate(intPtr)
        return ret


    @staticmethod

    def FindByIssuer(storeName:'StoreType',issuer:str)->'PdfCertificate':
        """
    <summary>
        Finds the certificate by issuer.
    </summary>
    <param name="storeName">The store name.</param>
    <param name="issuer">The certificate issuer.</param>
    <returns>The certificate.</returns>
        """
        enumstoreName:c_int = storeName.value

        GetDllLibPdf().PdfCertificate_FindByIssuer.argtypes=[ c_int,c_wchar_p]
        GetDllLibPdf().PdfCertificate_FindByIssuer.restype=c_void_p
        intPtr = GetDllLibPdf().PdfCertificate_FindByIssuer( enumstoreName,issuer)
        ret = None if intPtr==None else PdfCertificate(intPtr)
        return ret


#    @staticmethod
#
#    def FindBySerialId(storeName:'StoreType',certId:'Byte[]')->'PdfCertificate':
#        """
#    <summary>
#        Finds the certificate by serial number.
#    </summary>
#    <param name="type">The certification system store type.</param>
#    <param name="certId">The certificate id.</param>
#    <returns></returns>
#        """
#        enumstoreName:c_int = storeName.value
#        #arraycertId:ArrayTypecertId = ""
#        countcertId = len(certId)
#        ArrayTypecertId = c_void_p * countcertId
#        arraycertId = ArrayTypecertId()
#        for i in range(0, countcertId):
#            arraycertId[i] = certId[i].Ptr
#
#
#        GetDllLibPdf().PdfCertificate_FindBySerialId.argtypes=[ c_int,ArrayTypecertId]
#        GetDllLibPdf().PdfCertificate_FindBySerialId.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfCertificate_FindBySerialId( enumstoreName,arraycertId)
#        ret = None if intPtr==None else PdfCertificate(intPtr)
#        return ret
#


