from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfTableExtractor (SpireObject) :
    """
    <summary>
        Represent the pdf table extractor.
    </summary>
    """
#
#    def ExtractTable(self ,pageIndex:int)->List['PdfTable']:
#        """
#    <summary>
#        Extract table from the pdf document
#    </summary>
#    <param name="pageIndex">pageIndex</param>
#    <returns>An array of PdfTable.</returns>
#        """
#        
#        GetDllLibPdf().PdfTableExtractor_ExtractTable.argtypes=[c_void_p ,c_int]
#        GetDllLibPdf().PdfTableExtractor_ExtractTable.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().PdfTableExtractor_ExtractTable(self.Ptr, pageIndex)
#        ret = GetObjVectorFromArray(intPtrArray, PdfTable)
#        return ret


    def Dispose(self):
        """

        """
        GetDllLibPdf().PdfTableExtractor_Dispose.argtypes=[c_void_p]
        GetDllLibPdf().PdfTableExtractor_Dispose(self.Ptr)

