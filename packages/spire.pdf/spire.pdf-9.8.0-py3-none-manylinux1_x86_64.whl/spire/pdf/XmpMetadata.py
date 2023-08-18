from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class XmpMetadata (SpireObject) :
    """
    <summary>
        Represents XMP metadata of the document.
    </summary>
    """
#    @property
#
#    def XmlData(self)->'XmlDocument':
#        """
#    <summary>
#        Gets XMP data in XML format.
#    </summary>
#        """
#        GetDllLibPdf().XmpMetadata_get_XmlData.argtypes=[c_void_p]
#        GetDllLibPdf().XmpMetadata_get_XmlData.restype=c_void_p
#        intPtr = GetDllLibPdf().XmpMetadata_get_XmlData(self.Ptr)
#        ret = None if intPtr==None else XmlDocument(intPtr)
#        return ret
#


#    @property
#
#    def NamespaceManager(self)->'XmlNamespaceManager':
#        """
#    <summary>
#        Gets namespace manager of the Xmp metadata.
#    </summary>
#        """
#        GetDllLibPdf().XmpMetadata_get_NamespaceManager.argtypes=[c_void_p]
#        GetDllLibPdf().XmpMetadata_get_NamespaceManager.restype=c_void_p
#        intPtr = GetDllLibPdf().XmpMetadata_get_NamespaceManager(self.Ptr)
#        ret = None if intPtr==None else XmlNamespaceManager(intPtr)
#        return ret
#


#
#    def Add(self ,schema:'XmlElement'):
#        """
#    <summary>
#        Adds schema to the XMP in XML format.
#    </summary>
#    <param name="schema">XMP schema in XML format.</param>
#<remarks>If XMP already contains such schema - there will be two equal schemas at the xmp.</remarks>
#        """
#        intPtrschema:c_void_p = schema.Ptr
#
#        GetDllLibPdf().XmpMetadata_Add.argtypes=[c_void_p ,c_void_p]
#        GetDllLibPdf().XmpMetadata_Add(self.Ptr, intPtrschema)



    def GetTitle(self)->str:
        """
    <summary>
        Return title if exists; otherwise return null
    </summary>
    <returns></returns>
        """
        GetDllLibPdf().XmpMetadata_GetTitle.argtypes=[c_void_p]
        GetDllLibPdf().XmpMetadata_GetTitle.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().XmpMetadata_GetTitle(self.Ptr))
        return ret



    def GetSubject(self)->str:
        """
    <summary>
        Return subject if exists; otherwise return null
    </summary>
    <returns></returns>
        """
        GetDllLibPdf().XmpMetadata_GetSubject.argtypes=[c_void_p]
        GetDllLibPdf().XmpMetadata_GetSubject.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().XmpMetadata_GetSubject(self.Ptr))
        return ret



    def GetAuthor(self)->str:
        """
    <summary>
        Return author if exists; otherwise return null
    </summary>
    <returns></returns>
        """
        GetDllLibPdf().XmpMetadata_GetAuthor.argtypes=[c_void_p]
        GetDllLibPdf().XmpMetadata_GetAuthor.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().XmpMetadata_GetAuthor(self.Ptr))
        return ret



    def GetProducer(self)->str:
        """
    <summary>
        Return producer if exists; otherwise return null
    </summary>
    <returns></returns>
        """
        GetDllLibPdf().XmpMetadata_GetProducer.argtypes=[c_void_p]
        GetDllLibPdf().XmpMetadata_GetProducer.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().XmpMetadata_GetProducer(self.Ptr))
        return ret



    def GetKeywords(self)->str:
        """
    <summary>
        return keywords if exists; otherwise return null
    </summary>
    <returns></returns>
        """
        GetDllLibPdf().XmpMetadata_GetKeywords.argtypes=[c_void_p]
        GetDllLibPdf().XmpMetadata_GetKeywords.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().XmpMetadata_GetKeywords(self.Ptr))
        return ret



    def GetCustomProperty(self ,fieldName:str)->str:
        """
    <summary>
        Return specified custom field value if exists; otherwise return null
    </summary>
    <param name="fieldName"></param>
    <returns></returns>
        """
        
        GetDllLibPdf().XmpMetadata_GetCustomProperty.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().XmpMetadata_GetCustomProperty.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().XmpMetadata_GetCustomProperty(self.Ptr, fieldName))
        return ret


