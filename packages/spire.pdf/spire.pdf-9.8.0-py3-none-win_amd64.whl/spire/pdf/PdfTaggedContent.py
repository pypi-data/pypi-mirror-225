from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfTaggedContent (SpireObject) :
    """
    <summary>
        Represents the content of tagged pdf.
    </summary>
    """
    @property

    def StructureTreeRoot(self)->'PdfStructureTreeRoot':
        """
    <summary>
        Pdf logical structure tree root.
    </summary>
        """
        GetDllLibPdf().PdfTaggedContent_get_StructureTreeRoot.argtypes=[c_void_p]
        GetDllLibPdf().PdfTaggedContent_get_StructureTreeRoot.restype=c_void_p
        intPtr = GetDllLibPdf().PdfTaggedContent_get_StructureTreeRoot(self.Ptr)
        ret = None if intPtr==None else PdfStructureTreeRoot(intPtr)
        return ret



    def SetLanguage(self ,language:str):
        """
    <summary>
        Set the natural language for all text in the document.
            A Language-Tag as defined in RFC 3066, Tags for the Identification of Languages.
    </summary>
    <param name="language"></param>
        """
        
        GetDllLibPdf().PdfTaggedContent_SetLanguage.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfTaggedContent_SetLanguage(self.Ptr, language)


    def SetTitle(self ,title:str):
        """
    <summary>
        Set the document's title.
    </summary>
    <param name="title"></param>
        """
        
        GetDllLibPdf().PdfTaggedContent_SetTitle.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfTaggedContent_SetTitle(self.Ptr, title)

    def SetPdfUA1Identification(self):
        """
    <summary>
        Set pdf/UA identification.
    </summary>
        """
        GetDllLibPdf().PdfTaggedContent_SetPdfUA1Identification.argtypes=[c_void_p]
        GetDllLibPdf().PdfTaggedContent_SetPdfUA1Identification(self.Ptr)

