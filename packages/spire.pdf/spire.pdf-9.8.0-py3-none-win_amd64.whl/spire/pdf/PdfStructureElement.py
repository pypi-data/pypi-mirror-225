from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfStructureElement (SpireObject) :
    """
    <summary>
        Represents the pdf structure element.
    </summary>
    """
    @property

    def Title(self)->str:
        """
    <summary>
        The title of the structure element.
    </summary>
        """
        GetDllLibPdf().PdfStructureElement_get_Title.argtypes=[c_void_p]
        GetDllLibPdf().PdfStructureElement_get_Title.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfStructureElement_get_Title(self.Ptr))
        return ret


    @Title.setter
    def Title(self, value:str):
        GetDllLibPdf().PdfStructureElement_set_Title.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfStructureElement_set_Title(self.Ptr, value)

    @property

    def Alt(self)->str:
        """
    <summary>
        An alternate description of the structure element and
            its children in human-readable form, which is useful 
            when extracting the document’s contents in support of 
            accessibility to users with disabilities or for other purposes.
    </summary>
        """
        GetDllLibPdf().PdfStructureElement_get_Alt.argtypes=[c_void_p]
        GetDllLibPdf().PdfStructureElement_get_Alt.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfStructureElement_get_Alt(self.Ptr))
        return ret


    @Alt.setter
    def Alt(self, value:str):
        GetDllLibPdf().PdfStructureElement_set_Alt.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfStructureElement_set_Alt(self.Ptr, value)

    @property

    def ActualText(self)->str:
        """
    <summary>
        Text that is an exact replacement for the structure element 
            and its children. This replacement text (which should apply 
            to as small a piece of content as possible) is useful when 
            extracting the document’s contents in support of accessibility 
            to users with disabilities or for other purposes.
    </summary>
        """
        GetDllLibPdf().PdfStructureElement_get_ActualText.argtypes=[c_void_p]
        GetDllLibPdf().PdfStructureElement_get_ActualText.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfStructureElement_get_ActualText(self.Ptr))
        return ret


    @ActualText.setter
    def ActualText(self, value:str):
        GetDllLibPdf().PdfStructureElement_set_ActualText.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfStructureElement_set_ActualText(self.Ptr, value)

#
#    def GetChildNodes(self)->'List1':
#        """
#    <summary>
#        Get the children of this structure element.
#    </summary>
#    <returns>
#            The children of this structure element.
#            The value of list may be one of the following objects:
#            structure element or marked-content identifier or 
#            marked-content reference, object reference.
#            </returns>
#        """
#        GetDllLibPdf().PdfStructureElement_GetChildNodes.argtypes=[c_void_p]
#        GetDllLibPdf().PdfStructureElement_GetChildNodes.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfStructureElement_GetChildNodes(self.Ptr)
#        ret = None if intPtr==None else List1(intPtr)
#        return ret
#



    def AppendChildElement(self ,structureType:str)->'PdfStructureElement':
        """
    <summary>
        Append structure type element.
    </summary>
    <param name="structureType">The structure type.</param>
    <returns>The pdf structure type element.</returns>
        """
        
        GetDllLibPdf().PdfStructureElement_AppendChildElement.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfStructureElement_AppendChildElement.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStructureElement_AppendChildElement(self.Ptr, structureType)
        ret = None if intPtr==None else PdfStructureElement(intPtr)
        return ret


#    @dispatch
#
#    def GetAttributes(self)->IEnumerable1:
#        """
#    <summary>
#        Get all owner's attributes.
#    </summary>
#    <returns></returns>
#        """
#        GetDllLibPdf().PdfStructureElement_GetAttributes.argtypes=[c_void_p]
#        GetDllLibPdf().PdfStructureElement_GetAttributes.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfStructureElement_GetAttributes(self.Ptr)
#        ret = None if intPtr==None else IEnumerable1(intPtr)
#        return ret
#


    @dispatch

    def GetAttributes(self ,owner:PdfAttributeOwner)->PdfStructureAttributes:
        """
    <summary>
        Get the owner's attributes.
    </summary>
    <param name="owner">The owner.</param>
    <returns>The owner's attributes.</returns>
        """
        intPtrowner:c_void_p = owner.Ptr

        GetDllLibPdf().PdfStructureElement_GetAttributesO.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfStructureElement_GetAttributesO.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStructureElement_GetAttributesO(self.Ptr, intPtrowner)
        ret = None if intPtr==None else PdfStructureAttributes(intPtr)
        return ret



    def AddAttributes(self ,owner:'PdfAttributeOwner')->'PdfStructureAttributes':
        """
    <summary>
        Add the owner's attributes.
    </summary>
    <param name="owner">The owner.</param>
    <returns>The owner's attributes.</returns>
        """
        intPtrowner:c_void_p = owner.Ptr

        GetDllLibPdf().PdfStructureElement_AddAttributes.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfStructureElement_AddAttributes.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStructureElement_AddAttributes(self.Ptr, intPtrowner)
        ret = None if intPtr==None else PdfStructureAttributes(intPtr)
        return ret


    @dispatch

    def BeginMarkedContent(self ,page:PdfPageBase):
        """
    <summary>
        Begin a marked-content sequence of objects within the content stream.
    </summary>
    <param name="page">The pdf page.</param>
        """
        intPtrpage:c_void_p = page.Ptr

        GetDllLibPdf().PdfStructureElement_BeginMarkedContent.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfStructureElement_BeginMarkedContent(self.Ptr, intPtrpage)

    @dispatch

    def BeginMarkedContent(self ,page:PdfPageBase,artifactPropertyList:ArtifactPropertyList):
        """
    <summary>
        Begin a marked-content sequence of objects within the content stream.
    </summary>
    <param name="page">The pdf page.</param>
    <param name="artifactPropertyList">The artifact property list.</param>
        """
        intPtrpage:c_void_p = page.Ptr
        intPtrartifactPropertyList:c_void_p = artifactPropertyList.Ptr

        GetDllLibPdf().PdfStructureElement_BeginMarkedContentPA.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().PdfStructureElement_BeginMarkedContentPA(self.Ptr, intPtrpage,intPtrartifactPropertyList)


    def EndMarkedContent(self ,page:'PdfPageBase'):
        """
    <summary>
        End a marked-content sequence of objects within the content stream.
    </summary>
    <param name="page">The pdf page.</param>
        """
        intPtrpage:c_void_p = page.Ptr

        GetDllLibPdf().PdfStructureElement_EndMarkedContent.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfStructureElement_EndMarkedContent(self.Ptr, intPtrpage)

