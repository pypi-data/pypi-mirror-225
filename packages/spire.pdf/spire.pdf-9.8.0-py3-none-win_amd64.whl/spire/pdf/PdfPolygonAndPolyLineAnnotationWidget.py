from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfPolygonAndPolyLineAnnotationWidget (  PdfMarkUpAnnotationWidget) :
    """
    <summary>
        Represents the loaded text PolygonAndPolyLine annotation class.
    </summary>
    """
#    @property
#
#    def Vertices(self)->List['PointF']:
#        """
#    <summary>
#        The vertice coordinates.
#    </summary>
#        """
#        GetDllLibPdf().PdfPolygonAndPolyLineAnnotationWidget_get_Vertices.argtypes=[c_void_p]
#        GetDllLibPdf().PdfPolygonAndPolyLineAnnotationWidget_get_Vertices.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().PdfPolygonAndPolyLineAnnotationWidget_get_Vertices(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, PointF)
#        return ret


#    @Vertices.setter
#    def Vertices(self, value:List['PointF']):
#        vCount = len(value)
#        ArrayType = c_void_p * vCount
#        vArray = ArrayType()
#        for i in range(0, vCount):
#            vArray[i] = value[i].Ptr
#        GetDllLibPdf().PdfPolygonAndPolyLineAnnotationWidget_set_Vertices.argtypes=[c_void_p, ArrayType, c_int]
#        GetDllLibPdf().PdfPolygonAndPolyLineAnnotationWidget_set_Vertices(self.Ptr, vArray, vCount)


    def ObjectID(self)->int:
        """
    <summary>
        Represents the Form field identifier
    </summary>
        """
        GetDllLibPdf().PdfPolygonAndPolyLineAnnotationWidget_ObjectID.argtypes=[c_void_p]
        GetDllLibPdf().PdfPolygonAndPolyLineAnnotationWidget_ObjectID.restype=c_int
        ret = GetDllLibPdf().PdfPolygonAndPolyLineAnnotationWidget_ObjectID(self.Ptr)
        return ret

