from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class TimeZone (SpireObject) :
    """

    """
    @staticmethod

    def get_CurrentTimeZone()->'TimeZone':
        """

        """
        #GetDllLibPdf().TimeZone_get_CurrentTimeZone.argtypes=[]
        GetDllLibPdf().TimeZone_get_CurrentTimeZone.restype=c_void_p
        intPtr = GetDllLibPdf().TimeZone_get_CurrentTimeZone()
        ret = None if intPtr==None else TimeZone(intPtr)
        return ret



    def ToUniversalTime(self ,time:'DateTime')->'DateTime':
        """

        """
        intPtrtime:c_void_p = time.Ptr

        GetDllLibPdf().TimeZone_ToUniversalTime.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().TimeZone_ToUniversalTime.restype=c_void_p
        intPtr = GetDllLibPdf().TimeZone_ToUniversalTime(self.Ptr, intPtrtime)
        ret = None if intPtr==None else DateTime(intPtr)
        return ret



    def ToLocalTime(self ,time:'DateTime')->'DateTime':
        """

        """
        intPtrtime:c_void_p = time.Ptr

        GetDllLibPdf().TimeZone_ToLocalTime.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().TimeZone_ToLocalTime.restype=c_void_p
        intPtr = GetDllLibPdf().TimeZone_ToLocalTime(self.Ptr, intPtrtime)
        ret = None if intPtr==None else DateTime(intPtr)
        return ret


    @dispatch

    def IsDaylightSavingTime(self ,time:DateTime)->bool:
        """

        """
        intPtrtime:c_void_p = time.Ptr

        GetDllLibPdf().TimeZone_IsDaylightSavingTime.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().TimeZone_IsDaylightSavingTime.restype=c_bool
        ret = GetDllLibPdf().TimeZone_IsDaylightSavingTime(self.Ptr, intPtrtime)
        return ret

#    @staticmethod
#    @dispatch
#
#    def IsDaylightSavingTime(time:DateTime,daylightTimes:'DaylightTime')->bool:
#        """
#
#        """
#        intPtrtime:c_void_p = time.Ptr
#        intPtrdaylightTimes:c_void_p = daylightTimes.Ptr
#
#        GetDllLibPdf().TimeZone_IsDaylightSavingTimeTD.argtypes=[ c_void_p,c_void_p]
#        GetDllLibPdf().TimeZone_IsDaylightSavingTimeTD.restype=c_bool
#        ret = GetDllLibPdf().TimeZone_IsDaylightSavingTimeTD( intPtrtime,intPtrdaylightTimes)
#        return ret


    @property

    def StandardName(self)->str:
        """

        """
        GetDllLibPdf().TimeZone_get_StandardName.argtypes=[c_void_p]
        GetDllLibPdf().TimeZone_get_StandardName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().TimeZone_get_StandardName(self.Ptr))
        return ret


    @property

    def DaylightName(self)->str:
        """

        """
        GetDllLibPdf().TimeZone_get_DaylightName.argtypes=[c_void_p]
        GetDllLibPdf().TimeZone_get_DaylightName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().TimeZone_get_DaylightName(self.Ptr))
        return ret



    def GetUtcOffset(self ,time:'DateTime')->'TimeSpan':
        """

        """
        intPtrtime:c_void_p = time.Ptr

        GetDllLibPdf().TimeZone_GetUtcOffset.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().TimeZone_GetUtcOffset.restype=c_void_p
        intPtr = GetDllLibPdf().TimeZone_GetUtcOffset(self.Ptr, intPtrtime)
        ret = None if intPtr==None else TimeSpan(intPtr)
        return ret


#
#    def GetDaylightChanges(self ,year:int)->'DaylightTime':
#        """
#
#        """
#        
#        GetDllLibPdf().TimeZone_GetDaylightChanges.argtypes=[c_void_p ,c_int]
#        GetDllLibPdf().TimeZone_GetDaylightChanges.restype=c_void_p
#        intPtr = GetDllLibPdf().TimeZone_GetDaylightChanges(self.Ptr, year)
#        ret = None if intPtr==None else DaylightTime(intPtr)
#        return ret
#