#
#    def GetAllCustomProperties(self)->'Dictionary2':
#        """
#    <summary>
#        Return all custom properties if exsit; otherwise return empty Dictionary
#    </summary>
#    <returns></returns>
#        """
#        GetDllLibPdf().XmpMetadata_GetAllCustomProperties.argtypes=[c_void_p]
#        GetDllLibPdf().XmpMetadata_GetAllCustomProperties.restype=c_void_p
#        intPtr = GetDllLibPdf().XmpMetadata_GetAllCustomProperties(self.Ptr)
#        ret = None if intPtr==None else Dictionary2(intPtr)
#        return ret
#



    def GetCreateDate(self)->'DateTime':
        """
    <summary>
        Return create date if exists; otherwise return default DateTime
    </summary>
    <returns></returns>
        """
        GetDllLibPdf().XmpMetadata_GetCreateDate.argtypes=[c_void_p]
        GetDllLibPdf().XmpMetadata_GetCreateDate.restype=c_void_p
        intPtr = GetDllLibPdf().XmpMetadata_GetCreateDate(self.Ptr)
        ret = None if intPtr==None else DateTime(intPtr)
        return ret



    def GetCreator(self)->str:
        """
    <summary>
        Return creator if exists; otherwise return null
    </summary>
    <returns></returns>
        """
        GetDllLibPdf().XmpMetadata_GetCreator.argtypes=[c_void_p]
        GetDllLibPdf().XmpMetadata_GetCreator.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().XmpMetadata_GetCreator(self.Ptr))
        return ret



    def GetModifyDate(self)->'DateTime':
        """
    <summary>
        Return modify date if exists; otherwise return System.DateTime.MinValue
    </summary>
    <returns></returns>
        """
        GetDllLibPdf().XmpMetadata_GetModifyDate.argtypes=[c_void_p]
        GetDllLibPdf().XmpMetadata_GetModifyDate.restype=c_void_p
        intPtr = GetDllLibPdf().XmpMetadata_GetModifyDate(self.Ptr)
        ret = None if intPtr==None else DateTime(intPtr)
        return ret



    def SetTitle(self ,value:str):
        """
    <summary>
        Set title to xmpmeta; if value is null, remove the node; if the node is null, create the node
    </summary>
    <param name="value"></param>
        """
        
        GetDllLibPdf().XmpMetadata_SetTitle.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().XmpMetadata_SetTitle(self.Ptr, value)


    def SetSubject(self ,value:str):
        """
    <summary>
        Set subject to xmpmeta; if value is null, remove the node; if the node is null, create the node
    </summary>
    <param name="value"></param>
        """
        
        GetDllLibPdf().XmpMetadata_SetSubject.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().XmpMetadata_SetSubject(self.Ptr, value)


    def SetAuthor(self ,value:str):
        """
    <summary>
        Set subject to xmpmeta; if value is null, remove the node; if the node is null, create the node
    </summary>
    <param name="value"></param>
        """
        
        GetDllLibPdf().XmpMetadata_SetAuthor.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().XmpMetadata_SetAuthor(self.Ptr, value)


    def SetProducer(self ,value:str):
        """
    <summary>
        Set producer to xmpmeta; if value is null, remove the node; if the node is null, create the node
    </summary>
    <param name="value"></param>
        """
        
        GetDllLibPdf().XmpMetadata_SetProducer.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().XmpMetadata_SetProducer(self.Ptr, value)


    def SetKeywords(self ,value:str):
        """
    <summary>
        Set keywords to xmpmeta; if value is null, remove the node; if the node is null, create the node
    </summary>
    <param name="value"></param>
        """
        
        GetDllLibPdf().XmpMetadata_SetKeywords.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().XmpMetadata_SetKeywords(self.Ptr, value)


    def SetCustomProperty(self ,field:str,value:str):
        """
    <summary>
        Set custom property to xmpmeta; if value is null, remove the node; if the node is null, create the node
    </summary>
    <param name="field"></param>
    <param name="value"></param>
        """
        
        GetDllLibPdf().XmpMetadata_SetCustomProperty.argtypes=[c_void_p ,c_wchar_p,c_wchar_p]
        GetDllLibPdf().XmpMetadata_SetCustomProperty(self.Ptr, field,value)


    def SetCreateDate(self ,dt:'DateTime'):
        """
    <summary>
        Set title to xmpmeta; if value is null, remove the node; if the node is null, create the node
    </summary>
    <param name="dt"></param>
        """
        intPtrdt:c_void_p = dt.Ptr

        GetDllLibPdf().XmpMetadata_SetCreateDate.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().XmpMetadata_SetCreateDate(self.Ptr, intPtrdt)


    def SetCreator(self ,value:str):
        """
    <summary>
        Set Creator to xmpmeta; if value is null, remove the node; if the node is null, create the node
    </summary>
    <param name="value"></param>
        """
        
        GetDllLibPdf().XmpMetadata_SetCreator.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().XmpMetadata_SetCreator(self.Ptr, value)


    def SetModifyDate(self ,dt:'DateTime'):
        """
    <summary>
        Set ModifyDates to xmpmeta; if value is null, remove the node; if the node is null, create the node
    </summary>
    <param name="dt"></param>
        """
        intPtrdt:c_void_p = dt.Ptr

        GetDllLibPdf().XmpMetadata_SetModifyDate.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().XmpMetadata_SetModifyDate(self.Ptr, intPtrdt)

