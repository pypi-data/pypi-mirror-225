from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class BeginItemLayoutEventArgs (SpireObject) :
    """
    <summary>
        Represents begin layout event arguments.
    </summary>
    """
    @property

    def Item(self)->'PdfListItem':
        """
    <summary>
        Gets the item.
    </summary>
<value>The item that layout.</value>
        """
        GetDllLibPdf().BeginItemLayoutEventArgs_get_Item.argtypes=[c_void_p]
        GetDllLibPdf().BeginItemLayoutEventArgs_get_Item.restype=c_void_p
        intPtr = GetDllLibPdf().BeginItemLayoutEventArgs_get_Item(self.Ptr)
        ret = None if intPtr==None else PdfListItem(intPtr)
        return ret


    @property

    def Page(self)->'PdfPageBase':
        """
    <summary>
        Gets the page.
    </summary>
<value>The page in which item start layout.</value>
        """
        GetDllLibPdf().BeginItemLayoutEventArgs_get_Page.argtypes=[c_void_p]
        GetDllLibPdf().BeginItemLayoutEventArgs_get_Page.restype=c_void_p
        intPtr = GetDllLibPdf().BeginItemLayoutEventArgs_get_Page(self.Ptr)
        ret = None if intPtr==None else PdfPageBase(intPtr)
        return ret


