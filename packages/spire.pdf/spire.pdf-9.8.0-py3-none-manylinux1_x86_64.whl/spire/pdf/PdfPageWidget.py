from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfPageWidget (  PdfPageBase) :
    """
    <summary>
        Represents a page loaded from a document.
    </summary>
    """
    @property

    def Size(self)->'SizeF':
        """
    <summary>
        Gets the size of the page.
    </summary>
        """
        GetDllLibPdf().PdfPageWidget_get_Size.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageWidget_get_Size.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageWidget_get_Size(self.Ptr)
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @property

    def ActualSize(self)->'SizeF':
        """
    <summary>
        Get the visible region of the page.
    </summary>
        """
        GetDllLibPdf().PdfPageWidget_get_ActualSize.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageWidget_get_ActualSize.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageWidget_get_ActualSize(self.Ptr)
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @property

    def Document(self)->'PdfDocumentBase':
        """
    <summary>
        Gets the document.
    </summary>
        """
        GetDllLibPdf().PdfPageWidget_get_Document.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageWidget_get_Document.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageWidget_get_Document(self.Ptr)
        ret = None if intPtr==None else PdfDocumentBase(intPtr)
        return ret


