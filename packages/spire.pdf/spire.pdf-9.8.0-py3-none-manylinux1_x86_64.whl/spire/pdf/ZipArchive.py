from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class ZipArchive (SpireObject) :
    """

    """
    @dispatch

    def get_Item(self ,index:int)->'ZipArchiveItem':
        """

        """
        
        GetDllLibPdf().ZipArchive_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().ZipArchive_get_Item.restype=c_void_p
        intPtr = GetDllLibPdf().ZipArchive_get_Item(self.Ptr, index)
        ret = None if intPtr==None else ZipArchiveItem(intPtr)
        return ret


    @dispatch

    def get_Item(self ,itemName:str)->'ZipArchiveItem':
        """

        """
        
        GetDllLibPdf().ZipArchive_get_ItemI.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().ZipArchive_get_ItemI.restype=c_void_p
        intPtr = GetDllLibPdf().ZipArchive_get_ItemI(self.Ptr, itemName)
        ret = None if intPtr==None else ZipArchiveItem(intPtr)
        return ret


    @property
    def Count(self)->int:
        """

        """
        GetDllLibPdf().ZipArchive_get_Count.argtypes=[c_void_p]
        GetDllLibPdf().ZipArchive_get_Count.restype=c_int
        ret = GetDllLibPdf().ZipArchive_get_Count(self.Ptr)
        return ret

#    @property
#
#    def Items(self)->'List1':
#        """
#
#        """
#        GetDllLibPdf().ZipArchive_get_Items.argtypes=[c_void_p]
#        GetDllLibPdf().ZipArchive_get_Items.restype=c_void_p
#        intPtr = GetDllLibPdf().ZipArchive_get_Items(self.Ptr)
#        ret = None if intPtr==None else List1(intPtr)
#        return ret
#


    @property

    def FileNamePreprocessor(self)->'IFileNamePreprocessor':
        """

        """
        GetDllLibPdf().ZipArchive_get_FileNamePreprocessor.argtypes=[c_void_p]
        GetDllLibPdf().ZipArchive_get_FileNamePreprocessor.restype=c_void_p
        intPtr = GetDllLibPdf().ZipArchive_get_FileNamePreprocessor(self.Ptr)
        ret = None if intPtr==None else IFileNamePreprocessor(intPtr)
        return ret


    @FileNamePreprocessor.setter
    def FileNamePreprocessor(self, value:'IFileNamePreprocessor'):
        GetDllLibPdf().ZipArchive_set_FileNamePreprocessor.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().ZipArchive_set_FileNamePreprocessor(self.Ptr, value.Ptr)

    @property

    def DefaultCompressionLevel(self)->'CompressionLevel':
        """

        """
        GetDllLibPdf().ZipArchive_get_DefaultCompressionLevel.argtypes=[c_void_p]
        GetDllLibPdf().ZipArchive_get_DefaultCompressionLevel.restype=c_int
        ret = GetDllLibPdf().ZipArchive_get_DefaultCompressionLevel(self.Ptr)
        objwraped = CompressionLevel(ret)
        return objwraped

    @DefaultCompressionLevel.setter
    def DefaultCompressionLevel(self, value:'CompressionLevel'):
        GetDllLibPdf().ZipArchive_set_DefaultCompressionLevel.argtypes=[c_void_p, c_int]
        GetDllLibPdf().ZipArchive_set_DefaultCompressionLevel(self.Ptr, value.value)

    @property
    def CheckCrc(self)->bool:
        """

        """
        GetDllLibPdf().ZipArchive_get_CheckCrc.argtypes=[c_void_p]
        GetDllLibPdf().ZipArchive_get_CheckCrc.restype=c_bool
        ret = GetDllLibPdf().ZipArchive_get_CheckCrc(self.Ptr)
        return ret

    @CheckCrc.setter
    def CheckCrc(self, value:bool):
        GetDllLibPdf().ZipArchive_set_CheckCrc.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().ZipArchive_set_CheckCrc(self.Ptr, value)

    @property
    def UseNetCompression(self)->bool:
        """

        """
        GetDllLibPdf().ZipArchive_get_UseNetCompression.argtypes=[c_void_p]
        GetDllLibPdf().ZipArchive_get_UseNetCompression.restype=c_bool
        ret = GetDllLibPdf().ZipArchive_get_UseNetCompression(self.Ptr)
        return ret

    @UseNetCompression.setter
    def UseNetCompression(self, value:bool):
        GetDllLibPdf().ZipArchive_set_UseNetCompression.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().ZipArchive_set_UseNetCompression(self.Ptr, value)

    @staticmethod

    def FindValueFromEnd(stream:'Stream',value:'UInt32',maxCount:int)->int:
        """

        """
        intPtrstream:c_void_p = stream.Ptr
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().ZipArchive_FindValueFromEnd.argtypes=[ c_void_p,c_void_p,c_int]
        GetDllLibPdf().ZipArchive_FindValueFromEnd.restype=c_long
        ret = GetDllLibPdf().ZipArchive_FindValueFromEnd( intPtrstream,intPtrvalue,maxCount)
        return ret

    @staticmethod

    def ReadInt32(stream:'Stream')->int:
        """

        """
        intPtrstream:c_void_p = stream.Ptr

        GetDllLibPdf().ZipArchive_ReadInt32.argtypes=[ c_void_p]
        GetDllLibPdf().ZipArchive_ReadInt32.restype=c_int
        ret = GetDllLibPdf().ZipArchive_ReadInt32( intPtrstream)
        return ret

    @staticmethod

    def ReadInt16(stream:'Stream')->'Int16':
        """

        """
        intPtrstream:c_void_p = stream.Ptr

        GetDllLibPdf().ZipArchive_ReadInt16.argtypes=[ c_void_p]
        GetDllLibPdf().ZipArchive_ReadInt16.restype=c_void_p
        intPtr = GetDllLibPdf().ZipArchive_ReadInt16( intPtrstream)
        ret = None if intPtr==None else Int16(intPtr)
        return ret



    def AddDirectory(self ,directoryName:str)->'ZipArchiveItem':
        """

        """
        
        GetDllLibPdf().ZipArchive_AddDirectory.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().ZipArchive_AddDirectory.restype=c_void_p
        intPtr = GetDllLibPdf().ZipArchive_AddDirectory(self.Ptr, directoryName)
        ret = None if intPtr==None else ZipArchiveItem(intPtr)
        return ret



    def AddFile(self ,fileName:str)->'ZipArchiveItem':
        """

        """
        
        GetDllLibPdf().ZipArchive_AddFile.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().ZipArchive_AddFile.restype=c_void_p
        intPtr = GetDllLibPdf().ZipArchive_AddFile(self.Ptr, fileName)
        ret = None if intPtr==None else ZipArchiveItem(intPtr)
        return ret


