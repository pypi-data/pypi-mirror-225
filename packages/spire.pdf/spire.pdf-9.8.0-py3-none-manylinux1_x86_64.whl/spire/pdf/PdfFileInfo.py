from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfFileInfo (SpireObject) :
    """
    <summary>
        This class represents a set of the properties that define the internal structure of PDF file.
    </summary>
    """
    @property

    def Version(self)->'PdfVersion':
        """
    <summary>
        Gets or sets the version of the PDF document.
    </summary>
<value>The document version.</value>
        """
        GetDllLibPdf().PdfFileInfo_get_Version.argtypes=[c_void_p]
        GetDllLibPdf().PdfFileInfo_get_Version.restype=c_int
        ret = GetDllLibPdf().PdfFileInfo_get_Version(self.Ptr)
        objwraped = PdfVersion(ret)
        return objwraped

    @Version.setter
    def Version(self, value:'PdfVersion'):
        GetDllLibPdf().PdfFileInfo_set_Version.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfFileInfo_set_Version(self.Ptr, value.value)

    @property
    def IncrementalUpdate(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether [incremental update].
    </summary>
<value>
  <c>true</c> if [incremental update]; otherwise, <c>false</c>.</value>
        """
        GetDllLibPdf().PdfFileInfo_get_IncrementalUpdate.argtypes=[c_void_p]
        GetDllLibPdf().PdfFileInfo_get_IncrementalUpdate.restype=c_bool
        ret = GetDllLibPdf().PdfFileInfo_get_IncrementalUpdate(self.Ptr)
        return ret

    @IncrementalUpdate.setter
    def IncrementalUpdate(self, value:bool):
        GetDllLibPdf().PdfFileInfo_set_IncrementalUpdate.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfFileInfo_set_IncrementalUpdate(self.Ptr, value)

    @property

    def CrossReferenceType(self)->'PdfCrossReferenceType':
        """
    <summary>
        Gets or sets the type of PDF cross-reference.
    </summary>
<remarks>Please see the description of  for more details.</remarks>
        """
        GetDllLibPdf().PdfFileInfo_get_CrossReferenceType.argtypes=[c_void_p]
        GetDllLibPdf().PdfFileInfo_get_CrossReferenceType.restype=c_int
        ret = GetDllLibPdf().PdfFileInfo_get_CrossReferenceType(self.Ptr)
        objwraped = PdfCrossReferenceType(ret)
        return objwraped

    @CrossReferenceType.setter
    def CrossReferenceType(self, value:'PdfCrossReferenceType'):
        GetDllLibPdf().PdfFileInfo_set_CrossReferenceType.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfFileInfo_set_CrossReferenceType(self.Ptr, value.value)

    @property
    def TaggedPdf(self)->bool:
        """
    <summary>
        Gets the value indicating whether the PDF document is tagged one or not.
    </summary>
<value>If true PDF document is tagged, otherwise false.</value>
        """
        GetDllLibPdf().PdfFileInfo_get_TaggedPdf.argtypes=[c_void_p]
        GetDllLibPdf().PdfFileInfo_get_TaggedPdf.restype=c_bool
        ret = GetDllLibPdf().PdfFileInfo_get_TaggedPdf(self.Ptr)
        return ret

