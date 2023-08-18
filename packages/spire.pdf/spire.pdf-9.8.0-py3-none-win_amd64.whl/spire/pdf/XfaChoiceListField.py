from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class XfaChoiceListField (  XfaField) :
    """

    """
    @property
    def IsMultiSelect(self)->bool:
        """

        """
        GetDllLibPdf().XfaChoiceListField_get_IsMultiSelect.argtypes=[c_void_p]
        GetDllLibPdf().XfaChoiceListField_get_IsMultiSelect.restype=c_bool
        ret = GetDllLibPdf().XfaChoiceListField_get_IsMultiSelect(self.Ptr)
        return ret

#    @property
#
#    def Items(self)->'List1':
#        """
#
#        """
#        GetDllLibPdf().XfaChoiceListField_get_Items.argtypes=[c_void_p]
#        GetDllLibPdf().XfaChoiceListField_get_Items.restype=c_void_p
#        intPtr = GetDllLibPdf().XfaChoiceListField_get_Items(self.Ptr)
#        ret = None if intPtr==None else List1(intPtr)
#        return ret
#



    def GetEvents(self)->str:
        """

        """
        GetDllLibPdf().XfaChoiceListField_GetEvents.argtypes=[c_void_p]
        GetDllLibPdf().XfaChoiceListField_GetEvents.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().XfaChoiceListField_GetEvents(self.Ptr))
        return ret


    @property

    def SelectedItem(self)->str:
        """

        """
        GetDllLibPdf().XfaChoiceListField_get_SelectedItem.argtypes=[c_void_p]
        GetDllLibPdf().XfaChoiceListField_get_SelectedItem.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().XfaChoiceListField_get_SelectedItem(self.Ptr))
        return ret


    @SelectedItem.setter
    def SelectedItem(self, value:str):
        GetDllLibPdf().XfaChoiceListField_set_SelectedItem.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().XfaChoiceListField_set_SelectedItem(self.Ptr, value)

#    @property
#
#    def SelectedItems(self)->'List1':
#        """
#
#        """
#        GetDllLibPdf().XfaChoiceListField_get_SelectedItems.argtypes=[c_void_p]
#        GetDllLibPdf().XfaChoiceListField_get_SelectedItems.restype=c_void_p
#        intPtr = GetDllLibPdf().XfaChoiceListField_get_SelectedItems(self.Ptr)
#        ret = None if intPtr==None else List1(intPtr)
#        return ret
#


#    @SelectedItems.setter
#    def SelectedItems(self, value:'List1'):
#        GetDllLibPdf().XfaChoiceListField_set_SelectedItems.argtypes=[c_void_p, c_void_p]
#        GetDllLibPdf().XfaChoiceListField_set_SelectedItems(self.Ptr, value.Ptr)


