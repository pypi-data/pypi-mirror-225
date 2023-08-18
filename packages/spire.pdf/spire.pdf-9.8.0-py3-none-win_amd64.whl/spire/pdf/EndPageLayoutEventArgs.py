from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class EndPageLayoutEventArgs (  PdfCancelEventArgs) :
    """
    <summary>
        Contains information about layout`s element .
    </summary>
    """
    @property

    def Result(self)->'PdfLayoutResult':
        """
    <summary>
        Gets a result of the lay outing on the page.
    </summary>
        """
        GetDllLibPdf().EndPageLayoutEventArgs_get_Result.argtypes=[c_void_p]
        GetDllLibPdf().EndPageLayoutEventArgs_get_Result.restype=c_void_p
        intPtr = GetDllLibPdf().EndPageLayoutEventArgs_get_Result(self.Ptr)
        ret = None if intPtr==None else PdfLayoutResult(intPtr)
        return ret


    @property

    def NextPage(self)->'PdfNewPage':
        """
    <summary>
        Gets or sets a value indicating the next page where the element should be layout if the process is not finished or stopped.
    </summary>
<remarks>The default value is null. In this case the element will be layout on the next page.</remarks>
        """
        GetDllLibPdf().EndPageLayoutEventArgs_get_NextPage.argtypes=[c_void_p]
        GetDllLibPdf().EndPageLayoutEventArgs_get_NextPage.restype=c_void_p
        intPtr = GetDllLibPdf().EndPageLayoutEventArgs_get_NextPage(self.Ptr)
        ret = None if intPtr==None else PdfNewPage(intPtr)
        return ret


    @NextPage.setter
    def NextPage(self, value:'PdfNewPage'):
        GetDllLibPdf().EndPageLayoutEventArgs_set_NextPage.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().EndPageLayoutEventArgs_set_NextPage(self.Ptr, value.Ptr)

