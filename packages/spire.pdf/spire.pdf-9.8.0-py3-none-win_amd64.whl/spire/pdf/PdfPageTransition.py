from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfPageTransition (SpireObject) :
    """
    <summary>
        Represents parameters how to display the page in the presentation mode.
    </summary>
    """
    @property

    def Style(self)->'PdfTransitionStyle':
        """
    <summary>
        Gets or sets the transition style to use when moving to this page from another 
            during a presentation.
    </summary>
<value>The style.</value>
        """
        GetDllLibPdf().PdfPageTransition_get_Style.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageTransition_get_Style.restype=c_int
        ret = GetDllLibPdf().PdfPageTransition_get_Style(self.Ptr)
        objwraped = PdfTransitionStyle(ret)
        return objwraped

    @Style.setter
    def Style(self, value:'PdfTransitionStyle'):
        GetDllLibPdf().PdfPageTransition_set_Style.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfPageTransition_set_Style(self.Ptr, value.value)

    @property
    def Duration(self)->float:
        """
    <summary>
        Gets or sets the duration of the transition effect, in seconds.
    </summary>
<value>The transition duration.</value>
        """
        GetDllLibPdf().PdfPageTransition_get_Duration.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageTransition_get_Duration.restype=c_float
        ret = GetDllLibPdf().PdfPageTransition_get_Duration(self.Ptr)
        return ret

    @Duration.setter
    def Duration(self, value:float):
        GetDllLibPdf().PdfPageTransition_set_Duration.argtypes=[c_void_p, c_float]
        GetDllLibPdf().PdfPageTransition_set_Duration(self.Ptr, value)

    @property

    def Dimension(self)->'PdfTransitionDimension':
        """
    <summary>
        Gets or sets the dimension in which the specified transition effect occurs.
    </summary>
<value>The dimension.</value>
        """
        GetDllLibPdf().PdfPageTransition_get_Dimension.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageTransition_get_Dimension.restype=c_int
        ret = GetDllLibPdf().PdfPageTransition_get_Dimension(self.Ptr)
        objwraped = PdfTransitionDimension(ret)
        return objwraped

    @Dimension.setter
    def Dimension(self, value:'PdfTransitionDimension'):
        GetDllLibPdf().PdfPageTransition_set_Dimension.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfPageTransition_set_Dimension(self.Ptr, value.value)

    @property

    def Motion(self)->'PdfTransitionMotion':
        """
    <summary>
        Gets or sets the the direction of motion for the specified transition effect.
    </summary>
<value>The motion.</value>
        """
        GetDllLibPdf().PdfPageTransition_get_Motion.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageTransition_get_Motion.restype=c_int
        ret = GetDllLibPdf().PdfPageTransition_get_Motion(self.Ptr)
        objwraped = PdfTransitionMotion(ret)
        return objwraped

    @Motion.setter
    def Motion(self, value:'PdfTransitionMotion'):
        GetDllLibPdf().PdfPageTransition_set_Motion.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfPageTransition_set_Motion(self.Ptr, value.value)

    @property

    def Direction(self)->'PdfTransitionDirection':
        """
    <summary>
        The direction in which the specified transition effect moves, expressed in degrees counter 
            clockwise starting from a left-to-right direction. (This differs from the page objects 
            Rotate property, which is measured clockwise from the top.)
    </summary>
        """
        GetDllLibPdf().PdfPageTransition_get_Direction.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageTransition_get_Direction.restype=c_int
        ret = GetDllLibPdf().PdfPageTransition_get_Direction(self.Ptr)
        objwraped = PdfTransitionDirection(ret)
        return objwraped

    @Direction.setter
    def Direction(self, value:'PdfTransitionDirection'):
        GetDllLibPdf().PdfPageTransition_set_Direction.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfPageTransition_set_Direction(self.Ptr, value.value)

    @property
    def Scale(self)->float:
        """
    <summary>
        Gets or sets the starting or ending scale at which the changes are drawn. 
            If Motion property specifies an inward transition, the scale of the changes drawn progresses 
            from Scale to 1.0 over the course of the transition. If Motion specifies an outward 
            transition, the scale of the changes drawn progresses from 1.0 to Scale over the course 
            of the transition.
    </summary>
<remarks>
            This property has effect for Fly transition style only.
            </remarks>
<value>The scale.</value>
        """
        GetDllLibPdf().PdfPageTransition_get_Scale.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageTransition_get_Scale.restype=c_float
        ret = GetDllLibPdf().PdfPageTransition_get_Scale(self.Ptr)
        return ret

    @Scale.setter
    def Scale(self, value:float):
        GetDllLibPdf().PdfPageTransition_set_Scale.argtypes=[c_void_p, c_float]
        GetDllLibPdf().PdfPageTransition_set_Scale(self.Ptr, value)

    @property
    def PageDuration(self)->float:
        """
    <summary>
        Gets or sets The pages display duration (also called its advance timing): the maximum 
            length of time, in seconds, that the page is displayed during presentations before 
            the viewer application automatically advances to the next page. By default, 
            the viewer does not advance automatically.
    </summary>
<value>The page duration.</value>
        """
        GetDllLibPdf().PdfPageTransition_get_PageDuration.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageTransition_get_PageDuration.restype=c_float
        ret = GetDllLibPdf().PdfPageTransition_get_PageDuration(self.Ptr)
        return ret

    @PageDuration.setter
    def PageDuration(self, value:float):
        GetDllLibPdf().PdfPageTransition_set_PageDuration.argtypes=[c_void_p, c_float]
        GetDllLibPdf().PdfPageTransition_set_PageDuration(self.Ptr, value)


    def Clone(self)->'SpireObject':
        """
    <summary>
        Creates a new object that is a copy of the current instance.
    </summary>
    <returns>
            A new object that is a copy of this instance.
            </returns>
        """
        GetDllLibPdf().PdfPageTransition_Clone.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageTransition_Clone.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageTransition_Clone(self.Ptr)
        ret = None if intPtr==None else SpireObject(intPtr)
        return ret


