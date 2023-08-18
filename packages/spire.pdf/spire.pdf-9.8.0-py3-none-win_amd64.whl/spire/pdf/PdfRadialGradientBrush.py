from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfRadialGradientBrush (  PdfGradientBrush) :
    @dispatch
    def __init__(self, centreStart:PointF, radiusStart:float,centreEnd:PointF,radiusEnd:float,colorStart:PdfRGBColor,colorEnd:PdfRGBColor):
        ptrcentreStart:c_void_p = centreStart.Ptr
        ptrcentreEnd:c_void_p = centreEnd.Ptr
        ptrcolorStart:c_void_p = colorStart.Ptr
        ptrcolorEnd:c_void_p = colorEnd.Ptr

        GetDllLibPdf().PdfRadialGradientBrush_CreatePdfRadialGradientBrushCRCRCC.argtypes=[c_void_p,c_float,c_void_p,c_float,c_void_p,c_void_p]
        GetDllLibPdf().PdfRadialGradientBrush_CreatePdfRadialGradientBrushCRCRCC.restype = c_void_p
        intPtr = GetDllLibPdf().PdfRadialGradientBrush_CreatePdfRadialGradientBrushCRCRCC(ptrcentreStart,radiusStart,ptrcentreEnd,radiusEnd,ptrcolorStart,ptrcolorEnd)
        super(PdfRadialGradientBrush, self).__init__(intPtr)

    #@dispatch
    #def __init__(self, centreStart:PointF, radiusStart:float,centreEnd:PointF,radiusEnd:float,colorStart:PdfRGBColor,colorEnd:PdfRGBColor):
    #    ptrcentreStart:c_void_p = centreStart.Ptr
    #    ptrcentreEnd:c_void_p = centreEnd.Ptr
    #    ptrcolorStart:c_void_p = colorStart.Ptr
    #    ptrcolorEnd:c_void_p = colorEnd.Ptr

    #    GetDllLibPdf().PdfRadialGradientBrush_CreatePdfRadialGradientBrushCRCRCC.argtypes=[c_void_p,c_float,c_void_p,c_float,c_void_p,c_void_p]
    #    GetDllLibPdf().PdfRadialGradientBrush_CreatePdfRadialGradientBrushCRCRCC.restype = c_void_p
    #    intPtr = GetDllLibPdf().PdfRadialGradientBrush_CreatePdfRadialGradientBrushCRCRCC(ptrcentreStart,radiusStart,ptrcentreEnd,radiusEnd,ptrcolorStart,ptrcolorEnd)
    #    super(PdfRadialGradientBrush, self).__init__(intPtr)
    """
    <summary>
        Represent radial gradient brush.
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
        GetDllLibPdf().PdfRadialGradientBrush_get_Blend.argtypes=[c_void_p]
        GetDllLibPdf().PdfRadialGradientBrush_get_Blend.restype=c_void_p
        intPtr = GetDllLibPdf().PdfRadialGradientBrush_get_Blend(self.Ptr)
        ret = None if intPtr==None else PdfBlend(intPtr)
        return ret


    @Blend.setter
    def Blend(self, value:'PdfBlend'):
        GetDllLibPdf().PdfRadialGradientBrush_set_Blend.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfRadialGradientBrush_set_Blend(self.Ptr, value.Ptr)

    @property

    def InterpolationColors(self)->'PdfColorBlend':
        """
    <summary>
        Gets or sets a ColorBlend that defines a multicolor linear gradient.
    </summary>
        """
        GetDllLibPdf().PdfRadialGradientBrush_get_InterpolationColors.argtypes=[c_void_p]
        GetDllLibPdf().PdfRadialGradientBrush_get_InterpolationColors.restype=c_void_p
        intPtr = GetDllLibPdf().PdfRadialGradientBrush_get_InterpolationColors(self.Ptr)
        ret = None if intPtr==None else PdfColorBlend(intPtr)
        return ret


    @InterpolationColors.setter
    def InterpolationColors(self, value:'PdfColorBlend'):
        GetDllLibPdf().PdfRadialGradientBrush_set_InterpolationColors.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfRadialGradientBrush_set_InterpolationColors(self.Ptr, value.Ptr)

#    @property
#
#    def LinearColors(self)->List['PdfRGBColor']:
#        """
#    <summary>
#        Gets or sets the starting and ending colors of the gradient.
#    </summary>
#        """
#        GetDllLibPdf().PdfRadialGradientBrush_get_LinearColors.argtypes=[c_void_p]
#        GetDllLibPdf().PdfRadialGradientBrush_get_LinearColors.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().PdfRadialGradientBrush_get_LinearColors(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, PdfRGBColor)
#        return ret


#    @LinearColors.setter
#    def LinearColors(self, value:List['PdfRGBColor']):
#        vCount = len(value)
#        ArrayType = c_void_p * vCount
#        vArray = ArrayType()
#        for i in range(0, vCount):
#            vArray[i] = value[i].Ptr
#        GetDllLibPdf().PdfRadialGradientBrush_set_LinearColors.argtypes=[c_void_p, ArrayType, c_int]
#        GetDllLibPdf().PdfRadialGradientBrush_set_LinearColors(self.Ptr, vArray, vCount)


    @property

    def Rectangle(self)->'RectangleF':
        """
    <summary>
        Gets or sets the rectangle.
    </summary>
<value>The rectangle.</value>
        """
        GetDllLibPdf().PdfRadialGradientBrush_get_Rectangle.argtypes=[c_void_p]
        GetDllLibPdf().PdfRadialGradientBrush_get_Rectangle.restype=c_void_p
        intPtr = GetDllLibPdf().PdfRadialGradientBrush_get_Rectangle(self.Ptr)
        ret = None if intPtr==None else RectangleF(intPtr)
        return ret


    @Rectangle.setter
    def Rectangle(self, value:'RectangleF'):
        GetDllLibPdf().PdfRadialGradientBrush_set_Rectangle.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfRadialGradientBrush_set_Rectangle(self.Ptr, value.Ptr)

    @property

    def Extend(self)->'PdfExtend':
        """
    <summary>
        Gets or sets the value indicating whether the gradient
            should extend starting and ending points.
    </summary>
        """
        GetDllLibPdf().PdfRadialGradientBrush_get_Extend.argtypes=[c_void_p]
        GetDllLibPdf().PdfRadialGradientBrush_get_Extend.restype=c_int
        ret = GetDllLibPdf().PdfRadialGradientBrush_get_Extend(self.Ptr)
        objwraped = PdfExtend(ret)
        return objwraped

    @Extend.setter
    def Extend(self, value:'PdfExtend'):
        GetDllLibPdf().PdfRadialGradientBrush_set_Extend.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfRadialGradientBrush_set_Extend(self.Ptr, value.value)


    def Clone(self)->'PdfBrush':
        """
    <summary>
        Creates a new copy of a brush.
    </summary>
    <returns>A new instance of the Brush class.</returns>
        """
        GetDllLibPdf().PdfRadialGradientBrush_Clone.argtypes=[c_void_p]
        GetDllLibPdf().PdfRadialGradientBrush_Clone.restype=c_void_p
        intPtr = GetDllLibPdf().PdfRadialGradientBrush_Clone(self.Ptr)
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


