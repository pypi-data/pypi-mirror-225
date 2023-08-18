from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfLayerOutline (SpireObject) :
    """
    <summary>
        Represent the recommended order for presentation of optional content
            groups in user interface.
            Refrence "Optional content configuration dictionary's entry order".
    </summary>
    """
    @dispatch

    def AddGroup(self ,name:str)->'PdfLayerOutline':
        """
    <summary>
        Add a sub group outline.
    </summary>
    <param name="name">Group name.</param>
    <returns>Sub group outline.</returns>
        """
        
        GetDllLibPdf().PdfLayerOutline_AddGroup.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfLayerOutline_AddGroup.restype=c_void_p
        intPtr = GetDllLibPdf().PdfLayerOutline_AddGroup(self.Ptr, name)
        ret = None if intPtr==None else PdfLayerOutline(intPtr)
        return ret


    @dispatch

    def AddGroup(self ,layer:PdfLayer)->'PdfLayerOutline':
        """
    <summary>
        Add a outline entry of the pdf layer with a sub group outline.
    </summary>
    <param name="layer">Pdf layer</param>
    <returns>Sub group outline.</returns>
        """
        intPtrlayer:c_void_p = layer.Ptr

        GetDllLibPdf().PdfLayerOutline_AddGroupL.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfLayerOutline_AddGroupL.restype=c_void_p
        intPtr = GetDllLibPdf().PdfLayerOutline_AddGroupL(self.Ptr, intPtrlayer)
        ret = None if intPtr==None else PdfLayerOutline(intPtr)
        return ret



    def AddEntry(self ,layer:'PdfLayer'):
        """
    <summary>
        Add a outline entry of the pdf layer.
    </summary>
    <param name="layer">Pdf layer</param>
        """
        intPtrlayer:c_void_p = layer.Ptr

        GetDllLibPdf().PdfLayerOutline_AddEntry.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfLayerOutline_AddEntry(self.Ptr, intPtrlayer)

