from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfListWidgetFieldItemCollection (  PdfCollection) :
    """
    <summary>
        Represents loaded item collection.
    </summary>
    """

    def get_Item(self ,index:int)->'PdfListFieldWidgetItem':
        """
    <summary>
        Gets the  at the specified index.
    </summary>
        """
        
        GetDllLibPdf().PdfListWidgetFieldItemCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfListWidgetFieldItemCollection_get_Item.restype=c_void_p
        intPtr = GetDllLibPdf().PdfListWidgetFieldItemCollection_get_Item(self.Ptr, index)
        ret = None if intPtr==None else PdfListFieldWidgetItem(intPtr)
        return ret


