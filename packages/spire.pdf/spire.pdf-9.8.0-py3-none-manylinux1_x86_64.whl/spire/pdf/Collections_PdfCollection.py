from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Collections_PdfCollection (SpireObject) :
    """
    <summary>
        A collection specifies the viewing and organizational characteristics
            of portable collections.The intent of portable collections is to present,
            sort, and search collections of related document,such as email archives,
            photo collections, and engineering bidsets.
    </summary>
    """
    @property

    def Folders(self)->'PdfFolder':
        """
    <summary>
        (Required if the collection has folders; ExtensionLevel3)
            An indirect reference to the folder dictionary that is the
            single common ancestor of all other folders in a portable
            collection.
    </summary>
        """
        GetDllLibPdf().Collections_PdfCollection_get_Folders.argtypes=[c_void_p]
        GetDllLibPdf().Collections_PdfCollection_get_Folders.restype=c_void_p
        intPtr = GetDllLibPdf().Collections_PdfCollection_get_Folders(self.Ptr)
        ret = None if intPtr==None else PdfFolder(intPtr)
        return ret


    @property

    def AssociatedFiles(self)->List['PdfAttachment']:
        """
    <summary>
        Get the document collection associated files
    </summary>
        """
        GetDllLibPdf().Collections_PdfCollection_get_AssociatedFiles.argtypes=[c_void_p]
        GetDllLibPdf().Collections_PdfCollection_get_AssociatedFiles.restype=IntPtrArray
        intPtrArr = GetDllLibPdf().Collections_PdfCollection_get_AssociatedFiles(self.Ptr)
        ret = None if intPtrArr==None else GetObjVectorFromArray(intPtrArr,PdfAttachment)
        return ret



#    @property
#
#    def FieldNames(self)->'List1':
#        """
#    <summary>
#        Get the document collection associated field names
#    </summary>
#        """
#        GetDllLibPdf().Collections_PdfCollection_get_FieldNames.argtypes=[c_void_p]
#        GetDllLibPdf().Collections_PdfCollection_get_FieldNames.restype=c_void_p
#        intPtr = GetDllLibPdf().Collections_PdfCollection_get_FieldNames(self.Ptr)
#        ret = None if intPtr==None else List1(intPtr)
#        return ret
#


    @dispatch

    def AddFile(self ,filePath:str):
        """
    <summary>
        Add a local file.
    </summary>
    <param name="filePath">The local file path.</param>
        """
        
        GetDllLibPdf().Collections_PdfCollection_AddFile.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().Collections_PdfCollection_AddFile(self.Ptr, filePath)

    @dispatch

    def AddFile(self ,fileName:str,stream:Stream):
        """
    <summary>
        Add a stream.
    </summary>
    <param name="fileName">The file name of the stream.</param>
    <param name="stream">The stream.</param>
        """
        intPtrstream:c_void_p = stream.Ptr

        GetDllLibPdf().Collections_PdfCollection_AddFileFS.argtypes=[c_void_p ,c_wchar_p,c_void_p]
        GetDllLibPdf().Collections_PdfCollection_AddFileFS(self.Ptr, fileName,intPtrstream)


    def AddAttachment(self ,attachment:'PdfAttachment'):
        """
    <summary>
        Add an attachment.
    </summary>
    <param name="attachment">The attachment.</param>
        """
        intPtrattachment:c_void_p = attachment.Ptr

        GetDllLibPdf().Collections_PdfCollection_AddAttachment.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().Collections_PdfCollection_AddAttachment(self.Ptr, intPtrattachment)


    def AddCustomField(self ,fieldName:str,displayText:str,fieldType:'CustomFieldType'):
        """
    <summary>
        Add a custom field.
    </summary>
    <param name="fieldName">Custom field name.</param>
    <param name="displayText">Custom field display name.</param>
    <param name="fieldType">Custom field type.</param>
        """
        enumfieldType:c_int = fieldType.value

        GetDllLibPdf().Collections_PdfCollection_AddCustomField.argtypes=[c_void_p ,c_wchar_p,c_wchar_p,c_int]
        GetDllLibPdf().Collections_PdfCollection_AddCustomField(self.Ptr, fieldName,displayText,enumfieldType)


    def AddFileRelatedField(self ,fieldName:str,displayText:str,fieldType:'FileRelatedFieldType'):
        """
    <summary>
        Add a file related field.
    </summary>
    <param name="fieldName">File related field name.</param>
    <param name="displayText">File related field display name.</param>
    <param name="fieldType">File related field type.</param>
        """
        enumfieldType:c_int = fieldType.value

        GetDllLibPdf().Collections_PdfCollection_AddFileRelatedField.argtypes=[c_void_p ,c_wchar_p,c_wchar_p,c_int]
        GetDllLibPdf().Collections_PdfCollection_AddFileRelatedField(self.Ptr, fieldName,displayText,enumfieldType)


    def Sort(self ,fieldNames:List[str],order:List[bool]):
        """
    <summary>
        Sort embedded files with field names.
    </summary>
    <param name="fieldNames">The names of fields that the PDF viewer application
            uses to sort the items in the collection.</param>
    <param name="order">Specifies whether the items in the collection are sorted
            in ascending order.</param>
        """
        #arrayfieldNames:ArrayTypefieldNames = ""
        countfieldNames = len(fieldNames)
        ArrayTypefieldNames = c_wchar_p * countfieldNames
        arrayfieldNames = ArrayTypefieldNames()
        for i in range(0, countfieldNames):
            arrayfieldNames[i] = fieldNames[i]

        #arrayorder:ArrayTypeorder = ""
        countorder = len(order)
        ArrayTypeorder = c_int * countorder
        arrayorder = ArrayTypeorder()
        for i in range(0, countorder):
            arrayorder[i] = 1 if order[i] else 0

        GetDllLibPdf().Collections_PdfCollection_Sort.argtypes=[c_void_p ,ArrayTypefieldNames,c_int,ArrayTypeorder,c_int]
        GetDllLibPdf().Collections_PdfCollection_Sort(self.Ptr, arrayfieldNames,countfieldNames,arrayorder,countorder)


    def Clear(self):
        """
    <summary>
        Clear all files and folders.
    </summary>
        """
        GetDllLibPdf().Collections_PdfCollection_Clear.argtypes=[c_void_p]
        GetDllLibPdf().Collections_PdfCollection_Clear(self.Ptr)

