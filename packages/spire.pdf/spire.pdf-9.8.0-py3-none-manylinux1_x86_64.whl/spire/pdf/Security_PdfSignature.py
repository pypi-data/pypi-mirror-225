from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Security_PdfSignature (SpireObject) :
    """
    <summary>
        Represents a digital signature used for signing a PDF document.
    </summary>
    """
    def VerifySignature(self)->bool:
        """
    <summary>
        check thie validity of the signature
    </summary>
    <returns></returns>
        """
        GetDllLibPdf().Security_PdfSignature_VerifySignature.argtypes=[c_void_p]
        GetDllLibPdf().Security_PdfSignature_VerifySignature.restype=c_bool
        ret = GetDllLibPdf().Security_PdfSignature_VerifySignature(self.Ptr)
        return ret

    def VerifyDocModified(self)->bool:
        """
    <summary>
        Check if the document was altered after signed. True if modified; otherwise false.
    </summary>
    <returns></returns>
        """
        GetDllLibPdf().Security_PdfSignature_VerifyDocModified.argtypes=[c_void_p]
        GetDllLibPdf().Security_PdfSignature_VerifyDocModified.restype=c_bool
        ret = GetDllLibPdf().Security_PdfSignature_VerifyDocModified(self.Ptr)
        return ret


    def SetSignNameWidth(self ,width:float):
        """
    <summary>
        Set the Sign Name Width
    </summary>
    <returns></returns>
        """
        
        GetDllLibPdf().Security_PdfSignature_SetSignNameWidth.argtypes=[c_void_p ,c_float]
        GetDllLibPdf().Security_PdfSignature_SetSignNameWidth(self.Ptr, width)


    def ConfigureCustomGraphics(self ,handler:'GraphicsGenerateHandler'):
        """
    <summary>
        Configure custom graphics.
    </summary>
    <param name="handler">the handler which generate graphics.</param>
        """
        intPtrhandler:c_void_p = handler.Ptr

        GetDllLibPdf().Security_PdfSignature_ConfigureCustomGraphics.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().Security_PdfSignature_ConfigureCustomGraphics(self.Ptr, intPtrhandler)

    @dispatch

    def ConfigureTimestamp(self ,tsaUrl:str):
        """
    <summary>
        Configure timestamp which must conform to RFC 3161.
    </summary>
    <param name="tsaUrl">TSA url</param>
        """
        
        GetDllLibPdf().Security_PdfSignature_ConfigureTimestamp.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().Security_PdfSignature_ConfigureTimestamp(self.Ptr, tsaUrl)

    @dispatch

    def ConfigureTimestamp(self ,tsaUrl:str,user:str,password:str):
        """
    <summary>
        Configure timestamp which must conform to RFC 3161.
    </summary>
    <param name="tsaUrl">The tsa url.</param>
    <param name="user">The user(account) name.</param>
    <param name="password">The password.</param>
        """
        
        GetDllLibPdf().Security_PdfSignature_ConfigureTimestampTUP.argtypes=[c_void_p ,c_wchar_p,c_wchar_p,c_wchar_p]
        GetDllLibPdf().Security_PdfSignature_ConfigureTimestampTUP(self.Ptr, tsaUrl,user,password)

    @dispatch

    def ConfigureTimestamp(self ,handler:TimestampGenerateHandler):
        """
    <summary>
        Configure timestamp which must conform to RFC 3161.
    </summary>
    <param name="handler">the handler which generate timestamp token</param>
        """
        intPtrhandler:c_void_p = handler.Ptr

        GetDllLibPdf().Security_PdfSignature_ConfigureTimestampH.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().Security_PdfSignature_ConfigureTimestampH(self.Ptr, intPtrhandler)

#
#    def ConfigureHttpOCSP(self ,ocspUrl:str,extraCertificates:'X509Certificate2Collection'):
#        """
#    <summary>
#        Configure OCSP which must conform to RFC 2560.
#    </summary>
#    <param name="ocspUrl">
#            OCSP url. It it's null it will be taken from the checked cert.
#    </param>
#    <param name="extraCertificates">
#            Represents an additional collection of certificates that can be searched.
#            if null,only use windows cert store.
#    </param>
#        """
#        intPtrextraCertificates:c_void_p = extraCertificates.Ptr
#
#        GetDllLibPdf().Security_PdfSignature_ConfigureHttpOCSP.argtypes=[c_void_p ,c_wchar_p,c_void_p]
#        GetDllLibPdf().Security_PdfSignature_ConfigureHttpOCSP(self.Ptr, ocspUrl,intPtrextraCertificates)


