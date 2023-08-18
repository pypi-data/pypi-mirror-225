from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class LineInfo (SpireObject) :
    """
    <summary>
        Contains information about the line.
    </summary>
    """
    @property

    def LineType(self)->'LineType':
        """
    <summary>
        Gets width of the line text.
    </summary>
        """
        GetDllLibPdf().LineInfo_get_LineType.argtypes=[c_void_p]
        GetDllLibPdf().LineInfo_get_LineType.restype=c_int
        ret = GetDllLibPdf().LineInfo_get_LineType(self.Ptr)
        objwraped = LineType(ret)
        return objwraped

    @property
    def intLineType(self)->int:
        """
    <summary>
        Gets width of the line text.
    </summary>
        """
        GetDllLibPdf().LineInfo_get_LineType.argtypes=[c_void_p]
        GetDllLibPdf().LineInfo_get_LineType.restype=c_int
        ret = GetDllLibPdf().LineInfo_get_LineType(self.Ptr)
        return ret

    @property

    def Text(self)->str:
        """
    <summary>
        Gets line text.
    </summary>
        """
        GetDllLibPdf().LineInfo_get_Text.argtypes=[c_void_p]
        GetDllLibPdf().LineInfo_get_Text.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().LineInfo_get_Text(self.Ptr))
        return ret


    @property
    def Width(self)->float:
        """
    <summary>
        Gets width of the line text.
    </summary>
        """
        GetDllLibPdf().LineInfo_get_Width.argtypes=[c_void_p]
        GetDllLibPdf().LineInfo_get_Width.restype=c_float
        ret = GetDllLibPdf().LineInfo_get_Width(self.Ptr)
        return ret

