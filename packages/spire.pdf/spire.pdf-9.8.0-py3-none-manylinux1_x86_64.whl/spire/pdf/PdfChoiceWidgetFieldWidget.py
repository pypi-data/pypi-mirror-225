from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfChoiceWidgetFieldWidget (  PdfStyledFieldWidget) :
    """
    <summary>
        Represents a choice field of an existing PDF document`s form.
    </summary>
    """
    @property

    def Values(self)->'PdfListWidgetItemCollection':
        """
    <summary>
        Gets the collection of choice items.
    </summary>
        """
        GetDllLibPdf().PdfChoiceWidgetFieldWidget_get_Values.argtypes=[c_void_p]
        GetDllLibPdf().PdfChoiceWidgetFieldWidget_get_Values.restype=c_void_p
        intPtr = GetDllLibPdf().PdfChoiceWidgetFieldWidget_get_Values(self.Ptr)
        ret = None if intPtr==None else PdfListWidgetItemCollection(intPtr)
        return ret


    @property

    def SelectedIndex(self)->List[int]:
        """
    <summary>
        Gets or sets the first selected item in the list.
    </summary>
        """
        GetDllLibPdf().PdfChoiceWidgetFieldWidget_get_SelectedIndex.argtypes=[c_void_p]
        GetDllLibPdf().PdfChoiceWidgetFieldWidget_get_SelectedIndex.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().PdfChoiceWidgetFieldWidget_get_SelectedIndex(self.Ptr)
        ret = GetVectorFromArray(intPtrArray, c_int)
        return ret

    @SelectedIndex.setter
    def SelectedIndex(self, value:List[int]):
        vCount = len(value)
        ArrayType = c_int * vCount
        vArray = ArrayType()
        for i in range(0, vCount):
            vArray[i] = value[i]
        GetDllLibPdf().PdfChoiceWidgetFieldWidget_set_SelectedIndex.argtypes=[c_void_p, ArrayType, c_int]
        GetDllLibPdf().PdfChoiceWidgetFieldWidget_set_SelectedIndex(self.Ptr, vArray, vCount)

    @property

    def SelectedValue(self)->str:
        """
    <summary>
        Gets or sets the value of the first selected item in the list.
    </summary>
        """
        GetDllLibPdf().PdfChoiceWidgetFieldWidget_get_SelectedValue.argtypes=[c_void_p]
        GetDllLibPdf().PdfChoiceWidgetFieldWidget_get_SelectedValue.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfChoiceWidgetFieldWidget_get_SelectedValue(self.Ptr))
        return ret


    @SelectedValue.setter
    def SelectedValue(self, value:str):
        GetDllLibPdf().PdfChoiceWidgetFieldWidget_set_SelectedValue.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfChoiceWidgetFieldWidget_set_SelectedValue(self.Ptr, value)

    @property

    def SelectedWidgetItem(self)->'PdfListWidgetItemCollection':
        """
    <summary>
        Gets the first selected item in the list.
    </summary>
        """
        GetDllLibPdf().PdfChoiceWidgetFieldWidget_get_SelectedWidgetItem.argtypes=[c_void_p]
        GetDllLibPdf().PdfChoiceWidgetFieldWidget_get_SelectedWidgetItem.restype=c_void_p
        intPtr = GetDllLibPdf().PdfChoiceWidgetFieldWidget_get_SelectedWidgetItem(self.Ptr)
        ret = None if intPtr==None else PdfListWidgetItemCollection(intPtr)
        return ret


    @property

    def SelectedItem(self)->'PdfListWidgetItemCollection':
        """
    <summary>
        Gets the first selected item in the list.
    </summary>
        """
        GetDllLibPdf().PdfChoiceWidgetFieldWidget_get_SelectedItem.argtypes=[c_void_p]
        GetDllLibPdf().PdfChoiceWidgetFieldWidget_get_SelectedItem.restype=c_void_p
        intPtr = GetDllLibPdf().PdfChoiceWidgetFieldWidget_get_SelectedItem(self.Ptr)
        ret = None if intPtr==None else PdfListWidgetItemCollection(intPtr)
        return ret


    @property
    def CommitOnSelChange(self)->bool:
        """
    <summary>
        Gets or sets the flag indicating if a new value selected is committed immediately without waiting to leave the field.
    </summary>
        """
        GetDllLibPdf().PdfChoiceWidgetFieldWidget_get_CommitOnSelChange.argtypes=[c_void_p]
        GetDllLibPdf().PdfChoiceWidgetFieldWidget_get_CommitOnSelChange.restype=c_bool
        ret = GetDllLibPdf().PdfChoiceWidgetFieldWidget_get_CommitOnSelChange(self.Ptr)
        return ret

    @CommitOnSelChange.setter
    def CommitOnSelChange(self, value:bool):
        GetDllLibPdf().PdfChoiceWidgetFieldWidget_set_CommitOnSelChange.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfChoiceWidgetFieldWidget_set_CommitOnSelChange(self.Ptr, value)

    def ObjectID(self)->int:
        """
    <summary>
        Form field identifier
    </summary>
        """
        GetDllLibPdf().PdfChoiceWidgetFieldWidget_ObjectID.argtypes=[c_void_p]
        GetDllLibPdf().PdfChoiceWidgetFieldWidget_ObjectID.restype=c_int
        ret = GetDllLibPdf().PdfChoiceWidgetFieldWidget_ObjectID(self.Ptr)
        return ret

