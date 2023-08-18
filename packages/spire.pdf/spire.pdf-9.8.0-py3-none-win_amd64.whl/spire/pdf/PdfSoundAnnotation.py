from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfSoundAnnotation (  PdfFileAnnotation) :
    """
    <summary>
        Represents the sound annotation.
    </summary>
    """
    @property

    def Icon(self)->'PdfSoundIcon':
        """
    <summary>
        Gets or sets the icon to be used in displaying the annotation.
    </summary>
<value>The  enumeration member specifying the icon for the annotation.</value>
        """
        GetDllLibPdf().PdfSoundAnnotation_get_Icon.argtypes=[c_void_p]
        GetDllLibPdf().PdfSoundAnnotation_get_Icon.restype=c_int
        ret = GetDllLibPdf().PdfSoundAnnotation_get_Icon(self.Ptr)
        objwraped = PdfSoundIcon(ret)
        return objwraped

    @Icon.setter
    def Icon(self, value:'PdfSoundIcon'):
        GetDllLibPdf().PdfSoundAnnotation_set_Icon.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfSoundAnnotation_set_Icon(self.Ptr, value.value)

    @property

    def Sound(self)->'PdfSound':
        """
    <summary>
        Gets or sets the sound.
    </summary>
<value>The  object specified a sound for the annotation.</value>
        """
        GetDllLibPdf().PdfSoundAnnotation_get_Sound.argtypes=[c_void_p]
        GetDllLibPdf().PdfSoundAnnotation_get_Sound.restype=c_void_p
        intPtr = GetDllLibPdf().PdfSoundAnnotation_get_Sound(self.Ptr)
        ret = None if intPtr==None else PdfSound(intPtr)
        return ret


    @Sound.setter
    def Sound(self, value:'PdfSound'):
        GetDllLibPdf().PdfSoundAnnotation_set_Sound.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfSoundAnnotation_set_Sound(self.Ptr, value.Ptr)

    @property

    def FileName(self)->str:
        """
<value>The string specifies the file name of the sound annotation.</value>
        """
        GetDllLibPdf().PdfSoundAnnotation_get_FileName.argtypes=[c_void_p]
        GetDllLibPdf().PdfSoundAnnotation_get_FileName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfSoundAnnotation_get_FileName(self.Ptr))
        return ret


    @FileName.setter
    def FileName(self, value:str):
        GetDllLibPdf().PdfSoundAnnotation_set_FileName.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfSoundAnnotation_set_FileName(self.Ptr, value)

