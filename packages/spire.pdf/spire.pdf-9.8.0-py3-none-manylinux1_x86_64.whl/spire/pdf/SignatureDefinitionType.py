from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class SignatureDefinitionType (SpireObject) :
    """
<remarks />
    """
    @property

    def SpotLocation(self)->'SpotLocationType':
        """
<remarks />
        """
        GetDllLibPdf().SignatureDefinitionType_get_SpotLocation.argtypes=[c_void_p]
        GetDllLibPdf().SignatureDefinitionType_get_SpotLocation.restype=c_void_p
        intPtr = GetDllLibPdf().SignatureDefinitionType_get_SpotLocation(self.Ptr)
        ret = None if intPtr==None else SpotLocationType(intPtr)
        return ret


    @SpotLocation.setter
    def SpotLocation(self, value:'SpotLocationType'):
        GetDllLibPdf().SignatureDefinitionType_set_SpotLocation.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().SignatureDefinitionType_set_SpotLocation(self.Ptr, value.Ptr)

    @property

    def Intent(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().SignatureDefinitionType_get_Intent.argtypes=[c_void_p]
        GetDllLibPdf().SignatureDefinitionType_get_Intent.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().SignatureDefinitionType_get_Intent(self.Ptr))
        return ret


    @Intent.setter
    def Intent(self, value:str):
        GetDllLibPdf().SignatureDefinitionType_set_Intent.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().SignatureDefinitionType_set_Intent(self.Ptr, value)

    @property

    def SignBy(self)->'DateTime':
        """
<remarks />
        """
        GetDllLibPdf().SignatureDefinitionType_get_SignBy.argtypes=[c_void_p]
        GetDllLibPdf().SignatureDefinitionType_get_SignBy.restype=c_void_p
        intPtr = GetDllLibPdf().SignatureDefinitionType_get_SignBy(self.Ptr)
        ret = None if intPtr==None else DateTime(intPtr)
        return ret


    @SignBy.setter
    def SignBy(self, value:'DateTime'):
        GetDllLibPdf().SignatureDefinitionType_set_SignBy.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().SignatureDefinitionType_set_SignBy(self.Ptr, value.Ptr)

    @property
    def SignBySpecified(self)->bool:
        """
<remarks />
        """
        GetDllLibPdf().SignatureDefinitionType_get_SignBySpecified.argtypes=[c_void_p]
        GetDllLibPdf().SignatureDefinitionType_get_SignBySpecified.restype=c_bool
        ret = GetDllLibPdf().SignatureDefinitionType_get_SignBySpecified(self.Ptr)
        return ret

    @SignBySpecified.setter
    def SignBySpecified(self, value:bool):
        GetDllLibPdf().SignatureDefinitionType_set_SignBySpecified.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().SignatureDefinitionType_set_SignBySpecified(self.Ptr, value)

    @property

    def SigningLocation(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().SignatureDefinitionType_get_SigningLocation.argtypes=[c_void_p]
        GetDllLibPdf().SignatureDefinitionType_get_SigningLocation.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().SignatureDefinitionType_get_SigningLocation(self.Ptr))
        return ret


    @SigningLocation.setter
    def SigningLocation(self, value:str):
        GetDllLibPdf().SignatureDefinitionType_set_SigningLocation.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().SignatureDefinitionType_set_SigningLocation(self.Ptr, value)

    @property

    def SpotID(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().SignatureDefinitionType_get_SpotID.argtypes=[c_void_p]
        GetDllLibPdf().SignatureDefinitionType_get_SpotID.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().SignatureDefinitionType_get_SpotID(self.Ptr))
        return ret


    @SpotID.setter
    def SpotID(self, value:str):
        GetDllLibPdf().SignatureDefinitionType_set_SpotID.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().SignatureDefinitionType_set_SpotID(self.Ptr, value)

    @property

    def SignerName(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().SignatureDefinitionType_get_SignerName.argtypes=[c_void_p]
        GetDllLibPdf().SignatureDefinitionType_get_SignerName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().SignatureDefinitionType_get_SignerName(self.Ptr))
        return ret


    @SignerName.setter
    def SignerName(self, value:str):
        GetDllLibPdf().SignatureDefinitionType_set_SignerName.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().SignatureDefinitionType_set_SignerName(self.Ptr, value)

    @property

    def lang(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().SignatureDefinitionType_get_lang.argtypes=[c_void_p]
        GetDllLibPdf().SignatureDefinitionType_get_lang.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().SignatureDefinitionType_get_lang(self.Ptr))
        return ret


    @lang.setter
    def lang(self, value:str):
        GetDllLibPdf().SignatureDefinitionType_set_lang.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().SignatureDefinitionType_set_lang(self.Ptr, value)

