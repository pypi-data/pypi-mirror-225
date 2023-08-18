from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfCompositeField (  PdfMultipleValueField) :
    @dispatch
    def __init__(self):
        GetDllLibPdf().PdfCompositeField_CreatePdfCompositeField.restype = c_void_p
        intPtr = GetDllLibPdf().PdfCompositeField_CreatePdfCompositeField()
        super(PdfCompositeField, self).__init__(intPtr)

    @dispatch
    def __init__(self, font:PdfFontBase,brush:PdfBrush,text:str,listAf:List[PdfAutomaticField]):
        ptrFont:c_void_p = font.Ptr
        ptrBrush:c_void_p = brush.Ptr

        countnewValues = len(listAf)
        ArrayTypenewValues = c_void_p * countnewValues
        arraynewValues = ArrayTypenewValues()
        for i in range(0, countnewValues):
            arraynewValues[i] = listAf[i].Ptr

        GetDllLibPdf().PdfCompositeField_CreatePdfCompositeFieldFBTL.argtypes=[c_void_p,c_void_p,c_wchar_p,ArrayTypenewValues,c_int]
        GetDllLibPdf().PdfCompositeField_CreatePdfCompositeFieldFBTL.restype = c_void_p
        intPtr = GetDllLibPdf().PdfCompositeField_CreatePdfCompositeFieldFBTL(ptrFont,ptrBrush,text,arraynewValues,countnewValues)
        super(PdfCompositeField, self).__init__(intPtr)
    @dispatch
    def __init__(self, font:PdfFontBase):
        ptrFont:c_void_p = font.Ptr
        GetDllLibPdf().PdfCompositeField_CreatePdfCompositeFieldF.argtypes=[c_void_p]
        GetDllLibPdf().PdfCompositeField_CreatePdfCompositeFieldF.restype = c_void_p
        intPtr = GetDllLibPdf().PdfCompositeField_CreatePdfCompositeFieldF(ptrFont)
        super(PdfCompositeField, self).__init__(intPtr)

    @dispatch
    def __init__(self, font:PdfFontBase,brush:PdfBrush):
        ptrFont:c_void_p = font.Ptr
        ptrBrush:c_void_p = brush.Ptr
        GetDllLibPdf().PdfCompositeField_CreatePdfCompositeFieldFB.argtypes=[c_void_p,c_void_p]
        GetDllLibPdf().PdfCompositeField_CreatePdfCompositeFieldFB.restype = c_void_p
        intPtr = GetDllLibPdf().PdfCompositeField_CreatePdfCompositeFieldFB(ptrFont,ptrBrush)
        super(PdfCompositeField, self).__init__(intPtr)
    @dispatch
    def __init__(self, font:PdfFontBase,text:str):
        ptrFont:c_void_p = font.Ptr
        GetDllLibPdf().PdfCompositeField_CreatePdfCompositeFieldFT.argtypes=[c_void_p,c_wchar_p]
        GetDllLibPdf().PdfCompositeField_CreatePdfCompositeFieldFT.restype = c_void_p
        intPtr = GetDllLibPdf().PdfCompositeField_CreatePdfCompositeFieldFT(ptrFont,text)
        super(PdfCompositeField, self).__init__(intPtr)
    @dispatch
    def __init__(self, font:PdfFontBase,brush:PdfBrush,text:str):
        ptrFont:c_void_p = font.Ptr
        ptrBrush:c_void_p = brush.Ptr
        GetDllLibPdf().PdfCompositeField_CreatePdfCompositeFieldFBT.argtypes=[c_void_p,c_void_p,c_wchar_p]
        GetDllLibPdf().PdfCompositeField_CreatePdfCompositeFieldFBT.restype = c_void_p
        intPtr = GetDllLibPdf().PdfCompositeField_CreatePdfCompositeFieldFBT(ptrFont,ptrBrush,text)
        super(PdfCompositeField, self).__init__(intPtr)

    @dispatch
    def __init__(self,text:str,listAf:List[PdfAutomaticField]):

        countnewValues = len(listAf)
        ArrayTypenewValues = c_void_p * countnewValues
        arraynewValues = ArrayTypenewValues()
        for i in range(0, countnewValues):
            arraynewValues[i] = listAf[i].Ptr

        GetDllLibPdf().PdfCompositeField_CreatePdfCompositeFieldTL.argtypes=[c_wchar_p,ArrayTypenewValues,c_int]
        GetDllLibPdf().PdfCompositeField_CreatePdfCompositeFieldTL.restype = c_void_p
        intPtr = GetDllLibPdf().PdfCompositeField_CreatePdfCompositeFieldTL(text,arraynewValues,countnewValues)
        super(PdfCompositeField, self).__init__(intPtr)
    @dispatch
    def __init__(self, font:PdfFontBase,text:str,listAf:List[PdfAutomaticField]):
        ptrFont:c_void_p = font.Ptr

        countnewValues = len(listAf)
        ArrayTypenewValues = c_void_p * countnewValues
        arraynewValues = ArrayTypenewValues()
        for i in range(0, countnewValues):
            arraynewValues[i] = listAf[i].Ptr

        GetDllLibPdf().PdfCompositeField_CreatePdfCompositeFieldFTL.argtypes=[c_void_p,c_wchar_p,ArrayTypenewValues,c_int]
        GetDllLibPdf().PdfCompositeField_CreatePdfCompositeFieldFTL.restype = c_void_p
        intPtr = GetDllLibPdf().PdfCompositeField_CreatePdfCompositeFieldFTL(ptrFont,text,arraynewValues,countnewValues)
        super(PdfCompositeField, self).__init__(intPtr)
    """
    <summary>
        Represents class which can concatenate multiple automatic fields into single string.
    </summary>
    """
    @property

    def Text(self)->str:
        """
    <summary>
        Gets or sets the text.
    </summary>
<value>The wide-character string to be drawn.</value>
        """
        GetDllLibPdf().PdfCompositeField_get_Text.argtypes=[c_void_p]
        GetDllLibPdf().PdfCompositeField_get_Text.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfCompositeField_get_Text(self.Ptr))
        return ret


    @Text.setter
    def Text(self, value:str):
        GetDllLibPdf().PdfCompositeField_set_Text.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfCompositeField_set_Text(self.Ptr, value)

    @property

    def AutomaticFields(self)->List['PdfAutomaticField']:
        """
    <summary>
        Gets or sets the automatic fields.
    </summary>
<value>The automatic fields.</value>
        """
        GetDllLibPdf().PdfCompositeField_get_AutomaticFields.argtypes=[c_void_p]
        GetDllLibPdf().PdfCompositeField_get_AutomaticFields.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().PdfCompositeField_get_AutomaticFields(self.Ptr)
        ret = GetVectorFromArray(intPtrArray, PdfAutomaticField)
        return ret


    @AutomaticFields.setter
    def AutomaticFields(self, value:List['PdfAutomaticField']):
        vCount = len(value)
        ArrayType = c_void_p * vCount
        vArray = ArrayType()
        for i in range(0, vCount):
            vArray[i] = value[i].Ptr
        GetDllLibPdf().PdfCompositeField_set_AutomaticFields.argtypes=[c_void_p, ArrayType, c_int]
        GetDllLibPdf().PdfCompositeField_set_AutomaticFields(self.Ptr, vArray, vCount)


