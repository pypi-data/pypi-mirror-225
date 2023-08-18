from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfUnidimensionalBarcode (  PdfBarcode) :
    """
    <summary>
        Represents the Base class for all the Single dimensional barcodes
    </summary>
    """
    @property

    def Font(self)->'PdfFontBase':
        """
    <summary>
        Gets or sets the Text font.
    </summary>
        """
        GetDllLibPdf().PdfUnidimensionalBarcode_get_Font.argtypes=[c_void_p]
        GetDllLibPdf().PdfUnidimensionalBarcode_get_Font.restype=c_void_p
        intPtr = GetDllLibPdf().PdfUnidimensionalBarcode_get_Font(self.Ptr)
        ret = None if intPtr==None else PdfFontBase(intPtr)
        return ret


    @Font.setter
    def Font(self, value:'PdfFontBase'):
        GetDllLibPdf().PdfUnidimensionalBarcode_set_Font.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfUnidimensionalBarcode_set_Font(self.Ptr, value.Ptr)

    @property

    def TextDisplayLocation(self)->'TextLocation':
        """
    <summary>
        Gets or sets the text display location. 
    </summary>
        """
        GetDllLibPdf().PdfUnidimensionalBarcode_get_TextDisplayLocation.argtypes=[c_void_p]
        GetDllLibPdf().PdfUnidimensionalBarcode_get_TextDisplayLocation.restype=c_int
        ret = GetDllLibPdf().PdfUnidimensionalBarcode_get_TextDisplayLocation(self.Ptr)
        objwraped = TextLocation(ret)
        return objwraped

    @TextDisplayLocation.setter
    def TextDisplayLocation(self, value:'TextLocation'):
        GetDllLibPdf().PdfUnidimensionalBarcode_set_TextDisplayLocation.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfUnidimensionalBarcode_set_TextDisplayLocation(self.Ptr, value.value)

    @property
    def ShowCheckDigit(self)->bool:
        """
<summary></summary>
<remarks>The Default value is false.</remarks>
        """
        GetDllLibPdf().PdfUnidimensionalBarcode_get_ShowCheckDigit.argtypes=[c_void_p]
        GetDllLibPdf().PdfUnidimensionalBarcode_get_ShowCheckDigit.restype=c_bool
        ret = GetDllLibPdf().PdfUnidimensionalBarcode_get_ShowCheckDigit(self.Ptr)
        return ret

    @ShowCheckDigit.setter
    def ShowCheckDigit(self, value:bool):
        GetDllLibPdf().PdfUnidimensionalBarcode_set_ShowCheckDigit.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfUnidimensionalBarcode_set_ShowCheckDigit(self.Ptr, value)

    @property
    def EnableCheckDigit(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether to enable to check digit calculation in the generated barcode or not.
    </summary>
<remarks>The Default value is True.</remarks>
        """
        GetDllLibPdf().PdfUnidimensionalBarcode_get_EnableCheckDigit.argtypes=[c_void_p]
        GetDllLibPdf().PdfUnidimensionalBarcode_get_EnableCheckDigit.restype=c_bool
        ret = GetDllLibPdf().PdfUnidimensionalBarcode_get_EnableCheckDigit(self.Ptr)
        return ret

    @EnableCheckDigit.setter
    def EnableCheckDigit(self, value:bool):
        GetDllLibPdf().PdfUnidimensionalBarcode_set_EnableCheckDigit.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfUnidimensionalBarcode_set_EnableCheckDigit(self.Ptr, value)

    @property
    def BarcodeToTextGapHeight(self)->float:
        """
    <summary>
        Gets or sets the gap between the barcode and the displayed text.
    </summary>
        """
        GetDllLibPdf().PdfUnidimensionalBarcode_get_BarcodeToTextGapHeight.argtypes=[c_void_p]
        GetDllLibPdf().PdfUnidimensionalBarcode_get_BarcodeToTextGapHeight.restype=c_float
        ret = GetDllLibPdf().PdfUnidimensionalBarcode_get_BarcodeToTextGapHeight(self.Ptr)
        return ret

    @BarcodeToTextGapHeight.setter
    def BarcodeToTextGapHeight(self, value:float):
        GetDllLibPdf().PdfUnidimensionalBarcode_set_BarcodeToTextGapHeight.argtypes=[c_void_p, c_float]
        GetDllLibPdf().PdfUnidimensionalBarcode_set_BarcodeToTextGapHeight(self.Ptr, value)

    @property

    def TextAlignment(self)->'PdfBarcodeTextAlignment':
        """
    <summary>
        Gets or sets the alignment of the text displayed on the barcode.
    </summary>
<remarks>Default value is Center.</remarks>
        """
        GetDllLibPdf().PdfUnidimensionalBarcode_get_TextAlignment.argtypes=[c_void_p]
        GetDllLibPdf().PdfUnidimensionalBarcode_get_TextAlignment.restype=c_int
        ret = GetDllLibPdf().PdfUnidimensionalBarcode_get_TextAlignment(self.Ptr)
        objwraped = PdfBarcodeTextAlignment(ret)
        return objwraped

    @TextAlignment.setter
    def TextAlignment(self, value:'PdfBarcodeTextAlignment'):
        GetDllLibPdf().PdfUnidimensionalBarcode_set_TextAlignment.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfUnidimensionalBarcode_set_TextAlignment(self.Ptr, value.value)

    @property
    def EncodeStartStopSymbols(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether [encode start stop symbols].
    </summary>
<value>
  <c>true</c> if [encode start stop symbols]; otherwise, <c>false</c>.
            </value>
        """
        GetDllLibPdf().PdfUnidimensionalBarcode_get_EncodeStartStopSymbols.argtypes=[c_void_p]
        GetDllLibPdf().PdfUnidimensionalBarcode_get_EncodeStartStopSymbols.restype=c_bool
        ret = GetDllLibPdf().PdfUnidimensionalBarcode_get_EncodeStartStopSymbols(self.Ptr)
        return ret

    @EncodeStartStopSymbols.setter
    def EncodeStartStopSymbols(self, value:bool):
        GetDllLibPdf().PdfUnidimensionalBarcode_set_EncodeStartStopSymbols.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfUnidimensionalBarcode_set_EncodeStartStopSymbols(self.Ptr, value)

    @dispatch

    def Draw(self ,page:PdfPageBase,rect:RectangleF):
        """
    <summary>
        Draws the barcode on the  at the specified region.
    </summary>
    <param name="page">The pdf page.</param>
    <param name="rect">The barcode region.</param>
        """
        intPtrpage:c_void_p = page.Ptr
        intPtrrect:c_void_p = rect.Ptr

        GetDllLibPdf().PdfUnidimensionalBarcode_Draw.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().PdfUnidimensionalBarcode_Draw(self.Ptr, intPtrpage,intPtrrect)

    @dispatch

    def Draw(self ,page:PdfPageBase,location:PointF):
        """
    <summary>
        Draws the barcode on the  at the specified location.
    </summary>
    <param name="page">The pdf page.</param>
    <param name="location">The barcode location.</param>
        """
        intPtrpage:c_void_p = page.Ptr
        intPtrlocation:c_void_p = location.Ptr

        GetDllLibPdf().PdfUnidimensionalBarcode_DrawPL.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().PdfUnidimensionalBarcode_DrawPL(self.Ptr, intPtrpage,intPtrlocation)


    def ToImage(self)->'Image':
        """
    <summary>
        Exports the barcode as image.
                <returns>The barcode image.</returns></summary>
        """
        GetDllLibPdf().PdfUnidimensionalBarcode_ToImage.argtypes=[c_void_p]
        GetDllLibPdf().PdfUnidimensionalBarcode_ToImage.restype=c_void_p
        intPtr = GetDllLibPdf().PdfUnidimensionalBarcode_ToImage(self.Ptr)
        ret = None if intPtr==None else Image(intPtr)
        return ret


