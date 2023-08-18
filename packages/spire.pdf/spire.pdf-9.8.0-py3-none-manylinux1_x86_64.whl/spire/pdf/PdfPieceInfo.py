from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfPieceInfo (SpireObject) :
    """
    <summary>
        Represents the pdf piece info can used to hold private application datas.
    </summary>
    """
    @dispatch
    def __init__(self):
        GetDllLibPdf().PdfPieceInfo_CreatePdfPieceInfo.restype = c_void_p
        intPtr = GetDllLibPdf().PdfPieceInfo_CreatePdfPieceInfo()
        super(PdfPieceInfo, self).__init__(intPtr)
#    @property
#
#    def ApplicationDatas(self)->'IDictionary2':
#        """
#    <summary>
#        Get the application datas.
#    </summary>
#        """
#        GetDllLibPdf().PdfPieceInfo_get_ApplicationDatas.argtypes=[c_void_p]
#        GetDllLibPdf().PdfPieceInfo_get_ApplicationDatas.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPieceInfo_get_ApplicationDatas(self.Ptr)
#        ret = None if intPtr==None else IDictionary2(intPtr)
#        return ret
#



    def AddApplicationData(self ,applicationName:str,privateData:str):
        """
    <summary>
        Add application data.
    </summary>
    <param name="applicationName">The application name</param>
    <param name="privateData">The private data</param>
        """
        
        GetDllLibPdf().PdfPieceInfo_AddApplicationData.argtypes=[c_void_p ,c_wchar_p,c_wchar_p]
        GetDllLibPdf().PdfPieceInfo_AddApplicationData(self.Ptr, applicationName,privateData)


    def RemoveApplicationData(self ,applicationName:str):
        """
    <summary>
        Remove the application data.
    </summary>
    <param name="applicationName">The application name</param>
        """
        
        GetDllLibPdf().PdfPieceInfo_RemoveApplicationData.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfPieceInfo_RemoveApplicationData(self.Ptr, applicationName)

