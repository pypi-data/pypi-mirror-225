from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfFormFieldWidgetCollection (  PdfFieldCollection) :
    """
    <summary>
        Represents field collection of loaded form.
    </summary>
    """
    @dispatch

    def get_Item(self ,index:int)->PdfField:
        """
    <summary>
        Gets the  at the specified index.
    </summary>
        """
        
        GetDllLibPdf().PdfFormFieldWidgetCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfFormFieldWidgetCollection_get_Item.restype=IntPtrWithTypeName
        intPtr = GetDllLibPdf().PdfFormFieldWidgetCollection_get_Item(self.Ptr, index)
        ret = None if intPtr==None else self._create(intPtr)
        return ret

    def _create(self, intPtrWithTypeName:IntPtrWithTypeName)->PdfField:
        ret = None
        if intPtrWithTypeName == None :
            return ret
        intPtr = intPtrWithTypeName.intPtr[0] + (intPtrWithTypeName.intPtr[1]<<32)
        strName = PtrToStr(intPtrWithTypeName.typeName)
        if(strName == 'Spire.Pdf.Widget.PdfTextBoxFieldWidget'):
            ret = PdfTextBoxFieldWidget(intPtr)
        elif (strName == 'Spire.Pdf.Widget.PdfCheckBoxWidgetFieldWidget'):
            ret = PdfCheckBoxWidgetFieldWidget(intPtr)
        elif (strName == 'Spire.Pdf.Widget.PdfRadioButtonListFieldWidget'):
            ret = PdfRadioButtonListFieldWidget(intPtr)
        elif (strName == 'Spire.Pdf.Widget.PdfListBoxWidgetFieldWidget'):
            ret = PdfListBoxWidgetFieldWidget(intPtr)
        elif (strName == 'Spire.Pdf.Widget.PdfComboBoxWidgetFieldWidget'):
            ret = PdfComboBoxWidgetFieldWidget(intPtr)
        elif (strName == 'Spire.Pdf.Annotations.PdfRubberStampAnnotationWidget'):
            ret = PdfRubberStampAnnotationWidget(intPtr)
        elif (strName == 'Spire.Pdf.Widget.PdfButtonWidgetFieldWidget'):
            ret = PdfButtonWidgetFieldWidget(intPtr)
        else:
            ret = PdfField(intPtr)
        return ret

    @dispatch

    def get_Item(self ,name:str)->PdfField:
        """
    <summary>
        Returns field with specified name.
    </summary>
    <param name="name">The specified field name.</param>
        """
        
        GetDllLibPdf().PdfFormFieldWidgetCollection_get_ItemN.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfFormFieldWidgetCollection_get_ItemN.restype=c_void_p
        intPtr = GetDllLibPdf().PdfFormFieldWidgetCollection_get_ItemN(self.Ptr, name)
        ret = None if intPtr==None else PdfField(intPtr)
        return ret


    @property

    def FormWidget(self)->'PdfFormWidget':
        """
    <summary>
        Gets or sets the form.
    </summary>
        """
        GetDllLibPdf().PdfFormFieldWidgetCollection_get_FormWidget.argtypes=[c_void_p]
        GetDllLibPdf().PdfFormFieldWidgetCollection_get_FormWidget.restype=c_void_p
        intPtr = GetDllLibPdf().PdfFormFieldWidgetCollection_get_FormWidget(self.Ptr)
        ret = None if intPtr==None else PdfFormWidget(intPtr)
        return ret


    @FormWidget.setter
    def FormWidget(self, value:'PdfFormWidget'):
        GetDllLibPdf().PdfFormFieldWidgetCollection_set_FormWidget.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfFormFieldWidgetCollection_set_FormWidget(self.Ptr, value.Ptr)

#    @property
#
#    def FieldNames(self)->'List1':
#        """
#    <summary>
#        Field Signature Names
#    </summary>
#        """
#        GetDllLibPdf().PdfFormFieldWidgetCollection_get_FieldNames.argtypes=[c_void_p]
#        GetDllLibPdf().PdfFormFieldWidgetCollection_get_FieldNames.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfFormFieldWidgetCollection_get_FieldNames(self.Ptr)
#        ret = None if intPtr==None else List1(intPtr)
#        return ret
#


#
#    def GetFieldNameByExportValue(self ,exportValue:str)->'List1':
#        """
#    <summary>
#        Get FieldName from FormWidget by exportValue
#    </summary>
#    <param name="exportValue"></param>
#    <returns></returns>
#        """
#        
#        GetDllLibPdf().PdfFormFieldWidgetCollection_GetFieldNameByExportValue.argtypes=[c_void_p ,c_wchar_p]
#        GetDllLibPdf().PdfFormFieldWidgetCollection_GetFieldNameByExportValue.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfFormFieldWidgetCollection_GetFieldNameByExportValue(self.Ptr, exportValue)
#        ret = None if intPtr==None else List1(intPtr)
#        return ret
#


#
#    def GetFieldsByExportValue(self ,exportValue:str)->'List1':
#        """
#    <summary>
#        Get Fields from FormWidget by exportValue
#    </summary>
#    <param name="exportValue"></param>
#    <returns></returns>
#        """
#        
#        GetDllLibPdf().PdfFormFieldWidgetCollection_GetFieldsByExportValue.argtypes=[c_void_p ,c_wchar_p]
#        GetDllLibPdf().PdfFormFieldWidgetCollection_GetFieldsByExportValue.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfFormFieldWidgetCollection_GetFieldsByExportValue(self.Ptr, exportValue)
#        ret = None if intPtr==None else List1(intPtr)
#        return ret
#


