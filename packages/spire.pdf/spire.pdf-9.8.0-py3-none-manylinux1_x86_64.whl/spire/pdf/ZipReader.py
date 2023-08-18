from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class ZipReader (SpireObject) :
    """
    <summary>
        ZipReader defines an abstract class to read entries from a ZIP file.
    </summary>
    """

    def GetEntry(self ,relativePath:str)->'Stream':
        """
    <summary>
        Get an entry from a ZIP file.
    </summary>
    <param name="relativePath">The relative path of the entry in the ZIP
            file.</param>
    <returns>A stream containing the uncompressed data.</returns>
        """
        
        GetDllLibPdf().ZipReader_GetEntry.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().ZipReader_GetEntry.restype=c_void_p
        intPtr = GetDllLibPdf().ZipReader_GetEntry(self.Ptr, relativePath)
        ret = None if intPtr==None else Stream(intPtr)
        return ret


#
#    def ExtractOfficeDocument(self ,directory:str,dict:'Dictionary2'):
#        """
#
#        """
#        intPtrdict:c_void_p = dict.Ptr
#
#        GetDllLibPdf().ZipReader_ExtractOfficeDocument.argtypes=[c_void_p ,c_wchar_p,c_void_p]
#        GetDllLibPdf().ZipReader_ExtractOfficeDocument(self.Ptr, directory,intPtrdict)


#
#    def ExtractUOFDocument(self ,directory:str,dict:'Dictionary2'):
#        """
#
#        """
#        intPtrdict:c_void_p = dict.Ptr
#
#        GetDllLibPdf().ZipReader_ExtractUOFDocument.argtypes=[c_void_p ,c_wchar_p,c_void_p]
#        GetDllLibPdf().ZipReader_ExtractUOFDocument(self.Ptr, directory,intPtrdict)


    def Close(self):
        """
    <summary>
        Close the ZIP file.
    </summary>
        """
        GetDllLibPdf().ZipReader_Close.argtypes=[c_void_p]
        GetDllLibPdf().ZipReader_Close(self.Ptr)

