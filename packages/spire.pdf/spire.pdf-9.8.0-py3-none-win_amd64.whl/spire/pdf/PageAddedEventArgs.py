from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PageAddedEventArgs (SpireObject) :
    """
    <summary>
        Provides data for PageAdded event.
    </summary>
<remarks>
            This event raised on adding the pages. 
            </remarks>
    """
    @property

    def Page(self)->'PdfNewPage':
        """
    <summary>
        Gets the newly added page.
    </summary>
<value>a  object representing the page which is added in the document.</value>
        """
        GetDllLibPdf().PageAddedEventArgs_get_Page.argtypes=[c_void_p]
        GetDllLibPdf().PageAddedEventArgs_get_Page.restype=c_void_p
        intPtr = GetDllLibPdf().PageAddedEventArgs_get_Page(self.Ptr)
        ret = None if intPtr==None else PdfNewPage(intPtr)
        return ret


