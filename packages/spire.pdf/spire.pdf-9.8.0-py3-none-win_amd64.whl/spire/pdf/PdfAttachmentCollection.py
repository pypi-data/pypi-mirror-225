from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfAttachmentCollection (  PdfCollection) :
    """
    <summary>
        Represents a collection of the attachment objects.
    </summary>
    """

    def get_Item(self ,index:int)->'PdfAttachment':
        """
    <summary>
        Gets attachment by its index in the collection.
    </summary>
    <param name="index">Index of the attachment.</param>
    <returns>Attachment object by its index in the collection.</returns>
        """
        
        GetDllLibPdf().PdfAttachmentCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfAttachmentCollection_get_Item.restype=c_void_p
        intPtr = GetDllLibPdf().PdfAttachmentCollection_get_Item(self.Ptr, index)
        ret = None if intPtr==None else PdfAttachment(intPtr)
        return ret


    @dispatch

    def Add(self ,attachment:PdfAttachment)->int:
        """
    <summary>
        Adds the specified attachment.
    </summary>
    <param name="attachment">The attachment.</param>
    <returns>Position of the inserted attachment.</returns>
        """
        intPtrattachment:c_void_p = attachment.Ptr

        GetDllLibPdf().PdfAttachmentCollection_Add.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfAttachmentCollection_Add.restype=c_int
        ret = GetDllLibPdf().PdfAttachmentCollection_Add(self.Ptr, intPtrattachment)
        return ret

    @dispatch

    def Add(self ,attachment:PdfAttachment,associatedDocument,association:PdfAttachmentRelationship)->int:
        """
    <summary>
        Adds the specified attachment.
    </summary>
    <param name="attachment">The attachment.</param>
    <param name="associatedDocument">The associated document.</param>
    <param name="association">The relationship between attachment and associated document.</param>
    <returns>Position of the inserted attachment.</returns>
        """
        intPtrattachment:c_void_p = attachment.Ptr
        intPtrassociatedDocument:c_void_p = associatedDocument.Ptr
        enumassociation:c_int = association.value

        GetDllLibPdf().PdfAttachmentCollection_AddAAA.argtypes=[c_void_p ,c_void_p,c_void_p,c_int]
        GetDllLibPdf().PdfAttachmentCollection_AddAAA.restype=c_int
        ret = GetDllLibPdf().PdfAttachmentCollection_AddAAA(self.Ptr, intPtrattachment,intPtrassociatedDocument,enumassociation)
        return ret


    def Insert(self ,index:int,attachment:'PdfAttachment'):
        """
    <summary>
        Inserts the specified index.
    </summary>
    <param name="index">The index.</param>
    <param name="attachment">The attachment.</param>
        """
        intPtrattachment:c_void_p = attachment.Ptr

        GetDllLibPdf().PdfAttachmentCollection_Insert.argtypes=[c_void_p ,c_int,c_void_p]
        GetDllLibPdf().PdfAttachmentCollection_Insert(self.Ptr, index,intPtrattachment)


    def Remove(self ,attachment:'PdfAttachment'):
        """
    <summary>
        Removes the specified attachment.
    </summary>
    <param name="attachment">The attachment.</param>
        """
        intPtrattachment:c_void_p = attachment.Ptr

        GetDllLibPdf().PdfAttachmentCollection_Remove.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfAttachmentCollection_Remove(self.Ptr, intPtrattachment)


    def RemoveAt(self ,index:int):
        """
    <summary>
        Removes attachment at the specified index.
    </summary>
    <param name="index">The index.</param>
        """
        
        GetDllLibPdf().PdfAttachmentCollection_RemoveAt.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfAttachmentCollection_RemoveAt(self.Ptr, index)


    def IndexOf(self ,attachment:'PdfAttachment')->int:
        """
    <summary>
        Indexes the of attachment.
    </summary>
    <param name="attachment">The attachment.</param>
    <returns></returns>
        """
        intPtrattachment:c_void_p = attachment.Ptr

        GetDllLibPdf().PdfAttachmentCollection_IndexOf.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfAttachmentCollection_IndexOf.restype=c_int
        ret = GetDllLibPdf().PdfAttachmentCollection_IndexOf(self.Ptr, intPtrattachment)
        return ret


    def Contains(self ,attachment:'PdfAttachment')->bool:
        """
    <summary>
        Determines whether 
    </summary>
    <param name="attachment">The attachment.</param>
    <returns>
            if it contains the specified attachment, set to <c>true</c>.
            </returns>
        """
        intPtrattachment:c_void_p = attachment.Ptr

        GetDllLibPdf().PdfAttachmentCollection_Contains.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfAttachmentCollection_Contains.restype=c_bool
        ret = GetDllLibPdf().PdfAttachmentCollection_Contains(self.Ptr, intPtrattachment)
        return ret

    def Clear(self):
        """
    <summary>
        Clears the collection.
    </summary>
        """
        GetDllLibPdf().PdfAttachmentCollection_Clear.argtypes=[c_void_p]
        GetDllLibPdf().PdfAttachmentCollection_Clear(self.Ptr)

