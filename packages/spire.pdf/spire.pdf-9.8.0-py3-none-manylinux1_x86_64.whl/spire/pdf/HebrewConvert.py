from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class HebrewConvert (SpireObject) :
    """

    """
    @staticmethod

    def get_Instance()->'HebrewConvert':
        """

        """
        #GetDllLibPdf().HebrewConvert_get_Instance.argtypes=[]
        GetDllLibPdf().HebrewConvert_get_Instance.restype=c_void_p
        intPtr = GetDllLibPdf().HebrewConvert_get_Instance()
        ret = None if intPtr==None else HebrewConvert(intPtr)
        return ret



    def Convert(self ,charValue:int)->int:
        """

        """
        
        GetDllLibPdf().HebrewConvert_Convert.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().HebrewConvert_Convert.restype=c_int
        ret = GetDllLibPdf().HebrewConvert_Convert(self.Ptr, charValue)
        return ret

