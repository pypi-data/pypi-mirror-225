from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfLayer (SpireObject) :
    """
    <summary>
        Represent pdf optional content group.
            Content typically belongs to a single optional content group.
    </summary>
    """
    @property

    def Name(self)->str:
        """
    <summary>
        Get or set pdf layer name.
            Notice: 
            Name may be is not unique.
    </summary>
        """
        GetDllLibPdf().PdfLayer_get_Name.argtypes=[c_void_p]
        GetDllLibPdf().PdfLayer_get_Name.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfLayer_get_Name(self.Ptr))
        return ret


    @Name.setter
    def Name(self, value:str):
        GetDllLibPdf().PdfLayer_set_Name.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfLayer_set_Name(self.Ptr, value)

    @property

    def ViewState(self)->'LayerViewState':
        """
    <summary>
        Get or set pdf layer view state.
    </summary>
        """
        GetDllLibPdf().PdfLayer_get_ViewState.argtypes=[c_void_p]
        GetDllLibPdf().PdfLayer_get_ViewState.restype=c_int
        ret = GetDllLibPdf().PdfLayer_get_ViewState(self.Ptr)
        objwraped = LayerViewState(ret)
        return objwraped

    @ViewState.setter
    def ViewState(self, value:'LayerViewState'):
        GetDllLibPdf().PdfLayer_set_ViewState.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfLayer_set_ViewState(self.Ptr, value.value)

    @property

    def ExportState(self)->'LayerExportState':
        """
    <summary>
        Get or set pdf layer export state.
    </summary>
        """
        GetDllLibPdf().PdfLayer_get_ExportState.argtypes=[c_void_p]
        GetDllLibPdf().PdfLayer_get_ExportState.restype=c_int
        ret = GetDllLibPdf().PdfLayer_get_ExportState(self.Ptr)
        objwraped = LayerExportState(ret)
        return objwraped

    @ExportState.setter
    def ExportState(self, value:'LayerExportState'):
        GetDllLibPdf().PdfLayer_set_ExportState.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfLayer_set_ExportState(self.Ptr, value.value)

    @property

    def PrintState(self)->'LayerPrintState':
        """
    <summary>
        Get or set pdf layer print state.
    </summary>
        """
        GetDllLibPdf().PdfLayer_get_PrintState.argtypes=[c_void_p]
        GetDllLibPdf().PdfLayer_get_PrintState.restype=c_int
        ret = GetDllLibPdf().PdfLayer_get_PrintState(self.Ptr)
        objwraped = LayerPrintState(ret)
        return objwraped

    @PrintState.setter
    def PrintState(self, value:'LayerPrintState'):
        GetDllLibPdf().PdfLayer_set_PrintState.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfLayer_set_PrintState(self.Ptr, value.value)

    @property

    def Visibility(self)->'PdfVisibility':
        """
    <summary>
        Get or set pdf layer visible.
    </summary>
        """
        GetDllLibPdf().PdfLayer_get_Visibility.argtypes=[c_void_p]
        GetDllLibPdf().PdfLayer_get_Visibility.restype=c_int
        ret = GetDllLibPdf().PdfLayer_get_Visibility(self.Ptr)
        objwraped = PdfVisibility(ret)
        return objwraped

    @Visibility.setter
    def Visibility(self, value:'PdfVisibility'):
        GetDllLibPdf().PdfLayer_set_Visibility.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfLayer_set_Visibility(self.Ptr, value.value)

    @property
    def IsShowOnUI(self)->bool:
        """
    <summary>
        Get whether the layer shows on user interface or not.
    </summary>
        """
        GetDllLibPdf().PdfLayer_get_IsShowOnUI.argtypes=[c_void_p]
        GetDllLibPdf().PdfLayer_get_IsShowOnUI.restype=c_bool
        ret = GetDllLibPdf().PdfLayer_get_IsShowOnUI(self.Ptr)
        return ret

    @property

    def Reference(self)->str:
        """
    <summary>
        Get reference of the layer.
    </summary>
        """
        GetDllLibPdf().PdfLayer_get_Reference.argtypes=[c_void_p]
        GetDllLibPdf().PdfLayer_get_Reference.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfLayer_get_Reference(self.Ptr))
        return ret



    def CreateGraphics(self ,g:'PdfCanvas')->'PdfCanvas':
        """
    <summary>
        Create the layer graphics.
    </summary>
    <param name="g">
            The pdf layer container's graphics.
            eg: PdfPageBase.Canvas ...
    </param>
    <returns>The pdf layer graphics.</returns>
        """
        intPtrg:c_void_p = g.Ptr

        GetDllLibPdf().PdfLayer_CreateGraphics.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfLayer_CreateGraphics.restype=c_void_p
        intPtr = GetDllLibPdf().PdfLayer_CreateGraphics(self.Ptr, intPtrg)
        ret = None if intPtr==None else PdfCanvas(intPtr)
        return ret


