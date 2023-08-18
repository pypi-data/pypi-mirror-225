from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfSoundAction (  PdfAction) :
    @dispatch
    def __init__(self, fileName:str):
        GetDllLibPdf().PdfSoundAction_CreatePdfSoundActionF.argtypes=[c_wchar_p]
        GetDllLibPdf().PdfSoundAction_CreatePdfSoundActionF.restype = c_void_p
        intPtr = GetDllLibPdf().PdfSoundAction_CreatePdfSoundActionF(fileName)
        super(PdfSoundAction, self).__init__(intPtr)
    """
    <summary>
        Represents the sound action.
    </summary>
    """
    @property
    def Volume(self)->float:
        """
    <summary>
        Gets or sets the volume at which to play the sound, in the range -1.0 to 1.0.
    </summary>
<value>The volume of the sound.</value>
        """
        GetDllLibPdf().PdfSoundAction_get_Volume.argtypes=[c_void_p]
        GetDllLibPdf().PdfSoundAction_get_Volume.restype=c_float
        ret = GetDllLibPdf().PdfSoundAction_get_Volume(self.Ptr)
        return ret

    @Volume.setter
    def Volume(self, value:float):
        GetDllLibPdf().PdfSoundAction_set_Volume.argtypes=[c_void_p, c_float]
        GetDllLibPdf().PdfSoundAction_set_Volume(self.Ptr, value)

    @property

    def FileName(self)->str:
        """
<value>The name of the sound file.</value>
        """
        GetDllLibPdf().PdfSoundAction_get_FileName.argtypes=[c_void_p]
        GetDllLibPdf().PdfSoundAction_get_FileName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfSoundAction_get_FileName(self.Ptr))
        return ret


    @FileName.setter
    def FileName(self, value:str):
        GetDllLibPdf().PdfSoundAction_set_FileName.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfSoundAction_set_FileName(self.Ptr, value)

    @property

    def Sound(self)->'PdfSound':
        """
    <summary>
        Gets or sets the sound.
    </summary>
<value> represents the sound.</value>
        """
        GetDllLibPdf().PdfSoundAction_get_Sound.argtypes=[c_void_p]
        GetDllLibPdf().PdfSoundAction_get_Sound.restype=c_void_p
        intPtr = GetDllLibPdf().PdfSoundAction_get_Sound(self.Ptr)
        ret = None if intPtr==None else PdfSound(intPtr)
        return ret


    @Sound.setter
    def Sound(self, value:'PdfSound'):
        GetDllLibPdf().PdfSoundAction_set_Sound.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfSoundAction_set_Sound(self.Ptr, value.Ptr)

    @property
    def Synchronous(self)->bool:
        """
    <summary>
        Gets or sets a value whether to play the sound synchronously or asynchronously.
            If this flag is true, the viewer application retains control, allowing no further 
            user interaction other than canceling the sound, until the sound has been 
            completely played. Default value: false.
    </summary>
<value>
  <c>true</c> if synchronous; otherwise, <c>false</c>.</value>
        """
        GetDllLibPdf().PdfSoundAction_get_Synchronous.argtypes=[c_void_p]
        GetDllLibPdf().PdfSoundAction_get_Synchronous.restype=c_bool
        ret = GetDllLibPdf().PdfSoundAction_get_Synchronous(self.Ptr)
        return ret

    @Synchronous.setter
    def Synchronous(self, value:bool):
        GetDllLibPdf().PdfSoundAction_set_Synchronous.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfSoundAction_set_Synchronous(self.Ptr, value)

    @property
    def Repeat(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether to repeat the sound indefinitely. 
            If this entry is present, the  property is ignored. Default value: false.
    </summary>
<value>
  <c>true</c> if repeat; otherwise, <c>false</c>.</value>
        """
        GetDllLibPdf().PdfSoundAction_get_Repeat.argtypes=[c_void_p]
        GetDllLibPdf().PdfSoundAction_get_Repeat.restype=c_bool
        ret = GetDllLibPdf().PdfSoundAction_get_Repeat(self.Ptr)
        return ret

    @Repeat.setter
    def Repeat(self, value:bool):
        GetDllLibPdf().PdfSoundAction_set_Repeat.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfSoundAction_set_Repeat(self.Ptr, value)

    @property
    def Mix(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether to mix this sound with any other 
            sound already playing. If this flag is false, any previously playing sound is 
            stopped before starting this sound; this can be used to stop a repeating 
            sound. Default value: false.
    </summary>
<value>
  <c>true</c> if mix; otherwise, <c>false</c>.</value>
        """
        GetDllLibPdf().PdfSoundAction_get_Mix.argtypes=[c_void_p]
        GetDllLibPdf().PdfSoundAction_get_Mix.restype=c_bool
        ret = GetDllLibPdf().PdfSoundAction_get_Mix(self.Ptr)
        return ret

    @Mix.setter
    def Mix(self, value:bool):
        GetDllLibPdf().PdfSoundAction_set_Mix.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfSoundAction_set_Mix(self.Ptr, value)

