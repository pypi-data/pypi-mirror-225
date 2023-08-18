from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfAttachmentAnnotation (  PdfFileAnnotation) :
    @dispatch
    def __init__(self,rectangle:RectangleF, filename:str):
        ptrRec:c_void_p = rectangle.Ptr
        GetDllLibPdf().PdfAttachmentAnnotation_CreatePdfAttachmentAnnotationRF.argtypes=[c_void_p,c_wchar_p]
        GetDllLibPdf().PdfAttachmentAnnotation_CreatePdfAttachmentAnnotationRF.restype = c_void_p
        intPtr = GetDllLibPdf().PdfAttachmentAnnotation_CreatePdfAttachmentAnnotationRF(ptrRec,filename)
        super(PdfAttachmentAnnotation, self).__init__(intPtr)

    @dispatch
    def __init__(self,rectangle:RectangleF, filename:str,stream:Stream):
        ptrRec:c_void_p = rectangle.Ptr
        ptrStream:c_void_p = stream.Ptr
        GetDllLibPdf().PdfAttachmentAnnotation_CreatePdfAttachmentAnnotationRFS.argtypes=[c_void_p,c_wchar_p,c_void_p]
        GetDllLibPdf().PdfAttachmentAnnotation_CreatePdfAttachmentAnnotationRFS.restype = c_void_p
        intPtr = GetDllLibPdf().PdfAttachmentAnnotation_CreatePdfAttachmentAnnotationRFS(ptrRec,filename,ptrStream)
        super(PdfAttachmentAnnotation, self).__init__(intPtr)
    """
    <summary>
        Represents an attachment annotation.
    </summary>
    """
    @property

    def Icon(self)->'PdfAttachmentIcon':
        """
    <summary>
        Gets or Sets attachment's icon.
    </summary>
<value>A  enumeration member specifying the icon for the annotation when it is displayed in closed state.</value>
        """
        GetDllLibPdf().PdfAttachmentAnnotation_get_Icon.argtypes=[c_void_p]
        GetDllLibPdf().PdfAttachmentAnnotation_get_Icon.restype=c_int
        ret = GetDllLibPdf().PdfAttachmentAnnotation_get_Icon(self.Ptr)
        objwraped = PdfAttachmentIcon(ret)
        return objwraped

    @Icon.setter
    def Icon(self, value:'PdfAttachmentIcon'):
        GetDllLibPdf().PdfAttachmentAnnotation_set_Icon.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfAttachmentAnnotation_set_Icon(self.Ptr, value.value)

    @property

    def FileName(self)->str:
        """
<value>A string value specifying the full path to the file to be embedded in the PDF file.</value>
        """
        GetDllLibPdf().PdfAttachmentAnnotation_get_FileName.argtypes=[c_void_p]
        GetDllLibPdf().PdfAttachmentAnnotation_get_FileName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfAttachmentAnnotation_get_FileName(self.Ptr))
        return ret


    @FileName.setter
    def FileName(self, value:str):
        GetDllLibPdf().PdfAttachmentAnnotation_set_FileName.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfAttachmentAnnotation_set_FileName(self.Ptr, value)

