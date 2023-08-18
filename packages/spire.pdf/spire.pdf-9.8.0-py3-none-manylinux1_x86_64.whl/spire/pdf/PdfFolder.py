from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfFolder (SpireObject) :
    """
    <summary>
        A folder for the purpose of organizing files into a hierarchical structure.
            The structure is represented by a tree with a single root folder acting as
            the common ancestor for all other folders and files in the collection.
    </summary>
    """
    @property

    def Name(self)->str:
        """
    <summary>
        (Required;ExtensionLevel3)A file name representing the name of the
            folder.Two sibling folders shall not share the same name following
            case normalization.
            Note:Descriptions of file name and case normalization follow this
            table.
    </summary>
        """
        GetDllLibPdf().PdfFolder_get_Name.argtypes=[c_void_p]
        GetDllLibPdf().PdfFolder_get_Name.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfFolder_get_Name(self.Ptr))
        return ret


    @dispatch

    def AddFile(self ,filePath:str):
        """
    <summary>
        Add a local file into this folder.
    </summary>
    <param name="filePath">The local file path.</param>
        """
        
        GetDllLibPdf().PdfFolder_AddFile.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfFolder_AddFile(self.Ptr, filePath)

    @dispatch

    def AddFile(self ,fileName:str,stream:Stream):
        """
    <summary>
        Add a stream into this folder.
    </summary>
    <param name="fileName">The file name of the stream.</param>
    <param name="stream">The stream.</param>
        """
        intPtrstream:c_void_p = stream.Ptr

        GetDllLibPdf().PdfFolder_AddFileFS.argtypes=[c_void_p ,c_wchar_p,c_void_p]
        GetDllLibPdf().PdfFolder_AddFileFS(self.Ptr, fileName,intPtrstream)


    def DeleteFile(self ,file:'PdfAttachment'):
        """
    <summary>
        Delete the file in this folder.
    </summary>
    <param name="file">The file.</param>
        """
        intPtrfile:c_void_p = file.Ptr

        GetDllLibPdf().PdfFolder_DeleteFile.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfFolder_DeleteFile(self.Ptr, intPtrfile)

#
#    def GetFiles(self)->'List1':
#        """
#    <summary>
#        Get the files in this folder.
#    </summary>
#    <returns>The file list in this folder.</returns>
#        """
#        GetDllLibPdf().PdfFolder_GetFiles.argtypes=[c_void_p]
#        GetDllLibPdf().PdfFolder_GetFiles.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfFolder_GetFiles(self.Ptr)
#        ret = None if intPtr==None else List1(intPtr)
#        return ret
#



    def CreateSubfolder(self ,folderName:str)->'PdfFolder':
        """
    <summary>
        Create an subfolder.
    </summary>
    <param name="folderName">The subfolder name.</param>
    <returns>The PdfFolder.</returns>
        """
        
        GetDllLibPdf().PdfFolder_CreateSubfolder.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfFolder_CreateSubfolder.restype=c_void_p
        intPtr = GetDllLibPdf().PdfFolder_CreateSubfolder(self.Ptr, folderName)
        ret = None if intPtr==None else PdfFolder(intPtr)
        return ret



    def DeleteSubfolder(self ,folderName:str):
        """
    <summary>
        Delete an subfolder.
    </summary>
    <param name="folderName">The subfolder name.</param>
        """
        
        GetDllLibPdf().PdfFolder_DeleteSubfolder.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfFolder_DeleteSubfolder(self.Ptr, folderName)

#
#    def GetSubfolders(self)->'List1':
#        """
#    <summary>
#        Get the subfolders of this folder.
#    </summary>
#    <returns>The subfolder list in this folder.</returns>
#        """
#        GetDllLibPdf().PdfFolder_GetSubfolders.argtypes=[c_void_p]
#        GetDllLibPdf().PdfFolder_GetSubfolders.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfFolder_GetSubfolders(self.Ptr)
#        ret = None if intPtr==None else List1(intPtr)
#        return ret
#


    def HasSubfolders(self)->bool:
        """
    <summary>
        Whether has subfolders.
    </summary>
    <returns>True or False</returns>
        """
        GetDllLibPdf().PdfFolder_HasSubfolders.argtypes=[c_void_p]
        GetDllLibPdf().PdfFolder_HasSubfolders.restype=c_bool
        ret = GetDllLibPdf().PdfFolder_HasSubfolders(self.Ptr)
        return ret

    def Clear(self):
        """
    <summary>
        Clear this folder.
    </summary>
        """
        GetDllLibPdf().PdfFolder_Clear.argtypes=[c_void_p]
        GetDllLibPdf().PdfFolder_Clear(self.Ptr)


    def AddExistFolder(self ,folderPath:str):
        """
    <summary>
        Add local folder into this folder.
    </summary>
    <param name="folderPath">The local folder path.</param>
        """
        
        GetDllLibPdf().PdfFolder_AddExistFolder.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfFolder_AddExistFolder(self.Ptr, folderPath)

