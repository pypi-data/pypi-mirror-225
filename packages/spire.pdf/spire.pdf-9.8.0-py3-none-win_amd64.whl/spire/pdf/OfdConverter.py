from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class OfdConverter (SpireObject) :
    """
    <summary>
        This class provides support for converting ofd into pdf or image.
    </summary>
    """
    @property
    def PageCount(self)->int:
        """
    <summary>
        Gets the document page count.
    </summary>
        """
        GetDllLibPdf().OfdConverter_get_PageCount.argtypes=[c_void_p]
        GetDllLibPdf().OfdConverter_get_PageCount.restype=c_int
        ret = GetDllLibPdf().OfdConverter_get_PageCount(self.Ptr)
        return ret

    @dispatch

    def ToPdf(self ,filename:str):
        """
    <summary>
        Save ofd document to pdf.
    </summary>
    <param name="filename">A relative or absolute path for the file.</param>
        """
        
        GetDllLibPdf().OfdConverter_ToPdf.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().OfdConverter_ToPdf(self.Ptr, filename)

    @dispatch

    def ToPdf(self ,stream:Stream):
        """
    <summary>
        Save ofd document to pdf.
    </summary>
    <param name="stream">The pdf file stream.</param>
        """
        intPtrstream:c_void_p = stream.Ptr

        GetDllLibPdf().OfdConverter_ToPdfS.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().OfdConverter_ToPdfS(self.Ptr, intPtrstream)

    @dispatch

    def ToImage(self ,pageIndex:int)->Image:
        """
    <summary>
        Saves OFD document page as image
    </summary>
    <param name="pageIndex">Page index</param>
    <returns>Returns page as Image</returns>
        """
        
        GetDllLibPdf().OfdConverter_ToImage.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().OfdConverter_ToImage.restype=c_void_p
        intPtr = GetDllLibPdf().OfdConverter_ToImage(self.Ptr, pageIndex)
        ret = None if intPtr==None else Image(intPtr)
        return ret


    @dispatch

    def ToImage(self ,pageIndex:int,dpiX:int,dpiY:int)->Image:
        """
    <summary>
        Saves OFD document page as image
    </summary>
    <param name="pageIndex">Page index</param>
    <param name="dpiX">Pictures X resolution</param>
    <param name="dpiY">Pictures Y resolution</param>
    <returns>Returns page as Image</returns>
        """
        
        GetDllLibPdf().OfdConverter_ToImagePDD.argtypes=[c_void_p ,c_int,c_int,c_int]
        GetDllLibPdf().OfdConverter_ToImagePDD.restype=c_void_p
        intPtr = GetDllLibPdf().OfdConverter_ToImagePDD(self.Ptr, pageIndex,dpiX,dpiY)
        ret = None if intPtr==None else Image(intPtr)
        return ret


    def Dispose(self):
        """

        """
        GetDllLibPdf().OfdConverter_Dispose.argtypes=[c_void_p]
        GetDllLibPdf().OfdConverter_Dispose(self.Ptr)

