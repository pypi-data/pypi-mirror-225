from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class ZipArchiveItem (SpireObject) :
    """

    """
    @property

    def ItemName(self)->str:
        """

        """
        GetDllLibPdf().ZipArchiveItem_get_ItemName.argtypes=[c_void_p]
        GetDllLibPdf().ZipArchiveItem_get_ItemName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().ZipArchiveItem_get_ItemName(self.Ptr))
        return ret


    @ItemName.setter
    def ItemName(self, value:str):
        GetDllLibPdf().ZipArchiveItem_set_ItemName.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().ZipArchiveItem_set_ItemName(self.Ptr, value)

    @property

    def CompressionMethod(self)->'CompressionMethod':
        """

        """
        GetDllLibPdf().ZipArchiveItem_get_CompressionMethod.argtypes=[c_void_p]
        GetDllLibPdf().ZipArchiveItem_get_CompressionMethod.restype=c_int
        ret = GetDllLibPdf().ZipArchiveItem_get_CompressionMethod(self.Ptr)
        objwraped = CompressionMethod(ret)
        return objwraped

    @CompressionMethod.setter
    def CompressionMethod(self, value:'CompressionMethod'):
        GetDllLibPdf().ZipArchiveItem_set_CompressionMethod.argtypes=[c_void_p, c_int]
        GetDllLibPdf().ZipArchiveItem_set_CompressionMethod(self.Ptr, value.value)

    @property

    def CompressionLevel(self)->'CompressionLevel':
        """

        """
        GetDllLibPdf().ZipArchiveItem_get_CompressionLevel.argtypes=[c_void_p]
        GetDllLibPdf().ZipArchiveItem_get_CompressionLevel.restype=c_int
        ret = GetDllLibPdf().ZipArchiveItem_get_CompressionLevel(self.Ptr)
        objwraped = CompressionLevel(ret)
        return objwraped

    @CompressionLevel.setter
    def CompressionLevel(self, value:'CompressionLevel'):
        GetDllLibPdf().ZipArchiveItem_set_CompressionLevel.argtypes=[c_void_p, c_int]
        GetDllLibPdf().ZipArchiveItem_set_CompressionLevel(self.Ptr, value.value)

    @property

    def Crc32(self)->'UInt32':
        """

        """
        GetDllLibPdf().ZipArchiveItem_get_Crc32.argtypes=[c_void_p]
        GetDllLibPdf().ZipArchiveItem_get_Crc32.restype=c_void_p
        intPtr = GetDllLibPdf().ZipArchiveItem_get_Crc32(self.Ptr)
        ret = None if intPtr==None else UInt32(intPtr)
        return ret


    @property

    def DataStream(self)->'Stream':
        """

        """
        GetDllLibPdf().ZipArchiveItem_get_DataStream.argtypes=[c_void_p]
        GetDllLibPdf().ZipArchiveItem_get_DataStream.restype=c_void_p
        intPtr = GetDllLibPdf().ZipArchiveItem_get_DataStream(self.Ptr)
        ret = None if intPtr==None else Stream(intPtr)
        return ret


    @property
    def CompressedSize(self)->int:
        """

        """
        GetDllLibPdf().ZipArchiveItem_get_CompressedSize.argtypes=[c_void_p]
        GetDllLibPdf().ZipArchiveItem_get_CompressedSize.restype=c_long
        ret = GetDllLibPdf().ZipArchiveItem_get_CompressedSize(self.Ptr)
        return ret

    @property
    def OriginalSize(self)->int:
        """

        """
        GetDllLibPdf().ZipArchiveItem_get_OriginalSize.argtypes=[c_void_p]
        GetDllLibPdf().ZipArchiveItem_get_OriginalSize.restype=c_long
        ret = GetDllLibPdf().ZipArchiveItem_get_OriginalSize(self.Ptr)
        return ret

    @property
    def ControlStream(self)->bool:
        """

        """
        GetDllLibPdf().ZipArchiveItem_get_ControlStream.argtypes=[c_void_p]
        GetDllLibPdf().ZipArchiveItem_get_ControlStream.restype=c_bool
        ret = GetDllLibPdf().ZipArchiveItem_get_ControlStream(self.Ptr)
        return ret

    @property
    def Compressed(self)->bool:
        """

        """
        GetDllLibPdf().ZipArchiveItem_get_Compressed.argtypes=[c_void_p]
        GetDllLibPdf().ZipArchiveItem_get_Compressed.restype=c_bool
        ret = GetDllLibPdf().ZipArchiveItem_get_Compressed(self.Ptr)
        return ret

