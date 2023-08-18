from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfAttachment (  PdfEmbeddedFileSpecification) :
    @dispatch
    def __init__(self, filename:str):
        GetDllLibPdf().PdfAttachment_CreatePdfAttachmentF.argtypes=[c_wchar_p]
        GetDllLibPdf().PdfAttachment_CreatePdfAttachmentF.restype = c_void_p
        intPtr = GetDllLibPdf().PdfAttachment_CreatePdfAttachmentF(filename)
        super(PdfAttachment, self).__init__(intPtr)

    @dispatch
    def __init__(self, filename:str,stream:Stream):
        ptrStream:c_void_p = stream.Ptr
        GetDllLibPdf().PdfAttachment_CreatePdfAttachmentFS.argtypes=[c_wchar_p,c_void_p]
        GetDllLibPdf().PdfAttachment_CreatePdfAttachmentFS.restype = c_void_p
        intPtr = GetDllLibPdf().PdfAttachment_CreatePdfAttachmentFS(filename,ptrStream)
        super(PdfAttachment, self).__init__(intPtr)
    """
    <summary>
        Represents attachments of the Pdf document.
    </summary>
    """
