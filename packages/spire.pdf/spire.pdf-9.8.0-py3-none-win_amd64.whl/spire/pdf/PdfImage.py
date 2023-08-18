from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfImage (  PdfShapeWidget) :
    """
    <summary>
        Represents the base class for images.
    </summary>
    """
    @property
    def Height(self)->int:
        """
    <summary>
        Gets the height of the image in pixels.
    </summary>
<value>The height.</value>
        """
        GetDllLibPdf().PdfImage_get_Height.argtypes=[c_void_p]
        GetDllLibPdf().PdfImage_get_Height.restype=c_int
        ret = GetDllLibPdf().PdfImage_get_Height(self.Ptr)
        return ret

    @property
    def PngDirectToJpeg(self)->bool:
        """
    <summary>
        If True, png direct convert to Jpx and no mask.
    </summary>
        """
        GetDllLibPdf().PdfImage_get_PngDirectToJpeg.argtypes=[c_void_p]
        GetDllLibPdf().PdfImage_get_PngDirectToJpeg.restype=c_bool
        ret = GetDllLibPdf().PdfImage_get_PngDirectToJpeg(self.Ptr)
        return ret

    @PngDirectToJpeg.setter
    def PngDirectToJpeg(self, value:bool):
        GetDllLibPdf().PdfImage_set_PngDirectToJpeg.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfImage_set_PngDirectToJpeg(self.Ptr, value)

    @property
    def Width(self)->int:
        """
    <summary>
        Gets the width of the image in pixels.
    </summary>
<value>The width.</value>
        """
        GetDllLibPdf().PdfImage_get_Width.argtypes=[c_void_p]
        GetDllLibPdf().PdfImage_get_Width.restype=c_int
        ret = GetDllLibPdf().PdfImage_get_Width(self.Ptr)
        return ret

    @property
    def HorizontalResolution(self)->float:
        """
    <summary>
        Gets the horizontal resolution, in pixels per inch, of this Image. 
    </summary>
<value>The horizontal resolution.</value>
        """
        GetDllLibPdf().PdfImage_get_HorizontalResolution.argtypes=[c_void_p]
        GetDllLibPdf().PdfImage_get_HorizontalResolution.restype=c_float
        ret = GetDllLibPdf().PdfImage_get_HorizontalResolution(self.Ptr)
        return ret

    @property
    def VerticalResolution(self)->float:
        """
    <summary>
        Gets the vertical resolution, in pixels per inch, of this Image. 
    </summary>
<value>The vertical resolution.</value>
        """
        GetDllLibPdf().PdfImage_get_VerticalResolution.argtypes=[c_void_p]
        GetDllLibPdf().PdfImage_get_VerticalResolution.restype=c_float
        ret = GetDllLibPdf().PdfImage_get_VerticalResolution(self.Ptr)
        return ret

    @property

    def PhysicalDimension(self)->'SizeF':
        """
    <summary>
        Returns the size of the image in points.
    </summary>
<remarks>This property uses HorizontalResolution and VerticalResolution for calculating the size in points.</remarks>
        """
        GetDllLibPdf().PdfImage_get_PhysicalDimension.argtypes=[c_void_p]
        GetDllLibPdf().PdfImage_get_PhysicalDimension.restype=c_void_p
        intPtr = GetDllLibPdf().PdfImage_get_PhysicalDimension(self.Ptr)
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @property
    def ActiveFrame(self)->int:
        """
    <summary>
        Gets or sets the active frame of the image.
    </summary>
        """
        GetDllLibPdf().PdfImage_get_ActiveFrame.argtypes=[c_void_p]
        GetDllLibPdf().PdfImage_get_ActiveFrame.restype=c_int
        ret = GetDllLibPdf().PdfImage_get_ActiveFrame(self.Ptr)
        return ret

    @ActiveFrame.setter
    def ActiveFrame(self, value:int):
        GetDllLibPdf().PdfImage_set_ActiveFrame.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfImage_set_ActiveFrame(self.Ptr, value)

    @property
    def FrameCount(self)->int:
        """
    <summary>
        Gets the number of frames in the image.
    </summary>
        """
        GetDllLibPdf().PdfImage_get_FrameCount.argtypes=[c_void_p]
        GetDllLibPdf().PdfImage_get_FrameCount.restype=c_int
        ret = GetDllLibPdf().PdfImage_get_FrameCount(self.Ptr)
        return ret

    @staticmethod

    def FromFile(path:str)->'PdfImage':
        """
    <summary>
        Creates PdfImage from a file.
    </summary>
    <param name="path">Path to a file.</param>
    <returns>Returns a created PdfImage object.</returns>
        """
        
        GetDllLibPdf().PdfImage_FromFile.argtypes=[ c_wchar_p]
        GetDllLibPdf().PdfImage_FromFile.restype=c_void_p
        intPtr = GetDllLibPdf().PdfImage_FromFile( path)
        ret = None if intPtr==None else PdfImage(intPtr)
        return ret


    @staticmethod

    def FromStream(stream:'Stream')->'PdfImage':
        """
    <summary>
        Creates PdfImage from stream.
    </summary>
    <param name="stream">The stream.</param>
    <returns>Returns a created PdfImage object.</returns>
        """
        intPtrstream:c_void_p = stream.Ptr

        GetDllLibPdf().PdfImage_FromStream.argtypes=[ c_void_p]
        GetDllLibPdf().PdfImage_FromStream.restype=c_void_p
        intPtr = GetDllLibPdf().PdfImage_FromStream( intPtrstream)
        ret = None if intPtr==None else PdfImage(intPtr)
        return ret


    @staticmethod

    def FromImage(image:'Image')->'PdfImage':
        """
    <summary>
        Converts a  object into a PDF image.
    </summary>
    <param name="image">The image.</param>
    <returns>Returns a created PdfImage object.</returns>
        """
        intPtrimage:c_void_p = image.Ptr

        GetDllLibPdf().PdfImage_FromImage.argtypes=[ c_void_p]
        GetDllLibPdf().PdfImage_FromImage.restype=c_void_p
        intPtr = GetDllLibPdf().PdfImage_FromImage( intPtrimage)
        ret = None if intPtr==None else PdfImage(intPtr)
        return ret


    @staticmethod
    @dispatch

    def FromRtf(rtf:str,width:float,type:PdfImageType,format:PdfStringFormat)->'PdfImage':
        """
    <summary>
        Creates a new image instance from RTF text.
    </summary>
    <param name="rtf">RTF text data.</param>
    <param name="width">Width of the image in points.</param>
    <param name="type">Type of the image that should be created.</param>
    <param name="format">The text string format.</param>
    <returns>PdfImage containing RTF text.</returns>
        """
        enumtype:c_int = type.value
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfImage_FromRtf.argtypes=[ c_wchar_p,c_float,c_int,c_void_p]
        GetDllLibPdf().PdfImage_FromRtf.restype=c_void_p
        intPtr = GetDllLibPdf().PdfImage_FromRtf( rtf,width,enumtype,intPtrformat)
        ret = None if intPtr==None else PdfImage(intPtr)
        return ret


    @staticmethod
    @dispatch

    def FromRtf(rtf:str,width:float,type:PdfImageType)->'PdfImage':
        """
    <summary>
        Creates a new image instance from RTF text.
    </summary>
    <param name="rtf">RTF text data.</param>
    <param name="width">Width of the image in points.</param>
    <param name="type">Type of the image that should be created.</param>
    <returns>PdfImage containing RTF text.</returns>
        """
        enumtype:c_int = type.value

        GetDllLibPdf().PdfImage_FromRtfRWT.argtypes=[ c_wchar_p,c_float,c_int]
        GetDllLibPdf().PdfImage_FromRtfRWT.restype=c_void_p
        intPtr = GetDllLibPdf().PdfImage_FromRtfRWT( rtf,width,enumtype)
        ret = None if intPtr==None else PdfImage(intPtr)
        return ret


    @staticmethod
    @dispatch

    def FromRtf(rtf:str,width:float,height:float,type:PdfImageType)->'PdfImage':
        """
    <summary>
        Creates a new image instance from RTF text.
    </summary>
    <param name="rtf">RTF text data.</param>
    <param name="width">Width of the image in points.</param>
    <param name="height">Height of the image in points.</param>
    <param name="type">Type of the image that should be created.</param>
    <returns>PdfImage containing RTF text.</returns>
        """
        enumtype:c_int = type.value

        GetDllLibPdf().PdfImage_FromRtfRWHT.argtypes=[ c_wchar_p,c_float,c_float,c_int]
        GetDllLibPdf().PdfImage_FromRtfRWHT.restype=c_void_p
        intPtr = GetDllLibPdf().PdfImage_FromRtfRWHT( rtf,width,height,enumtype)
        ret = None if intPtr==None else PdfImage(intPtr)
        return ret


    @staticmethod
    @dispatch

    def FromRtf(rtf:str,width:float,height:float,type:PdfImageType,format:PdfStringFormat)->'PdfImage':
        """
    <summary>
        Creates a new image instance from RTF text.
    </summary>
    <param name="rtf">RTF text data.</param>
    <param name="width">Width of the image in points.</param>
    <param name="height">Height of the image in points.</param>
    <param name="type">Type of the image that should be created.</param>
    <param name="format">The text string format.</param>
    <returns>PdfImage containing RTF text.</returns>
        """
        enumtype:c_int = type.value
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfImage_FromRtfRWHTF.argtypes=[ c_wchar_p,c_float,c_float,c_int,c_void_p]
        GetDllLibPdf().PdfImage_FromRtfRWHTF.restype=c_void_p
        intPtr = GetDllLibPdf().PdfImage_FromRtfRWHTF( rtf,width,height,enumtype,intPtrformat)
        ret = None if intPtr==None else PdfImage(intPtr)
        return ret


