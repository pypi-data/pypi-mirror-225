from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class XmpEntityBase (SpireObject) :
    """
    <summary>
        Base class for the xmp entities.
    </summary>
    """
#    @property
#
#    def XmlData(self)->'XmlElement':
#        """
#    <summary>
#        Gets Xml data of the entity.
#    </summary>
#        """
#        GetDllLibPdf().XmpEntityBase_get_XmlData.argtypes=[c_void_p]
#        GetDllLibPdf().XmpEntityBase_get_XmlData.restype=c_void_p
#        intPtr = GetDllLibPdf().XmpEntityBase_get_XmlData(self.Ptr)
#        ret = None if intPtr==None else XmlElement(intPtr)
#        return ret
#


