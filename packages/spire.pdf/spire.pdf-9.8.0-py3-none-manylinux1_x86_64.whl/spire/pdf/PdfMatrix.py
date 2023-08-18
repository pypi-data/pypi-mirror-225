from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfMatrix (SpireObject) :
    """
    <summary>
        Represent the matrix
    </summary>
    """
    @property
    def OffsetX(self)->float:
        """
    <summary>
        Gets the x translation value (the dx value, or the element in the third row and first column).
    </summary>
        """
        GetDllLibPdf().PdfMatrix_get_OffsetX.argtypes=[c_void_p]
        GetDllLibPdf().PdfMatrix_get_OffsetX.restype=c_float
        ret = GetDllLibPdf().PdfMatrix_get_OffsetX(self.Ptr)
        return ret

    @property
    def OffsetY(self)->float:
        """
    <summary>
        Gets the x translation value (the dx value, or the element in the third row and second column).
    </summary>
        """
        GetDllLibPdf().PdfMatrix_get_OffsetY.argtypes=[c_void_p]
        GetDllLibPdf().PdfMatrix_get_OffsetY.restype=c_float
        ret = GetDllLibPdf().PdfMatrix_get_OffsetY(self.Ptr)
        return ret

    @property

    def Elements(self)->List[float]:
        """
    <summary>
        Gets an array of floating-point values that represents the elements.
    </summary>
        """
        GetDllLibPdf().PdfMatrix_get_Elements.argtypes=[c_void_p]
        GetDllLibPdf().PdfMatrix_get_Elements.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().PdfMatrix_get_Elements(self.Ptr)
        ret = GetVectorFromArray(intPtrArray, c_float)
        return ret

    @dispatch

    def Multiply(self ,matrix:'PdfMatrix'):
        """
    <summary>
        Prepend the specified matrix.
    </summary>
    <param name="matrix">Matrix is to be multiplied.</param>
        """
        intPtrmatrix:c_void_p = matrix.Ptr

        GetDllLibPdf().PdfMatrix_Multiply.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfMatrix_Multiply(self.Ptr, intPtrmatrix)

    @dispatch

    def Multiply(self ,matrix:'PdfMatrix',order:PdfMatrixOrder):
        """
    <summary>
        Apply the specified matrix by the specified order.
    </summary>
    <param name="matrix">Matrix is to be multiplied.</param>
    <param name="order">Represent the applying order.</param>
        """
        intPtrmatrix:c_void_p = matrix.Ptr
        enumorder:c_int = order.value

        GetDllLibPdf().PdfMatrix_MultiplyMO.argtypes=[c_void_p ,c_void_p,c_int]
        GetDllLibPdf().PdfMatrix_MultiplyMO(self.Ptr, intPtrmatrix,enumorder)

    @dispatch

    def Translate(self ,offsetX:float,offsetY:float):
        """
    <summary>
        Prepend the specified translation vector (offsetX and offsetY).
    </summary>
    <param name="offsetX">The x value by which to translate.</param>
    <param name="offsetY">The y value by which to translate.</param>
        """
        
        GetDllLibPdf().PdfMatrix_Translate.argtypes=[c_void_p ,c_float,c_float]
        GetDllLibPdf().PdfMatrix_Translate(self.Ptr, offsetX,offsetY)

    @dispatch

    def Translate(self ,offsetX:float,offsetY:float,order:PdfMatrixOrder):
        """
    <summary>
        Apply the specified translation vector (offsetX and offsetY) by the specified order.
    </summary>
    <param name="offsetX">The x value by which to translate.</param>
    <param name="offsetY">The y value by which to translate.</param>
    <param name="order">Represent the applying order.</param>
        """
        enumorder:c_int = order.value

        GetDllLibPdf().PdfMatrix_TranslateOOO.argtypes=[c_void_p ,c_float,c_float,c_int]
        GetDllLibPdf().PdfMatrix_TranslateOOO(self.Ptr, offsetX,offsetY,enumorder)

    @dispatch

    def Scale(self ,scaleX:float,scaleY:float):
        """
    <summary>
        Prepend the specified scale vector (scaleX and scaleY).
    </summary>
    <param name="scaleX">The value by which to scale in the x-axis direction.</param>
    <param name="scaleY">The value by which to scale in the y-axis direction.</param>
        """
        
        GetDllLibPdf().PdfMatrix_Scale.argtypes=[c_void_p ,c_float,c_float]
        GetDllLibPdf().PdfMatrix_Scale(self.Ptr, scaleX,scaleY)

    @dispatch

    def Scale(self ,scaleX:float,scaleY:float,order:PdfMatrixOrder):
        """
    <summary>
        Apply the specified scale vector (scaleX and scaleY) by the specified order.
    </summary>
    <param name="scaleX">The value by which to scale in the x-axis direction.</param>
    <param name="scaleY">The value by which to scale in the y-axis direction.</param>
    <param name="order">Represent the applying order.</param>
        """
        enumorder:c_int = order.value

        GetDllLibPdf().PdfMatrix_ScaleSSO.argtypes=[c_void_p ,c_float,c_float,c_int]
        GetDllLibPdf().PdfMatrix_ScaleSSO(self.Ptr, scaleX,scaleY,enumorder)

    @dispatch

    def Rotate(self ,angle:float):
        """
    <summary>
        Prepend a clockwise rotation(angle) around the origin.
    </summary>
    <param name="angle">The angle of the rotation, in degrees.</param>
        """
        
        GetDllLibPdf().PdfMatrix_Rotate.argtypes=[c_void_p ,c_float]
        GetDllLibPdf().PdfMatrix_Rotate(self.Ptr, angle)

    @dispatch

    def Rotate(self ,angle:float,order:PdfMatrixOrder):
        """
    <summary>
        Apply a clockwise rotation(angle) around the origin by the specified order.
    </summary>
    <param name="angle">The angle of the rotation, in degrees.</param>
    <param name="order">Represent the applying order.</param>
        """
        enumorder:c_int = order.value

        GetDllLibPdf().PdfMatrix_RotateAO.argtypes=[c_void_p ,c_float,c_int]
        GetDllLibPdf().PdfMatrix_RotateAO(self.Ptr, angle,enumorder)

    @dispatch

    def Skew(self ,angleX:float,angleY:float):
        """
    <summary>
        Prepend the specified skew angles(angleX angleY).
    </summary>
    <param name="angleX">The horizontal skew angle, in degrees.</param>
    <param name="angleY">The vertical skew angle, in degrees.</param>
        """
        
        GetDllLibPdf().PdfMatrix_Skew.argtypes=[c_void_p ,c_float,c_float]
        GetDllLibPdf().PdfMatrix_Skew(self.Ptr, angleX,angleY)

    @dispatch

    def Skew(self ,angleX:float,angleY:float,order:PdfMatrixOrder):
        """
    <summary>
        Prepend the specified skew angles(angleX angleY) by the specified order.
    </summary>
    <param name="angleX">The horizontal skew angle, in degrees.</param>
    <param name="angleY">The vertical skew angle, in degrees.</param>
    <param name="order">Represent the applying order.</param>
        """
        enumorder:c_int = order.value

        GetDllLibPdf().PdfMatrix_SkewAAO.argtypes=[c_void_p ,c_float,c_float,c_int]
        GetDllLibPdf().PdfMatrix_SkewAAO(self.Ptr, angleX,angleY,enumorder)

    @dispatch

    def Shear(self ,shearX:float,shearY:float):
        """
    <summary>
        Prepend the specified Shear vector (shearX and shearY).
    </summary>
    <param name="shearX">The horizontal shear factor.</param>
    <param name="shearY">The vertical shear factor.</param>
        """
        
        GetDllLibPdf().PdfMatrix_Shear.argtypes=[c_void_p ,c_float,c_float]
        GetDllLibPdf().PdfMatrix_Shear(self.Ptr, shearX,shearY)

    @dispatch

    def Shear(self ,shearX:float,shearY:float,order:PdfMatrixOrder):
        """
    <summary>
        Apply the specified Shear vector (shearX and shearY) by the specified order.
    </summary>
    <param name="shearX">The horizontal shear factor.</param>
    <param name="shearY">The vertical shear factor.</param>
    <param name="order">Represent the applying order.</param>
        """
        enumorder:c_int = order.value

        GetDllLibPdf().PdfMatrix_ShearSSO.argtypes=[c_void_p ,c_float,c_float,c_int]
        GetDllLibPdf().PdfMatrix_ShearSSO(self.Ptr, shearX,shearY,enumorder)

