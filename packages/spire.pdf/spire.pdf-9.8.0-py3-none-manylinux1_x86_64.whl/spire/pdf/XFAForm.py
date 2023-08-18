from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class XFAForm (SpireObject) :
    """
    <summary>
        Represents XML Forms Architecture (XFA).
    </summary>
    """
#    @property
#
#    def XmlTemplate(self)->'XmlNode':
#        """
#    <summary>
#        XFA Template.
#    </summary>
#        """
#        GetDllLibPdf().XFAForm_get_XmlTemplate.argtypes=[c_void_p]
#        GetDllLibPdf().XFAForm_get_XmlTemplate.restype=c_void_p
#        intPtr = GetDllLibPdf().XFAForm_get_XmlTemplate(self.Ptr)
#        ret = None if intPtr==None else XmlNode(intPtr)
#        return ret
#


#    @property
#
#    def XmlDatasets(self)->'XmlNode':
#        """
#    <summary>
#        XFA Datasets.
#    </summary>
#        """
#        GetDllLibPdf().XFAForm_get_XmlDatasets.argtypes=[c_void_p]
#        GetDllLibPdf().XFAForm_get_XmlDatasets.restype=c_void_p
#        intPtr = GetDllLibPdf().XFAForm_get_XmlDatasets(self.Ptr)
#        ret = None if intPtr==None else XmlNode(intPtr)
#        return ret
#


#    @property
#
#    def XmlConfig(self)->'XmlNode':
#        """
#    <summary>
#        XFA Config.
#    </summary>
#        """
#        GetDllLibPdf().XFAForm_get_XmlConfig.argtypes=[c_void_p]
#        GetDllLibPdf().XFAForm_get_XmlConfig.restype=c_void_p
#        intPtr = GetDllLibPdf().XFAForm_get_XmlConfig(self.Ptr)
#        ret = None if intPtr==None else XmlNode(intPtr)
#        return ret
#


#    @property
#
#    def XmlDataPackage(self)->'XmlDocument':
#        """
#    <summary>
#        XML Data Package
#    </summary>
#        """
#        GetDllLibPdf().XFAForm_get_XmlDataPackage.argtypes=[c_void_p]
#        GetDllLibPdf().XFAForm_get_XmlDataPackage.restype=c_void_p
#        intPtr = GetDllLibPdf().XFAForm_get_XmlDataPackage(self.Ptr)
#        ret = None if intPtr==None else XmlDocument(intPtr)
#        return ret
#



    def get_Item(self ,XmlPath:str)->str:
        """
    <summary>
        Gets of sets data node value.deprecated to use,instead use xfaField to set field value.
    </summary>
        """
        
        GetDllLibPdf().XFAForm_get_Item.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().XFAForm_get_Item.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().XFAForm_get_Item(self.Ptr, XmlPath))
        return ret



    def set_Item(self ,XmlPath:str,value:str):
        """

        """
        
        GetDllLibPdf().XFAForm_set_Item.argtypes=[c_void_p ,c_wchar_p,c_wchar_p]
        GetDllLibPdf().XFAForm_set_Item(self.Ptr, XmlPath,value)

#    @property
#
#    def Fields(self)->'List1':
#        """
#
#        """
#        GetDllLibPdf().XFAForm_get_Fields.argtypes=[c_void_p]
#        GetDllLibPdf().XFAForm_get_Fields.restype=c_void_p
#        intPtr = GetDllLibPdf().XFAForm_get_Fields(self.Ptr)
#        ret = None if intPtr==None else List1(intPtr)
#        return ret
#


#    @property
#
#    def XfaFields(self)->'List1':
#        """
#
#        """
#        GetDllLibPdf().XFAForm_get_XfaFields.argtypes=[c_void_p]
#        GetDllLibPdf().XFAForm_get_XfaFields.restype=c_void_p
#        intPtr = GetDllLibPdf().XFAForm_get_XfaFields(self.Ptr)
#        ret = None if intPtr==None else List1(intPtr)
#        return ret
#


    @property
    def Count(self)->int:
        """

        """
        GetDllLibPdf().XFAForm_get_Count.argtypes=[c_void_p]
        GetDllLibPdf().XFAForm_get_Count.restype=c_int
        ret = GetDllLibPdf().XFAForm_get_Count(self.Ptr)
        return ret

#
#    def GetTemplate(self ,fieldName:str)->'XmlNode':
#        """
#    <summary>
#        Returns XML node of field tempalte. 
#    </summary>
#        """
#        
#        GetDllLibPdf().XFAForm_GetTemplate.argtypes=[c_void_p ,c_wchar_p]
#        GetDllLibPdf().XFAForm_GetTemplate.restype=c_void_p
#        intPtr = GetDllLibPdf().XFAForm_GetTemplate(self.Ptr, fieldName)
#        ret = None if intPtr==None else XmlNode(intPtr)
#        return ret
#



    def CheckFieldExists(self ,fieldName:str)->bool:
        """

        """
        
        GetDllLibPdf().XFAForm_CheckFieldExists.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().XFAForm_CheckFieldExists.restype=c_bool
        ret = GetDllLibPdf().XFAForm_CheckFieldExists(self.Ptr, fieldName)
        return ret

#
#    def GetDataSets(self)->'XmlNode':
#        """
#
#        """
#        GetDllLibPdf().XFAForm_GetDataSets.argtypes=[c_void_p]
#        GetDllLibPdf().XFAForm_GetDataSets.restype=c_void_p
#        intPtr = GetDllLibPdf().XFAForm_GetDataSets(self.Ptr)
#        ret = None if intPtr==None else XmlNode(intPtr)
#        return ret
#


#
#    def GetConfig(self)->'XmlNode':
#        """
#
#        """
#        GetDllLibPdf().XFAForm_GetConfig.argtypes=[c_void_p]
#        GetDllLibPdf().XFAForm_GetConfig.restype=c_void_p
#        intPtr = GetDllLibPdf().XFAForm_GetConfig(self.Ptr)
#        ret = None if intPtr==None else XmlNode(intPtr)
#        return ret
#



    def getField(self ,name:str)->'XfaField':
        """
    <summary>
        Added by Henry Zhou. 
            To get the xfaField through its name. Notes: the param 'name' is the name have been midified by codes instead of originals.
    </summary>
    <param name="name"></param>
    <returns></returns>
        """
        
        GetDllLibPdf().XFAForm_getField.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().XFAForm_getField.restype=c_void_p
        intPtr = GetDllLibPdf().XFAForm_getField(self.Ptr, name)
        ret = None if intPtr==None else XfaField(intPtr)
        return ret


    @staticmethod
    def FieldNameEscape()->int:
        """

        """
        #GetDllLibPdf().XFAForm_FieldNameEscape.argtypes=[]
        GetDllLibPdf().XFAForm_FieldNameEscape.restype=c_int
        ret = GetDllLibPdf().XFAForm_FieldNameEscape()
        return ret

