from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfPolygonAnnotation (  PdfAnnotation) :
    @dispatch
    def __init__(self,page:PdfPageBase, points:List[PointF]):
        ptrPage:c_void_p = page.Ptr

        countnewValues = len(points)
        ArrayTypenewValues = c_void_p * countnewValues
        arraynewValues = ArrayTypenewValues()
        for i in range(0, countnewValues):
            arraynewValues[i] = points[i].Ptr

        GetDllLibPdf().PdfPolygonAnnotation_CreatePdfPolygonAnnotationPP.argtypes=[c_void_p,ArrayTypenewValues,c_int]
        GetDllLibPdf().PdfPolygonAnnotation_CreatePdfPolygonAnnotationPP.restype = c_void_p
        intPtr = GetDllLibPdf().PdfPolygonAnnotation_CreatePdfPolygonAnnotationPP(ptrPage,arraynewValues,countnewValues)
        super(PdfPolygonAnnotation, self).__init__(intPtr)
    """
    <summary>
        Represents the polygon annotation.
    </summary>
    """
    @property

    def Author(self)->str:
        """
    <summary>
        The user who created the annotation.
    </summary>
        """
        GetDllLibPdf().PdfPolygonAnnotation_get_Author.argtypes=[c_void_p]
        GetDllLibPdf().PdfPolygonAnnotation_get_Author.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfPolygonAnnotation_get_Author(self.Ptr))
        return ret


    @Author.setter
    def Author(self, value:str):
        GetDllLibPdf().PdfPolygonAnnotation_set_Author.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfPolygonAnnotation_set_Author(self.Ptr, value)

    @property

    def Subject(self)->str:
        """
    <summary>
        The description of the annotation.
    </summary>
        """
        GetDllLibPdf().PdfPolygonAnnotation_get_Subject.argtypes=[c_void_p]
        GetDllLibPdf().PdfPolygonAnnotation_get_Subject.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfPolygonAnnotation_get_Subject(self.Ptr))
        return ret


    @Subject.setter
    def Subject(self, value:str):
        GetDllLibPdf().PdfPolygonAnnotation_set_Subject.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfPolygonAnnotation_set_Subject(self.Ptr, value)

#    @property
#
#    def Vertices(self)->List['PointF']:
#        """
#    <summary>
#        The vertice coordinates.
#    </summary>
#        """
#        GetDllLibPdf().PdfPolygonAnnotation_get_Vertices.argtypes=[c_void_p]
#        GetDllLibPdf().PdfPolygonAnnotation_get_Vertices.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().PdfPolygonAnnotation_get_Vertices(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, PointF)
#        return ret


#    @Vertices.setter
#    def Vertices(self, value:List['PointF']):
#        vCount = len(value)
#        ArrayType = c_void_p * vCount
#        vArray = ArrayType()
#        for i in range(0, vCount):
#            vArray[i] = value[i].Ptr
#        GetDllLibPdf().PdfPolygonAnnotation_set_Vertices.argtypes=[c_void_p, ArrayType, c_int]
#        GetDllLibPdf().PdfPolygonAnnotation_set_Vertices(self.Ptr, vArray, vCount)


    @property

    def ModifiedDate(self)->'DateTime':
        """
    <summary>
        The date and time when the annotation was most recently modified.
    </summary>
        """
        GetDllLibPdf().PdfPolygonAnnotation_get_ModifiedDate.argtypes=[c_void_p]
        GetDllLibPdf().PdfPolygonAnnotation_get_ModifiedDate.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPolygonAnnotation_get_ModifiedDate(self.Ptr)
        ret = None if intPtr==None else DateTime(intPtr)
        return ret


    @ModifiedDate.setter
    def ModifiedDate(self, value:'DateTime'):
        GetDllLibPdf().PdfPolygonAnnotation_set_ModifiedDate.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfPolygonAnnotation_set_ModifiedDate(self.Ptr, value.Ptr)

    @property

    def BorderEffect(self)->'PdfBorderEffect':
        """
    <summary>
        The border effect.
    </summary>
        """
        GetDllLibPdf().PdfPolygonAnnotation_get_BorderEffect.argtypes=[c_void_p]
        GetDllLibPdf().PdfPolygonAnnotation_get_BorderEffect.restype=c_int
        ret = GetDllLibPdf().PdfPolygonAnnotation_get_BorderEffect(self.Ptr)
        objwraped = PdfBorderEffect(ret)
        return objwraped

    @BorderEffect.setter
    def BorderEffect(self, value:'PdfBorderEffect'):
        GetDllLibPdf().PdfPolygonAnnotation_set_BorderEffect.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfPolygonAnnotation_set_BorderEffect(self.Ptr, value.value)

    @staticmethod
    def RADIUS()->float:
        """
    <summary>
        The radius.
    </summary>
        """
        #GetDllLibPdf().PdfPolygonAnnotation_RADIUS.argtypes=[]
        GetDllLibPdf().PdfPolygonAnnotation_RADIUS.restype=c_float
        ret = GetDllLibPdf().PdfPolygonAnnotation_RADIUS()
        return ret

