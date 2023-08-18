from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfStructureAttributes (SpireObject) :
    """
    <summary>
        The attribute information is held in one or more attribute objects
            associated with the structure element.
    </summary>
    """
    @property

    def Owner(self)->'PdfAttributeOwner':
        """

        """
        GetDllLibPdf().PdfStructureAttributes_get_Owner.argtypes=[c_void_p]
        GetDllLibPdf().PdfStructureAttributes_get_Owner.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStructureAttributes_get_Owner(self.Ptr)
        ret = None if intPtr==None else PdfAttributeOwner(intPtr)
        return ret



    def GetNameValue(self ,key:str)->str:
        """
    <summary>
        Get the attribute value.
    </summary>
    <param name="key">The attribute key.</param>
    <returns>The attribute value.</returns>
        """
        
        GetDllLibPdf().PdfStructureAttributes_GetNameValue.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfStructureAttributes_GetNameValue.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfStructureAttributes_GetNameValue(self.Ptr, key))
        return ret



    def SetNameValue(self ,key:str,value:str):
        """
    <summary>
        Set attribute value.
    </summary>
    <param name="key">The attribute key.</param>
    <param name="value">The attribute value.</param>
        """
        
        GetDllLibPdf().PdfStructureAttributes_SetNameValue.argtypes=[c_void_p ,c_wchar_p,c_wchar_p]
        GetDllLibPdf().PdfStructureAttributes_SetNameValue(self.Ptr, key,value)


    def GetNameArrayValue(self ,key:str)->List[str]:
        """
    <summary>
        Get the attribute value.
    </summary>
    <param name="key">The attribute key.</param>
    <returns>The attribute value.</returns>
        """
        
        GetDllLibPdf().PdfStructureAttributes_GetNameArrayValue.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfStructureAttributes_GetNameArrayValue.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().PdfStructureAttributes_GetNameArrayValue(self.Ptr, key)
        ret = GetStrVectorFromArray(intPtrArray, c_void_p)
        return ret


    def SetNameArrayValue(self ,key:str,value:List[str]):
        """
    <summary>
        Set attribute value.
    </summary>
    <param name="key">The attribute key.</param>
    <param name="value">The attribute value.</param>
        """
        #arrayvalue:ArrayTypevalue = ""
        countvalue = len(value)
        ArrayTypevalue = c_wchar_p * countvalue
        arrayvalue = ArrayTypevalue()
        for i in range(0, countvalue):
            arrayvalue[i] = value[i]


        GetDllLibPdf().PdfStructureAttributes_SetNameArrayValue.argtypes=[c_void_p ,c_wchar_p,ArrayTypevalue]
        GetDllLibPdf().PdfStructureAttributes_SetNameArrayValue(self.Ptr, key,arrayvalue)

#
#    def GetNumberValue(self ,key:str)->'Nullable1':
#        """
#    <summary>
#        Get the attribute value.
#    </summary>
#    <param name="key">The attribute key.</param>
#    <returns>The attribute value.</returns>
#        """
#        
#        GetDllLibPdf().PdfStructureAttributes_GetNumberValue.argtypes=[c_void_p ,c_wchar_p]
#        GetDllLibPdf().PdfStructureAttributes_GetNumberValue.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfStructureAttributes_GetNumberValue(self.Ptr, key)
#        ret = None if intPtr==None else Nullable1(intPtr)
#        return ret
#


#
#    def SetNumberValue(self ,key:str,value:'Nullable1'):
#        """
#    <summary>
#        Set attribute value.
#    </summary>
#    <param name="key">The attribute key.</param>
#    <param name="value">The attribute value.</param>
#        """
#        intPtrvalue:c_void_p = value.Ptr
#
#        GetDllLibPdf().PdfStructureAttributes_SetNumberValue.argtypes=[c_void_p ,c_wchar_p,c_void_p]
#        GetDllLibPdf().PdfStructureAttributes_SetNumberValue(self.Ptr, key,intPtrvalue)


#
#    def GetNumberArrayValue(self ,key:str)->List['Nullable1']:
#        """
#    <summary>
#        Get the attribute value.
#    </summary>
#    <param name="key">The attribute key.</param>
#    <returns>The attribute value.</returns>
#        """
#        
#        GetDllLibPdf().PdfStructureAttributes_GetNumberArrayValue.argtypes=[c_void_p ,c_wchar_p]
#        GetDllLibPdf().PdfStructureAttributes_GetNumberArrayValue.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().PdfStructureAttributes_GetNumberArrayValue(self.Ptr, key)
#        ret = GetObjVectorFromArray(intPtrArray, Nullable1)
#        return ret


#
#    def SetNumberArrayValue(self ,key:str,value:'Nullable1[]'):
#        """
#    <summary>
#        Set attribute value.
#    </summary>
#    <param name="key">The attribute key.</param>
#    <param name="value">The attribute value.</param>
#        """
#        #arrayvalue:ArrayTypevalue = ""
#        countvalue = len(value)
#        ArrayTypevalue = c_void_p * countvalue
#        arrayvalue = ArrayTypevalue()
#        for i in range(0, countvalue):
#            arrayvalue[i] = value[i].Ptr
#
#
#        GetDllLibPdf().PdfStructureAttributes_SetNumberArrayValue.argtypes=[c_void_p ,c_wchar_p,ArrayTypevalue]
#        GetDllLibPdf().PdfStructureAttributes_SetNumberArrayValue(self.Ptr, key,arrayvalue)


