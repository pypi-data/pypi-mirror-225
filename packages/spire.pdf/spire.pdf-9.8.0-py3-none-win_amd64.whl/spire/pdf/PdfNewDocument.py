from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfNewDocument (  PdfDocumentBase) :
    @dispatch
    def __init__(self):
        GetDllLibPdf().PdfNewDocument_CreatePdfNewDocument.restype = c_void_p
        intPtr = GetDllLibPdf().PdfNewDocument_CreatePdfNewDocument()
        super(PdfNewDocument, self).__init__(intPtr)

    """
    <summary>
        Represents a logic to create Pdf document.
    </summary>
    """

    def add_SaveProgress(self ,value:'ProgressEventHandler'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().PdfNewDocument_add_SaveProgress.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfNewDocument_add_SaveProgress(self.Ptr, intPtrvalue)


    def remove_SaveProgress(self ,value:'ProgressEventHandler'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().PdfNewDocument_remove_SaveProgress.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfNewDocument_remove_SaveProgress(self.Ptr, intPtrvalue)

    @property

    def Bookmarks(self)->'PdfBookmarkCollection':
        """
    <summary>
        Gets the root of the bookmark tree in the document.
    </summary>
<value>A  object specifying the document's bookmarks. </value>
<remarks>Creates an bookmark root instance
            if it's called for first time.</remarks>
        """
        GetDllLibPdf().PdfNewDocument_get_Bookmarks.argtypes=[c_void_p]
        GetDllLibPdf().PdfNewDocument_get_Bookmarks.restype=c_void_p
        intPtr = GetDllLibPdf().PdfNewDocument_get_Bookmarks(self.Ptr)
        ret = None if intPtr==None else PdfBookmarkCollection(intPtr)
        return ret


    @property

    def Attachments(self)->'PdfAttachmentCollection':
        """
    <summary>
        Gets the attachments of the document.
    </summary>
<value>The  object contains list of files which are attached in the PDF document.</value>
        """
        GetDllLibPdf().PdfNewDocument_get_Attachments.argtypes=[c_void_p]
        GetDllLibPdf().PdfNewDocument_get_Attachments.restype=c_void_p
        intPtr = GetDllLibPdf().PdfNewDocument_get_Attachments(self.Ptr)
        ret = None if intPtr==None else PdfAttachmentCollection(intPtr)
        return ret


    @property

    def Form(self)->'PdfForm':
        """
    <summary>
        Gets the interactive form of the document.
    </summary>
<value>The  object contains the list of form elements of the document.</value>
        """
        GetDllLibPdf().PdfNewDocument_get_Form.argtypes=[c_void_p]
        GetDllLibPdf().PdfNewDocument_get_Form.restype=c_void_p
        intPtr = GetDllLibPdf().PdfNewDocument_get_Form(self.Ptr)
        ret = None if intPtr==None else PdfForm(intPtr)
        return ret


    @property

    def ColorSpace(self)->'PdfColorSpace':
        """
    <summary>
        Gets or sets the color space of the document.
    </summary>
<remarks>This property has impact on the new created pages only.
            If a page was created it remains its colour space obliviously
            to this property changes.</remarks>
<value>The  of the document.</value>
        """
        GetDllLibPdf().PdfNewDocument_get_ColorSpace.argtypes=[c_void_p]
        GetDllLibPdf().PdfNewDocument_get_ColorSpace.restype=c_int
        ret = GetDllLibPdf().PdfNewDocument_get_ColorSpace(self.Ptr)
        objwraped = PdfColorSpace(ret)
        return objwraped

    @ColorSpace.setter
    def ColorSpace(self, value:'PdfColorSpace'):
        GetDllLibPdf().PdfNewDocument_set_ColorSpace.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfNewDocument_set_ColorSpace(self.Ptr, value.value)

    @property

    def Conformance(self)->'PdfConformanceLevel':
        """
    <summary>
        Gets or Sets the Pdf Conformance level.
            Supported : PDF/A-1b - Level B compliance in Part 1
    </summary>
        """
        GetDllLibPdf().PdfNewDocument_get_Conformance.argtypes=[c_void_p]
        GetDllLibPdf().PdfNewDocument_get_Conformance.restype=c_int
        ret = GetDllLibPdf().PdfNewDocument_get_Conformance(self.Ptr)
        objwraped = PdfConformanceLevel(ret)
        return objwraped

    def Save(self ,stream:'Stream'):
        """
    <summary>
        Saves the document to the specified stream.
    </summary>
    <param name="stream">The stream object where PDF document will be saved.</param>
        """
        intPtrstream:c_void_p = stream.Ptr

        GetDllLibPdf().PdfNewDocument_Save.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfNewDocument_Save(self.Ptr, intPtrstream)


    def Close(self ,completely:bool):
        """
    <summary>
        Closes the document.
    </summary>
    <param name="completely">if set to <c>true</c> the document should be disposed completely.</param>
<remarks>The document is disposed after calling the Close method. So, the document can not be saved if Close method was invoked.</remarks>
        """
        
        GetDllLibPdf().PdfNewDocument_Close.argtypes=[c_void_p ,c_bool]
        GetDllLibPdf().PdfNewDocument_Close(self.Ptr, completely)


    def Clone(self)->'SpireObject':
        """
    <summary>
        Creates a new object that is a copy of the current instance.
    </summary>
<value>A new object that is a copy of this instance.</value>
<remarks>The resulting clone must be of the same type as or a compatible type to the original instance.</remarks>
        """
        GetDllLibPdf().PdfNewDocument_Clone.argtypes=[c_void_p]
        GetDllLibPdf().PdfNewDocument_Clone.restype=c_void_p
        intPtr = GetDllLibPdf().PdfNewDocument_Clone(self.Ptr)
        ret = None if intPtr==None else SpireObject(intPtr)
        return ret


