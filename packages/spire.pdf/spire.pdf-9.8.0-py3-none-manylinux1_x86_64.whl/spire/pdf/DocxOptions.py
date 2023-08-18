from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class DocxOptions (SpireObject) :
    """
    <summary>
        the pdf document convert to docx document,set the options
    </summary>
    """
    @property

    def Title(self)->str:
        """

        """
        GetDllLibPdf().DocxOptions_get_Title.argtypes=[c_void_p]
        GetDllLibPdf().DocxOptions_get_Title.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().DocxOptions_get_Title(self.Ptr))
        return ret


    @Title.setter
    def Title(self, value:str):
        GetDllLibPdf().DocxOptions_set_Title.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().DocxOptions_set_Title(self.Ptr, value)

    @property

    def Subject(self)->str:
        """

        """
        GetDllLibPdf().DocxOptions_get_Subject.argtypes=[c_void_p]
        GetDllLibPdf().DocxOptions_get_Subject.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().DocxOptions_get_Subject(self.Ptr))
        return ret


    @Subject.setter
    def Subject(self, value:str):
        GetDllLibPdf().DocxOptions_set_Subject.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().DocxOptions_set_Subject(self.Ptr, value)

    @property

    def Tags(self)->str:
        """

        """
        GetDllLibPdf().DocxOptions_get_Tags.argtypes=[c_void_p]
        GetDllLibPdf().DocxOptions_get_Tags.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().DocxOptions_get_Tags(self.Ptr))
        return ret


    @Tags.setter
    def Tags(self, value:str):
        GetDllLibPdf().DocxOptions_set_Tags.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().DocxOptions_set_Tags(self.Ptr, value)

    @property

    def Categories(self)->str:
        """

        """
        GetDllLibPdf().DocxOptions_get_Categories.argtypes=[c_void_p]
        GetDllLibPdf().DocxOptions_get_Categories.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().DocxOptions_get_Categories(self.Ptr))
        return ret


    @Categories.setter
    def Categories(self, value:str):
        GetDllLibPdf().DocxOptions_set_Categories.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().DocxOptions_set_Categories(self.Ptr, value)

    @property

    def Commments(self)->str:
        """

        """
        GetDllLibPdf().DocxOptions_get_Commments.argtypes=[c_void_p]
        GetDllLibPdf().DocxOptions_get_Commments.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().DocxOptions_get_Commments(self.Ptr))
        return ret


    @Commments.setter
    def Commments(self, value:str):
        GetDllLibPdf().DocxOptions_set_Commments.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().DocxOptions_set_Commments(self.Ptr, value)

    @property

    def Authors(self)->str:
        """

        """
        GetDllLibPdf().DocxOptions_get_Authors.argtypes=[c_void_p]
        GetDllLibPdf().DocxOptions_get_Authors.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().DocxOptions_get_Authors(self.Ptr))
        return ret


    @Authors.setter
    def Authors(self, value:str):
        GetDllLibPdf().DocxOptions_set_Authors.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().DocxOptions_set_Authors(self.Ptr, value)

    @property

    def LastSavedBy(self)->str:
        """

        """
        GetDllLibPdf().DocxOptions_get_LastSavedBy.argtypes=[c_void_p]
        GetDllLibPdf().DocxOptions_get_LastSavedBy.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().DocxOptions_get_LastSavedBy(self.Ptr))
        return ret


    @LastSavedBy.setter
    def LastSavedBy(self, value:str):
        GetDllLibPdf().DocxOptions_set_LastSavedBy.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().DocxOptions_set_LastSavedBy(self.Ptr, value)

    @property
    def Revision(self)->int:
        """

        """
        GetDllLibPdf().DocxOptions_get_Revision.argtypes=[c_void_p]
        GetDllLibPdf().DocxOptions_get_Revision.restype=c_int
        ret = GetDllLibPdf().DocxOptions_get_Revision(self.Ptr)
        return ret

    @Revision.setter
    def Revision(self, value:int):
        GetDllLibPdf().DocxOptions_set_Revision.argtypes=[c_void_p, c_int]
        GetDllLibPdf().DocxOptions_set_Revision(self.Ptr, value)

    @property

    def Version(self)->str:
        """

        """
        GetDllLibPdf().DocxOptions_get_Version.argtypes=[c_void_p]
        GetDllLibPdf().DocxOptions_get_Version.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().DocxOptions_get_Version(self.Ptr))
        return ret


    @Version.setter
    def Version(self, value:str):
        GetDllLibPdf().DocxOptions_set_Version.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().DocxOptions_set_Version(self.Ptr, value)

    @property

    def ProgramName(self)->str:
        """

        """
        GetDllLibPdf().DocxOptions_get_ProgramName.argtypes=[c_void_p]
        GetDllLibPdf().DocxOptions_get_ProgramName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().DocxOptions_get_ProgramName(self.Ptr))
        return ret


    @ProgramName.setter
    def ProgramName(self, value:str):
        GetDllLibPdf().DocxOptions_set_ProgramName.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().DocxOptions_set_ProgramName(self.Ptr, value)

    @property

    def Company(self)->str:
        """

        """
        GetDllLibPdf().DocxOptions_get_Company.argtypes=[c_void_p]
        GetDllLibPdf().DocxOptions_get_Company.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().DocxOptions_get_Company(self.Ptr))
        return ret


    @Company.setter
    def Company(self, value:str):
        GetDllLibPdf().DocxOptions_set_Company.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().DocxOptions_set_Company(self.Ptr, value)

    @property

    def Manager(self)->str:
        """

        """
        GetDllLibPdf().DocxOptions_get_Manager.argtypes=[c_void_p]
        GetDllLibPdf().DocxOptions_get_Manager.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().DocxOptions_get_Manager(self.Ptr))
        return ret


    @Manager.setter
    def Manager(self, value:str):
        GetDllLibPdf().DocxOptions_set_Manager.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().DocxOptions_set_Manager(self.Ptr, value)

