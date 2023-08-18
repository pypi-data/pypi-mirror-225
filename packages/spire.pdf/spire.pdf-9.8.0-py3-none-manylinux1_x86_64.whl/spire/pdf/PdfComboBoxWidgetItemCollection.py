from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfComboBoxWidgetItemCollection (  PdfCollection) :
    """
    <summary>
        Represents collection of Combo box items.
    </summary>
    """

    def get_Item(self ,index:int)->'PdfComboBoxWidgetWidgetItem':
        """
    <summary>
        Gets the  at the specified index.
    </summary>
        """
        
        GetDllLibPdf().PdfComboBoxWidgetItemCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfComboBoxWidgetItemCollection_get_Item.restype=c_void_p
        intPtr = GetDllLibPdf().PdfComboBoxWidgetItemCollection_get_Item(self.Ptr, index)
        ret = None if intPtr==None else PdfComboBoxWidgetWidgetItem(intPtr)
        return ret


