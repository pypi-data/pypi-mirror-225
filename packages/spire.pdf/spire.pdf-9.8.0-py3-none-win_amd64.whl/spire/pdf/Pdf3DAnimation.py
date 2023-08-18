from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Pdf3DAnimation (SpireObject) :
    """
    <summary>
        Represents the lighting to apply for the 3D artwork.
    </summary>
    """
    @property

    def Type(self)->'PDF3DAnimationType':
        """
    <summary>
        Gets or sets the type of the animation.
    </summary>
        """
        GetDllLibPdf().Pdf3DAnimation_get_Type.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DAnimation_get_Type.restype=c_int
        ret = GetDllLibPdf().Pdf3DAnimation_get_Type(self.Ptr)
        objwraped = PDF3DAnimationType(ret)
        return objwraped

    @Type.setter
    def Type(self, value:'PDF3DAnimationType'):
        GetDllLibPdf().Pdf3DAnimation_set_Type.argtypes=[c_void_p, c_int]
        GetDllLibPdf().Pdf3DAnimation_set_Type(self.Ptr, value.value)

    @property
    def PlayCount(self)->int:
        """
    <summary>
        Gets or sets the play count. 
    </summary>
        """
        GetDllLibPdf().Pdf3DAnimation_get_PlayCount.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DAnimation_get_PlayCount.restype=c_int
        ret = GetDllLibPdf().Pdf3DAnimation_get_PlayCount(self.Ptr)
        return ret

    @PlayCount.setter
    def PlayCount(self, value:int):
        GetDllLibPdf().Pdf3DAnimation_set_PlayCount.argtypes=[c_void_p, c_int]
        GetDllLibPdf().Pdf3DAnimation_set_PlayCount(self.Ptr, value)

    @property
    def TimeMultiplier(self)->float:
        """
    <summary>
        Gets or sets the rendering opacity.
            <remarks>A positive number specifying the time multiplier to be used when running the animation. A value greater than one shortens the time it takes to play the animation, or effectively speeds up the animation.</remarks></summary>
        """
        GetDllLibPdf().Pdf3DAnimation_get_TimeMultiplier.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DAnimation_get_TimeMultiplier.restype=c_float
        ret = GetDllLibPdf().Pdf3DAnimation_get_TimeMultiplier(self.Ptr)
        return ret

    @TimeMultiplier.setter
    def TimeMultiplier(self, value:float):
        GetDllLibPdf().Pdf3DAnimation_set_TimeMultiplier.argtypes=[c_void_p, c_float]
        GetDllLibPdf().Pdf3DAnimation_set_TimeMultiplier(self.Ptr, value)

