from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfDocumentInformation (SpireObject) :
    """
    <summary>
        A class containing the information about the document.
    </summary>
    """
    @property

    def CreationDate(self)->'DateTime':
        """
    <summary>
        Gets or sets the creation date.
    </summary>
        """
        GetDllLibPdf().PdfDocumentInformation_get_CreationDate.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocumentInformation_get_CreationDate.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocumentInformation_get_CreationDate(self.Ptr)
        ret = None if intPtr==None else DateTime(intPtr)
        return ret


    @CreationDate.setter
    def CreationDate(self, value:'DateTime'):
        GetDllLibPdf().PdfDocumentInformation_set_CreationDate.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfDocumentInformation_set_CreationDate(self.Ptr, value.Ptr)

    @property

    def ModificationDate(self)->'DateTime':
        """
    <summary>
        Gets or sets the modification date.
    </summary>
        """
        GetDllLibPdf().PdfDocumentInformation_get_ModificationDate.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocumentInformation_get_ModificationDate.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocumentInformation_get_ModificationDate(self.Ptr)
        ret = None if intPtr==None else DateTime(intPtr)
        return ret


    @ModificationDate.setter
    def ModificationDate(self, value:'DateTime'):
        GetDllLibPdf().PdfDocumentInformation_set_ModificationDate.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfDocumentInformation_set_ModificationDate(self.Ptr, value.Ptr)

    @property

    def Title(self)->str:
        """
    <summary>
        Gets or sets the title.
    </summary>
        """
        GetDllLibPdf().PdfDocumentInformation_get_Title.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocumentInformation_get_Title.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfDocumentInformation_get_Title(self.Ptr))
        return ret


    @Title.setter
    def Title(self, value:str):
        GetDllLibPdf().PdfDocumentInformation_set_Title.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfDocumentInformation_set_Title(self.Ptr, value)

    @property

    def Author(self)->str:
        """
    <summary>
        Gets or sets the author.
    </summary>
        """
        GetDllLibPdf().PdfDocumentInformation_get_Author.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocumentInformation_get_Author.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfDocumentInformation_get_Author(self.Ptr))
        return ret


    @Author.setter
    def Author(self, value:str):
        GetDllLibPdf().PdfDocumentInformation_set_Author.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfDocumentInformation_set_Author(self.Ptr, value)

    @property

    def Subject(self)->str:
        """
    <summary>
        Gets or sets the subject.
    </summary>
        """
        GetDllLibPdf().PdfDocumentInformation_get_Subject.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocumentInformation_get_Subject.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfDocumentInformation_get_Subject(self.Ptr))
        return ret


    @Subject.setter
    def Subject(self, value:str):
        GetDllLibPdf().PdfDocumentInformation_set_Subject.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfDocumentInformation_set_Subject(self.Ptr, value)

    @property

    def Keywords(self)->str:
        """
    <summary>
        Gets or sets the keywords.
    </summary>
        """
        GetDllLibPdf().PdfDocumentInformation_get_Keywords.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocumentInformation_get_Keywords.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfDocumentInformation_get_Keywords(self.Ptr))
        return ret


    @Keywords.setter
    def Keywords(self, value:str):
        GetDllLibPdf().PdfDocumentInformation_set_Keywords.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfDocumentInformation_set_Keywords(self.Ptr, value)

    @property

    def Creator(self)->str:
        """
    <summary>
        Gets or sets the creator.
    </summary>
        """
        GetDllLibPdf().PdfDocumentInformation_get_Creator.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocumentInformation_get_Creator.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfDocumentInformation_get_Creator(self.Ptr))
        return ret


    @Creator.setter
    def Creator(self, value:str):
        GetDllLibPdf().PdfDocumentInformation_set_Creator.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfDocumentInformation_set_Creator(self.Ptr, value)

    @property

    def Producer(self)->str:
        """
    <summary>
        Gets or sets the producer.
    </summary>
        """
        GetDllLibPdf().PdfDocumentInformation_get_Producer.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocumentInformation_get_Producer.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfDocumentInformation_get_Producer(self.Ptr))
        return ret


    @Producer.setter
    def Producer(self, value:str):
        GetDllLibPdf().PdfDocumentInformation_set_Producer.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfDocumentInformation_set_Producer(self.Ptr, value)


    def RemoveCustomerDefined(self ,key:str):
        """

        """
        
        GetDllLibPdf().PdfDocumentInformation_RemoveCustomerDefined.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfDocumentInformation_RemoveCustomerDefined(self.Ptr, key)


    def RemoveCustomProperty(self ,name:str):
        """
    <summary>
        Remove custom property.
    </summary>
    <param name="name">
            The property name.
            Name not be Title,Author,Subject,Keywords,Creator,Producer,CreationDate,ModificationDate,Trap.
    </param>
        """
        
        GetDllLibPdf().PdfDocumentInformation_RemoveCustomProperty.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfDocumentInformation_RemoveCustomProperty(self.Ptr, name)


    def SetCustomerDefined(self ,key:str,value:str)->bool:
        """

        """
        
        GetDllLibPdf().PdfDocumentInformation_SetCustomerDefined.argtypes=[c_void_p ,c_wchar_p,c_wchar_p]
        GetDllLibPdf().PdfDocumentInformation_SetCustomerDefined.restype=c_bool
        ret = GetDllLibPdf().PdfDocumentInformation_SetCustomerDefined(self.Ptr, key,value)
        return ret


    def SetCustomProperty(self ,name:str,value:str):
        """
    <summary>
        Set custom property.
    </summary>
    <param name="name">
            The property name.
            Name not be Title,Author,Subject,Keywords,Creator,Producer,CreationDate,ModificationDate,Trap.
    </param>
    <param name="value">The property value.</param>
        """
        
        GetDllLibPdf().PdfDocumentInformation_SetCustomProperty.argtypes=[c_void_p ,c_wchar_p,c_wchar_p]
        GetDllLibPdf().PdfDocumentInformation_SetCustomProperty(self.Ptr, name,value)


    def GetCustomerDefined(self ,key:str)->str:
        """

        """
        
        GetDllLibPdf().PdfDocumentInformation_GetCustomerDefined.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfDocumentInformation_GetCustomerDefined.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfDocumentInformation_GetCustomerDefined(self.Ptr, key))
        return ret



    def GetCustomProperty(self ,name:str)->str:
        """
    <summary>
        Get custom property.
    </summary>
    <param name="name">
            The property name.
            Name not be Title,Author,Subject,Keywords,Creator,Producer,CreationDate,ModificationDate,Trap.
    </param>
    <returns>The property value.null if property not exist.</returns>
        """
        
        GetDllLibPdf().PdfDocumentInformation_GetCustomProperty.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfDocumentInformation_GetCustomProperty.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfDocumentInformation_GetCustomProperty(self.Ptr, name))
        return ret


