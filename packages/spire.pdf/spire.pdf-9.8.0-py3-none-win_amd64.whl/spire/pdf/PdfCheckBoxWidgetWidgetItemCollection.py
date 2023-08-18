from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfCheckBoxWidgetWidgetItemCollection (  PdfStateWidgetItemCollection) :
    """
    <summary>
        Represents collection of text box group items.
    </summary>
    """

    def get_Item(self ,index:int)->'PdfCheckBoxWidgetWidgetItem':
        """
    <summary>
        Gets the  at the specified index.
    </summary>
        """
        
        GetDllLibPdf().PdfCheckBoxWidgetWidgetItemCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfCheckBoxWidgetWidgetItemCollection_get_Item.restype=c_void_p
        intPtr = GetDllLibPdf().PdfCheckBoxWidgetWidgetItemCollection_get_Item(self.Ptr, index)
        ret = None if intPtr==None else PdfCheckBoxWidgetWidgetItem(intPtr)
        return ret


