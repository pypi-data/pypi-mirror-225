from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfSoundAnnotationWidget (  PdfStyledAnnotationWidget) :
    """
    <summary>
        Represents the loaded sound annotation class.
    </summary>
    """
    @property

    def Sound(self)->'PdfSound':
        """
    <summary>
        Gets or sets the sound of the annotation.
    </summary>
        """
        GetDllLibPdf().PdfSoundAnnotationWidget_get_Sound.argtypes=[c_void_p]
        GetDllLibPdf().PdfSoundAnnotationWidget_get_Sound.restype=c_void_p
        intPtr = GetDllLibPdf().PdfSoundAnnotationWidget_get_Sound(self.Ptr)
        ret = None if intPtr==None else PdfSound(intPtr)
        return ret


    @Sound.setter
    def Sound(self, value:'PdfSound'):
        GetDllLibPdf().PdfSoundAnnotationWidget_set_Sound.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfSoundAnnotationWidget_set_Sound(self.Ptr, value.Ptr)

    @property

    def FileName(self)->str:
        """
    <summary>
        Gets the filename of the annotation.
    </summary>
        """
        GetDllLibPdf().PdfSoundAnnotationWidget_get_FileName.argtypes=[c_void_p]
        GetDllLibPdf().PdfSoundAnnotationWidget_get_FileName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfSoundAnnotationWidget_get_FileName(self.Ptr))
        return ret


    @property

    def Icon(self)->'PdfSoundIcon':
        """
    <summary>
        Gets or sets the icon of the annotation.
    </summary>
        """
        GetDllLibPdf().PdfSoundAnnotationWidget_get_Icon.argtypes=[c_void_p]
        GetDllLibPdf().PdfSoundAnnotationWidget_get_Icon.restype=c_int
        ret = GetDllLibPdf().PdfSoundAnnotationWidget_get_Icon(self.Ptr)
        objwraped = PdfSoundIcon(ret)
        return objwraped

    @Icon.setter
    def Icon(self, value:'PdfSoundIcon'):
        GetDllLibPdf().PdfSoundAnnotationWidget_set_Icon.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfSoundAnnotationWidget_set_Icon(self.Ptr, value.value)

    def ObjectID(self)->int:
        """
    <summary>
        Represents the Form field identifier
    </summary>
        """
        GetDllLibPdf().PdfSoundAnnotationWidget_ObjectID.argtypes=[c_void_p]
        GetDllLibPdf().PdfSoundAnnotationWidget_ObjectID.restype=c_int
        ret = GetDllLibPdf().PdfSoundAnnotationWidget_ObjectID(self.Ptr)
        return ret