#
#    def GetAllCustomerDefined(self)->'Dictionary2':
#        """
#
#        """
#        GetDllLibPdf().PdfDocumentInformation_GetAllCustomerDefined.argtypes=[c_void_p]
#        GetDllLibPdf().PdfDocumentInformation_GetAllCustomerDefined.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfDocumentInformation_GetAllCustomerDefined(self.Ptr)
#        ret = None if intPtr==None else Dictionary2(intPtr)
#        return ret
#


#
#    def GetAllCustomProperties(self)->'Dictionary2':
#        """
#    <summary>
#        Get all custom properties.
#    </summary>
#    <returns>The all properties.</returns>
#        """
#        GetDllLibPdf().PdfDocumentInformation_GetAllCustomProperties.argtypes=[c_void_p]
#        GetDllLibPdf().PdfDocumentInformation_GetAllCustomProperties.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfDocumentInformation_GetAllCustomProperties(self.Ptr)
#        ret = None if intPtr==None else Dictionary2(intPtr)
#        return ret
#



    def GetMetaData(self)->'XmpMetadata':
        """

        """
        GetDllLibPdf().PdfDocumentInformation_GetMetaData.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocumentInformation_GetMetaData.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocumentInformation_GetMetaData(self.Ptr)
        ret = None if intPtr==None else XmpMetadata(intPtr)
        return ret