#
#    def TransformPoints(self ,pts:'PointF[]')->List['PointF']:
#        """
#    <summary>
#        Applies the geometric transform to a specified array of points.
#    </summary>
#    <param name="pt">An array of points to transform.</param>
#    <returns>The transformed points.</returns>
#        """
#        #arraypts:ArrayTypepts = ""
#        countpts = len(pts)
#        ArrayTypepts = c_void_p * countpts
#        arraypts = ArrayTypepts()
#        for i in range(0, countpts):
#            arraypts[i] = pts[i].Ptr
#
#
#        GetDllLibPdf().PdfMatrix_TransformPoints.argtypes=[c_void_p ,ArrayTypepts]
#        GetDllLibPdf().PdfMatrix_TransformPoints.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().PdfMatrix_TransformPoints(self.Ptr, arraypts)
#        ret = GetObjVectorFromArray(intPtrArray, PointF)
#        return ret



    def Clone(self)->'PdfMatrix':
        """

        """
        GetDllLibPdf().PdfMatrix_Clone.argtypes=[c_void_p]
        GetDllLibPdf().PdfMatrix_Clone.restype=c_void_p
        intPtr = GetDllLibPdf().PdfMatrix_Clone(self.Ptr)
        ret = None if intPtr==None else PdfMatrix(intPtr)
        return ret



    def DegreeToRadian(self ,degree:float)->float:
        """
    <summary>
        Converts degree to radian.
    </summary>
    <param name="degree">The degree</param>
    <returns>The radian</returns>
        """
        
        GetDllLibPdf().PdfMatrix_DegreeToRadian.argtypes=[c_void_p ,c_double]
        GetDllLibPdf().PdfMatrix_DegreeToRadian.restype=c_double
        ret = GetDllLibPdf().PdfMatrix_DegreeToRadian(self.Ptr, degree)
        return ret

