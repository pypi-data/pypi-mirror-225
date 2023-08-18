from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Pdf3DProjection (SpireObject) :
    """
    <summary>
         Represents the mapping of 3D camera co-ordinates onto the target coordinate system of the annotation.
    </summary>
    """
    @property

    def ProjectionType(self)->'Pdf3DProjectionType':
        """
    <summary>
        Gets or sets the type of the projection.
    </summary>
        """
        GetDllLibPdf().Pdf3DProjection_get_ProjectionType.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DProjection_get_ProjectionType.restype=c_int
        ret = GetDllLibPdf().Pdf3DProjection_get_ProjectionType(self.Ptr)
        objwraped = Pdf3DProjectionType(ret)
        return objwraped

    @ProjectionType.setter
    def ProjectionType(self, value:'Pdf3DProjectionType'):
        GetDllLibPdf().Pdf3DProjection_set_ProjectionType.argtypes=[c_void_p, c_int]
        GetDllLibPdf().Pdf3DProjection_set_ProjectionType(self.Ptr, value.value)

    @property

    def ClipStyle(self)->'Pdf3DProjectionClipStyle':
        """
    <summary>
        Gets or sets the projection ClipStyle.
    </summary>
        """
        GetDllLibPdf().Pdf3DProjection_get_ClipStyle.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DProjection_get_ClipStyle.restype=c_int
        ret = GetDllLibPdf().Pdf3DProjection_get_ClipStyle(self.Ptr)
        objwraped = Pdf3DProjectionClipStyle(ret)
        return objwraped

    @ClipStyle.setter
    def ClipStyle(self, value:'Pdf3DProjectionClipStyle'):
        GetDllLibPdf().Pdf3DProjection_set_ClipStyle.argtypes=[c_void_p, c_int]
        GetDllLibPdf().Pdf3DProjection_set_ClipStyle(self.Ptr, value.value)

    @property

    def OrthoScaleMode(self)->'Pdf3DProjectionOrthoScaleMode':
        """
    <summary>
         Gets or sets the scale mode for ortho graphic projections.
    </summary>
        """
        GetDllLibPdf().Pdf3DProjection_get_OrthoScaleMode.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DProjection_get_OrthoScaleMode.restype=c_int
        ret = GetDllLibPdf().Pdf3DProjection_get_OrthoScaleMode(self.Ptr)
        objwraped = Pdf3DProjectionOrthoScaleMode(ret)
        return objwraped

    @OrthoScaleMode.setter
    def OrthoScaleMode(self, value:'Pdf3DProjectionOrthoScaleMode'):
        GetDllLibPdf().Pdf3DProjection_set_OrthoScaleMode.argtypes=[c_void_p, c_int]
        GetDllLibPdf().Pdf3DProjection_set_OrthoScaleMode(self.Ptr, value.value)

    @property
    def FarClipDistance(self)->float:
        """
    <summary>
        Gets or sets the far clipping distance.
    </summary>
        """
        GetDllLibPdf().Pdf3DProjection_get_FarClipDistance.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DProjection_get_FarClipDistance.restype=c_float
        ret = GetDllLibPdf().Pdf3DProjection_get_FarClipDistance(self.Ptr)
        return ret

    @FarClipDistance.setter
    def FarClipDistance(self, value:float):
        GetDllLibPdf().Pdf3DProjection_set_FarClipDistance.argtypes=[c_void_p, c_float]
        GetDllLibPdf().Pdf3DProjection_set_FarClipDistance(self.Ptr, value)

    @property
    def FieldOfView(self)->float:
        """
    <summary>
        Gets or sets the field of view.
    </summary>
        """
        GetDllLibPdf().Pdf3DProjection_get_FieldOfView.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DProjection_get_FieldOfView.restype=c_float
        ret = GetDllLibPdf().Pdf3DProjection_get_FieldOfView(self.Ptr)
        return ret

    @FieldOfView.setter
    def FieldOfView(self, value:float):
        GetDllLibPdf().Pdf3DProjection_set_FieldOfView.argtypes=[c_void_p, c_float]
        GetDllLibPdf().Pdf3DProjection_set_FieldOfView(self.Ptr, value)

    @property
    def NearClipDistance(self)->float:
        """
    <summary>
        Gets or sets the near clipping distance.
    </summary>
        """
        GetDllLibPdf().Pdf3DProjection_get_NearClipDistance.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DProjection_get_NearClipDistance.restype=c_float
        ret = GetDllLibPdf().Pdf3DProjection_get_NearClipDistance(self.Ptr)
        return ret

    @NearClipDistance.setter
    def NearClipDistance(self, value:float):
        GetDllLibPdf().Pdf3DProjection_set_NearClipDistance.argtypes=[c_void_p, c_float]
        GetDllLibPdf().Pdf3DProjection_set_NearClipDistance(self.Ptr, value)

    @property
    def Scaling(self)->float:
        """
    <summary>
        Gets or sets the projection scaling.
    </summary>
        """
        GetDllLibPdf().Pdf3DProjection_get_Scaling.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DProjection_get_Scaling.restype=c_float
        ret = GetDllLibPdf().Pdf3DProjection_get_Scaling(self.Ptr)
        return ret

    @Scaling.setter
    def Scaling(self, value:float):
        GetDllLibPdf().Pdf3DProjection_set_Scaling.argtypes=[c_void_p, c_float]
        GetDllLibPdf().Pdf3DProjection_set_Scaling(self.Ptr, value)

