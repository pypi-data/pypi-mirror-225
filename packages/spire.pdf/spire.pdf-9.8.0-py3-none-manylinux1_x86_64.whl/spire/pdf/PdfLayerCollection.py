from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfLayerCollection (SpireObject) :
    """
    <summary>
        Represent pdf layer collection.
    </summary>
    """
    @dispatch

    def get_Item(self ,index:int)->PdfLayer:
        """
    <summary>
        Get the pdf layer of the index.
    </summary>
    <param name="index">Pdf layer index</param>
    <returns>Pdf layer</returns>
        """
        
        GetDllLibPdf().PdfLayerCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfLayerCollection_get_Item.restype=c_void_p
        intPtr = GetDllLibPdf().PdfLayerCollection_get_Item(self.Ptr, index)
        ret = None if intPtr==None else PdfLayer(intPtr)
        return ret


    @dispatch

    def get_Item(self ,name:str)->PdfLayer:
        """
    <summary>
        Get the pdf layer of name.
            Notice: 
            Pdf layer name may be is not unique.
            If exist duplication of name,return first pdf layer of name.
            If not exist pdf layer of name,return null;
    </summary>
    <param name="name">Pdf layer name</param>
    <returns>Pdf layer</returns>
        """
        
        GetDllLibPdf().PdfLayerCollection_get_ItemN.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfLayerCollection_get_ItemN.restype=c_void_p
        intPtr = GetDllLibPdf().PdfLayerCollection_get_ItemN(self.Ptr, name)
        ret = None if intPtr==None else PdfLayer(intPtr)
        return ret


    @property
    def Count(self)->int:
        """
    <summary>
        Gets the number of pdf layers contained.
    </summary>
        """
        GetDllLibPdf().PdfLayerCollection_get_Count.argtypes=[c_void_p]
        GetDllLibPdf().PdfLayerCollection_get_Count.restype=c_int
        ret = GetDllLibPdf().PdfLayerCollection_get_Count(self.Ptr)
        return ret


    def NewOutline(self)->'PdfLayerOutline':
        """
    <summary>
        Create a new empty pdf layer outline.
    </summary>
    <returns>Pdf layer outline.</returns>
        """
        GetDllLibPdf().PdfLayerCollection_NewOutline.argtypes=[c_void_p]
        GetDllLibPdf().PdfLayerCollection_NewOutline.restype=c_void_p
        intPtr = GetDllLibPdf().PdfLayerCollection_NewOutline(self.Ptr)
        ret = None if intPtr==None else PdfLayerOutline(intPtr)
        return ret


    @dispatch

    def AddLayer(self ,name:str)->PdfLayer:
        """
    <summary>
        Add a new pdf layer.
    </summary>
    <param name="name">Pdf layer name.</param>
    <returns>Pdf layer.</returns>
        """
        
        GetDllLibPdf().PdfLayerCollection_AddLayer.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfLayerCollection_AddLayer.restype=c_void_p
        intPtr = GetDllLibPdf().PdfLayerCollection_AddLayer(self.Ptr, name)
        ret = None if intPtr==None else PdfLayer(intPtr)
        return ret


    @dispatch

    def AddLayer(self ,name:str,state:PdfVisibility)->PdfLayer:
        """
    <summary>
        Add a new pdf layer.
    </summary>
    <param name="name">Pdf layer name.</param>
    <param name="state">Pdf layer's visibility.</param>
    <returns>Pdf layer.</returns>
        """
        enumstate:c_int = state.value

        GetDllLibPdf().PdfLayerCollection_AddLayerNS.argtypes=[c_void_p ,c_wchar_p,c_int]
        GetDllLibPdf().PdfLayerCollection_AddLayerNS.restype=c_void_p
        intPtr = GetDllLibPdf().PdfLayerCollection_AddLayerNS(self.Ptr, name,enumstate)
        ret = None if intPtr==None else PdfLayer(intPtr)
        return ret


    @dispatch

    def RemoveLayer(self ,layer:PdfLayer)->bool:
        """
    <summary>
        Remove the pdf layer.
    </summary>
    <param name="layer">The pdf layer.</param>
    <returns>
            True if item is successfully removed; otherwise, false. This method also
             returns false if item was not found
            </returns>
        """
        intPtrlayer:c_void_p = layer.Ptr

        GetDllLibPdf().PdfLayerCollection_RemoveLayer.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfLayerCollection_RemoveLayer.restype=c_bool
        ret = GetDllLibPdf().PdfLayerCollection_RemoveLayer(self.Ptr, intPtrlayer)
        return ret

    @dispatch

    def RemoveLayer(self ,layer:PdfLayer,withContent:bool)->bool:
        """
    <summary>
        Remove the pdf layer.
    </summary>
    <param name="layer">The pdf layer.</param>
    <param name="withContent">If true,remove content with the pdf layer.Otherwise,false.</param>
    <returns>
            True if item is successfully removed; otherwise, false. This method also
             returns false if item was not found
            </returns>
        """
        intPtrlayer:c_void_p = layer.Ptr

        GetDllLibPdf().PdfLayerCollection_RemoveLayerLW.argtypes=[c_void_p ,c_void_p,c_bool]
        GetDllLibPdf().PdfLayerCollection_RemoveLayerLW.restype=c_bool
        ret = GetDllLibPdf().PdfLayerCollection_RemoveLayerLW(self.Ptr, intPtrlayer,withContent)
        return ret

    @dispatch

    def RemoveLayer(self ,name:str)->bool:
        """
    <summary>
        Remove the pdf layer.
            Notice: Pdf layer name may be is not unique.
            If exist duplication of name,will remove all pdf layers of name.
    </summary>
    <param name="name">Pdf layer name.</param>
    <returns>
            True if item is successfully removed; otherwise, false. This method also
             returns false if item was not found
            </returns>
        """
        
        GetDllLibPdf().PdfLayerCollection_RemoveLayerN.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfLayerCollection_RemoveLayerN.restype=c_bool
        ret = GetDllLibPdf().PdfLayerCollection_RemoveLayerN(self.Ptr, name)
        return ret

    @dispatch

    def RemoveLayer(self ,name:str,withContent:bool)->bool:
        """
    <summary>
        Remove the pdf layer.
            Notice: Pdf layer name may be is not unique.
            If exist duplication of name,will remove all pdf layers of name.
    </summary>
    <param name="name">Pdf layer name.</param>
    <param name="withContent">If true,remove content with the pdf layer.Otherwise,false.</param>
    <returns>
            True if item is successfully removed; otherwise, false. This method also
             returns false if item was not found
            </returns>
        """
        
        GetDllLibPdf().PdfLayerCollection_RemoveLayerNW.argtypes=[c_void_p ,c_wchar_p,c_bool]
        GetDllLibPdf().PdfLayerCollection_RemoveLayerNW.restype=c_bool
        ret = GetDllLibPdf().PdfLayerCollection_RemoveLayerNW(self.Ptr, name,withContent)
        return ret


    def GetEnumerator(self)->'IEnumerator':
        """

        """
        GetDllLibPdf().PdfLayerCollection_GetEnumerator.argtypes=[c_void_p]
        GetDllLibPdf().PdfLayerCollection_GetEnumerator.restype=c_void_p
        intPtr = GetDllLibPdf().PdfLayerCollection_GetEnumerator(self.Ptr)
        ret = None if intPtr==None else IEnumerator(intPtr)
        return ret


