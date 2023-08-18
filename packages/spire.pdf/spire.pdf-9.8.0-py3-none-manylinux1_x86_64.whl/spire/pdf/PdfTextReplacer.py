from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfTextReplacer (SpireObject) :

    @dispatch
    def __init__(self,page:'PdfPageBase'):
        ptrPage:c_void_p = page.Ptr

        GetDllLibPdf().PdfTextReplacer_CreatePdfTextReplacerP.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextReplacer_CreatePdfTextReplacerP.restype = c_void_p
        intPtr = GetDllLibPdf().PdfTextReplacer_CreatePdfTextReplacerP(ptrPage)
        super(PdfTextReplacer, self).__init__(intPtr)
    """
    <summary>
        Represents the text replace.
    </summary>
    """

    def ReplaceText(self ,oldText:str,newText:str):
        """
    <summary>
        Replaces the target text in the page.
    </summary>
    <param name="oldText">The old text.</param>
    <param name="newText">The new text.</param>
        """
        
        GetDllLibPdf().PdfTextReplacer_ReplaceText.argtypes=[c_void_p ,c_wchar_p,c_wchar_p]
        GetDllLibPdf().PdfTextReplacer_ReplaceText(self.Ptr, oldText,newText)

    @dispatch

    def ReplaceAllText(self ,oldText:str,newText:str):
        """
    <summary>
        Replaces all the text in the page.
    </summary>
    <param name="oldText">The old text</param>
    <param name="newText">The new text</param>
        """
        
        GetDllLibPdf().PdfTextReplacer_ReplaceAllText.argtypes=[c_void_p ,c_wchar_p,c_wchar_p]
        GetDllLibPdf().PdfTextReplacer_ReplaceAllText(self.Ptr, oldText,newText)

    @dispatch

    def ReplaceAllText(self ,oldText:str,newText:str,textColor:Color):
        """
    <summary>
        Replaces all target text in the page.
    </summary>
    <param name="oldText">The old text</param>
    <param name="newText">The new text</param>
    <param name="textColor">The color of the new text.</param>
        """
        intPtrtextColor:c_void_p = textColor.Ptr

        GetDllLibPdf().PdfTextReplacer_ReplaceAllTextONT.argtypes=[c_void_p ,c_wchar_p,c_wchar_p,c_void_p]
        GetDllLibPdf().PdfTextReplacer_ReplaceAllTextONT(self.Ptr, oldText,newText,intPtrtextColor)

    def Dispose(self):
        """
    <summary>
        Releases all resources used.
    </summary>
        """
        GetDllLibPdf().PdfTextReplacer_Dispose.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextReplacer_Dispose(self.Ptr)

