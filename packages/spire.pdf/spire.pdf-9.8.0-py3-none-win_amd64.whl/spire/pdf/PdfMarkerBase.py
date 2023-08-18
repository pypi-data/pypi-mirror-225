from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfMarkerBase (SpireObject) :
    """
    <summary>
        Represents base class for markers.
    </summary>
    """
    @property

    def Font(self)->'PdfFontBase':
        """
    <summary>
        Gets or sets marker font.
    </summary>
        """
        GetDllLibPdf().PdfMarkerBase_get_Font.argtypes=[c_void_p]
        GetDllLibPdf().PdfMarkerBase_get_Font.restype=c_void_p
        intPtr = GetDllLibPdf().PdfMarkerBase_get_Font(self.Ptr)
        ret = None if intPtr==None else PdfFontBase(intPtr)
        return ret


    @Font.setter
    def Font(self, value:'PdfFontBase'):
        GetDllLibPdf().PdfMarkerBase_set_Font.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfMarkerBase_set_Font(self.Ptr, value.Ptr)

    @property

    def Brush(self)->'PdfBrush':
        """
    <summary>
        Gets or sets marker brush.
    </summary>
        """
        GetDllLibPdf().PdfMarkerBase_get_Brush.argtypes=[c_void_p]
        GetDllLibPdf().PdfMarkerBase_get_Brush.restype=c_void_p
        intPtr = GetDllLibPdf().PdfMarkerBase_get_Brush(self.Ptr)
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @Brush.setter
    def Brush(self, value:'PdfBrush'):
        GetDllLibPdf().PdfMarkerBase_set_Brush.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfMarkerBase_set_Brush(self.Ptr, value.Ptr)

    @property

    def Pen(self)->'PdfPen':
        """
    <summary>
        Gets or sets marker pen.
    </summary>
        """
        GetDllLibPdf().PdfMarkerBase_get_Pen.argtypes=[c_void_p]
        GetDllLibPdf().PdfMarkerBase_get_Pen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfMarkerBase_get_Pen(self.Ptr)
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @Pen.setter
    def Pen(self, value:'PdfPen'):
        GetDllLibPdf().PdfMarkerBase_set_Pen.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfMarkerBase_set_Pen(self.Ptr, value.Ptr)

    @property

    def StringFormat(self)->'PdfStringFormat':
        """
    <summary>
        Gets or sets the format.
    </summary>
<value>The format.</value>
        """
        GetDllLibPdf().PdfMarkerBase_get_StringFormat.argtypes=[c_void_p]
        GetDllLibPdf().PdfMarkerBase_get_StringFormat.restype=c_void_p
        intPtr = GetDllLibPdf().PdfMarkerBase_get_StringFormat(self.Ptr)
        ret = None if intPtr==None else PdfStringFormat(intPtr)
        return ret


    @StringFormat.setter
    def StringFormat(self, value:'PdfStringFormat'):
        GetDllLibPdf().PdfMarkerBase_set_StringFormat.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfMarkerBase_set_StringFormat(self.Ptr, value.Ptr)

    @property

    def Alignment(self)->'PdfListMarkerAlignment':
        """
    <summary>
        Gets or sets a value indicating whether the marker is
            situated at the left of the list or at the right of the list.
    </summary>
        """
        GetDllLibPdf().PdfMarkerBase_get_Alignment.argtypes=[c_void_p]
        GetDllLibPdf().PdfMarkerBase_get_Alignment.restype=c_int
        ret = GetDllLibPdf().PdfMarkerBase_get_Alignment(self.Ptr)
        objwraped = PdfListMarkerAlignment(ret)
        return objwraped

    @Alignment.setter
    def Alignment(self, value:'PdfListMarkerAlignment'):
        GetDllLibPdf().PdfMarkerBase_set_Alignment.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfMarkerBase_set_Alignment(self.Ptr, value.value)

