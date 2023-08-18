from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class ZlibZipWriter (  ZipWriter) :
    """

    """

    def AddEntry(self ,relativePath:str):
        """

        """
        
        GetDllLibPdf().ZlibZipWriter_AddEntry.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().ZlibZipWriter_AddEntry(self.Ptr, relativePath)

    def Close(self):
        """

        """
        GetDllLibPdf().ZlibZipWriter_Close.argtypes=[c_void_p]
        GetDllLibPdf().ZlibZipWriter_Close(self.Ptr)

#
#    def Read(self ,buffer:'Byte[]',offset:int,count:int)->int:
#        """
#
#        """
#        #arraybuffer:ArrayTypebuffer = ""
#        countbuffer = len(buffer)
#        ArrayTypebuffer = c_void_p * countbuffer
#        arraybuffer = ArrayTypebuffer()
#        for i in range(0, countbuffer):
#            arraybuffer[i] = buffer[i].Ptr
#
#
#        GetDllLibPdf().ZlibZipWriter_Read.argtypes=[c_void_p ,ArrayTypebuffer,c_int,c_int]
#        GetDllLibPdf().ZlibZipWriter_Read.restype=c_int
#        ret = GetDllLibPdf().ZlibZipWriter_Read(self.Ptr, arraybuffer,offset,count)
#        return ret


#
#    def Write(self ,buffer:'Byte[]',offset:int,count:int):
#        """
#
#        """
#        #arraybuffer:ArrayTypebuffer = ""
#        countbuffer = len(buffer)
#        ArrayTypebuffer = c_void_p * countbuffer
#        arraybuffer = ArrayTypebuffer()
#        for i in range(0, countbuffer):
#            arraybuffer[i] = buffer[i].Ptr
#
#
#        GetDllLibPdf().ZlibZipWriter_Write.argtypes=[c_void_p ,ArrayTypebuffer,c_int,c_int]
#        GetDllLibPdf().ZlibZipWriter_Write(self.Ptr, arraybuffer,offset,count)


#
#    def Seek(self ,offset:int,origin:'SeekOrigin')->int:
#        """
#
#        """
#        enumorigin:c_int = origin.value
#
#        GetDllLibPdf().ZlibZipWriter_Seek.argtypes=[c_void_p ,c_long,c_int]
#        GetDllLibPdf().ZlibZipWriter_Seek.restype=c_long
#        ret = GetDllLibPdf().ZlibZipWriter_Seek(self.Ptr, offset,enumorigin)
#        return ret



    def SetLength(self ,value:int):
        """

        """
        
        GetDllLibPdf().ZlibZipWriter_SetLength.argtypes=[c_void_p ,c_long]
        GetDllLibPdf().ZlibZipWriter_SetLength(self.Ptr, value)

    def Flush(self):
        """

        """
        GetDllLibPdf().ZlibZipWriter_Flush.argtypes=[c_void_p]
        GetDllLibPdf().ZlibZipWriter_Flush(self.Ptr)

    @property
    def Position(self)->int:
        """

        """
        GetDllLibPdf().ZlibZipWriter_get_Position.argtypes=[c_void_p]
        GetDllLibPdf().ZlibZipWriter_get_Position.restype=c_long
        ret = GetDllLibPdf().ZlibZipWriter_get_Position(self.Ptr)
        return ret

    @Position.setter
    def Position(self, value:int):
        GetDllLibPdf().ZlibZipWriter_set_Position.argtypes=[c_void_p, c_long]
        GetDllLibPdf().ZlibZipWriter_set_Position(self.Ptr, value)

    @property
    def Length(self)->int:
        """

        """
        GetDllLibPdf().ZlibZipWriter_get_Length.argtypes=[c_void_p]
        GetDllLibPdf().ZlibZipWriter_get_Length.restype=c_long
        ret = GetDllLibPdf().ZlibZipWriter_get_Length(self.Ptr)
        return ret

    @property
    def CanRead(self)->bool:
        """

        """
        GetDllLibPdf().ZlibZipWriter_get_CanRead.argtypes=[c_void_p]
        GetDllLibPdf().ZlibZipWriter_get_CanRead.restype=c_bool
        ret = GetDllLibPdf().ZlibZipWriter_get_CanRead(self.Ptr)
        return ret

    @property
    def CanWrite(self)->bool:
        """

        """
        GetDllLibPdf().ZlibZipWriter_get_CanWrite.argtypes=[c_void_p]
        GetDllLibPdf().ZlibZipWriter_get_CanWrite.restype=c_bool
        ret = GetDllLibPdf().ZlibZipWriter_get_CanWrite(self.Ptr)
        return ret

    @property
    def CanSeek(self)->bool:
        """

        """
        GetDllLibPdf().ZlibZipWriter_get_CanSeek.argtypes=[c_void_p]
        GetDllLibPdf().ZlibZipWriter_get_CanSeek.restype=c_bool
        ret = GetDllLibPdf().ZlibZipWriter_get_CanSeek(self.Ptr)
        return ret

    @staticmethod

    def ResolvePath(path:str)->str:
        """
    <summary>
        Resolves a path by interpreting "." and "..".
    </summary>
    <param name="path">The path to resolve.</param>
    <returns>The resolved path.</returns>
        """
        
        GetDllLibPdf().ZlibZipWriter_ResolvePath.argtypes=[ c_wchar_p]
        GetDllLibPdf().ZlibZipWriter_ResolvePath.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().ZlibZipWriter_ResolvePath( path))
        return ret


