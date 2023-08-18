from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class ZipFactory (SpireObject) :
    """
    <summary>
        ZipFactory provides instances of IZipReader and IZipWriter.
    </summary>
    """
    @staticmethod
    @dispatch

    def CreateArchive(path:str)->ZipWriter:
        """
    <summary>
        Provides an instance of IZipWriter.
    </summary>
    <param name="path">The path of the ZIP file to create.</param>
    <returns></returns>
        """
        
        GetDllLibPdf().ZipFactory_CreateArchive.argtypes=[ c_wchar_p]
        GetDllLibPdf().ZipFactory_CreateArchive.restype=c_void_p
        intPtr = GetDllLibPdf().ZipFactory_CreateArchive( path)
        ret = None if intPtr==None else ZipWriter(intPtr)
        return ret


    @staticmethod
    @dispatch

    def CreateArchive(stream:Stream)->ZipWriter:
        """

        """
        intPtrstream:c_void_p = stream.Ptr

        GetDllLibPdf().ZipFactory_CreateArchiveS.argtypes=[ c_void_p]
        GetDllLibPdf().ZipFactory_CreateArchiveS.restype=c_void_p
        intPtr = GetDllLibPdf().ZipFactory_CreateArchiveS( intPtrstream)
        ret = None if intPtr==None else ZipWriter(intPtr)
        return ret


    @staticmethod
    @dispatch

    def OpenArchive(path:str)->ZipReader:
        """
    <summary>
        Provides an instance of IZipReader.
    </summary>
    <param name="path">The path of the ZIP file to read.</param>
    <returns></returns>
        """
        
        GetDllLibPdf().ZipFactory_OpenArchive.argtypes=[ c_wchar_p]
        GetDllLibPdf().ZipFactory_OpenArchive.restype=c_void_p
        intPtr = GetDllLibPdf().ZipFactory_OpenArchive( path)
        ret = None if intPtr==None else ZipReader(intPtr)
        return ret


    @staticmethod
    @dispatch

    def OpenArchive(stream:Stream)->ZipReader:
        """

        """
        intPtrstream:c_void_p = stream.Ptr

        GetDllLibPdf().ZipFactory_OpenArchiveS.argtypes=[ c_void_p]
        GetDllLibPdf().ZipFactory_OpenArchiveS.restype=c_void_p
        intPtr = GetDllLibPdf().ZipFactory_OpenArchiveS( intPtrstream)
        ret = None if intPtr==None else ZipReader(intPtr)
        return ret


