from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfAttachmentAnnotationWidget (  PdfStyledAnnotationWidget) :
    """
    <summary>
        Represents the attachment annotation from the loaded document.
    </summary>
    """
    @property

    def Icon(self)->'PdfAttachmentIcon':
        """
    <summary>
        Gets or sets the icon of the annotation.
    </summary>
        """
        GetDllLibPdf().PdfAttachmentAnnotationWidget_get_Icon.argtypes=[c_void_p]
        GetDllLibPdf().PdfAttachmentAnnotationWidget_get_Icon.restype=c_int
        ret = GetDllLibPdf().PdfAttachmentAnnotationWidget_get_Icon(self.Ptr)
        objwraped = PdfAttachmentIcon(ret)
        return objwraped

    @Icon.setter
    def Icon(self, value:'PdfAttachmentIcon'):
        GetDllLibPdf().PdfAttachmentAnnotationWidget_set_Icon.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfAttachmentAnnotationWidget_set_Icon(self.Ptr, value.value)

    @property

    def FileName(self)->str:
        """
    <summary>
         Gets the attachment file name of the annotation.
    </summary>
        """
        GetDllLibPdf().PdfAttachmentAnnotationWidget_get_FileName.argtypes=[c_void_p]
        GetDllLibPdf().PdfAttachmentAnnotationWidget_get_FileName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfAttachmentAnnotationWidget_get_FileName(self.Ptr))
        return ret


#    @property
#
#    def Data(self)->List['Byte']:
#        """
#
#        """
#        GetDllLibPdf().PdfAttachmentAnnotationWidget_get_Data.argtypes=[c_void_p]
#        GetDllLibPdf().PdfAttachmentAnnotationWidget_get_Data.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().PdfAttachmentAnnotationWidget_get_Data(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, Byte)
#        return ret


    def ObjectID(self)->int:
        """
    <summary>
        Represents the Form field identifier
    </summary>
        """
        GetDllLibPdf().PdfAttachmentAnnotationWidget_ObjectID.argtypes=[c_void_p]
        GetDllLibPdf().PdfAttachmentAnnotationWidget_ObjectID.restype=c_int
        ret = GetDllLibPdf().PdfAttachmentAnnotationWidget_ObjectID(self.Ptr)
        return ret

