from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfRadioButtonWidgetWidgetItemCollection (  PdfStateWidgetItemCollection) :
    """
    <summary>
        Represents collection of radio box group items.
    </summary>
    """

    def get_Item(self ,index:int)->'PdfRadioButtonWidgetItem':
        """
    <summary>
        Gets the  at the specified index.
    </summary>
    <returns>Returns  object at the specified index.</returns>
        """
        
        GetDllLibPdf().PdfRadioButtonWidgetWidgetItemCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfRadioButtonWidgetWidgetItemCollection_get_Item.restype=c_void_p
        intPtr = GetDllLibPdf().PdfRadioButtonWidgetWidgetItemCollection_get_Item(self.Ptr, index)
        ret = None if intPtr==None else PdfRadioButtonWidgetItem(intPtr)
        return ret