#    @dispatch
#
#    def AddItem(self ,itemName:str,data:Stream,bControlStream:bool,attributes:'FileAttributes')->ZipArchiveItem:
#        """
#
#        """
#        intPtrdata:c_void_p = data.Ptr
#        enumattributes:c_int = attributes.value
#
#        GetDllLibPdf().ZipArchive_AddItem.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_bool,c_int]
#        GetDllLibPdf().ZipArchive_AddItem.restype=c_void_p
#        intPtr = GetDllLibPdf().ZipArchive_AddItem(self.Ptr, itemName,intPtrdata,bControlStream,enumattributes)
#        ret = None if intPtr==None else ZipArchiveItem(intPtr)
#        return ret
#


    @dispatch

    def AddItem(self ,item:'ZipArchiveItem')->'ZipArchiveItem':
        """

        """
        intPtritem:c_void_p = item.Ptr

        GetDllLibPdf().ZipArchive_AddItemI.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().ZipArchive_AddItemI.restype=c_void_p
        intPtr = GetDllLibPdf().ZipArchive_AddItemI(self.Ptr, intPtritem)
        ret = None if intPtr==None else ZipArchiveItem(intPtr)
        return ret



    def RemoveItem(self ,itemName:str):
        """

        """
        
        GetDllLibPdf().ZipArchive_RemoveItem.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().ZipArchive_RemoveItem(self.Ptr, itemName)


    def RemoveAt(self ,index:int):
        """

        """
        
        GetDllLibPdf().ZipArchive_RemoveAt.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().ZipArchive_RemoveAt(self.Ptr, index)

#
#    def Remove(self ,mask:'Regex'):
#        """
#
#        """
#        intPtrmask:c_void_p = mask.Ptr
#
#        GetDllLibPdf().ZipArchive_Remove.argtypes=[c_void_p ,c_void_p]
#        GetDllLibPdf().ZipArchive_Remove(self.Ptr, intPtrmask)


    @dispatch

    def UpdateItem(self ,itemName:str,newDataStream:Stream,controlStream:bool):
        """

        """
        intPtrnewDataStream:c_void_p = newDataStream.Ptr

        GetDllLibPdf().ZipArchive_UpdateItem.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_bool]
        GetDllLibPdf().ZipArchive_UpdateItem(self.Ptr, itemName,intPtrnewDataStream,controlStream)

#    @dispatch
#
#    def UpdateItem(self ,itemName:str,newDataStream:Stream,controlStream:bool,attributes:'FileAttributes'):
#        """
#
#        """
#        intPtrnewDataStream:c_void_p = newDataStream.Ptr
#        enumattributes:c_int = attributes.value
#
#        GetDllLibPdf().ZipArchive_UpdateItemINCA.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_bool,c_int]
#        GetDllLibPdf().ZipArchive_UpdateItemINCA(self.Ptr, itemName,intPtrnewDataStream,controlStream,enumattributes)


