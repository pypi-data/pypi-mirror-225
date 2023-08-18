from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfSignatureMaker (SpireObject) :
    """
    <summary>
        Pdf signatue maker.
    </summary>
    """
    @property

    def Signature(self)->'PdfSignature':
        """
    <summary>
        The signature.
    </summary>
        """
        GetDllLibPdf().PdfSignatureMaker_get_Signature.argtypes=[c_void_p]
        GetDllLibPdf().PdfSignatureMaker_get_Signature.restype=c_void_p
        intPtr = GetDllLibPdf().PdfSignatureMaker_get_Signature(self.Ptr)
        ret = None if intPtr==None else PdfSignature(intPtr)
        return ret



    def SetName(self ,name:str):
        """
    <summary>
        The name of the person or anthority signing the document
            this value should be used only when it is not possible to extract the name from the signature
            for example, from the certificat of the signer
    </summary>
    <param name="name"></param>
        """
        
        GetDllLibPdf().PdfSignatureMaker_SetName.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfSignatureMaker_SetName(self.Ptr, name)


    def SetDistinguishedName(self ,distinguishedName:str):
        """

            Digital Signature Distinguished name.
            Notes: Assigning a stirng value to it directly is not recommended unless you know what is the Distinguish Name exactly.
            One way suggested of value Assignment is using pdfSignature.Certificate.IssuerName.Name,in which, pdfSignature is an instance of PDFSignature class.
                <param name="distinguishedName"></param>
        """
        
        GetDllLibPdf().PdfSignatureMaker_SetDistinguishedName.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfSignatureMaker_SetDistinguishedName(self.Ptr, distinguishedName)


    def SetDate(self ,date:str):
        """
    <summary>
        It is recommended to use "D:{0:yyyyMMddHHmmss}" to format the datetime,for example:String.Format("D:{0:yyyyMMddHHmmss}",DateTime.Now)
            The time of signing. Depending on the signature handler
            this may be a normal unverified computer time or a time generated in a verifiable way from a secure time server
    </summary>
    <param name="date"></param>
        """
        
        GetDllLibPdf().PdfSignatureMaker_SetDate.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfSignatureMaker_SetDate(self.Ptr, date)


    def SetLocation(self ,location:str):
        """
    <summary>
        The CPU host name or physical location of the signing.
    </summary>
    <param name="location"></param>
        """
        
        GetDllLibPdf().PdfSignatureMaker_SetLocation.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfSignatureMaker_SetLocation(self.Ptr, location)


    def SetReason(self ,reason:str):
        """
    <summary>
        The reason for the signing, such as ( I agree … ).
    </summary>
    <param name="reason"></param>
        """
        
        GetDllLibPdf().PdfSignatureMaker_SetReason.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfSignatureMaker_SetReason(self.Ptr, reason)


    def SetContactInfo(self ,contactInfo:str):
        """
    <summary>
        Information provided by the signer to enable a recipient to contact the signer to verify the signature
            for example, a phone number.
    </summary>
    <param name="contactInfo"></param>
        """
        
        GetDllLibPdf().PdfSignatureMaker_SetContactInfo.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfSignatureMaker_SetContactInfo(self.Ptr, contactInfo)


    def SetNameLabel(self ,nameLabel:str):
        """
    <summary>
        The content to the left of property name
    </summary>
    <param name="nameLabel"></param>
        """
        
        GetDllLibPdf().PdfSignatureMaker_SetNameLabel.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfSignatureMaker_SetNameLabel(self.Ptr, nameLabel)


    def SetDistinguishedNameLabel(self ,distinguishedNameLabel:str):
        """
    <summary>
        The content to the left of property distinguishedName
    </summary>
    <param name="distinguishedNameLabel"></param>
        """
        
        GetDllLibPdf().PdfSignatureMaker_SetDistinguishedNameLabel.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfSignatureMaker_SetDistinguishedNameLabel(self.Ptr, distinguishedNameLabel)


    def SetReasonLabel(self ,reasonLabel:str):
        """
    <summary>
        The content to the left of property reason
    </summary>
    <param name="reasonLabel"></param>
        """
        
        GetDllLibPdf().PdfSignatureMaker_SetReasonLabel.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfSignatureMaker_SetReasonLabel(self.Ptr, reasonLabel)


    def SetLocationLabel(self ,locationLabel:str):
        """
    <summary>
        The content to the left of property location
    </summary>
    <param name="locationLabel"></param>
        """
        
        GetDllLibPdf().PdfSignatureMaker_SetLocationLabel.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfSignatureMaker_SetLocationLabel(self.Ptr, locationLabel)


    def SetContactInfoLabel(self ,contactInfoLabel:str):
        """
    <summary>
        The content to the left of property contactInfo
    </summary>
    <param name="contactInfoLabel"></param>
        """
        
        GetDllLibPdf().PdfSignatureMaker_SetContactInfoLabel.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfSignatureMaker_SetContactInfoLabel(self.Ptr, contactInfoLabel)


    def SetDateLabel(self ,dateLabel:str):
        """
    <summary>
        The content to the left of property date
    </summary>
    <param name="dateLabel"></param>
        """
        
        GetDllLibPdf().PdfSignatureMaker_SetDateLabel.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfSignatureMaker_SetDateLabel(self.Ptr, dateLabel)


    def SetAcro6Layers(self ,acro6Layers:bool):
        """
    <summary>
        Only for compatibility old version.
            Whether move away signature validity visualizations in document.
            Default true.
    </summary>
    <param name="acro6Layers">
            false, display signature validity visualizations in document.
            true, move away signature validity visualizations in document. 
    </param>
        """
        
        GetDllLibPdf().PdfSignatureMaker_SetAcro6Layers.argtypes=[c_void_p ,c_bool]
        GetDllLibPdf().PdfSignatureMaker_SetAcro6Layers(self.Ptr, acro6Layers)

    @dispatch

    def MakeSignature(self ,sigFieldName:str):
        """
    <summary>
        Make signature.
    </summary>
    <param name="sigFieldName">The signature filed name.</param>
        """
        
        GetDllLibPdf().PdfSignatureMaker_MakeSignature.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfSignatureMaker_MakeSignature(self.Ptr, sigFieldName)

    @dispatch

    def MakeSignature(self ,sigFieldName:str,signatureAppearance:IPdfSignatureAppearance):
        """
    <summary>
        Make signature.
    </summary>
    <param name="sigFieldName">The signature filed name.</param>
    <param name="signatureAppearance">Implement a custom signature appearance.</param>
        """
        intPtrsignatureAppearance:c_void_p = signatureAppearance.Ptr

        GetDllLibPdf().PdfSignatureMaker_MakeSignatureSS.argtypes=[c_void_p ,c_wchar_p,c_void_p]
        GetDllLibPdf().PdfSignatureMaker_MakeSignatureSS(self.Ptr, sigFieldName,intPtrsignatureAppearance)

    @dispatch

    def MakeSignature(self ,sigFieldName:str,page:PdfPageBase,x:float,y:float,width:float,height:float):
        """
    <summary>
        Make signature.
    </summary>
    <param name="sigFieldName">The signature filed name.</param>
    <param name="page">The page index.</param>
    <param name="x">The x position of the annotation on the page.</param>
    <param name="y">The y position of the annotation on the page.</param>
    <param name="width">The width of the annotation on the page.</param>
    <param name="height">The height of the annotation on the page.</param>
    <param name="rect">The location of the annotation on the page.</param>
        """
        intPtrpage:c_void_p = page.Ptr

        GetDllLibPdf().PdfSignatureMaker_MakeSignatureSPXYWH.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_float,c_float,c_float,c_float]
        GetDllLibPdf().PdfSignatureMaker_MakeSignatureSPXYWH(self.Ptr, sigFieldName,intPtrpage,x,y,width,height)

    @dispatch

    def MakeSignature(self ,sigFieldName:str,page:PdfPageBase,x:float,y:float,width:float,height:float,signatureAppearance:IPdfSignatureAppearance):
        """
    <summary>
        Make signature.
    </summary>
    <param name="sigFieldName">The signature filed name.</param>
    <param name="page">The page index.</param>
    <param name="x">The x position of the annotation on the page.</param>
    <param name="y">The y position of the annotation on the page.</param>
    <param name="width">The width of the annotation on the page.</param>
    <param name="height">The height of the annotation on the page.</param>
    <param name="signatureAppearance">Implement a custom signature appearance.</param>
        """
        intPtrpage:c_void_p = page.Ptr
        intPtrsignatureAppearance:c_void_p = signatureAppearance.Ptr

        GetDllLibPdf().PdfSignatureMaker_MakeSignatureSPXYWHS.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_float,c_float,c_float,c_float,c_void_p]
        GetDllLibPdf().PdfSignatureMaker_MakeSignatureSPXYWHS(self.Ptr, sigFieldName,intPtrpage,x,y,width,height,intPtrsignatureAppearance)

