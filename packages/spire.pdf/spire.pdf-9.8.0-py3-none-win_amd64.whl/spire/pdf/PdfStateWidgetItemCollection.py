from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfStateWidgetItemCollection (  PdfCollection) :
    """
    <summary>
        Represents the collection of loaded state item.
    </summary>
    """

    def get_Item(self ,index:int)->'PdfStateWidgetItem':
        """
    <summary>
        Gets the  at the specified index.
    </summary>
        """
        
        GetDllLibPdf().PdfStateWidgetItemCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfStateWidgetItemCollection_get_Item.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStateWidgetItemCollection_get_Item(self.Ptr, index)
        ret = None if intPtr==None else PdfStateWidgetItem(intPtr)
        return ret


