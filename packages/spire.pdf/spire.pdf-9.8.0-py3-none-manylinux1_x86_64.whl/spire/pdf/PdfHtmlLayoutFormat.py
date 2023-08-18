from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfHtmlLayoutFormat (SpireObject) :
    """

    """
    @property

    def Layout(self)->'PdfLayoutType':
        """
    <summary>
        Gets or sets layout type of the element.
    </summary>
        """
        GetDllLibPdf().PdfHtmlLayoutFormat_get_Layout.argtypes=[c_void_p]
        GetDllLibPdf().PdfHtmlLayoutFormat_get_Layout.restype=c_int
        ret = GetDllLibPdf().PdfHtmlLayoutFormat_get_Layout(self.Ptr)
        objwraped = PdfLayoutType(ret)
        return objwraped

    @Layout.setter
    def Layout(self, value:'PdfLayoutType'):
        GetDllLibPdf().PdfHtmlLayoutFormat_set_Layout.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfHtmlLayoutFormat_set_Layout(self.Ptr, value.value)

    @property

    def FitToPage(self)->'Clip':
        """
    <summary>
        If html view is larger than pdf page, zooms out it to fit pdf page.
            But if html view is smaller than, will not zoom in it.
    </summary>
        """
        GetDllLibPdf().PdfHtmlLayoutFormat_get_FitToPage.argtypes=[c_void_p]
        GetDllLibPdf().PdfHtmlLayoutFormat_get_FitToPage.restype=c_int
        ret = GetDllLibPdf().PdfHtmlLayoutFormat_get_FitToPage(self.Ptr)
        objwraped = Clip(ret)
        return objwraped

    @FitToPage.setter
    def FitToPage(self, value:'Clip'):
        GetDllLibPdf().PdfHtmlLayoutFormat_set_FitToPage.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfHtmlLayoutFormat_set_FitToPage(self.Ptr, value.value)

    @property

    def FitToHtml(self)->'Clip':
        """
    <summary>
        If html view is larger than page, resize pdf page to fit html view.
            But if html view is smaller than, will not resize pdf page.
    </summary>
        """
        GetDllLibPdf().PdfHtmlLayoutFormat_get_FitToHtml.argtypes=[c_void_p]
        GetDllLibPdf().PdfHtmlLayoutFormat_get_FitToHtml.restype=c_int
        ret = GetDllLibPdf().PdfHtmlLayoutFormat_get_FitToHtml(self.Ptr)
        objwraped = Clip(ret)
        return objwraped

    @FitToHtml.setter
    def FitToHtml(self, value:'Clip'):
        GetDllLibPdf().PdfHtmlLayoutFormat_set_FitToHtml.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfHtmlLayoutFormat_set_FitToHtml(self.Ptr, value.value)

    @property

    def TrimPage(self)->'Clip':
        """
    <summary>
        If html view is smaller than page, trim pdf page to fit html view.
    </summary>
        """
        GetDllLibPdf().PdfHtmlLayoutFormat_get_TrimPage.argtypes=[c_void_p]
        GetDllLibPdf().PdfHtmlLayoutFormat_get_TrimPage.restype=c_int
        ret = GetDllLibPdf().PdfHtmlLayoutFormat_get_TrimPage(self.Ptr)
        objwraped = Clip(ret)
        return objwraped

    @TrimPage.setter
    def TrimPage(self, value:'Clip'):
        GetDllLibPdf().PdfHtmlLayoutFormat_set_TrimPage.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfHtmlLayoutFormat_set_TrimPage(self.Ptr, value.value)

    @property
    def LoadHtmlTimeout(self)->int:
        """
    <summary>
        The maximum time in milliseconds to wait the completion of loading html.
            Default is 30000.
    </summary>
        """
        GetDllLibPdf().PdfHtmlLayoutFormat_get_LoadHtmlTimeout.argtypes=[c_void_p]
        GetDllLibPdf().PdfHtmlLayoutFormat_get_LoadHtmlTimeout.restype=c_int
        ret = GetDllLibPdf().PdfHtmlLayoutFormat_get_LoadHtmlTimeout(self.Ptr)
        return ret

    @LoadHtmlTimeout.setter
    def LoadHtmlTimeout(self, value:int):
        GetDllLibPdf().PdfHtmlLayoutFormat_set_LoadHtmlTimeout.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfHtmlLayoutFormat_set_LoadHtmlTimeout(self.Ptr, value)

    @property
    def IsWaiting(self)->bool:
        """
    <summary>
        webBrowser load html  whether  Waiting
     </summary>
        """
        GetDllLibPdf().PdfHtmlLayoutFormat_get_IsWaiting.argtypes=[c_void_p]
        GetDllLibPdf().PdfHtmlLayoutFormat_get_IsWaiting.restype=c_bool
        ret = GetDllLibPdf().PdfHtmlLayoutFormat_get_IsWaiting(self.Ptr)
        return ret

    @IsWaiting.setter
    def IsWaiting(self, value:bool):
        GetDllLibPdf().PdfHtmlLayoutFormat_set_IsWaiting.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfHtmlLayoutFormat_set_IsWaiting(self.Ptr, value)

    @property
    def WaitingTime(self)->int:
        """
    <summary>
        webBrowser load html  whether  Waiting time  in milliseconds.
     </summary>
        """
        GetDllLibPdf().PdfHtmlLayoutFormat_get_WaitingTime.argtypes=[c_void_p]
        GetDllLibPdf().PdfHtmlLayoutFormat_get_WaitingTime.restype=c_int
        ret = GetDllLibPdf().PdfHtmlLayoutFormat_get_WaitingTime(self.Ptr)
        return ret

    @WaitingTime.setter
    def WaitingTime(self, value:int):
        GetDllLibPdf().PdfHtmlLayoutFormat_set_WaitingTime.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfHtmlLayoutFormat_set_WaitingTime(self.Ptr, value)

