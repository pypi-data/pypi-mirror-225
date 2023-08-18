from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Pdf3DNode (SpireObject) :
    """
    <summary>
        Represents the particular areas of 3D artwork and the opacity and visibility with which individual nodes are displayed.  
    </summary>
    """
    @property
    def Visible(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether the node is visible or not. 
    </summary>
<value>True if the node is visible. </value>
        """
        GetDllLibPdf().Pdf3DNode_get_Visible.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DNode_get_Visible.restype=c_bool
        ret = GetDllLibPdf().Pdf3DNode_get_Visible(self.Ptr)
        return ret

    @Visible.setter
    def Visible(self, value:bool):
        GetDllLibPdf().Pdf3DNode_set_Visible.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().Pdf3DNode_set_Visible(self.Ptr, value)

    @property

    def Name(self)->str:
        """
    <summary>
        Gets or sets the node name. 
    </summary>
<value>The name of the 3D node.</value>
        """
        GetDllLibPdf().Pdf3DNode_get_Name.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DNode_get_Name.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Pdf3DNode_get_Name(self.Ptr))
        return ret


    @Name.setter
    def Name(self, value:str):
        GetDllLibPdf().Pdf3DNode_set_Name.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Pdf3DNode_set_Name(self.Ptr, value)

    @property
    def Opacity(self)->float:
        """
    <summary>
        Gets or sets the cutting plane opacity. 
    </summary>
<value>A number indicating the opacity of the cutting plane using a standard additive blend mode. </value>
<remarks>The opacity is given in percents, 100 is full opacity, 0 is no opacity.</remarks>
        """
        GetDllLibPdf().Pdf3DNode_get_Opacity.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DNode_get_Opacity.restype=c_float
        ret = GetDllLibPdf().Pdf3DNode_get_Opacity(self.Ptr)
        return ret

    @Opacity.setter
    def Opacity(self, value:float):
        GetDllLibPdf().Pdf3DNode_set_Opacity.argtypes=[c_void_p, c_float]
        GetDllLibPdf().Pdf3DNode_set_Opacity(self.Ptr, value)

    @property

    def Matrix(self)->List[float]:
        """
    <summary>
        Gets or sets the 3D transformation matrix. 
    </summary>
<value>A 12-element 3D transformation matrix that specifies the position and orientation of this node, relative to its parent, in world coordinates. </value>
<remarks>If the array has more than 12 elements, only the first 12 will be considered.</remarks>
        """
        GetDllLibPdf().Pdf3DNode_get_Matrix.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DNode_get_Matrix.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().Pdf3DNode_get_Matrix(self.Ptr)
        ret = GetVectorFromArray(intPtrArray, c_float)
        return ret

    @Matrix.setter
    def Matrix(self, value:List[float]):
        vCount = len(value)
        ArrayType = c_float * vCount
        vArray = ArrayType()
        for i in range(0, vCount):
            vArray[i] = value[i]
        GetDllLibPdf().Pdf3DNode_set_Matrix.argtypes=[c_void_p, ArrayType, c_int]
        GetDllLibPdf().Pdf3DNode_set_Matrix(self.Ptr, vArray, vCount)

