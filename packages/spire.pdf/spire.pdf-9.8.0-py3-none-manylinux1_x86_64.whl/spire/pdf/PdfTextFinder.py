from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfTextFinder (SpireObject) :
    @dispatch
    def __init__(self, page:PdfPageBase):
        intPtrPage:c_void_p = page.Ptr

        GetDllLibPdf().PdfTextFinder_CreatePdfTextFinderP.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextFinder_CreatePdfTextFinderP.restype = c_void_p
        intPtr = GetDllLibPdf().PdfTextFinder_CreatePdfTextFinderP(intPtrPage)
        super(PdfTextFinder, self).__init__(intPtr)
    """
    <summary>
        Representing the way how to find text on a page.
    </summary>
    """
    @property

    def Options(self)->'PdfTextFindOptions':
        """

        """
        GetDllLibPdf().PdfTextFinder_get_Options.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextFinder_get_Options.restype=c_void_p
        intPtr = GetDllLibPdf().PdfTextFinder_get_Options(self.Ptr)
        ret = None if intPtr==None else PdfTextFindOptions(intPtr)
        return ret


    @Options.setter
    def Options(self, value:'PdfTextFindOptions'):
        GetDllLibPdf().PdfTextFinder_set_Options.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfTextFinder_set_Options(self.Ptr, value.Ptr)


    def Find(self ,text:str)->List[PdfTextFragment]:
        """
    <summary>
        Find target text.
    </summary>
    <param name="text">The target text.</param>
    <returns>Returns the PdfTextFragment as PdfTextFragment[].</returns>
        """
        GetDllLibPdf().PdfTextFinder_Find.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfTextFinder_Find.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().PdfTextFinder_Find(self.Ptr, text)
        ret = GetObjVectorFromArray(intPtrArray, PdfTextFragment)
        return ret




    def FindAllText(self)->List[PdfTextFragment]:
        """
    <summary>
        Find all text in the page
    </summary>
    <returns>All text find in the page.</returns>
        """
        GetDllLibPdf().PdfTextFinder_FindAllText.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextFinder_FindAllText.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().PdfTextFinder_FindAllText(self.Ptr)
        ret = GetObjVectorFromArray(intPtrArray, PdfTextFragment)
        return ret



    def Dispose(self):
        """
    <summary>
        Releases all resources used.
    </summary>
        """
        GetDllLibPdf().PdfTextFinder_Dispose.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextFinder_Dispose(self.Ptr)

