from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfSignatureField (  PdfSignatureAppearanceField) :
    """
    <summary>
        Represents signature field in the PDF Form.
    </summary>
    """
    @property

    def Appearance(self)->'PdfAppearance':
        """

        """
        GetDllLibPdf().PdfSignatureField_get_Appearance.argtypes=[c_void_p]
        GetDllLibPdf().PdfSignatureField_get_Appearance.restype=c_void_p
        intPtr = GetDllLibPdf().PdfSignatureField_get_Appearance(self.Ptr)
        ret = None if intPtr==None else PdfAppearance(intPtr)
        return ret


    @property

    def Signature(self)->'PdfSignature':
        """

        """
        GetDllLibPdf().PdfSignatureField_get_Signature.argtypes=[c_void_p]
        GetDllLibPdf().PdfSignatureField_get_Signature.restype=c_void_p
        intPtr = GetDllLibPdf().PdfSignatureField_get_Signature(self.Ptr)
        ret = None if intPtr==None else PdfSignature(intPtr)
        return ret


    @Signature.setter
    def Signature(self, value:'PdfSignature'):
        GetDllLibPdf().PdfSignatureField_set_Signature.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfSignatureField_set_Signature(self.Ptr, value.Ptr)

    @dispatch

    def DrawImage(self ,image:PdfImage,x:float,y:float):
        """
    <summary>
        Draws an image.
    </summary>
    <param name="image">The image.</param>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
        """
        intPtrimage:c_void_p = image.Ptr

        GetDllLibPdf().PdfSignatureField_DrawImage.argtypes=[c_void_p ,c_void_p,c_float,c_float]
        GetDllLibPdf().PdfSignatureField_DrawImage(self.Ptr, intPtrimage,x,y)

    @dispatch

    def DrawImage(self ,image:PdfImage,rectangle:RectangleF):
        """
    <summary>
        Draws an image.
    </summary>
    <param name="image">The image.</param>
    <param name="rectangle">The rectangle.</param>
        """
        intPtrimage:c_void_p = image.Ptr
        intPtrrectangle:c_void_p = rectangle.Ptr

        GetDllLibPdf().PdfSignatureField_DrawImageIR.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().PdfSignatureField_DrawImageIR(self.Ptr, intPtrimage,intPtrrectangle)

    @dispatch

    def DrawImage(self ,image:PdfImage,point:PointF,size:SizeF):
        """
    <summary>
        Draws an image.
    </summary>
    <param name="image">The image.</param>
    <param name="point">The point.</param>
    <param name="size">The size.</param>
        """
        intPtrimage:c_void_p = image.Ptr
        intPtrpoint:c_void_p = point.Ptr
        intPtrsize:c_void_p = size.Ptr

        GetDllLibPdf().PdfSignatureField_DrawImageIPS.argtypes=[c_void_p ,c_void_p,c_void_p,c_void_p]
        GetDllLibPdf().PdfSignatureField_DrawImageIPS(self.Ptr, intPtrimage,intPtrpoint,intPtrsize)

