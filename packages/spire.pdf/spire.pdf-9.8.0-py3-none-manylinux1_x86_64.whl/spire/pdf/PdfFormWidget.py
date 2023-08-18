from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfFormWidget (  PdfForm) :
    """
    <summary>
        Represents Loaded form.
    </summary>
    """
    @property

    def FieldsWidget(self)->'PdfFormFieldWidgetCollection':
        """
    <summary>
        Gets the field collection.
    </summary>
        """
        GetDllLibPdf().PdfFormWidget_get_FieldsWidget.argtypes=[c_void_p]
        GetDllLibPdf().PdfFormWidget_get_FieldsWidget.restype=c_void_p
        intPtr = GetDllLibPdf().PdfFormWidget_get_FieldsWidget(self.Ptr)
        ret = None if intPtr==None else PdfFormFieldWidgetCollection(intPtr)
        return ret


    @property
    def ReadOnly(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether the form is read only.
    </summary>
<value>True if the field is read-only, false otherwise. Default is false.</value>
        """
        GetDllLibPdf().PdfFormWidget_get_ReadOnly.argtypes=[c_void_p]
        GetDllLibPdf().PdfFormWidget_get_ReadOnly.restype=c_bool
        ret = GetDllLibPdf().PdfFormWidget_get_ReadOnly(self.Ptr)
        return ret

    @ReadOnly.setter
    def ReadOnly(self, value:bool):
        GetDllLibPdf().PdfFormWidget_set_ReadOnly.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfFormWidget_set_ReadOnly(self.Ptr, value)

    @property

    def XFAForm(self)->'XFAForm':
        """
    <summary>
        Gets XFA data of the form.
    </summary>
        """
        GetDllLibPdf().PdfFormWidget_get_XFAForm.argtypes=[c_void_p]
        GetDllLibPdf().PdfFormWidget_get_XFAForm.restype=c_void_p
        intPtr = GetDllLibPdf().PdfFormWidget_get_XFAForm(self.Ptr)
        ret = None if intPtr==None else XFAForm(intPtr)
        return ret


    @property
    def IsDynamicForm(self)->bool:
        """

        """
        GetDllLibPdf().PdfFormWidget_get_IsDynamicForm.argtypes=[c_void_p]
        GetDllLibPdf().PdfFormWidget_get_IsDynamicForm.restype=c_bool
        ret = GetDllLibPdf().PdfFormWidget_get_IsDynamicForm(self.Ptr)
        return ret

    @property
    def NeedAppearances(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether need appearances.
    </summary>
        """
        GetDllLibPdf().PdfFormWidget_get_NeedAppearances.argtypes=[c_void_p]
        GetDllLibPdf().PdfFormWidget_get_NeedAppearances.restype=c_bool
        ret = GetDllLibPdf().PdfFormWidget_get_NeedAppearances(self.Ptr)
        return ret

    @NeedAppearances.setter
    def NeedAppearances(self, value:bool):
        GetDllLibPdf().PdfFormWidget_set_NeedAppearances.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfFormWidget_set_NeedAppearances(self.Ptr, value)


    def SetFieldValueForXFAForm(self ,field:'PdfField',value:str)->bool:
        """

        """
        intPtrfield:c_void_p = field.Ptr

        GetDllLibPdf().PdfFormWidget_SetFieldValueForXFAForm.argtypes=[c_void_p ,c_void_p,c_wchar_p]
        GetDllLibPdf().PdfFormWidget_SetFieldValueForXFAForm.restype=c_bool
        ret = GetDllLibPdf().PdfFormWidget_SetFieldValueForXFAForm(self.Ptr, intPtrfield,value)
        return ret

    @dispatch

    def ExportData(self ,fileName:str,dataFormat:DataFormat,formName:str):
        """
    <summary>
        Export the form data to a file.
    </summary>
    <param name="fileName">Name of the document which is need to export.</param>
    <param name="dataFormat">The format of exported data.</param>
    <param name="formName"> The name of the PDF file the data is exported from.</param>
        """
        enumdataFormat:c_int = dataFormat.value

        GetDllLibPdf().PdfFormWidget_ExportData.argtypes=[c_void_p ,c_wchar_p,c_int,c_wchar_p]
        GetDllLibPdf().PdfFormWidget_ExportData(self.Ptr, fileName,enumdataFormat,formName)

    @dispatch

    def ExportData(self ,stream:Stream,dataFormat:DataFormat,formName:str):
        """
    <summary>
        Export the form data to a file.
    </summary>
    <param name="fileName">The stream where form data will be exported.</param>
    <param name="dataFormat">The format of exported data</param>
    <param name="formName"> The name of the PDF file the data is exported from</param>
        """
        intPtrstream:c_void_p = stream.Ptr
        enumdataFormat:c_int = dataFormat.value

        GetDllLibPdf().PdfFormWidget_ExportDataSDF.argtypes=[c_void_p ,c_void_p,c_int,c_wchar_p]
        GetDllLibPdf().PdfFormWidget_ExportDataSDF(self.Ptr, intPtrstream,enumdataFormat,formName)

    @dispatch

    def ImportData(self ,fileName:str,dataFormat:DataFormat):
        """
    <summary>
        Imports the data.
    </summary>
    <param name="fileName">Name of the file.</param>
    <param name="dataFormat">The data format.</param>
        """
        enumdataFormat:c_int = dataFormat.value

        GetDllLibPdf().PdfFormWidget_ImportData.argtypes=[c_void_p ,c_wchar_p,c_int]
        GetDllLibPdf().PdfFormWidget_ImportData(self.Ptr, fileName,enumdataFormat)


    def ImportDataXFDF(self ,fileName:str):
        """
    <summary>
        Import form data from XFDF file.
    </summary>
    <param name="fileName"></param>
        """
        
        GetDllLibPdf().PdfFormWidget_ImportDataXFDF.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfFormWidget_ImportDataXFDF(self.Ptr, fileName)

#    @dispatch
#
#    def ImportData(self ,fileName:str,dataFormat:DataFormat,errorFlag:bool)->List[PdfFieldWidgetImportError]:
#        """
#    <summary>
#        Imports the data.
#    </summary>
#    <param name="fileName">Name of the file.</param>
#    <param name="dataFormat">The data format.</param>
#    <param name="errorFlag">if it is error flag, set to <c>true</c>.</param>
#    <returns></returns>
#        """
#        enumdataFormat:c_int = dataFormat.value
#
#        GetDllLibPdf().PdfFormWidget_ImportDataFDE.argtypes=[c_void_p ,c_wchar_p,c_int,c_bool]
#        GetDllLibPdf().PdfFormWidget_ImportDataFDE.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().PdfFormWidget_ImportDataFDE(self.Ptr, fileName,enumdataFormat,errorFlag)
#        ret = GetObjVectorFromArray(intPtrArray, PdfFieldWidgetImportError)
#        return ret


#
#    def ImportDataFDF(self ,stream:'Stream',continueImportOnError:bool)->List['PdfFieldWidgetImportError']:
#        """
#    <summary>
#        Import form data from FDF file.
#    </summary>
#    <param name="stream">The FDF file stream</param>
#    <param name="continueImportOnError">False if the import should stop on the first field that generates an error, or true if the import should ignore the error and continue with the next field.</param>
#    <returns>Document form fields filled with data which are imported from FDF.</returns>
#        """
#        intPtrstream:c_void_p = stream.Ptr
#
#        GetDllLibPdf().PdfFormWidget_ImportDataFDF.argtypes=[c_void_p ,c_void_p,c_bool]
#        GetDllLibPdf().PdfFormWidget_ImportDataFDF.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().PdfFormWidget_ImportDataFDF(self.Ptr, intPtrstream,continueImportOnError)
#        ret = GetObjVectorFromArray(intPtrArray, PdfFieldWidgetImportError)
#        return ret



    def HighlightFields(self ,highlight:bool):
        """
    <summary>
        Sets/Resets the form field highlight option.
    </summary>
        """
        
        GetDllLibPdf().PdfFormWidget_HighlightFields.argtypes=[c_void_p ,c_bool]
        GetDllLibPdf().PdfFormWidget_HighlightFields(self.Ptr, highlight)


    def OnlyHexInString(self ,test:str)->bool:
        """
    <summary>
        Called when [hex in string].
    </summary>
    <param name="test">The test.</param>
    <returns></returns>
        """
        
        GetDllLibPdf().PdfFormWidget_OnlyHexInString.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfFormWidget_OnlyHexInString.restype=c_bool
        ret = GetDllLibPdf().PdfFormWidget_OnlyHexInString(self.Ptr, test)
        return ret

#
#    def ExtractSignatureAsImages(self)->List['Image']:
#        """
#    <summary>
#        Extract Images from Signature
#    </summary>
#    <returns></returns>
#        """
#        GetDllLibPdf().PdfFormWidget_ExtractSignatureAsImages.argtypes=[c_void_p]
#        GetDllLibPdf().PdfFormWidget_ExtractSignatureAsImages.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().PdfFormWidget_ExtractSignatureAsImages(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, Image)
#        return ret


