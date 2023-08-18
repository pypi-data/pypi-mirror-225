from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfFieldWidgetImportError (SpireObject) :
    """

    """
#    @property
#
#    def Exception(self)->'Exception':
#        """
#
#        """
#        GetDllLibPdf().PdfFieldWidgetImportError_get_Exception.argtypes=[c_void_p]
#        GetDllLibPdf().PdfFieldWidgetImportError_get_Exception.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfFieldWidgetImportError_get_Exception(self.Ptr)
#        ret = None if intPtr==None else Exception(intPtr)
#        return ret
#


    @property

    def FieldWidget(self)->'PdfFieldWidget':
        """

        """
        GetDllLibPdf().PdfFieldWidgetImportError_get_FieldWidget.argtypes=[c_void_p]
        GetDllLibPdf().PdfFieldWidgetImportError_get_FieldWidget.restype=c_void_p
        intPtr = GetDllLibPdf().PdfFieldWidgetImportError_get_FieldWidget(self.Ptr)
        ret = None if intPtr==None else PdfFieldWidget(intPtr)
        return ret


