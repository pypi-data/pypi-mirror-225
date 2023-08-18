from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class ZippedContentStream (  Stream) :
    """

    """
    @property
    def CanRead(self)->bool:
        """

        """
        GetDllLibPdf().ZippedContentStream_get_CanRead.argtypes=[c_void_p]
        GetDllLibPdf().ZippedContentStream_get_CanRead.restype=c_bool
        ret = GetDllLibPdf().ZippedContentStream_get_CanRead(self.Ptr)
        return ret

    @property
    def CanSeek(self)->bool:
        """

        """
        GetDllLibPdf().ZippedContentStream_get_CanSeek.argtypes=[c_void_p]
        GetDllLibPdf().ZippedContentStream_get_CanSeek.restype=c_bool
        ret = GetDllLibPdf().ZippedContentStream_get_CanSeek(self.Ptr)
        return ret

    @property
    def CanWrite(self)->bool:
        """

        """
        GetDllLibPdf().ZippedContentStream_get_CanWrite.argtypes=[c_void_p]
        GetDllLibPdf().ZippedContentStream_get_CanWrite.restype=c_bool
        ret = GetDllLibPdf().ZippedContentStream_get_CanWrite(self.Ptr)
        return ret

    @property
    def Length(self)->int:
        """

        """
        GetDllLibPdf().ZippedContentStream_get_Length.argtypes=[c_void_p]
        GetDllLibPdf().ZippedContentStream_get_Length.restype=c_long
        ret = GetDllLibPdf().ZippedContentStream_get_Length(self.Ptr)
        return ret

    @property
    def Position(self)->int:
        """

        """
        GetDllLibPdf().ZippedContentStream_get_Position.argtypes=[c_void_p]
        GetDllLibPdf().ZippedContentStream_get_Position.restype=c_long
        ret = GetDllLibPdf().ZippedContentStream_get_Position(self.Ptr)
        return ret

    @Position.setter
    def Position(self, value:int):
        GetDllLibPdf().ZippedContentStream_set_Position.argtypes=[c_void_p, c_long]
        GetDllLibPdf().ZippedContentStream_set_Position(self.Ptr, value)

    @property

    def ZippedContent(self)->'Stream':
        """

        """
        GetDllLibPdf().ZippedContentStream_get_ZippedContent.argtypes=[c_void_p]
        GetDllLibPdf().ZippedContentStream_get_ZippedContent.restype=c_void_p
        intPtr = GetDllLibPdf().ZippedContentStream_get_ZippedContent(self.Ptr)
        ret = None if intPtr==None else Stream(intPtr)
        return ret


    @property

    def Crc32(self)->'UInt32':
        """

        """
        GetDllLibPdf().ZippedContentStream_get_Crc32.argtypes=[c_void_p]
        GetDllLibPdf().ZippedContentStream_get_Crc32.restype=c_void_p
        intPtr = GetDllLibPdf().ZippedContentStream_get_Crc32(self.Ptr)
        ret = None if intPtr==None else UInt32(intPtr)
        return ret


    @property
    def UnzippedSize(self)->int:
        """

        """
        GetDllLibPdf().ZippedContentStream_get_UnzippedSize.argtypes=[c_void_p]
        GetDllLibPdf().ZippedContentStream_get_UnzippedSize.restype=c_long
        ret = GetDllLibPdf().ZippedContentStream_get_UnzippedSize(self.Ptr)
        return ret

    def Flush(self):
        """

        """
        GetDllLibPdf().ZippedContentStream_Flush.argtypes=[c_void_p]
        GetDllLibPdf().ZippedContentStream_Flush(self.Ptr)

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
#        GetDllLibPdf().ZippedContentStream_Read.argtypes=[c_void_p ,ArrayTypebuffer,c_int,c_int]
#        GetDllLibPdf().ZippedContentStream_Read.restype=c_int
#        ret = GetDllLibPdf().ZippedContentStream_Read(self.Ptr, arraybuffer,offset,count)
#        return ret


#
#    def Seek(self ,offset:int,origin:'SeekOrigin')->int:
#        """
#
#        """
#        enumorigin:c_int = origin.value
#
#        GetDllLibPdf().ZippedContentStream_Seek.argtypes=[c_void_p ,c_long,c_int]
#        GetDllLibPdf().ZippedContentStream_Seek.restype=c_long
#        ret = GetDllLibPdf().ZippedContentStream_Seek(self.Ptr, offset,enumorigin)
#        return ret



    def SetLength(self ,value:int):
        """

        """
        
        GetDllLibPdf().ZippedContentStream_SetLength.argtypes=[c_void_p ,c_long]
        GetDllLibPdf().ZippedContentStream_SetLength(self.Ptr, value)

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
#        GetDllLibPdf().ZippedContentStream_Write.argtypes=[c_void_p ,ArrayTypebuffer,c_int,c_int]
#        GetDllLibPdf().ZippedContentStream_Write(self.Ptr, arraybuffer,offset,count)


