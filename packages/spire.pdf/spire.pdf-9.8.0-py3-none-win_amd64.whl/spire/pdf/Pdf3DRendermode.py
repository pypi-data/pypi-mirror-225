from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Pdf3DRendermode (SpireObject) :
    @dispatch
    def __init__(self):
        GetDllLibPdf().Pdf3DRendermode_CreatePdf3DRendermode.restype = c_void_p
        intPtr = GetDllLibPdf().Pdf3DRendermode_CreatePdf3DRendermode()
        super(Pdf3DRendermode, self).__init__(intPtr)
    @dispatch
    def __init__(self, style:Pdf3DRenderStyle):
        enumStyle:c_int = style.value
        GetDllLibPdf().Pdf3DRendermode_CreatePdf3DRendermodeS.argtypes=[c_int]
        GetDllLibPdf().Pdf3DRendermode_CreatePdf3DRendermodeS.restype = c_void_p
        intPtr = GetDllLibPdf().Pdf3DRendermode_CreatePdf3DRendermodeS(enumStyle)
        super(Pdf3DRendermode, self).__init__(intPtr)
    """
    <summary>
        Represents the rendering mode of the 3D artwork. 
    </summary>
    """
    @property

    def Style(self)->'Pdf3DRenderStyle':
        """
    <summary>
        Gets or sets the type of the projection.
    </summary>
        """
        GetDllLibPdf().Pdf3DRendermode_get_Style.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DRendermode_get_Style.restype=c_int
        ret = GetDllLibPdf().Pdf3DRendermode_get_Style(self.Ptr)
        objwraped = Pdf3DRenderStyle(ret)
        return objwraped

    @Style.setter
    def Style(self, value:'Pdf3DRenderStyle'):
        GetDllLibPdf().Pdf3DRendermode_set_Style.argtypes=[c_void_p, c_int]
        GetDllLibPdf().Pdf3DRendermode_set_Style(self.Ptr, value.value)

    @property

    def AuxilaryColor(self)->'PdfRGBColor':
        """
    <summary>
        Gets or sets the Auxiliary color.
    </summary>
        """
        GetDllLibPdf().Pdf3DRendermode_get_AuxilaryColor.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DRendermode_get_AuxilaryColor.restype=c_void_p
        intPtr = GetDllLibPdf().Pdf3DRendermode_get_AuxilaryColor(self.Ptr)
        ret = None if intPtr==None else PdfRGBColor(intPtr)
        return ret


    @AuxilaryColor.setter
    def AuxilaryColor(self, value:'PdfRGBColor'):
        GetDllLibPdf().Pdf3DRendermode_set_AuxilaryColor.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().Pdf3DRendermode_set_AuxilaryColor(self.Ptr, value.Ptr)

    @property

    def FaceColor(self)->'PdfRGBColor':
        """
    <summary>
        Gets or sets the Face color.
    </summary>
        """
        GetDllLibPdf().Pdf3DRendermode_get_FaceColor.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DRendermode_get_FaceColor.restype=c_void_p
        intPtr = GetDllLibPdf().Pdf3DRendermode_get_FaceColor(self.Ptr)
        ret = None if intPtr==None else PdfRGBColor(intPtr)
        return ret


    @FaceColor.setter
    def FaceColor(self, value:'PdfRGBColor'):
        GetDllLibPdf().Pdf3DRendermode_set_FaceColor.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().Pdf3DRendermode_set_FaceColor(self.Ptr, value.Ptr)

    @property
    def CreaseValue(self)->float:
        """
    <summary>
        Gets or sets the crease value. 
            <remarks>The crease value is specified in degrees, from 0 to 360.</remarks></summary>
        """
        GetDllLibPdf().Pdf3DRendermode_get_CreaseValue.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DRendermode_get_CreaseValue.restype=c_float
        ret = GetDllLibPdf().Pdf3DRendermode_get_CreaseValue(self.Ptr)
        return ret

    @CreaseValue.setter
    def CreaseValue(self, value:float):
        GetDllLibPdf().Pdf3DRendermode_set_CreaseValue.argtypes=[c_void_p, c_float]
        GetDllLibPdf().Pdf3DRendermode_set_CreaseValue(self.Ptr, value)

    @property
    def Opacity(self)->float:
        """
    <summary>
        Gets or sets the rendering opacity. 
    </summary>
<remarks>The opacity is given in percents, 100 is full opacity, 0 is no opacity.</remarks>
        """
        GetDllLibPdf().Pdf3DRendermode_get_Opacity.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DRendermode_get_Opacity.restype=c_float
        ret = GetDllLibPdf().Pdf3DRendermode_get_Opacity(self.Ptr)
        return ret

    @Opacity.setter
    def Opacity(self, value:float):
        GetDllLibPdf().Pdf3DRendermode_set_Opacity.argtypes=[c_void_p, c_float]
        GetDllLibPdf().Pdf3DRendermode_set_Opacity(self.Ptr, value)

