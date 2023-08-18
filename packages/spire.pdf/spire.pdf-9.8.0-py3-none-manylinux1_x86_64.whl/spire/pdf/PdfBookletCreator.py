from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfBookletCreator (SpireObject) :
    """
    <summary>
        Represents a booklet creator, which allows to create a booklet from a Pdf document.
    </summary>
    """
    @staticmethod
    @dispatch

    def CreateBooklet(document:PdfDocument,outfile:str,pageSize:SizeF):
        """
    <summary>
        Thie method creates a booklet
    </summary>
    <param name="document">The loaded document.</param>
    <param name="outfile">The out file</param>
    <param name="pageSize">Size of the page.</param>
        """
        intPtrdocument:c_void_p = document.Ptr
        intPtrpageSize:c_void_p = pageSize.Ptr

        GetDllLibPdf().PdfBookletCreator_CreateBooklet.argtypes=[ c_void_p,c_void_p,c_wchar_p,c_void_p]
        GetDllLibPdf().PdfBookletCreator_CreateBooklet(None, intPtrdocument,outfile,intPtrpageSize)

    @staticmethod
    @dispatch

    def CreateBooklet(document:PdfDocument,outStream:Stream,pageSize:SizeF):
        """
    <summary>
        Thie method creates a booklet
    </summary>
    <param name="document">The loaded document.</param>
    <param name="outStream">The out stream</param>
    <param name="pageSize">Size of the page.</param>
        """
        intPtrdocument:c_void_p = document.Ptr
        intPtroutStream:c_void_p = outStream.Ptr
        intPtrpageSize:c_void_p = pageSize.Ptr

        GetDllLibPdf().PdfBookletCreator_CreateBookletDOP.argtypes=[ c_void_p,c_void_p,c_void_p,c_void_p]
        GetDllLibPdf().PdfBookletCreator_CreateBookletDOP( None,intPtrdocument,intPtroutStream,intPtrpageSize)

    @staticmethod
    @dispatch

    def CreateBooklet(document:PdfDocument,outStream:Stream,pageSize:SizeF,bookletOptions:BookletOptions):
        """
    <summary>
        Thie method creates a booklet
    </summary>
    <param name="document">The loaded document.</param>
    <param name="outStream">The out stream</param>
    <param name="pageSize">Size of the page.</param>
    <param name="bookletOptions">Set BookletBinding,default value Left.</param>
        """
        intPtrdocument:c_void_p = document.Ptr
        intPtroutStream:c_void_p = outStream.Ptr
        intPtrpageSize:c_void_p = pageSize.Ptr
        intPtrbookletOptions:c_void_p = bookletOptions.Ptr

        GetDllLibPdf().PdfBookletCreator_CreateBookletDOPB.argtypes=[ c_void_p,c_void_p,c_void_p,c_void_p,c_void_p]
        GetDllLibPdf().PdfBookletCreator_CreateBookletDOPB( None,intPtrdocument,intPtroutStream,intPtrpageSize,intPtrbookletOptions)