#    @dispatch
#
#    def UpdateItem(self ,itemName:str,newData:'Byte[]'):
#        """
#
#        """
#        #arraynewData:ArrayTypenewData = ""
#        countnewData = len(newData)
#        ArrayTypenewData = c_void_p * countnewData
#        arraynewData = ArrayTypenewData()
#        for i in range(0, countnewData):
#            arraynewData[i] = newData[i].Ptr
#
#
#        GetDllLibPdf().ZipArchive_UpdateItemIN.argtypes=[c_void_p ,c_wchar_p,ArrayTypenewData]
#        GetDllLibPdf().ZipArchive_UpdateItemIN(self.Ptr, itemName,arraynewData)


    @dispatch

    def Save(self ,outputFileName:str):
        """

        """
        
        GetDllLibPdf().ZipArchive_Save.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().ZipArchive_Save(self.Ptr, outputFileName)

    @dispatch

    def Save(self ,outputFileName:str,createFilePath:bool):
        """

        """
        
        GetDllLibPdf().ZipArchive_SaveOC.argtypes=[c_void_p ,c_wchar_p,c_bool]
        GetDllLibPdf().ZipArchive_SaveOC(self.Ptr, outputFileName,createFilePath)

    @dispatch

    def Save(self ,stream:Stream,closeStream:bool):
        """

        """
        intPtrstream:c_void_p = stream.Ptr

        GetDllLibPdf().ZipArchive_SaveSC.argtypes=[c_void_p ,c_void_p,c_bool]
        GetDllLibPdf().ZipArchive_SaveSC(self.Ptr, intPtrstream,closeStream)

    @dispatch

    def Open(self ,inputFileName:str):
        """

        """
        
        GetDllLibPdf().ZipArchive_Open.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().ZipArchive_Open(self.Ptr, inputFileName)

    @dispatch

    def Open(self ,stream:Stream,closeStream:bool):
        """

        """
        intPtrstream:c_void_p = stream.Ptr

        GetDllLibPdf().ZipArchive_OpenSC.argtypes=[c_void_p ,c_void_p,c_bool]
        GetDllLibPdf().ZipArchive_OpenSC(self.Ptr, intPtrstream,closeStream)


    def LocateBlockWithSignature(self ,signature:int,stream:'Stream',minimumBlockSize:int,maximumVariableData:int)->int:
        """

        """
        intPtrstream:c_void_p = stream.Ptr

        GetDllLibPdf().ZipArchive_LocateBlockWithSignature.argtypes=[c_void_p ,c_int,c_void_p,c_int,c_int]
        GetDllLibPdf().ZipArchive_LocateBlockWithSignature.restype=c_long
        ret = GetDllLibPdf().ZipArchive_LocateBlockWithSignature(self.Ptr, signature,intPtrstream,minimumBlockSize,maximumVariableData)
        return ret

    @dispatch

    def Open(self ,stream:Stream):
        """

        """
        intPtrstream:c_void_p = stream.Ptr

        GetDllLibPdf().ZipArchive_OpenS.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().ZipArchive_OpenS(self.Ptr, intPtrstream)

    def Close(self):
        """

        """
        GetDllLibPdf().ZipArchive_Close.argtypes=[c_void_p]
        GetDllLibPdf().ZipArchive_Close(self.Ptr)

    @dispatch

    def Find(self ,itemName:str)->int:
        """

        """
        
        GetDllLibPdf().ZipArchive_Find.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().ZipArchive_Find.restype=c_int
        ret = GetDllLibPdf().ZipArchive_Find(self.Ptr, itemName)
        return ret

#    @dispatch
#
#    def Find(self ,itemRegex:'Regex')->int:
#        """
#
#        """
#        intPtritemRegex:c_void_p = itemRegex.Ptr
#
#        GetDllLibPdf().ZipArchive_FindI.argtypes=[c_void_p ,c_void_p]
#        GetDllLibPdf().ZipArchive_FindI.restype=c_int
#        ret = GetDllLibPdf().ZipArchive_FindI(self.Ptr, intPtritemRegex)
#        return ret



    def Clone(self)->'ZipArchive':
        """

        """
        GetDllLibPdf().ZipArchive_Clone.argtypes=[c_void_p]
        GetDllLibPdf().ZipArchive_Clone.restype=c_void_p
        intPtr = GetDllLibPdf().ZipArchive_Clone(self.Ptr)
        ret = None if intPtr==None else ZipArchive(intPtr)
        return ret


    def Dispose(self):
        """

        """
        GetDllLibPdf().ZipArchive_Dispose.argtypes=[c_void_p]
        GetDllLibPdf().ZipArchive_Dispose(self.Ptr)


    def CreateCompressor(self)->'CompressorCreator':
        """

        """
        GetDllLibPdf().ZipArchive_CreateCompressor.argtypes=[c_void_p]
        GetDllLibPdf().ZipArchive_CreateCompressor.restype=c_void_p
        intPtr = GetDllLibPdf().ZipArchive_CreateCompressor(self.Ptr)
        ret = None if intPtr==None else CompressorCreator(intPtr)
        return ret


