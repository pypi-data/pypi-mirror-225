from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfSignatureAppearance (  IPdfSignatureAppearance) :
    """
    <summary>
         Provide a custom signature appearance implemation.
    </summary>
    """
    @property

    def NameLabel(self)->str:
        """
    <summary>
        The label of The name of the person or authority signing the document.
    </summary>
        """
        GetDllLibPdf().PdfSignatureAppearance_get_NameLabel.argtypes=[c_void_p]
        GetDllLibPdf().PdfSignatureAppearance_get_NameLabel.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfSignatureAppearance_get_NameLabel(self.Ptr))
        return ret


    @NameLabel.setter
    def NameLabel(self, value:str):
        GetDllLibPdf().PdfSignatureAppearance_set_NameLabel.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfSignatureAppearance_set_NameLabel(self.Ptr, value)

    @property

    def ReasonLabel(self)->str:
        """
    <summary>
        The label of signature's reason
    </summary>
        """
        GetDllLibPdf().PdfSignatureAppearance_get_ReasonLabel.argtypes=[c_void_p]
        GetDllLibPdf().PdfSignatureAppearance_get_ReasonLabel.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfSignatureAppearance_get_ReasonLabel(self.Ptr))
        return ret


    @ReasonLabel.setter
    def ReasonLabel(self, value:str):
        GetDllLibPdf().PdfSignatureAppearance_set_ReasonLabel.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfSignatureAppearance_set_ReasonLabel(self.Ptr, value)

    @property

    def LocationLabel(self)->str:
        """
    <summary>
        The label of signature's location
    </summary>
        """
        GetDllLibPdf().PdfSignatureAppearance_get_LocationLabel.argtypes=[c_void_p]
        GetDllLibPdf().PdfSignatureAppearance_get_LocationLabel.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfSignatureAppearance_get_LocationLabel(self.Ptr))
        return ret


    @LocationLabel.setter
    def LocationLabel(self, value:str):
        GetDllLibPdf().PdfSignatureAppearance_set_LocationLabel.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfSignatureAppearance_set_LocationLabel(self.Ptr, value)

    @property

    def ContactInfoLabel(self)->str:
        """
    <summary>
        The label of signature's contactInfo
    </summary>
        """
        GetDllLibPdf().PdfSignatureAppearance_get_ContactInfoLabel.argtypes=[c_void_p]
        GetDllLibPdf().PdfSignatureAppearance_get_ContactInfoLabel.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfSignatureAppearance_get_ContactInfoLabel(self.Ptr))
        return ret


    @ContactInfoLabel.setter
    def ContactInfoLabel(self, value:str):
        GetDllLibPdf().PdfSignatureAppearance_set_ContactInfoLabel.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfSignatureAppearance_set_ContactInfoLabel(self.Ptr, value)

    @property

    def DateLabel(self)->str:
        """
    <summary>
        The label of signature's date
    </summary>
        """
        GetDllLibPdf().PdfSignatureAppearance_get_DateLabel.argtypes=[c_void_p]
        GetDllLibPdf().PdfSignatureAppearance_get_DateLabel.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfSignatureAppearance_get_DateLabel(self.Ptr))
        return ret


    @DateLabel.setter
    def DateLabel(self, value:str):
        GetDllLibPdf().PdfSignatureAppearance_set_DateLabel.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfSignatureAppearance_set_DateLabel(self.Ptr, value)

    @property

    def SignatureImage(self)->'PdfImage':
        """

        """
        GetDllLibPdf().PdfSignatureAppearance_get_SignatureImage.argtypes=[c_void_p]
        GetDllLibPdf().PdfSignatureAppearance_get_SignatureImage.restype=c_void_p
        intPtr = GetDllLibPdf().PdfSignatureAppearance_get_SignatureImage(self.Ptr)
        ret = None if intPtr==None else PdfImage(intPtr)
        return ret


    @SignatureImage.setter
    def SignatureImage(self, value:'PdfImage'):
        GetDllLibPdf().PdfSignatureAppearance_set_SignatureImage.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfSignatureAppearance_set_SignatureImage(self.Ptr, value.Ptr)

    @property

    def GraphicMode(self)->'GraphicMode':
        """
    <summary>
        The Grapphic render/display mode.
    </summary>
        """
        GetDllLibPdf().PdfSignatureAppearance_get_GraphicMode.argtypes=[c_void_p]
        GetDllLibPdf().PdfSignatureAppearance_get_GraphicMode.restype=c_int
        ret = GetDllLibPdf().PdfSignatureAppearance_get_GraphicMode(self.Ptr)
        objwraped = GraphicMode(ret)
        return objwraped

    @GraphicMode.setter
    def GraphicMode(self, value:'GraphicMode'):
        GetDllLibPdf().PdfSignatureAppearance_set_GraphicMode.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfSignatureAppearance_set_GraphicMode(self.Ptr, value.value)

    @property

    def SignImageLayout(self)->'SignImageLayout':
        """
    <summary>
        Set or get the sign image layout. 
    </summary>
        """
        GetDllLibPdf().PdfSignatureAppearance_get_SignImageLayout.argtypes=[c_void_p]
        GetDllLibPdf().PdfSignatureAppearance_get_SignImageLayout.restype=c_int
        ret = GetDllLibPdf().PdfSignatureAppearance_get_SignImageLayout(self.Ptr)
        objwraped = SignImageLayout(ret)
        return objwraped

    @SignImageLayout.setter
    def SignImageLayout(self, value:'SignImageLayout'):
        GetDllLibPdf().PdfSignatureAppearance_set_SignImageLayout.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfSignatureAppearance_set_SignImageLayout(self.Ptr, value.value)


    def Generate(self ,g:'PdfCanvas'):
        """
    <summary>
        Generate custom signature appearance by a graphics context.
    </summary>
    <param name="g">A graphics context of signature appearance.</param>
        """
        intPtrg:c_void_p = g.Ptr

        GetDllLibPdf().PdfSignatureAppearance_Generate.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfSignatureAppearance_Generate(self.Ptr, intPtrg)

