from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfLinearGradientBrush (  PdfGradientBrush) :
    @dispatch
    def __init__(self, point1:PointF, point2:PointF,color1:PdfRGBColor,color2:PdfRGBColor):
        ptrpoint1:c_void_p = point1.Ptr
        ptrpoint2:c_void_p = point2.Ptr
        ptrcolor1:c_void_p = color1.Ptr
        ptrcolor2:c_void_p = color2.Ptr

        GetDllLibPdf().PdfLinearGradientBrush_CreatePdfLinearGradientBrushPPCC.argtypes=[c_void_p,c_void_p,c_void_p,c_void_p]
        GetDllLibPdf().PdfLinearGradientBrush_CreatePdfLinearGradientBrushPPCC.restype = c_void_p
        intPtr = GetDllLibPdf().PdfLinearGradientBrush_CreatePdfLinearGradientBrushPPCC(ptrpoint1,ptrpoint2,ptrcolor1,ptrcolor2)
        super(PdfLinearGradientBrush, self).__init__(intPtr)

    @dispatch
    def __init__(self, rect:RectangleF, color1:PdfRGBColor,color2:PdfRGBColor,mode:PdfLinearGradientMode):
        ptrrect:c_void_p = rect.Ptr
        ptrcolor1:c_void_p = color1.Ptr
        ptrcolor2:c_void_p = color2.Ptr
        enumLinearGradientMode:c_int = mode.value

        GetDllLibPdf().PdfLinearGradientBrush_CreatePdfLinearGradientBrushRCCM.argtypes=[c_void_p,c_void_p,c_void_p,c_int]
        GetDllLibPdf().PdfLinearGradientBrush_CreatePdfLinearGradientBrushRCCM.restype = c_void_p
        intPtr = GetDllLibPdf().PdfLinearGradientBrush_CreatePdfLinearGradientBrushRCCM(ptrrect,ptrcolor1,ptrcolor2,enumLinearGradientMode)
        super(PdfLinearGradientBrush, self).__init__(intPtr)

    @dispatch
    def __init__(self, rect:RectangleF, color1:PdfRGBColor,color2:PdfRGBColor,angle:float):
        ptrrect:c_void_p = rect.Ptr
        ptrcolor1:c_void_p = color1.Ptr
        ptrcolor2:c_void_p = color2.Ptr

        GetDllLibPdf().PdfLinearGradientBrush_CreatePdfLinearGradientBrushRCCA.argtypes=[c_void_p,c_void_p,c_void_p,c_float]
        GetDllLibPdf().PdfLinearGradientBrush_CreatePdfLinearGradientBrushRCCA.restype = c_void_p
        intPtr = GetDllLibPdf().PdfLinearGradientBrush_CreatePdfLinearGradientBrushRCCA(ptrrect,ptrcolor1,ptrcolor2,angle)
        super(PdfLinearGradientBrush, self).__init__(intPtr)
    """
    <summary>
        Implements linear gradient brush by using PDF axial shading pattern.
    </summary>
    """
    @property

    def Blend(self)->'PdfBlend':
        """
    <summary>
        Gets or sets a PdfBlend that specifies positions
            and factors that define a custom falloff for the gradient.
    </summary>
        """
        GetDllLibPdf().PdfLinearGradientBrush_get_Blend.argtypes=[c_void_p]
        GetDllLibPdf().PdfLinearGradientBrush_get_Blend.restype=c_void_p
        intPtr = GetDllLibPdf().PdfLinearGradientBrush_get_Blend(self.Ptr)
        ret = None if intPtr==None else PdfBlend(intPtr)
        return ret


    @Blend.setter
    def Blend(self, value:'PdfBlend'):
        GetDllLibPdf().PdfLinearGradientBrush_set_Blend.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfLinearGradientBrush_set_Blend(self.Ptr, value.Ptr)

    @property

    def InterpolationColors(self)->'PdfColorBlend':
        """
    <summary>
        Gets or sets a ColorBlend that defines a multicolor linear gradient.
    </summary>
        """
        GetDllLibPdf().PdfLinearGradientBrush_get_InterpolationColors.argtypes=[c_void_p]
        GetDllLibPdf().PdfLinearGradientBrush_get_InterpolationColors.restype=c_void_p
        intPtr = GetDllLibPdf().PdfLinearGradientBrush_get_InterpolationColors(self.Ptr)
        ret = None if intPtr==None else PdfColorBlend(intPtr)
        return ret


    @InterpolationColors.setter
    def InterpolationColors(self, value:'PdfColorBlend'):
        GetDllLibPdf().PdfLinearGradientBrush_set_InterpolationColors.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfLinearGradientBrush_set_InterpolationColors(self.Ptr, value.Ptr)

#    @property
#
#    def LinearColors(self)->List['PdfRGBColor']:
#        """
#    <summary>
#        Gets or sets the starting and ending colors of the gradient.
#    </summary>
#        """
#        GetDllLibPdf().PdfLinearGradientBrush_get_LinearColors.argtypes=[c_void_p]
#        GetDllLibPdf().PdfLinearGradientBrush_get_LinearColors.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().PdfLinearGradientBrush_get_LinearColors(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, PdfRGBColor)
#        return ret


#    @LinearColors.setter
#    def LinearColors(self, value:List['PdfRGBColor']):
#        vCount = len(value)
#        ArrayType = c_void_p * vCount
#        vArray = ArrayType()
#        for i in range(0, vCount):
#            vArray[i] = value[i].Ptr
#        GetDllLibPdf().PdfLinearGradientBrush_set_LinearColors.argtypes=[c_void_p, ArrayType, c_int]
#        GetDllLibPdf().PdfLinearGradientBrush_set_LinearColors(self.Ptr, vArray, vCount)


    @property

    def Rectangle(self)->'RectangleF':
        """
    <summary>
        Gets a rectangular region that defines
            the boundaries of the gradient.
    </summary>
        """
        GetDllLibPdf().PdfLinearGradientBrush_get_Rectangle.argtypes=[c_void_p]
        GetDllLibPdf().PdfLinearGradientBrush_get_Rectangle.restype=c_void_p
        intPtr = GetDllLibPdf().PdfLinearGradientBrush_get_Rectangle(self.Ptr)
        ret = None if intPtr==None else RectangleF(intPtr)
        return ret


    @property

    def Extend(self)->'PdfExtend':
        """
    <summary>
        Gets or sets the value indicating whether the gradient
            should extend starting and ending points.
    </summary>
        """
        GetDllLibPdf().PdfLinearGradientBrush_get_Extend.argtypes=[c_void_p]
        GetDllLibPdf().PdfLinearGradientBrush_get_Extend.restype=c_int
        ret = GetDllLibPdf().PdfLinearGradientBrush_get_Extend(self.Ptr)
        objwraped = PdfExtend(ret)
        return objwraped

    @Extend.setter
    def Extend(self, value:'PdfExtend'):
        GetDllLibPdf().PdfLinearGradientBrush_set_Extend.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfLinearGradientBrush_set_Extend(self.Ptr, value.value)


    def Clone(self)->'PdfBrush':
        """
    <summary>
        Creates a new copy of a brush.
    </summary>
    <returns>A new instance of the Brush class.</returns>
        """
        GetDllLibPdf().PdfLinearGradientBrush_Clone.argtypes=[c_void_p]
        GetDllLibPdf().PdfLinearGradientBrush_Clone.restype=c_void_p
        intPtr = GetDllLibPdf().PdfLinearGradientBrush_Clone(self.Ptr)
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


