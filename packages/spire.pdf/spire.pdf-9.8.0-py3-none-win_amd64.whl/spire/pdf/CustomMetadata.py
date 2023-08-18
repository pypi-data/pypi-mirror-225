from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class CustomMetadata (  XmpSchema) :
    """
    <summary>
        Represents custom Metadata.
    </summary>
    """

    def get_Item(self ,name:str)->str:
        """
    <summary>
        Sets the xmp property.
    </summary>
        """
        
        GetDllLibPdf().CustomMetadata_get_Item.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().CustomMetadata_get_Item.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().CustomMetadata_get_Item(self.Ptr, name))
        return ret



    def set_Item(self ,name:str,value:str):
        """

        """
        
        GetDllLibPdf().CustomMetadata_set_Item.argtypes=[c_void_p ,c_wchar_p,c_wchar_p]
        GetDllLibPdf().CustomMetadata_set_Item(self.Ptr, name,value)

    @property

    def SchemaType(self)->'XmpSchemaType':
        """
    <summary>
        Gets type of the schema.
    </summary>
        """
        GetDllLibPdf().CustomMetadata_get_SchemaType.argtypes=[c_void_p]
        GetDllLibPdf().CustomMetadata_get_SchemaType.restype=c_int
        ret = GetDllLibPdf().CustomMetadata_get_SchemaType(self.Ptr)
        objwraped = XmpSchemaType(ret)
        return objwraped

