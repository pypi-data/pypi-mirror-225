from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfConvertOptions (SpireObject) :
    """
    <summary>
        The class can be used to set some options when do convert operation.
    </summary>
    """
    @property
    def FindTextByAbsolutePosition(self)->bool:
        """
    <summary>
        Find Text in PDF file by absolute position or operator order.default is true. 
    </summary>
        """
        GetDllLibPdf().PdfConvertOptions_get_FindTextByAbsolutePosition.argtypes=[c_void_p]
        GetDllLibPdf().PdfConvertOptions_get_FindTextByAbsolutePosition.restype=c_bool
        ret = GetDllLibPdf().PdfConvertOptions_get_FindTextByAbsolutePosition(self.Ptr)
        return ret

    @FindTextByAbsolutePosition.setter
    def FindTextByAbsolutePosition(self, value:bool):
        GetDllLibPdf().PdfConvertOptions_set_FindTextByAbsolutePosition.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfConvertOptions_set_FindTextByAbsolutePosition(self.Ptr, value)


    def SetPdfToImageOptions(self ,bgTransparentValue:int):
        """
    <summary>
        Set pdf to image convert options.
    </summary>
    <param name="bgTransparentValue">Alpha values rang from 0 to 255</param>
        """
        
        GetDllLibPdf().PdfConvertOptions_SetPdfToImageOptions.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfConvertOptions_SetPdfToImageOptions(self.Ptr, bgTransparentValue)


    def SetPdfToXlsxOptions(self ,options:'XlsxOptions'):
        """
    <summary>
        Set pdf to xlsx convert options
            the parameter is：the implementation class the xlsxOptions class
            The implementation class:XlsxLineLayoutOptions or XlsxTextLayoutOptions
    </summary>
    <param name="options"></param>
        """
        intPtroptions:c_void_p = options.Ptr

        GetDllLibPdf().PdfConvertOptions_SetPdfToXlsxOptions.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfConvertOptions_SetPdfToXlsxOptions(self.Ptr, intPtroptions)

    @dispatch
    def SetPdfToXpsOptions(self):
        """
    <summary>
        Set pdf to xps convert options.
            Default usePsMode = true,useInvariantCulture = false,useHighQualityImg = false.
    </summary>
        """
        GetDllLibPdf().PdfConvertOptions_SetPdfToXpsOptions.argtypes=[c_void_p]
        GetDllLibPdf().PdfConvertOptions_SetPdfToXpsOptions(self.Ptr)

    @dispatch

    def SetPdfToXpsOptions(self ,usePsMode:bool):
        """
    <summary>
        Set pdf to xps convert options.
    </summary>
    <param name="usePsMode">Indicates whether to use PS mode.</param>
        """
        
        GetDllLibPdf().PdfConvertOptions_SetPdfToXpsOptionsU.argtypes=[c_void_p ,c_bool]
        GetDllLibPdf().PdfConvertOptions_SetPdfToXpsOptionsU(self.Ptr, usePsMode)

    @dispatch

    def SetPdfToXpsOptions(self ,usePsMode:bool,useInvariantCulture:bool):
        """
    <summary>
        Set pdf to xps convert options.
    </summary>
    <param name="usePsMode">Indicates whether to use PS mode.</param>
    <param name="useInvariantCulture">Indicates whether to use invariant culture.</param>
        """
        
        GetDllLibPdf().PdfConvertOptions_SetPdfToXpsOptionsUU.argtypes=[c_void_p ,c_bool,c_bool]
        GetDllLibPdf().PdfConvertOptions_SetPdfToXpsOptionsUU(self.Ptr, usePsMode,useInvariantCulture)

    @dispatch

    def SetPdfToXpsOptions(self ,usePsMode:bool,useInvariantCulture:bool,useHighQualityImg:bool):
        """
    <summary>
        Set pdf to xps convert options.
    </summary>
    <param name="usePsMode">Indicates whether to use PS mode.</param>
    <param name="useInvariantCulture">Indicates whether to use invariant culture.</param>
    <param name="useHighQualityImg">Indicates whether to use the high qulity image.</param>
        """
        
        GetDllLibPdf().PdfConvertOptions_SetPdfToXpsOptionsUUU.argtypes=[c_void_p ,c_bool,c_bool,c_bool]
        GetDllLibPdf().PdfConvertOptions_SetPdfToXpsOptionsUUU(self.Ptr, usePsMode,useInvariantCulture,useHighQualityImg)

    @dispatch
    def SetPdfToDocOptions(self):
        """
    <summary>
        Set pdf to doc convert options.
            Default usePsMode = true.
    </summary>
        """
        GetDllLibPdf().PdfConvertOptions_SetPdfToDocOptions.argtypes=[c_void_p]
        GetDllLibPdf().PdfConvertOptions_SetPdfToDocOptions(self.Ptr)

    @dispatch

    def SetPdfToDocOptions(self ,usePsMode:bool):
        """
    <summary>
        Set pdf to doc convert options.
    </summary>
    <param name="usePsMode">Indicates whether to use PS mode.</param>
        """
        
        GetDllLibPdf().PdfConvertOptions_SetPdfToDocOptionsU.argtypes=[c_void_p ,c_bool]
        GetDllLibPdf().PdfConvertOptions_SetPdfToDocOptionsU(self.Ptr, usePsMode)

    @dispatch

    def SetPdfToDocOptions(self ,usePsMode:bool,useFlowRecognitionMode:bool):
        """
    <summary>
        Set pdf to doc convert options.
    </summary>
    <param name="usePsMode">Indicates whether to use PS mode.</param>
    <param name="useFlowRecognitionMode">Indicates whether to use flow recognition mode.</param>
        """
        
        GetDllLibPdf().PdfConvertOptions_SetPdfToDocOptionsUU.argtypes=[c_void_p ,c_bool,c_bool]
        GetDllLibPdf().PdfConvertOptions_SetPdfToDocOptionsUU(self.Ptr, usePsMode,useFlowRecognitionMode)

    @dispatch
    def SetXpsToPdfOptions(self):
        """
    <summary>
        Set xps to pdf convert options.
            Default useHighQualityImg = false.
    </summary>
        """
        GetDllLibPdf().PdfConvertOptions_SetXpsToPdfOptions.argtypes=[c_void_p]
        GetDllLibPdf().PdfConvertOptions_SetXpsToPdfOptions(self.Ptr)

    @dispatch

    def SetXpsToPdfOptions(self ,useHighQualityImg:bool):
        """
    <summary>
        Set xps to pdf convert options.
    </summary>
    <param name="useHighQualityImg">Indicates whether to use the high qulity image.</param>
        """
        
        GetDllLibPdf().PdfConvertOptions_SetXpsToPdfOptionsU.argtypes=[c_void_p ,c_bool]
        GetDllLibPdf().PdfConvertOptions_SetXpsToPdfOptionsU(self.Ptr, useHighQualityImg)

    @dispatch
    def SetPdfToHtmlOptions(self):
        """
    <summary>
        Set pdf to html convert options.
            Default useEmbeddedSvg = true, useEmbeddedImg = false, maxPageOneFile = 500, useHighQualityEmbeddedSvg=true.
    </summary>
        """
        GetDllLibPdf().PdfConvertOptions_SetPdfToHtmlOptions.argtypes=[c_void_p]
        GetDllLibPdf().PdfConvertOptions_SetPdfToHtmlOptions(self.Ptr)

    @dispatch

    def SetPdfToHtmlOptions(self ,useEmbeddedSvg:bool):
        """
    <summary>
        Set pdf to html convert options.
    </summary>
    <param name="useEmbeddedSvg">Indicates whether to use the embedded svg in html file.</param>
        """
        
        GetDllLibPdf().PdfConvertOptions_SetPdfToHtmlOptionsU.argtypes=[c_void_p ,c_bool]
        GetDllLibPdf().PdfConvertOptions_SetPdfToHtmlOptionsU(self.Ptr, useEmbeddedSvg)

    @dispatch

    def SetPdfToHtmlOptions(self ,useEmbeddedSvg:bool,useEmbeddedImg:bool):
        """
    <summary>
        Set pdf to html convert options.
    </summary>
    <param name="useEmbeddedSvg">Indicates whether to use the embedded svg in html file.</param>
    <param name="useEmbeddedImg">Indicates whether to embed image data in html file, works only when useEmbeddedSvg is set to false.</param>
        """
        
        GetDllLibPdf().PdfConvertOptions_SetPdfToHtmlOptionsUU.argtypes=[c_void_p ,c_bool,c_bool]
        GetDllLibPdf().PdfConvertOptions_SetPdfToHtmlOptionsUU(self.Ptr, useEmbeddedSvg,useEmbeddedImg)

    @dispatch

    def SetPdfToHtmlOptions(self ,useEmbeddedSvg:bool,useEmbeddedImg:bool,maxPageOneFile:int):
        """
    <summary>
        Set pdf to html convert options.
    </summary>
    <param name="useEmbeddedSvg">Indicates whether to use the embedded svg in html file.</param>
    <param name="useEmbeddedImg">Indicates whether to embed image data in html file, works only when useEmbeddedSvg is set to false.</param>
    <param name="maxPageOneFile">Indicates the count of page contents in one html file, works only when useEmbeddedSvg is set to false.</param>
        """
        
        GetDllLibPdf().PdfConvertOptions_SetPdfToHtmlOptionsUUM.argtypes=[c_void_p ,c_bool,c_bool,c_int]
        GetDllLibPdf().PdfConvertOptions_SetPdfToHtmlOptionsUUM(self.Ptr, useEmbeddedSvg,useEmbeddedImg,maxPageOneFile)

    @dispatch

    def SetPdfToHtmlOptions(self ,useEmbeddedSvg:bool,useEmbeddedImg:bool,maxPageOneFile:int,useHighQualityEmbeddedSvg:bool):
        """
    <summary>
        Set pdf to html convert options.
    </summary>
    <param name="useEmbeddedSvg">Indicates whether to use the embedded svg in html file.</param>
    <param name="useEmbeddedImg">Indicates whether to embed image data in html file, works only when useEmbeddedSvg is set to false.</param>
    <param name="maxPageOneFile">Indicates the count of page contents in one html file, works only when useEmbeddedSvg is set to false.</param>
    <param name="useHighQualityEmbeddedSvg">Indicates whether to use the high quality embedded svg in html file, works only when useEmbeddedSvg is set to true.</param>
        """
        
        GetDllLibPdf().PdfConvertOptions_SetPdfToHtmlOptionsUUMU.argtypes=[c_void_p ,c_bool,c_bool,c_int,c_bool]
        GetDllLibPdf().PdfConvertOptions_SetPdfToHtmlOptionsUUMU(self.Ptr, useEmbeddedSvg,useEmbeddedImg,maxPageOneFile,useHighQualityEmbeddedSvg)

    @dispatch
    def SetPdfToSvgOptions(self):
        """
    <summary>
        Set pdf to svg options.
            Default wPixel = -1f, hPixel = -1f, -1f means no change.
    </summary>
        """
        GetDllLibPdf().PdfConvertOptions_SetPdfToSvgOptions.argtypes=[c_void_p]
        GetDllLibPdf().PdfConvertOptions_SetPdfToSvgOptions(self.Ptr)

    @dispatch

    def SetPdfToSvgOptions(self ,wPixel:float):
        """
    <summary>
        Set pdf to svg options.
    </summary>
    <param name="wPixel">The output svg's width in pixel unit, -1f means no change.</param>
        """
        
        GetDllLibPdf().PdfConvertOptions_SetPdfToSvgOptionsW.argtypes=[c_void_p ,c_float]
        GetDllLibPdf().PdfConvertOptions_SetPdfToSvgOptionsW(self.Ptr, wPixel)

    @dispatch

    def SetPdfToSvgOptions(self ,wPixel:float,hPixel:float):
        """
    <summary>
        Set pdf to svg options.
    </summary>
    <param name="wPixel">The output svg's width in pixel unit, -1f means no change.</param>
    <param name="hPixel">The output svg's height in pixel unit, -1f means no change.</param>
        """
        
        GetDllLibPdf().PdfConvertOptions_SetPdfToSvgOptionsWH.argtypes=[c_void_p ,c_float,c_float]
        GetDllLibPdf().PdfConvertOptions_SetPdfToSvgOptionsWH(self.Ptr, wPixel,hPixel)