#
#    def ConfigureCustomOCSP(self ,handler:'OCSPResponseGenerateHandler',extraCertificates:'X509Certificate2Collection'):
#        """
#    <summary>
#        Configure OCSP which must conform to RFC 2560.
#    </summary>
#    <param name="extraCertificates">
#            Represents an additional collection of certificates that can be searched
#            if null,only use windows cert store.
#    </param>
#    <param name="handler">the handler which generate OCSP response.</param>
#        """
#        intPtrhandler:c_void_p = handler.Ptr
#        intPtrextraCertificates:c_void_p = extraCertificates.Ptr
#
#        GetDllLibPdf().Security_PdfSignature_ConfigureCustomOCSP.argtypes=[c_void_p ,c_void_p,c_void_p]
#        GetDllLibPdf().Security_PdfSignature_ConfigureCustomOCSP(self.Ptr, intPtrhandler,intPtrextraCertificates)


#    @property
#
#    def Certificates(self)->'X509Certificate2Collection':
#        """
#    <summary>
#        Get all certificates.
#    </summary>
#        """
#        GetDllLibPdf().Security_PdfSignature_get_Certificates.argtypes=[c_void_p]
#        GetDllLibPdf().Security_PdfSignature_get_Certificates.restype=c_void_p
#        intPtr = GetDllLibPdf().Security_PdfSignature_get_Certificates(self.Ptr)
#        ret = None if intPtr==None else X509Certificate2Collection(intPtr)
#        return ret
#


    @property

    def Appearence(self)->'PdfAppearance':
        """
    <summary>
        Gets the signature Appearance.
    </summary>
<value>An object defines signature`s appearance.</value>
        """
        GetDllLibPdf().Security_PdfSignature_get_Appearence.argtypes=[c_void_p]
        GetDllLibPdf().Security_PdfSignature_get_Appearence.restype=c_void_p
        intPtr = GetDllLibPdf().Security_PdfSignature_get_Appearence(self.Ptr)
        ret = None if intPtr==None else PdfAppearance(intPtr)
        return ret


    @property

    def Location(self)->'PointF':
        """
    <summary>
        Gets or sets signature location on the page.
    </summary>
        """
        GetDllLibPdf().Security_PdfSignature_get_Location.argtypes=[c_void_p]
        GetDllLibPdf().Security_PdfSignature_get_Location.restype=c_void_p
        intPtr = GetDllLibPdf().Security_PdfSignature_get_Location(self.Ptr)
        ret = None if intPtr==None else PointF(intPtr)
        return ret


    @Location.setter
    def Location(self, value:'PointF'):
        GetDllLibPdf().Security_PdfSignature_set_Location.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().Security_PdfSignature_set_Location(self.Ptr, value.Ptr)

    @property

    def Bounds(self)->'RectangleF':
        """
    <summary>
        Gets or sets bounds of signature.
    </summary>
        """
        GetDllLibPdf().Security_PdfSignature_get_Bounds.argtypes=[c_void_p]
        GetDllLibPdf().Security_PdfSignature_get_Bounds.restype=c_void_p
        intPtr = GetDllLibPdf().Security_PdfSignature_get_Bounds(self.Ptr)
        ret = None if intPtr==None else RectangleF(intPtr)
        return ret


    @Bounds.setter
    def Bounds(self, value:'RectangleF'):
        GetDllLibPdf().Security_PdfSignature_set_Bounds.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().Security_PdfSignature_set_Bounds(self.Ptr, value.Ptr)

    @property

    def ContactInfo(self)->str:
        """
    <summary>
        Gets or sets information provided by the signer to enable a recipient to contact
            the signer to verify the signature; for example, a phone number.
    </summary>
        """
        GetDllLibPdf().Security_PdfSignature_get_ContactInfo.argtypes=[c_void_p]
        GetDllLibPdf().Security_PdfSignature_get_ContactInfo.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Security_PdfSignature_get_ContactInfo(self.Ptr))
        return ret


    @ContactInfo.setter
    def ContactInfo(self, value:str):
        GetDllLibPdf().Security_PdfSignature_set_ContactInfo.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Security_PdfSignature_set_ContactInfo(self.Ptr, value)

    @property

    def Reason(self)->str:
        """
    <summary>
        Gets or sets reason of signing.
    </summary>
        """
        GetDllLibPdf().Security_PdfSignature_get_Reason.argtypes=[c_void_p]
        GetDllLibPdf().Security_PdfSignature_get_Reason.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Security_PdfSignature_get_Reason(self.Ptr))
        return ret


    @Reason.setter
    def Reason(self, value:str):
        GetDllLibPdf().Security_PdfSignature_set_Reason.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Security_PdfSignature_set_Reason(self.Ptr, value)

    @property

    def LocationInfo(self)->str:
        """
    <summary>
        Gets or sets the physical location of the signing.
    </summary>
        """
        GetDllLibPdf().Security_PdfSignature_get_LocationInfo.argtypes=[c_void_p]
        GetDllLibPdf().Security_PdfSignature_get_LocationInfo.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Security_PdfSignature_get_LocationInfo(self.Ptr))
        return ret


    @LocationInfo.setter
    def LocationInfo(self, value:str):
        GetDllLibPdf().Security_PdfSignature_set_LocationInfo.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Security_PdfSignature_set_LocationInfo(self.Ptr, value)

    @property
    def Certificated(self)->bool:
        """
    <summary>
        Gets or sets a value indicating certificate document or not.
            NOTE: Works only with Adobe Reader 7.0.8 or higher.
    </summary>
<value>certificate document if true.</value>
        """
        GetDllLibPdf().Security_PdfSignature_get_Certificated.argtypes=[c_void_p]
        GetDllLibPdf().Security_PdfSignature_get_Certificated.restype=c_bool
        ret = GetDllLibPdf().Security_PdfSignature_get_Certificated(self.Ptr)
        return ret

    @Certificated.setter
    def Certificated(self, value:bool):
        GetDllLibPdf().Security_PdfSignature_set_Certificated.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().Security_PdfSignature_set_Certificated(self.Ptr, value)

    @property

    def DocumentPermissions(self)->'PdfCertificationFlags':
        """
    <summary>
        Gets or sets the permission for certificated document.
    </summary>
<value>The document permission.</value>
        """
        GetDllLibPdf().Security_PdfSignature_get_DocumentPermissions.argtypes=[c_void_p]
        GetDllLibPdf().Security_PdfSignature_get_DocumentPermissions.restype=c_int
        ret = GetDllLibPdf().Security_PdfSignature_get_DocumentPermissions(self.Ptr)
        objwraped = PdfCertificationFlags(ret)
        return objwraped

    @DocumentPermissions.setter
    def DocumentPermissions(self, value:'PdfCertificationFlags'):
        GetDllLibPdf().Security_PdfSignature_set_DocumentPermissions.argtypes=[c_void_p, c_int]
        GetDllLibPdf().Security_PdfSignature_set_DocumentPermissions(self.Ptr, value.value)

    @property

    def Certificate(self)->'PdfCertificate':
        """
    <summary>
        Gets signing certificate.
    </summary>
        """
        GetDllLibPdf().Security_PdfSignature_get_Certificate.argtypes=[c_void_p]
        GetDllLibPdf().Security_PdfSignature_get_Certificate.restype=c_void_p
        intPtr = GetDllLibPdf().Security_PdfSignature_get_Certificate(self.Ptr)
        ret = None if intPtr==None else PdfCertificate(intPtr)
        return ret


    @Certificate.setter
    def Certificate(self, value:'PdfCertificate'):
        GetDllLibPdf().Security_PdfSignature_set_Certificate.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().Security_PdfSignature_set_Certificate(self.Ptr, value.Ptr)

    @property

    def SignTextAlignment(self)->'SignTextAlignment':
        """
    <summary>
        Sets the alignment of signature text 
    </summary>
        """
        GetDllLibPdf().Security_PdfSignature_get_SignTextAlignment.argtypes=[c_void_p]
        GetDllLibPdf().Security_PdfSignature_get_SignTextAlignment.restype=c_int
        ret = GetDllLibPdf().Security_PdfSignature_get_SignTextAlignment(self.Ptr)
        objwraped = SignTextAlignment(ret)
        return objwraped

    @SignTextAlignment.setter
    def SignTextAlignment(self, value:'SignTextAlignment'):
        GetDllLibPdf().Security_PdfSignature_set_SignTextAlignment.argtypes=[c_void_p, c_int]
        GetDllLibPdf().Security_PdfSignature_set_SignTextAlignment(self.Ptr, value.value)

    @property
    def Visible(self)->bool:
        """
    <summary>
        Gets a value indicating whether signature visible or not.
    </summary>
<remarks>Signature can be set as invisible when its  size is set to empty.</remarks>
        """
        GetDllLibPdf().Security_PdfSignature_get_Visible.argtypes=[c_void_p]
        GetDllLibPdf().Security_PdfSignature_get_Visible.restype=c_bool
        ret = GetDllLibPdf().Security_PdfSignature_get_Visible(self.Ptr)
        return ret

    @property

    def Date(self)->'DateTime':
        """
    <summary>
        Get Signature Datetime
    </summary>
        """
        GetDllLibPdf().Security_PdfSignature_get_Date.argtypes=[c_void_p]
        GetDllLibPdf().Security_PdfSignature_get_Date.restype=c_void_p
        intPtr = GetDllLibPdf().Security_PdfSignature_get_Date(self.Ptr)
        ret = None if intPtr==None else DateTime(intPtr)
        return ret


    @Date.setter
    def Date(self, value:'DateTime'):
        GetDllLibPdf().Security_PdfSignature_set_Date.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().Security_PdfSignature_set_Date(self.Ptr, value.Ptr)

    @SignNameFont.setter
    def SignNameFont(self, value:'PdfFontBase'):
        GetDllLibPdf().Security_PdfSignature_set_SignNameFont.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().Security_PdfSignature_set_SignNameFont(self.Ptr, value.Ptr)

    @SignFontColor.setter
    def SignFontColor(self, value:'Color'):
        GetDllLibPdf().Security_PdfSignature_set_SignFontColor.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().Security_PdfSignature_set_SignFontColor(self.Ptr, value.Ptr)

    @SignDetailsFont.setter
    def SignDetailsFont(self, value:'PdfFontBase'):
        GetDllLibPdf().Security_PdfSignature_set_SignDetailsFont.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().Security_PdfSignature_set_SignDetailsFont(self.Ptr, value.Ptr)

