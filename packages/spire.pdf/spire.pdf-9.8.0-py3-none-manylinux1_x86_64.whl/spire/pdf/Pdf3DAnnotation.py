from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Pdf3DAnnotation (  PdfFileAnnotation) :
    @dispatch
    def __init__(self, rectangle:RectangleF):
        ptrRec:c_void_p = rectangle.Ptr

        GetDllLibPdf().Pdf3DAnnotation_CreatePdf3DAnnotationR.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DAnnotation_CreatePdf3DAnnotationR.restype = c_void_p
        intPtr = GetDllLibPdf().Pdf3DAnnotation_CreatePdf3DAnnotationR(ptrRec)
        super(Pdf3DAnnotation, self).__init__(intPtr)

    @dispatch
    def __init__(self, rectangle:RectangleF,fileName:str):
        ptrRec:c_void_p = rectangle.Ptr

        GetDllLibPdf().Pdf3DAnnotation_CreatePdf3DAnnotationRF.argtypes=[c_void_p,c_wchar_p]
        GetDllLibPdf().Pdf3DAnnotation_CreatePdf3DAnnotationRF.restype = c_void_p
        intPtr = GetDllLibPdf().Pdf3DAnnotation_CreatePdf3DAnnotationRF(ptrRec,fileName)
        super(Pdf3DAnnotation, self).__init__(intPtr)
    """
    <summary>
        Represents the 3D annotation for a PDF document.
    </summary>
    """
    @property

    def Views(self)->'Pdf3DViewCollection':
        """
    <summary>
        Gets the list of available views for the current 3D artwork.
    </summary>
        """
        GetDllLibPdf().Pdf3DAnnotation_get_Views.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DAnnotation_get_Views.restype=c_void_p
        intPtr = GetDllLibPdf().Pdf3DAnnotation_get_Views(self.Ptr)
        ret = None if intPtr==None else Pdf3DViewCollection(intPtr)
        return ret


    @property
    def DefaultView(self)->int:
        """
    <summary>
        Gets or sets the default view.
    </summary>
<value>The default view.</value>
        """
        GetDllLibPdf().Pdf3DAnnotation_get_DefaultView.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DAnnotation_get_DefaultView.restype=c_int
        ret = GetDllLibPdf().Pdf3DAnnotation_get_DefaultView(self.Ptr)
        return ret

    @DefaultView.setter
    def DefaultView(self, value:int):
        GetDllLibPdf().Pdf3DAnnotation_set_DefaultView.argtypes=[c_void_p, c_int]
        GetDllLibPdf().Pdf3DAnnotation_set_DefaultView(self.Ptr, value)

    @property

    def OnInstantiate(self)->str:
        """
    <summary>
        Gets or sets the code to execute when the 3D artwork is instantiated. 
            <value>Javascript code to be executed when the 3D artwork is instantiated.</value></summary>
        """
        GetDllLibPdf().Pdf3DAnnotation_get_OnInstantiate.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DAnnotation_get_OnInstantiate.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Pdf3DAnnotation_get_OnInstantiate(self.Ptr))
        return ret


    @OnInstantiate.setter
    def OnInstantiate(self, value:str):
        GetDllLibPdf().Pdf3DAnnotation_set_OnInstantiate.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Pdf3DAnnotation_set_OnInstantiate(self.Ptr, value)

    @property

    def Activation(self)->'Pdf3DActivation':
        """
    <summary>
        Gets or sets the activation options for the annotation. 
    </summary>
<remarks>Defines the times at which the annotation should be activated and deactivated and the state of the 3D artwork instance at those times.</remarks>
        """
        GetDllLibPdf().Pdf3DAnnotation_get_Activation.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DAnnotation_get_Activation.restype=c_void_p
        intPtr = GetDllLibPdf().Pdf3DAnnotation_get_Activation(self.Ptr)
        ret = None if intPtr==None else Pdf3DActivation(intPtr)
        return ret


    @Activation.setter
    def Activation(self, value:'Pdf3DActivation'):
        GetDllLibPdf().Pdf3DAnnotation_set_Activation.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().Pdf3DAnnotation_set_Activation(self.Ptr, value.Ptr)

    @property

    def _3DData(self)->Stream:
        """
    <summary>
        Gets a 3d viedo file from Pdf3DAnnotation
    </summary>
        """
        GetDllLibPdf().Pdf3DAnnotation_get__3DData.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DAnnotation_get__3DData.restype=c_void_p
        intPtr = GetDllLibPdf().Pdf3DAnnotation_get__3DData(self.Ptr)
        ret = None if intPtr==None else Stream(intPtr)
        return ret


    @property

    def FileName(self)->str:
        """
<value>Filename with Full path</value>
        """
        GetDllLibPdf().Pdf3DAnnotation_get_FileName.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DAnnotation_get_FileName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Pdf3DAnnotation_get_FileName(self.Ptr))
        return ret


    @FileName.setter
    def FileName(self, value:str):
        GetDllLibPdf().Pdf3DAnnotation_set_FileName.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Pdf3DAnnotation_set_FileName(self.Ptr, value)

