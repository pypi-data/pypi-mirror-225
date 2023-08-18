from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfMarker (  PdfMarkerBase) :
    """
    <summary>
        Represents bullet for the list.
    </summary>
    """
    @property

    def Template(self)->'PdfTemplate':
        """
    <summary>
        Gets or sets template of the marker.
    </summary>
        """
        GetDllLibPdf().PdfMarker_get_Template.argtypes=[c_void_p]
        GetDllLibPdf().PdfMarker_get_Template.restype=c_void_p
        intPtr = GetDllLibPdf().PdfMarker_get_Template(self.Ptr)
        ret = None if intPtr==None else PdfTemplate(intPtr)
        return ret


    @Template.setter
    def Template(self, value:'PdfTemplate'):
        GetDllLibPdf().PdfMarker_set_Template.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfMarker_set_Template(self.Ptr, value.Ptr)

    @property

    def Image(self)->'PdfImage':
        """
    <summary>
        Gets or sets image of the marker.
    </summary>
        """
        GetDllLibPdf().PdfMarker_get_Image.argtypes=[c_void_p]
        GetDllLibPdf().PdfMarker_get_Image.restype=c_void_p
        intPtr = GetDllLibPdf().PdfMarker_get_Image(self.Ptr)
        ret = None if intPtr==None else PdfImage(intPtr)
        return ret


    @Image.setter
    def Image(self, value:'PdfImage'):
        GetDllLibPdf().PdfMarker_set_Image.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfMarker_set_Image(self.Ptr, value.Ptr)

    @property

    def Text(self)->str:
        """
    <summary>
        Gets or sets marker text.
    </summary>
        """
        GetDllLibPdf().PdfMarker_get_Text.argtypes=[c_void_p]
        GetDllLibPdf().PdfMarker_get_Text.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfMarker_get_Text(self.Ptr))
        return ret


    @Text.setter
    def Text(self, value:str):
        GetDllLibPdf().PdfMarker_set_Text.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfMarker_set_Text(self.Ptr, value)

    @property

    def Style(self)->'PdfUnorderedMarkerStyle':
        """
    <summary>
        Gets or sets the style.
    </summary>
        """
        GetDllLibPdf().PdfMarker_get_Style.argtypes=[c_void_p]
        GetDllLibPdf().PdfMarker_get_Style.restype=c_int
        ret = GetDllLibPdf().PdfMarker_get_Style(self.Ptr)
        objwraped = PdfUnorderedMarkerStyle(ret)
        return objwraped

    @Style.setter
    def Style(self, value:'PdfUnorderedMarkerStyle'):
        GetDllLibPdf().PdfMarker_set_Style.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfMarker_set_Style(self.Ptr, value.value)

