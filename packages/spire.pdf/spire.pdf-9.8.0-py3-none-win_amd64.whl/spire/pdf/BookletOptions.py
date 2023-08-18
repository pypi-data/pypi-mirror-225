from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class BookletOptions (SpireObject) :
    """
    <summary>
        The booklet options 
    </summary>
    """
    @dispatch
    def __init__(self):
        GetDllLibPdf().BookletOptions_CreateBookletOptions.restype = c_void_p
        intPtr = GetDllLibPdf().BookletOptions_CreateBookletOptions()
        super(BookletOptions, self).__init__(intPtr)
		
    @property

    def BookletBinding(self)->'PdfBookletBindingMode':
        """
    <summary>
        Get or set BookletBinding,default value Left.
    </summary>
        """
        GetDllLibPdf().BookletOptions_get_BookletBinding.argtypes=[c_void_p]
        GetDllLibPdf().BookletOptions_get_BookletBinding.restype=c_int
        ret = GetDllLibPdf().BookletOptions_get_BookletBinding(self.Ptr)
        objwraped = PdfBookletBindingMode(ret)
        return objwraped

    @BookletBinding.setter
    def BookletBinding(self, value:'PdfBookletBindingMode'):
        GetDllLibPdf().BookletOptions_set_BookletBinding.argtypes=[c_void_p, c_int]
        GetDllLibPdf().BookletOptions_set_BookletBinding(self.Ptr, value.value)

