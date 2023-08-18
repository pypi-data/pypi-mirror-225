from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfPolyLineAnnotation (  PdfAnnotation) :
    @dispatch
    def __init__(self,page:PdfPageBase, points:List[PointF]):
        ptrPage:c_void_p = page.Ptr

        countnewValues = len(points)
        ArrayTypenewValues = c_void_p * countnewValues
        arraynewValues = ArrayTypenewValues()
        for i in range(0, countnewValues):
            arraynewValues[i] = points[i].Ptr

        GetDllLibPdf().PdfPolyLineAnnotation_CreatePdfPolyLineAnnotationPP.argtypes=[c_void_p,ArrayTypenewValues,c_int]
        GetDllLibPdf().PdfPolyLineAnnotation_CreatePdfPolyLineAnnotationPP.restype = c_void_p
        intPtr = GetDllLibPdf().PdfPolyLineAnnotation_CreatePdfPolyLineAnnotationPP(ptrPage,arraynewValues,countnewValues)
        super(PdfPolyLineAnnotation, self).__init__(intPtr)
    """
    <summary>
        Represents the poly line annotation.
    </summary>
    """
    @property

    def Author(self)->str:
        """
    <summary>
        The user who created the annotation.
    </summary>
        """
        GetDllLibPdf().PdfPolyLineAnnotation_get_Author.argtypes=[c_void_p]
        GetDllLibPdf().PdfPolyLineAnnotation_get_Author.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfPolyLineAnnotation_get_Author(self.Ptr))
        return ret


    @Author.setter
    def Author(self, value:str):
        GetDllLibPdf().PdfPolyLineAnnotation_set_Author.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfPolyLineAnnotation_set_Author(self.Ptr, value)

    @property

    def Subject(self)->str:
        """
    <summary>
        The description of the annotation.
    </summary>
        """
        GetDllLibPdf().PdfPolyLineAnnotation_get_Subject.argtypes=[c_void_p]
        GetDllLibPdf().PdfPolyLineAnnotation_get_Subject.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfPolyLineAnnotation_get_Subject(self.Ptr))
        return ret


    @Subject.setter
    def Subject(self, value:str):
        GetDllLibPdf().PdfPolyLineAnnotation_set_Subject.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfPolyLineAnnotation_set_Subject(self.Ptr, value)

#    @property
#
#    def Vertices(self)->List['PointF']:
#        """
#    <summary>
#        The vertice coordinates.
#    </summary>
#        """
#        GetDllLibPdf().PdfPolyLineAnnotation_get_Vertices.argtypes=[c_void_p]
#        GetDllLibPdf().PdfPolyLineAnnotation_get_Vertices.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().PdfPolyLineAnnotation_get_Vertices(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, PointF)
#        return ret


#    @Vertices.setter
#    def Vertices(self, value:List['PointF']):
#        vCount = len(value)
#        ArrayType = c_void_p * vCount
#        vArray = ArrayType()
#        for i in range(0, vCount):
#            vArray[i] = value[i].Ptr
#        GetDllLibPdf().PdfPolyLineAnnotation_set_Vertices.argtypes=[c_void_p, ArrayType, c_int]
#        GetDllLibPdf().PdfPolyLineAnnotation_set_Vertices(self.Ptr, vArray, vCount)


