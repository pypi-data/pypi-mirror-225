from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfTextBoxWidgetItemCollection (  PdfCollection) :
    """
    <summary>
        Represents collection of text box group items.
    </summary>
    """

    def get_Item(self ,index:int)->'PdfTexBoxWidgetItem':
        """
    <summary>
        Gets the  at the specified index.
    </summary>
        """
        
        GetDllLibPdf().PdfTextBoxWidgetItemCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfTextBoxWidgetItemCollection_get_Item.restype=c_void_p
        intPtr = GetDllLibPdf().PdfTextBoxWidgetItemCollection_get_Item(self.Ptr, index)
        ret = None if intPtr==None else PdfTexBoxWidgetItem(intPtr)
        return ret