#    @property
#
#    def ExternalAttributes(self)->'FileAttributes':
#        """
#
#        """
#        GetDllLibPdf().ZipArchiveItem_get_ExternalAttributes.argtypes=[c_void_p]
#        GetDllLibPdf().ZipArchiveItem_get_ExternalAttributes.restype=c_int
#        ret = GetDllLibPdf().ZipArchiveItem_get_ExternalAttributes(self.Ptr)
#        objwraped = FileAttributes(ret)
#        return objwraped


#    @ExternalAttributes.setter
#    def ExternalAttributes(self, value:'FileAttributes'):
#        GetDllLibPdf().ZipArchiveItem_set_ExternalAttributes.argtypes=[c_void_p, c_int]
#        GetDllLibPdf().ZipArchiveItem_set_ExternalAttributes(self.Ptr, value.value)


    @property
    def OptimizedDecompress(self)->bool:
        """

        """
        GetDllLibPdf().ZipArchiveItem_get_OptimizedDecompress.argtypes=[c_void_p]
        GetDllLibPdf().ZipArchiveItem_get_OptimizedDecompress.restype=c_bool
        ret = GetDllLibPdf().ZipArchiveItem_get_OptimizedDecompress(self.Ptr)
        return ret

    @OptimizedDecompress.setter
    def OptimizedDecompress(self, value:bool):
        GetDllLibPdf().ZipArchiveItem_set_OptimizedDecompress.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().ZipArchiveItem_set_OptimizedDecompress(self.Ptr, value)

    @dispatch

    def Update(self ,stream:'ZippedContentStream'):
        """

        """
        intPtrstream:c_void_p = stream.Ptr

        GetDllLibPdf().ZipArchiveItem_Update.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().ZipArchiveItem_Update(self.Ptr, intPtrstream)

    @dispatch

    def Update(self ,newDataStream:Stream,controlStream:bool):
        """

        """
        intPtrnewDataStream:c_void_p = newDataStream.Ptr

        GetDllLibPdf().ZipArchiveItem_UpdateNC.argtypes=[c_void_p ,c_void_p,c_bool]
        GetDllLibPdf().ZipArchiveItem_UpdateNC(self.Ptr, intPtrnewDataStream,controlStream)

    def ResetFlags(self):
        """

        """
        GetDllLibPdf().ZipArchiveItem_ResetFlags.argtypes=[c_void_p]
        GetDllLibPdf().ZipArchiveItem_ResetFlags(self.Ptr)

    @staticmethod

    def CloneStream(stream:'Stream')->'Stream':
        """

        """
        intPtrstream:c_void_p = stream.Ptr

        GetDllLibPdf().ZipArchiveItem_CloneStream.argtypes=[ c_void_p]
        GetDllLibPdf().ZipArchiveItem_CloneStream.restype=c_void_p
        intPtr = GetDllLibPdf().ZipArchiveItem_CloneStream( intPtrstream)
        ret = None if intPtr==None else Stream(intPtr)
        return ret


    def Dispose(self):
        """

        """
        GetDllLibPdf().ZipArchiveItem_Dispose.argtypes=[c_void_p]
        GetDllLibPdf().ZipArchiveItem_Dispose(self.Ptr)