#    @property
#
#    def SignInfoFont(self)->'Dictionary2':
#        """
#    <summary>
#        Set signature info font
#    </summary>
#        """
#        GetDllLibPdf().Security_PdfSignature_get_SignInfoFont.argtypes=[c_void_p]
#        GetDllLibPdf().Security_PdfSignature_get_SignInfoFont.restype=c_void_p
#        intPtr = GetDllLibPdf().Security_PdfSignature_get_SignInfoFont(self.Ptr)
#        ret = None if intPtr==None else Dictionary2(intPtr)
#        return ret
#


#    @SignInfoFont.setter
#    def SignInfoFont(self, value:'Dictionary2'):
#        GetDllLibPdf().Security_PdfSignature_set_SignInfoFont.argtypes=[c_void_p, c_void_p]
#        GetDllLibPdf().Security_PdfSignature_set_SignInfoFont(self.Ptr, value.Ptr)


    @property

    def DigitalSigner(self)->str:
        """
    <summary>
        The name of the person or authority signing the document, usually called signer. 
     </summary>
        """
        GetDllLibPdf().Security_PdfSignature_get_DigitalSigner.argtypes=[c_void_p]
        GetDllLibPdf().Security_PdfSignature_get_DigitalSigner.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Security_PdfSignature_get_DigitalSigner(self.Ptr))
        return ret


    @DigitalSigner.setter
    def DigitalSigner(self, value:str):
        GetDllLibPdf().Security_PdfSignature_set_DigitalSigner.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Security_PdfSignature_set_DigitalSigner(self.Ptr, value)

    @property

    def DigitalSignerLable(self)->str:
        """
    <summary>
        Digital Signature Common name label
    </summary>
        """
        GetDllLibPdf().Security_PdfSignature_get_DigitalSignerLable.argtypes=[c_void_p]
        GetDllLibPdf().Security_PdfSignature_get_DigitalSignerLable.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Security_PdfSignature_get_DigitalSignerLable(self.Ptr))
        return ret


    @DigitalSignerLable.setter
    def DigitalSignerLable(self, value:str):
        GetDllLibPdf().Security_PdfSignature_set_DigitalSignerLable.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Security_PdfSignature_set_DigitalSignerLable(self.Ptr, value)

    @property

    def Name(self)->str:
        """
    <summary>
        The name of the person or authority signing the document.
     </summary>
        """
        GetDllLibPdf().Security_PdfSignature_get_Name.argtypes=[c_void_p]
        GetDllLibPdf().Security_PdfSignature_get_Name.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Security_PdfSignature_get_Name(self.Ptr))
        return ret


    @Name.setter
    def Name(self, value:str):
        GetDllLibPdf().Security_PdfSignature_set_Name.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Security_PdfSignature_set_Name(self.Ptr, value)

    @property

    def NameLabel(self)->str:
        """
    <summary>
        Name label
    </summary>
        """
        GetDllLibPdf().Security_PdfSignature_get_NameLabel.argtypes=[c_void_p]
        GetDllLibPdf().Security_PdfSignature_get_NameLabel.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Security_PdfSignature_get_NameLabel(self.Ptr))
        return ret


    @NameLabel.setter
    def NameLabel(self, value:str):
        GetDllLibPdf().Security_PdfSignature_set_NameLabel.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Security_PdfSignature_set_NameLabel(self.Ptr, value)

    @property

    def DistinguishedNameLabel(self)->str:
        """
    <summary>
        Signature Distinguished Name label
    </summary>
        """
        GetDllLibPdf().Security_PdfSignature_get_DistinguishedNameLabel.argtypes=[c_void_p]
        GetDllLibPdf().Security_PdfSignature_get_DistinguishedNameLabel.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Security_PdfSignature_get_DistinguishedNameLabel(self.Ptr))
        return ret


    @DistinguishedNameLabel.setter
    def DistinguishedNameLabel(self, value:str):
        GetDllLibPdf().Security_PdfSignature_set_DistinguishedNameLabel.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Security_PdfSignature_set_DistinguishedNameLabel(self.Ptr, value)

    @property

    def DistinguishedName(self)->str:
        """
    <summary>
        Digital Signature Distinguished name.
            Notes: Assigning a stirng value to it directly is not recommended unless you know what is the Distinguish Name exactly.
            One way suggested of value Assignment is using pdfSignature.Certificate.IssuerName.Name,in which, pdfSignature is an instance of PDFSignature class.
    </summary>
        """
        GetDllLibPdf().Security_PdfSignature_get_DistinguishedName.argtypes=[c_void_p]
        GetDllLibPdf().Security_PdfSignature_get_DistinguishedName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Security_PdfSignature_get_DistinguishedName(self.Ptr))
        return ret


    @DistinguishedName.setter
    def DistinguishedName(self, value:str):
        GetDllLibPdf().Security_PdfSignature_set_DistinguishedName.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Security_PdfSignature_set_DistinguishedName(self.Ptr, value)

    @property
    def IsTag(self)->bool:
        """
    <summary>
        Flag determine whether to display the labels
    </summary>
        """
        GetDllLibPdf().Security_PdfSignature_get_IsTag.argtypes=[c_void_p]
        GetDllLibPdf().Security_PdfSignature_get_IsTag.restype=c_bool
        ret = GetDllLibPdf().Security_PdfSignature_get_IsTag(self.Ptr)
        return ret

    @IsTag.setter
    def IsTag(self, value:bool):
        GetDllLibPdf().Security_PdfSignature_set_IsTag.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().Security_PdfSignature_set_IsTag(self.Ptr, value)

    @property

    def ShowConfiguerText(self)->'SignatureConfiguerText':
        """
    <summary>
        Show Digital Signature,Configuer Text 
    </summary>
        """
        GetDllLibPdf().Security_PdfSignature_get_ShowConfiguerText.argtypes=[c_void_p]
        GetDllLibPdf().Security_PdfSignature_get_ShowConfiguerText.restype=c_int
        ret = GetDllLibPdf().Security_PdfSignature_get_ShowConfiguerText(self.Ptr)
        objwraped = SignatureConfiguerText(ret)
        return objwraped

    @ShowConfiguerText.setter
    def ShowConfiguerText(self, value:'SignatureConfiguerText'):
        GetDllLibPdf().Security_PdfSignature_set_ShowConfiguerText.argtypes=[c_void_p, c_int]
        GetDllLibPdf().Security_PdfSignature_set_ShowConfiguerText(self.Ptr, value.value)

    @property

    def GraphicsMode(self)->'GraphicMode':
        """
    <summary>
        The Grapphic render/display mode.
    </summary>
        """
        GetDllLibPdf().Security_PdfSignature_get_GraphicsMode.argtypes=[c_void_p]
        GetDllLibPdf().Security_PdfSignature_get_GraphicsMode.restype=c_int
        ret = GetDllLibPdf().Security_PdfSignature_get_GraphicsMode(self.Ptr)
        objwraped = GraphicMode(ret)
        return objwraped

    @GraphicsMode.setter
    def GraphicsMode(self, value:'GraphicMode'):
        GetDllLibPdf().Security_PdfSignature_set_GraphicsMode.argtypes=[c_void_p, c_int]
        GetDllLibPdf().Security_PdfSignature_set_GraphicsMode(self.Ptr, value.value)

    @property

    def ConfigGraphicType(self)->'ConfiguerGraphicType':
        """
    <summary>
        Digital Signature Graphic Type
    </summary>
        """
        GetDllLibPdf().Security_PdfSignature_get_ConfigGraphicType.argtypes=[c_void_p]
        GetDllLibPdf().Security_PdfSignature_get_ConfigGraphicType.restype=c_int
        ret = GetDllLibPdf().Security_PdfSignature_get_ConfigGraphicType(self.Ptr)
        objwraped = ConfiguerGraphicType(ret)
        return objwraped

    @ConfigGraphicType.setter
    def ConfigGraphicType(self, value:'ConfiguerGraphicType'):
        GetDllLibPdf().Security_PdfSignature_set_ConfigGraphicType.argtypes=[c_void_p, c_int]
        GetDllLibPdf().Security_PdfSignature_set_ConfigGraphicType(self.Ptr, value.value)

    @property

    def ConfiguerGraphicPath(self)->str:
        """
    <summary>
        Digital Signature Configuer Graphic file Path
    </summary>
        """
        GetDllLibPdf().Security_PdfSignature_get_ConfiguerGraphicPath.argtypes=[c_void_p]
        GetDllLibPdf().Security_PdfSignature_get_ConfiguerGraphicPath.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Security_PdfSignature_get_ConfiguerGraphicPath(self.Ptr))
        return ret


    @ConfiguerGraphicPath.setter
    def ConfiguerGraphicPath(self, value:str):
        GetDllLibPdf().Security_PdfSignature_set_ConfiguerGraphicPath.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Security_PdfSignature_set_ConfiguerGraphicPath(self.Ptr, value)

    @property

    def SignImageSource(self)->'PdfImage':
        """
    <summary>
        Signature Image Source 
    </summary>
        """
        GetDllLibPdf().Security_PdfSignature_get_SignImageSource.argtypes=[c_void_p]
        GetDllLibPdf().Security_PdfSignature_get_SignImageSource.restype=c_void_p
        intPtr = GetDllLibPdf().Security_PdfSignature_get_SignImageSource(self.Ptr)
        ret = None if intPtr==None else PdfImage(intPtr)
        return ret


    @SignImageSource.setter
    def SignImageSource(self, value:'PdfImage'):
        GetDllLibPdf().Security_PdfSignature_set_SignImageSource.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().Security_PdfSignature_set_SignImageSource(self.Ptr, value.Ptr)

    @property
    def IsConfiguerGraphicFilledBounds(self)->bool:
        """
    <summary>
        Digital Signature Configuer Graphic is filled bounds.
    </summary>
        """
        GetDllLibPdf().Security_PdfSignature_get_IsConfiguerGraphicFilledBounds.argtypes=[c_void_p]
        GetDllLibPdf().Security_PdfSignature_get_IsConfiguerGraphicFilledBounds.restype=c_bool
        ret = GetDllLibPdf().Security_PdfSignature_get_IsConfiguerGraphicFilledBounds(self.Ptr)
        return ret

    @IsConfiguerGraphicFilledBounds.setter
    def IsConfiguerGraphicFilledBounds(self, value:bool):
        GetDllLibPdf().Security_PdfSignature_set_IsConfiguerGraphicFilledBounds.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().Security_PdfSignature_set_IsConfiguerGraphicFilledBounds(self.Ptr, value)

    @property

    def SignImageLayout(self)->'SignImageLayout':
        """
    <summary>
        Set or get the sign image layout. 
    </summary>
        """
        GetDllLibPdf().Security_PdfSignature_get_SignImageLayout.argtypes=[c_void_p]
        GetDllLibPdf().Security_PdfSignature_get_SignImageLayout.restype=c_int
        ret = GetDllLibPdf().Security_PdfSignature_get_SignImageLayout(self.Ptr)
        objwraped = SignImageLayout(ret)
        return objwraped

    @SignImageLayout.setter
    def SignImageLayout(self, value:'SignImageLayout'):
        GetDllLibPdf().Security_PdfSignature_set_SignImageLayout.argtypes=[c_void_p, c_int]
        GetDllLibPdf().Security_PdfSignature_set_SignImageLayout(self.Ptr, value.value)

    @property

    def ReasonLabel(self)->str:
        """
    <summary>
        Digital Signature Reason  Label
    </summary>
        """
        GetDllLibPdf().Security_PdfSignature_get_ReasonLabel.argtypes=[c_void_p]
        GetDllLibPdf().Security_PdfSignature_get_ReasonLabel.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Security_PdfSignature_get_ReasonLabel(self.Ptr))
        return ret


    @ReasonLabel.setter
    def ReasonLabel(self, value:str):
        GetDllLibPdf().Security_PdfSignature_set_ReasonLabel.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Security_PdfSignature_set_ReasonLabel(self.Ptr, value)

    @property

    def DateLabel(self)->str:
        """
    <summary>
        Digital Signature Date Label
    </summary>
        """
        GetDllLibPdf().Security_PdfSignature_get_DateLabel.argtypes=[c_void_p]
        GetDllLibPdf().Security_PdfSignature_get_DateLabel.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Security_PdfSignature_get_DateLabel(self.Ptr))
        return ret


    @DateLabel.setter
    def DateLabel(self, value:str):
        GetDllLibPdf().Security_PdfSignature_set_DateLabel.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Security_PdfSignature_set_DateLabel(self.Ptr, value)

    @property

    def ContactInfoLabel(self)->str:
        """
    <summary>
        Digital Signature ContactInfo Label
    </summary>
        """
        GetDllLibPdf().Security_PdfSignature_get_ContactInfoLabel.argtypes=[c_void_p]
        GetDllLibPdf().Security_PdfSignature_get_ContactInfoLabel.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Security_PdfSignature_get_ContactInfoLabel(self.Ptr))
        return ret


    @ContactInfoLabel.setter
    def ContactInfoLabel(self, value:str):
        GetDllLibPdf().Security_PdfSignature_set_ContactInfoLabel.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Security_PdfSignature_set_ContactInfoLabel(self.Ptr, value)

    @property

    def LocationInfoLabel(self)->str:
        """
    <summary>
        Digital Signature LocationInfo Label
    </summary>
        """
        GetDllLibPdf().Security_PdfSignature_get_LocationInfoLabel.argtypes=[c_void_p]
        GetDllLibPdf().Security_PdfSignature_get_LocationInfoLabel.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Security_PdfSignature_get_LocationInfoLabel(self.Ptr))
        return ret


    @LocationInfoLabel.setter
    def LocationInfoLabel(self, value:str):
        GetDllLibPdf().Security_PdfSignature_set_LocationInfoLabel.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Security_PdfSignature_set_LocationInfoLabel(self.Ptr, value)

