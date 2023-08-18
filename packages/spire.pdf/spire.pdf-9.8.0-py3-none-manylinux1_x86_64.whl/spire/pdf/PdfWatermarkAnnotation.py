from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfWatermarkAnnotation (  PdfAnnotation) :
    """
    <summary>
        The water mark annotation.
    </summary>
    """
    @property
    def Appearance(self)->'PdfAppearance':
        return None

    @Appearance.setter
    def Appearance(self, value:'PdfAppearance'):
        GetDllLibPdf().PdfWatermarkAnnotation_set_Appearance.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfWatermarkAnnotation_set_Appearance(self.Ptr, value.Ptr)


    def SetMatrix(self ,matrix:List[float]):
        """
    <summary>
        Set the matrix.
    </summary>
    <param name="matrix">The matrix</param>
        """
        #arraymatrix:ArrayTypematrix = ""
        countmatrix = len(matrix)
        ArrayTypematrix = c_float * countmatrix
        arraymatrix = ArrayTypematrix()
        for i in range(0, countmatrix):
            arraymatrix[i] = matrix[i]


        GetDllLibPdf().PdfWatermarkAnnotation_SetMatrix.argtypes=[c_void_p ,ArrayTypematrix]
        GetDllLibPdf().PdfWatermarkAnnotation_SetMatrix(self.Ptr, arraymatrix)


    def SetHorizontalTranslation(self ,horizontal:float):
        """
    <summary>
        Set the horizontal translation.
    </summary>
    <param name="horizontal">The horizontal</param>
        """
        
        GetDllLibPdf().PdfWatermarkAnnotation_SetHorizontalTranslation.argtypes=[c_void_p ,c_float]
        GetDllLibPdf().PdfWatermarkAnnotation_SetHorizontalTranslation(self.Ptr, horizontal)


    def SetVerticalTranslation(self ,vertical:float):
        """
    <summary>
        Set the vertical translation.
    </summary>
    <param name="vertical">The vertiacl</param>
        """
        
        GetDllLibPdf().PdfWatermarkAnnotation_SetVerticalTranslation.argtypes=[c_void_p ,c_float]
        GetDllLibPdf().PdfWatermarkAnnotation_SetVerticalTranslation(self.Ptr, vertical)

