from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Constants (SpireObject) :
    """

    """
    @staticmethod
    def HeaderSignature()->int:
        """

        """
        #GetDllLibPdf().Constants_HeaderSignature.argtypes=[]
        GetDllLibPdf().Constants_HeaderSignature.restype=c_int
        ret = GetDllLibPdf().Constants_HeaderSignature()
        return ret

    @staticmethod
    def HeaderSignatureBytes()->int:
        """

        """
        #GetDllLibPdf().Constants_HeaderSignatureBytes.argtypes=[]
        GetDllLibPdf().Constants_HeaderSignatureBytes.restype=c_int
        ret = GetDllLibPdf().Constants_HeaderSignatureBytes()
        return ret

    @staticmethod
    def BufferSize()->int:
        """

        """
        #GetDllLibPdf().Constants_BufferSize.argtypes=[]
        GetDllLibPdf().Constants_BufferSize.restype=c_int
        ret = GetDllLibPdf().Constants_BufferSize()
        return ret

    @staticmethod

    def VersionNeededToExtract()->'Int16':
        """

        """
        #GetDllLibPdf().Constants_VersionNeededToExtract.argtypes=[]
        GetDllLibPdf().Constants_VersionNeededToExtract.restype=c_void_p
        intPtr = GetDllLibPdf().Constants_VersionNeededToExtract()
        ret = None if intPtr==None else Int16(intPtr)
        return ret


    @staticmethod

    def VersionMadeBy()->'Int16':
        """

        """
        #GetDllLibPdf().Constants_VersionMadeBy.argtypes=[]
        GetDllLibPdf().Constants_VersionMadeBy.restype=c_void_p
        intPtr = GetDllLibPdf().Constants_VersionMadeBy()
        ret = None if intPtr==None else Int16(intPtr)
        return ret


    @staticmethod
    def ShortSize()->int:
        """

        """
        #GetDllLibPdf().Constants_ShortSize.argtypes=[]
        GetDllLibPdf().Constants_ShortSize.restype=c_int
        ret = GetDllLibPdf().Constants_ShortSize()
        return ret

    @staticmethod
    def IntSize()->int:
        """

        """
        #GetDllLibPdf().Constants_IntSize.argtypes=[]
        GetDllLibPdf().Constants_IntSize.restype=c_int
        ret = GetDllLibPdf().Constants_IntSize()
        return ret

    @staticmethod
    def CentralHeaderSignature()->int:
        """

        """
        #GetDllLibPdf().Constants_CentralHeaderSignature.argtypes=[]
        GetDllLibPdf().Constants_CentralHeaderSignature.restype=c_int
        ret = GetDllLibPdf().Constants_CentralHeaderSignature()
        return ret

    @staticmethod
    def CentralDirectoryEndSignature()->int:
        """

        """
        #GetDllLibPdf().Constants_CentralDirectoryEndSignature.argtypes=[]
        GetDllLibPdf().Constants_CentralDirectoryEndSignature.restype=c_int
        ret = GetDllLibPdf().Constants_CentralDirectoryEndSignature()
        return ret

    @staticmethod

    def StartCrc()->'UInt32':
        """

        """
        #GetDllLibPdf().Constants_StartCrc.argtypes=[]
        GetDllLibPdf().Constants_StartCrc.restype=c_void_p
        intPtr = GetDllLibPdf().Constants_StartCrc()
        ret = None if intPtr==None else UInt32(intPtr)
        return ret


    @staticmethod
    def CentralDirSizeOffset()->int:
        """

        """
        #GetDllLibPdf().Constants_CentralDirSizeOffset.argtypes=[]
        GetDllLibPdf().Constants_CentralDirSizeOffset.restype=c_int
        ret = GetDllLibPdf().Constants_CentralDirSizeOffset()
        return ret

    @staticmethod
    def EndOfCentralRecordBaseSize()->int:
        """

        """
        #GetDllLibPdf().Constants_EndOfCentralRecordBaseSize.argtypes=[]
        GetDllLibPdf().Constants_EndOfCentralRecordBaseSize.restype=c_int
        ret = GetDllLibPdf().Constants_EndOfCentralRecordBaseSize()
        return ret

    @staticmethod
    def Zip64CentralDirLocatorSignature()->int:
        """

        """
        #GetDllLibPdf().Constants_Zip64CentralDirLocatorSignature.argtypes=[]
        GetDllLibPdf().Constants_Zip64CentralDirLocatorSignature.restype=c_int
        ret = GetDllLibPdf().Constants_Zip64CentralDirLocatorSignature()
        return ret

    @staticmethod
    def Zip64CentralFileHeaderSignature()->int:
        """

        """
        #GetDllLibPdf().Constants_Zip64CentralFileHeaderSignature.argtypes=[]
        GetDllLibPdf().Constants_Zip64CentralFileHeaderSignature.restype=c_int
        ret = GetDllLibPdf().Constants_Zip64CentralFileHeaderSignature()
        return ret

