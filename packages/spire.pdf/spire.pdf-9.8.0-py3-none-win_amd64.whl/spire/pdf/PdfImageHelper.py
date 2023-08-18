from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfImageHelper (SpireObject) :
    """

    """
#
#    def GetImagesInfo(self ,page:'PdfPageBase')->List['PdfImageInfo']:
#        """
#    <summary>
#        Get all image information on the page.
#    </summary>
#    <param name="page">The pdf page.</param>
#        """
#        intPtrpage:c_void_p = page.Ptr
#
#        GetDllLibPdf().PdfImageHelper_GetImagesInfo.argtypes=[c_void_p ,c_void_p]
#        GetDllLibPdf().PdfImageHelper_GetImagesInfo.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().PdfImageHelper_GetImagesInfo(self.Ptr, intPtrpage)
#        ret = GetObjVectorFromArray(intPtrArray, PdfImageInfo)
#        return ret



    def ReplaceImage(self ,imageInfo:'PdfImageInfo',newImage:'PdfImage'):
        """
    <summary>
        Replace image.
    </summary>
    <param name="imageInfo">The original image info.</param>
    <param name="newImage">The new replace image.</param>
        """
        intPtrimageInfo:c_void_p = imageInfo.Ptr
        intPtrnewImage:c_void_p = newImage.Ptr

        GetDllLibPdf().PdfImageHelper_ReplaceImage.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().PdfImageHelper_ReplaceImage(self.Ptr, intPtrimageInfo,intPtrnewImage)

