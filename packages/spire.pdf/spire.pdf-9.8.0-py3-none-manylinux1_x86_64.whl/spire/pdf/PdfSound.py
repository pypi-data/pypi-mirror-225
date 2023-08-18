from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfSound (SpireObject) :
    """
    <summary>
        Represents sound embedded into pdf document.
    </summary>
    """
    @property
    def Rate(self)->int:
        """
    <summary>
        Gets or sets the sampling rate, in samples per second (in Hz).
    </summary>
        """
        GetDllLibPdf().PdfSound_get_Rate.argtypes=[c_void_p]
        GetDllLibPdf().PdfSound_get_Rate.restype=c_int
        ret = GetDllLibPdf().PdfSound_get_Rate(self.Ptr)
        return ret

    @Rate.setter
    def Rate(self, value:int):
        GetDllLibPdf().PdfSound_set_Rate.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfSound_set_Rate(self.Ptr, value)

    @property
    def Bits(self)->int:
        """
    <summary>
        Gets or sets the number of bits per sample value per channel.
    </summary>
        """
        GetDllLibPdf().PdfSound_get_Bits.argtypes=[c_void_p]
        GetDllLibPdf().PdfSound_get_Bits.restype=c_int
        ret = GetDllLibPdf().PdfSound_get_Bits(self.Ptr)
        return ret

    @Bits.setter
    def Bits(self, value:int):
        GetDllLibPdf().PdfSound_set_Bits.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfSound_set_Bits(self.Ptr, value)

    @property

    def Encoding(self)->'PdfSoundEncoding':
        """
    <summary>
        Gets or sets the encoding format for the sample data.
    </summary>
        """
        GetDllLibPdf().PdfSound_get_Encoding.argtypes=[c_void_p]
        GetDllLibPdf().PdfSound_get_Encoding.restype=c_int
        ret = GetDllLibPdf().PdfSound_get_Encoding(self.Ptr)
        objwraped = PdfSoundEncoding(ret)
        return objwraped

    @Encoding.setter
    def Encoding(self, value:'PdfSoundEncoding'):
        GetDllLibPdf().PdfSound_set_Encoding.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfSound_set_Encoding(self.Ptr, value.value)

    @property

    def Channels(self)->'PdfSoundChannels':
        """
    <summary>
        Gets or sets the number of sound channels.
    </summary>
        """
        GetDllLibPdf().PdfSound_get_Channels.argtypes=[c_void_p]
        GetDllLibPdf().PdfSound_get_Channels.restype=c_int
        ret = GetDllLibPdf().PdfSound_get_Channels(self.Ptr)
        objwraped = PdfSoundChannels(ret)
        return objwraped

    @Channels.setter
    def Channels(self, value:'PdfSoundChannels'):
        GetDllLibPdf().PdfSound_set_Channels.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfSound_set_Channels(self.Ptr, value.value)

    @property

    def FileName(self)->str:
        """
<value>The name of the file.</value>
        """
        GetDllLibPdf().PdfSound_get_FileName.argtypes=[c_void_p]
        GetDllLibPdf().PdfSound_get_FileName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfSound_get_FileName(self.Ptr))
        return ret


    @FileName.setter
    def FileName(self, value:str):
        GetDllLibPdf().PdfSound_set_FileName.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfSound_set_FileName(self.Ptr, value)

