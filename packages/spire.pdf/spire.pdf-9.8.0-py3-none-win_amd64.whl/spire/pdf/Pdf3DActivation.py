from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Pdf3DActivation (SpireObject) :
    @dispatch
    def __init__(self):
        GetDllLibPdf().Pdf3DActivation_CreatePdf3DActivation.restype = c_void_p
        intPtr = GetDllLibPdf().Pdf3DActivation_CreatePdf3DActivation()
        super(Pdf3DActivation, self).__init__(intPtr)
    """
    <summary>
        Represents the activation states for the 3D annotation. 
    </summary>
    """
    @property

    def ActivationMode(self)->'Pdf3DActivationMode':
        """
    <summary>
        Gets or sets the activation mode for the annotation.
    </summary>
        """
        GetDllLibPdf().Pdf3DActivation_get_ActivationMode.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DActivation_get_ActivationMode.restype=c_int
        ret = GetDllLibPdf().Pdf3DActivation_get_ActivationMode(self.Ptr)
        objwraped = Pdf3DActivationMode(ret)
        return objwraped

    @ActivationMode.setter
    def ActivationMode(self, value:'Pdf3DActivationMode'):
        GetDllLibPdf().Pdf3DActivation_set_ActivationMode.argtypes=[c_void_p, c_int]
        GetDllLibPdf().Pdf3DActivation_set_ActivationMode(self.Ptr, value.value)

    @property

    def DeactivationMode(self)->'Pdf3DDeactivationMode':
        """
    <summary>
        Gets or sets the deactivation mode for the annotation.
    </summary>
        """
        GetDllLibPdf().Pdf3DActivation_get_DeactivationMode.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DActivation_get_DeactivationMode.restype=c_int
        ret = GetDllLibPdf().Pdf3DActivation_get_DeactivationMode(self.Ptr)
        objwraped = Pdf3DDeactivationMode(ret)
        return objwraped

    @DeactivationMode.setter
    def DeactivationMode(self, value:'Pdf3DDeactivationMode'):
        GetDllLibPdf().Pdf3DActivation_set_DeactivationMode.argtypes=[c_void_p, c_int]
        GetDllLibPdf().Pdf3DActivation_set_DeactivationMode(self.Ptr, value.value)

    @property

    def ActivationState(self)->'Pdf3DActivationState':
        """
    <summary>
        Gets or sets the activation state for the annotation.
    </summary>
        """
        GetDllLibPdf().Pdf3DActivation_get_ActivationState.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DActivation_get_ActivationState.restype=c_int
        ret = GetDllLibPdf().Pdf3DActivation_get_ActivationState(self.Ptr)
        objwraped = Pdf3DActivationState(ret)
        return objwraped

    @ActivationState.setter
    def ActivationState(self, value:'Pdf3DActivationState'):
        GetDllLibPdf().Pdf3DActivation_set_ActivationState.argtypes=[c_void_p, c_int]
        GetDllLibPdf().Pdf3DActivation_set_ActivationState(self.Ptr, value.value)

    @property

    def DeactivationState(self)->'Pdf3DDeactivationState':
        """
    <summary>
        Gets or sets the deactivation state for the annotation.
    </summary>
        """
        GetDllLibPdf().Pdf3DActivation_get_DeactivationState.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DActivation_get_DeactivationState.restype=c_int
        ret = GetDllLibPdf().Pdf3DActivation_get_DeactivationState(self.Ptr)
        objwraped = Pdf3DDeactivationState(ret)
        return objwraped

    @DeactivationState.setter
    def DeactivationState(self, value:'Pdf3DDeactivationState'):
        GetDllLibPdf().Pdf3DActivation_set_DeactivationState.argtypes=[c_void_p, c_int]
        GetDllLibPdf().Pdf3DActivation_set_DeactivationState(self.Ptr, value.value)

    @property
    def ShowToolbar(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether the toolbar should be displayed when the annotation is activated or not. 
    </summary>
<value>If true, a toolbar should be displayed by default when the annotation is activated and given focus. If false, a toolbar should not be displayed by default. </value>
        """
        GetDllLibPdf().Pdf3DActivation_get_ShowToolbar.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DActivation_get_ShowToolbar.restype=c_bool
        ret = GetDllLibPdf().Pdf3DActivation_get_ShowToolbar(self.Ptr)
        return ret

    @ShowToolbar.setter
    def ShowToolbar(self, value:bool):
        GetDllLibPdf().Pdf3DActivation_set_ShowToolbar.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().Pdf3DActivation_set_ShowToolbar(self.Ptr, value)

    @property
    def ShowUI(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether the UI for managing the 3D artwork should be displayed when the annotation is activated. 
    </summary>
<value>If true, the user interface should be made visible when the annotation is activated. If false, the user interface should not be made visible by default.</value>
        """
        GetDllLibPdf().Pdf3DActivation_get_ShowUI.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DActivation_get_ShowUI.restype=c_bool
        ret = GetDllLibPdf().Pdf3DActivation_get_ShowUI(self.Ptr)
        return ret

    @ShowUI.setter
    def ShowUI(self, value:bool):
        GetDllLibPdf().Pdf3DActivation_set_ShowUI.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().Pdf3DActivation_set_ShowUI(self.Ptr, value)

