from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfStateItemCollection (  PdfCollection) :
    """
    <summary>
        Represents state item collection.
    </summary>
    """

    def get_Item(self ,index:int)->'PdfStateWidgetItem':
        """
    <summary>
        Gets the  at the specified index.
    </summary>
<value>The index of specified  item.</value>
        """
        
        GetDllLibPdf().PdfStateItemCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfStateItemCollection_get_Item.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStateItemCollection_get_Item(self.Ptr, index)
        ret = None if intPtr==None else PdfStateWidgetItem(intPtr)
        return ret


