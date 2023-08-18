from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfEmbeddedFileSpecification (  PdfFileSpecificationBase) :
    """
    <summary>
        Represents specification of embedded file.
    </summary>
    """
    @property

    def FileName(self)->str:
        """
<value></value>
        """
        GetDllLibPdf().PdfEmbeddedFileSpecification_get_FileName.argtypes=[c_void_p]
        GetDllLibPdf().PdfEmbeddedFileSpecification_get_FileName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfEmbeddedFileSpecification_get_FileName(self.Ptr))
        return ret


    @FileName.setter
    def FileName(self, value:str):
        GetDllLibPdf().PdfEmbeddedFileSpecification_set_FileName.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfEmbeddedFileSpecification_set_FileName(self.Ptr, value)

    @property

    def Data(self)->Stream:
        """
    <summary>
        Gets or sets the data.
    </summary>
<value>The data.</value>
        """
        GetDllLibPdf().PdfEmbeddedFileSpecification_get_Data.argtypes=[c_void_p]
        GetDllLibPdf().PdfEmbeddedFileSpecification_get_Data.restype=c_void_p
        intPtr = GetDllLibPdf().PdfEmbeddedFileSpecification_get_Data(self.Ptr)
        ret = None if intPtr==None else Stream(intPtr)
        return ret


    @Data.setter
    def Data(self, value:List[bytes]):
        vCount = len(value)
        ArrayType = c_void_p * vCount
        vArray = ArrayType()
        for i in range(0, vCount):
            vArray[i] = value[i]
        GetDllLibPdf().PdfEmbeddedFileSpecification_set_Data.argtypes=[c_void_p, ArrayType, c_int]
        GetDllLibPdf().PdfEmbeddedFileSpecification_set_Data(self.Ptr, vArray, vCount)


    @property

    def Description(self)->str:
        """
    <summary>
        Gets or sets the description.
    </summary>
<value>The description.</value>
        """
        GetDllLibPdf().PdfEmbeddedFileSpecification_get_Description.argtypes=[c_void_p]
        GetDllLibPdf().PdfEmbeddedFileSpecification_get_Description.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfEmbeddedFileSpecification_get_Description(self.Ptr))
        return ret


    @Description.setter
    def Description(self, value:str):
        GetDllLibPdf().PdfEmbeddedFileSpecification_set_Description.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfEmbeddedFileSpecification_set_Description(self.Ptr, value)

    @property

    def MimeType(self)->str:
        """
    <summary>
        Gets or sets the MIME type of the embedded file.
    </summary>
<value>The MIME type of the embedded file.</value>
        """
        GetDllLibPdf().PdfEmbeddedFileSpecification_get_MimeType.argtypes=[c_void_p]
        GetDllLibPdf().PdfEmbeddedFileSpecification_get_MimeType.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfEmbeddedFileSpecification_get_MimeType(self.Ptr))
        return ret


    @MimeType.setter
    def MimeType(self, value:str):
        GetDllLibPdf().PdfEmbeddedFileSpecification_set_MimeType.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfEmbeddedFileSpecification_set_MimeType(self.Ptr, value)

    @property

    def CreationDate(self)->'DateTime':
        """
    <summary>
        Gets or sets creation date.
    </summary>
<value>Creation date.</value>
        """
        GetDllLibPdf().PdfEmbeddedFileSpecification_get_CreationDate.argtypes=[c_void_p]
        GetDllLibPdf().PdfEmbeddedFileSpecification_get_CreationDate.restype=c_void_p
        intPtr = GetDllLibPdf().PdfEmbeddedFileSpecification_get_CreationDate(self.Ptr)
        ret = None if intPtr==None else DateTime(intPtr)
        return ret


    @CreationDate.setter
    def CreationDate(self, value:'DateTime'):
        GetDllLibPdf().PdfEmbeddedFileSpecification_set_CreationDate.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfEmbeddedFileSpecification_set_CreationDate(self.Ptr, value.Ptr)

    @property

    def ModificationDate(self)->'DateTime':
        """
    <summary>
        Gets or sets modification date.
    </summary>
<value>Modification date.</value>
        """
        GetDllLibPdf().PdfEmbeddedFileSpecification_get_ModificationDate.argtypes=[c_void_p]
        GetDllLibPdf().PdfEmbeddedFileSpecification_get_ModificationDate.restype=c_void_p
        intPtr = GetDllLibPdf().PdfEmbeddedFileSpecification_get_ModificationDate(self.Ptr)
        ret = None if intPtr==None else DateTime(intPtr)
        return ret


    @ModificationDate.setter
    def ModificationDate(self, value:'DateTime'):
        GetDllLibPdf().PdfEmbeddedFileSpecification_set_ModificationDate.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfEmbeddedFileSpecification_set_ModificationDate(self.Ptr, value.Ptr)

    @dispatch

    def SetFieldValue(self ,fieldName:str,fieldValue:str):
        """
    <summary>
        Set the corresponding field value by field name.
    </summary>
    <param name="fieldName">Custom field name.</param>
    <param name="fieldValue">The corresponding field value.</param>
        """
        
        GetDllLibPdf().PdfEmbeddedFileSpecification_SetFieldValue.argtypes=[c_void_p ,c_wchar_p,c_wchar_p]
        GetDllLibPdf().PdfEmbeddedFileSpecification_SetFieldValue(self.Ptr, fieldName,fieldValue)

    @dispatch

    def SetFieldValue(self ,fieldName:str,fieldValue:DateTime):
        """
    <summary>
        Set the corresponding field value by field name.
    </summary>
    <param name="fieldName">Custom field name.</param>
    <param name="fieldValue">The corresponding field value.</param>
        """
        intPtrfieldValue:c_void_p = fieldValue.Ptr

        GetDllLibPdf().PdfEmbeddedFileSpecification_SetFieldValueFF.argtypes=[c_void_p ,c_wchar_p,c_void_p]
        GetDllLibPdf().PdfEmbeddedFileSpecification_SetFieldValueFF(self.Ptr, fieldName,intPtrfieldValue)

    @dispatch

    def SetFieldValue(self ,fieldName:str,fieldValue:int):
        """
    <summary>
        Set the corresponding field value by field name.
    </summary>
    <param name="fieldName">Custom field name.</param>
    <param name="fieldValue">The corresponding field value.</param>
        """
        
        GetDllLibPdf().PdfEmbeddedFileSpecification_SetFieldValueFF1.argtypes=[c_void_p ,c_wchar_p,c_int]
        GetDllLibPdf().PdfEmbeddedFileSpecification_SetFieldValueFF1(self.Ptr, fieldName,fieldValue)

