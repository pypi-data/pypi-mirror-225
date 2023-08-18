from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

#from spire.pdf.SimpleTextExtractionStrategy import SimpleTextExtractionStrategy 
#from spire.pdf.PdfTextFindCollection import PdfTextFindCollection 

class PdfPageBase (SpireObject) :
    """
    <summary>
        The base class for all pages.
    </summary>
    """
    @dispatch

    def ExtractText(self)->str:
        """
    <summary>
        Extracts text from the Page.
    </summary>
        """
        GetDllLibPdf().PdfPageBase_ExtractText.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageBase_ExtractText.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfPageBase_ExtractText(self.Ptr))
        return ret


    @dispatch

    def ExtractText(self ,strategy:SimpleTextExtractionStrategy)->str:
        """
    <summary>
        Extracts text from the given PDF Page by SimpleTextExtractionStrategy.
    </summary>
    <returns>The Extracted Text.</returns>
        """
        intPtrstrategy:c_void_p = strategy.Ptr

        GetDllLibPdf().PdfPageBase_ExtractTextS.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfPageBase_ExtractTextS.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfPageBase_ExtractTextS(self.Ptr, intPtrstrategy))
        return ret


    @dispatch

    def ExtractText(self ,rectangleF:RectangleF)->str:
        """
    <summary>
        Extracts text in the range of rectangle from the given PDF Page.
            The unit is Point,1/72 inch default.
            the coordinate origin is top left corner of the page.
    </summary>
    <param name="rectangleF">Provide a rangle to extract text.</param>
    <returns>The Extracted Text.</returns>
        """
        intPtrrectangleF:c_void_p = rectangleF.Ptr

        GetDllLibPdf().PdfPageBase_ExtractTextR.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfPageBase_ExtractTextR.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfPageBase_ExtractTextR(self.Ptr, intPtrrectangleF))
        return ret


    @dispatch

    def ExtractText(self ,rectangleF:RectangleF,sim:SimpleTextExtractionStrategy)->str:
        """
    <summary>
        Extracts text in the range of rectangle from the given PDF page by SimpleTextExtractionStrategy.
            the coordinate origin is top left corner of the page.
    </summary>
    <param name="rectangleF">Provide a rangle to extract text.</param>
    <param name="sim">Provide simple text extraction policy</param>
    <returns>The Extracted Text.</returns>
        """
        intPtrrectangleF:c_void_p = rectangleF.Ptr
        intPtrsim:c_void_p = sim.Ptr

        GetDllLibPdf().PdfPageBase_ExtractTextRS.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().PdfPageBase_ExtractTextRS.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfPageBase_ExtractTextRS(self.Ptr, intPtrrectangleF,intPtrsim))
        return ret

    @dispatch
    
    def ExtractText(self ,keepWhiteSpace:bool)->str:
        """
    <summary>
        Extracts text from the given PDF Page.
    </summary>
    <returns>The Extracted Text.</returns>
        """
        
        GetDllLibPdf().PdfPageBase_ExtractTextK.argtypes=[c_void_p ,c_bool]
        GetDllLibPdf().PdfPageBase_ExtractTextK.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfPageBase_ExtractTextK(self.Ptr, keepWhiteSpace))
        return ret


    @dispatch

    def ExtractText(self ,options:PdfTextExtractOptions)->str:
        """
    <summary>
        Extracts text from the given PDF Page.
    </summary>
    <param name="options">textExtractContext</param>
    <returns>The Extracted Text.</returns>
        """
        intPtroptions:c_void_p = options.Ptr

        GetDllLibPdf().PdfPageBase_ExtractTextO.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfPageBase_ExtractTextO.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfPageBase_ExtractTextO(self.Ptr, intPtroptions))
        return ret


    @dispatch

    def ExtractImages(self)->List[Image]:
        """
    <summary>
        Extracts images from the given PDF Page.
            The name of a image in the resources save in the Tag attribute of the iamge.
    </summary>
    <returns>Returns the extracted image as Image[].</returns>
        """
        GetDllLibPdf().PdfPageBase_ExtractImages.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageBase_ExtractImages.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().PdfPageBase_ExtractImages(self.Ptr)
        ret = GetObjVectorFromArray(intPtrArray, Image)
        return ret


    @dispatch

    def ExtractImages(self ,processImage:bool)->List[Image]:
        """
    <summary>
        Extracts images from the given PDF Page. and image is not processed.
            The name of a image in the resources save in the Tag attribute of the image.
    </summary>
    <returns>Returns the extracted image as Image[].</returns>
        """
        
        GetDllLibPdf().PdfPageBase_ExtractImagesP.argtypes=[c_void_p ,c_bool]
        GetDllLibPdf().PdfPageBase_ExtractImagesP.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().PdfPageBase_ExtractImagesP(self.Ptr, processImage)
        ret = GetObjVectorFromArray(intPtrArray, Image)
        return ret


    @dispatch

    def DeleteImage(self ,image:PdfImageInfo):
        """
    <summary>
        Delete an image.
            The value of the image's Tag attribute is the name of the image in the resources.
            If the value of Tag is null,the sample image is an inline image type.
    </summary>
    <param name="image">The image to be delete.</param>
        """
        intPtrimage:c_void_p = image.Ptr

        GetDllLibPdf().PdfPageBase_DeleteImage.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfPageBase_DeleteImage(self.Ptr, intPtrimage)

    @dispatch

    def DeleteImage(self ,image:PdfImageInfo,deleteResource:bool):
        """
    <summary>
        Delete an image.
            The value of the image's Tag attribute is the name of the image in the resources.
            If the value of Tag is null,the sample image is an inline image type.
            Warning : You must make sure that the image resource you are removing is the only
            one referenced,otherwise an error will occur.
    </summary>
    <param name="image">The image to be delete.</param>
    <param name="deleteResource">whether to delete the image resource.</param>
        """
        intPtrimage:c_void_p = image.Ptr

        GetDllLibPdf().PdfPageBase_DeleteImageID.argtypes=[c_void_p ,c_void_p,c_bool]
        GetDllLibPdf().PdfPageBase_DeleteImageID(self.Ptr, intPtrimage,deleteResource)

    @dispatch

    def DeleteImage(self ,imageIndex:int):
        """
    <summary>
         Delete an image by index in a page.
    </summary>
    <param name="imageIndex">The image index.</param>
        """
        
        GetDllLibPdf().PdfPageBase_DeleteImageI.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfPageBase_DeleteImageI(self.Ptr, imageIndex)


    def TryCompressImage(self ,imgIndex:int)->bool:
        """
    <summary>
        Try to compress images(except inline image).
    </summary>
    <param name="index">The image index</param>
    <returns>If success, return true; otherwise false.</returns>
        """
        
        GetDllLibPdf().PdfPageBase_TryCompressImage.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfPageBase_TryCompressImage.restype=c_bool
        ret = GetDllLibPdf().PdfPageBase_TryCompressImage(self.Ptr, imgIndex)
        return ret


    def SetTabOrder(self ,tabOrder:'TabOrder'):
        """
    <summary>
        Set tab order.
    </summary>
    <param name="tabOrder">The order name</param>
        """
        enumtabOrder:c_int = tabOrder.value

        GetDllLibPdf().PdfPageBase_SetTabOrder.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfPageBase_SetTabOrder(self.Ptr, enumtabOrder)

    #@dispatch

    #def LoadFromRTF(self ,rtf:str,width:float,IsSplitLine:bool):
    #    """
    #<summary>
    #    Insert rich text to page
    #</summary>
    #<param name="rtf">rich text</param>
    #<param name="width">width</param>
    #<param name="IsSplitLine">IsSplitLine</param>
    #    """
        
    #    GetDllLibPdf().PdfPageBase_LoadFromRTF.argtypes=[c_void_p ,c_wchar_p,c_float,c_bool]
    #    GetDllLibPdf().PdfPageBase_LoadFromRTF(self.Ptr, rtf,width,IsSplitLine)

    #@dispatch

    #def LoadFromRTF(self ,rtf:str,width:float,IsSplitLine:bool,point:PointF):
    #    """
    #<summary>
    #    Insert rich text to page
    #</summary>
    #<param name="rtf">rich text</param>
    #<param name="width">width</param>
    #<param name="IsSplitLine">IsSplitLine</param>
    #<param name="point">Draw text x,y point</param>
    #    """
    #    intPtrpoint:c_void_p = point.Ptr

    #    GetDllLibPdf().PdfPageBase_LoadFromRTFRWIP.argtypes=[c_void_p ,c_wchar_p,c_float,c_bool,c_void_p]
    #    GetDllLibPdf().PdfPageBase_LoadFromRTFRWIP(self.Ptr, rtf,width,IsSplitLine,intPtrpoint)

    #@dispatch

    #def LoadFromRTF(self ,rtf:str,width:float,height:float,IsSplitLine:bool):
    #    """
    #<summary>
    #    Insert rich text to page
    #</summary>
    #<param name="rtf">rich text</param>
    #<param name="width">width</param>
    #<param name="IsSplitLine">IsSplitLine</param>
    #    """
        
    #    GetDllLibPdf().PdfPageBase_LoadFromRTFRWHI.argtypes=[c_void_p ,c_wchar_p,c_float,c_float,c_bool]
    #    GetDllLibPdf().PdfPageBase_LoadFromRTFRWHI(self.Ptr, rtf,width,height,IsSplitLine)

    #@dispatch

    #def LoadFromRTF(self ,rtf:str,width:float,height:float,IsSplitLine:bool,point:PointF):
    #    """
    #<summary>
    #    Insert rich text to page
    #</summary>
    #<param name="rtf">rich text</param>
    #<param name="width">width</param>
    #<param name="IsSplitLine">IsSplitLine</param>
    #<param name="point">Draw text x,y point</param>
    #    """
    #    intPtrpoint:c_void_p = point.Ptr

    #    GetDllLibPdf().PdfPageBase_LoadFromRTFRWHIP.argtypes=[c_void_p ,c_wchar_p,c_float,c_float,c_bool,c_void_p]
    #    GetDllLibPdf().PdfPageBase_LoadFromRTFRWHIP(self.Ptr, rtf,width,height,IsSplitLine,intPtrpoint)

#
#    def add_BeginSave(self ,value:'EventHandler'):
#        """
#
#        """
#        intPtrvalue:c_void_p = value.Ptr
#
#        GetDllLibPdf().PdfPageBase_add_BeginSave.argtypes=[c_void_p ,c_void_p]
#        GetDllLibPdf().PdfPageBase_add_BeginSave(self.Ptr, intPtrvalue)


#
#    def remove_BeginSave(self ,value:'EventHandler'):
#        """
#
#        """
#        intPtrvalue:c_void_p = value.Ptr
#
#        GetDllLibPdf().PdfPageBase_remove_BeginSave.argtypes=[c_void_p ,c_void_p]
#        GetDllLibPdf().PdfPageBase_remove_BeginSave(self.Ptr, intPtrvalue)


    @property
    def AllowContainAllDocTemplates(self)->bool:
        """

        """
        GetDllLibPdf().PdfPageBase_get_AllowContainAllDocTemplates.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageBase_get_AllowContainAllDocTemplates.restype=c_bool
        ret = GetDllLibPdf().PdfPageBase_get_AllowContainAllDocTemplates(self.Ptr)
        return ret

    @AllowContainAllDocTemplates.setter
    def AllowContainAllDocTemplates(self, value:bool):
        GetDllLibPdf().PdfPageBase_set_AllowContainAllDocTemplates.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfPageBase_set_AllowContainAllDocTemplates(self.Ptr, value)

    @property
    def AllowContainLeftDocTemplates(self)->bool:
        """

        """
        GetDllLibPdf().PdfPageBase_get_AllowContainLeftDocTemplates.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageBase_get_AllowContainLeftDocTemplates.restype=c_bool
        ret = GetDllLibPdf().PdfPageBase_get_AllowContainLeftDocTemplates(self.Ptr)
        return ret

    @AllowContainLeftDocTemplates.setter
    def AllowContainLeftDocTemplates(self, value:bool):
        GetDllLibPdf().PdfPageBase_set_AllowContainLeftDocTemplates.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfPageBase_set_AllowContainLeftDocTemplates(self.Ptr, value)

    @property
    def AllowContainRightDocTemplates(self)->bool:
        """

        """
        GetDllLibPdf().PdfPageBase_get_AllowContainRightDocTemplates.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageBase_get_AllowContainRightDocTemplates.restype=c_bool
        ret = GetDllLibPdf().PdfPageBase_get_AllowContainRightDocTemplates(self.Ptr)
        return ret

    @AllowContainRightDocTemplates.setter
    def AllowContainRightDocTemplates(self, value:bool):
        GetDllLibPdf().PdfPageBase_set_AllowContainRightDocTemplates.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfPageBase_set_AllowContainRightDocTemplates(self.Ptr, value)

    @property
    def AllowContainTopDocTemplates(self)->bool:
        """

        """
        GetDllLibPdf().PdfPageBase_get_AllowContainTopDocTemplates.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageBase_get_AllowContainTopDocTemplates.restype=c_bool
        ret = GetDllLibPdf().PdfPageBase_get_AllowContainTopDocTemplates(self.Ptr)
        return ret

    @AllowContainTopDocTemplates.setter
    def AllowContainTopDocTemplates(self, value:bool):
        GetDllLibPdf().PdfPageBase_set_AllowContainTopDocTemplates.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfPageBase_set_AllowContainTopDocTemplates(self.Ptr, value)

    @property
    def AllowContainBottomDocTemplates(self)->bool:
        """

        """
        GetDllLibPdf().PdfPageBase_get_AllowContainBottomDocTemplates.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageBase_get_AllowContainBottomDocTemplates.restype=c_bool
        ret = GetDllLibPdf().PdfPageBase_get_AllowContainBottomDocTemplates(self.Ptr)
        return ret

    @AllowContainBottomDocTemplates.setter
    def AllowContainBottomDocTemplates(self, value:bool):
        GetDllLibPdf().PdfPageBase_set_AllowContainBottomDocTemplates.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfPageBase_set_AllowContainBottomDocTemplates(self.Ptr, value)

    @property

    def CropBox(self)->'RectangleF':
        """
    <summary>
        Returns the visible region of the page.
    </summary>
        """
        GetDllLibPdf().PdfPageBase_get_CropBox.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageBase_get_CropBox.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageBase_get_CropBox(self.Ptr)
        ret = None if intPtr==None else RectangleF(intPtr)
        return ret


    @property

    def BleedBox(self)->'RectangleF':
        """
    <summary>
        Returns page region after clipping.
    </summary>
        """
        GetDllLibPdf().PdfPageBase_get_BleedBox.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageBase_get_BleedBox.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageBase_get_BleedBox(self.Ptr)
        ret = None if intPtr==None else RectangleF(intPtr)
        return ret


    @property

    def MediaBox(self)->'RectangleF':
        """
    <summary>
        Returns page region mediabox.
    </summary>
        """
        GetDllLibPdf().PdfPageBase_get_MediaBox.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageBase_get_MediaBox.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageBase_get_MediaBox(self.Ptr)
        ret = None if intPtr==None else RectangleF(intPtr)
        return ret


    @property

    def TrimBox(self)->'RectangleF':
        """
    <summary>
        Returns page region after trimming.
    </summary>
        """
        GetDllLibPdf().PdfPageBase_get_TrimBox.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageBase_get_TrimBox.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageBase_get_TrimBox(self.Ptr)
        ret = None if intPtr==None else RectangleF(intPtr)
        return ret


    @property

    def ArtBox(self)->'RectangleF':
        """
    <summary>
        Returns page region containing content.
    </summary>
        """
        GetDllLibPdf().PdfPageBase_get_ArtBox.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageBase_get_ArtBox.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageBase_get_ArtBox(self.Ptr)
        ret = None if intPtr==None else RectangleF(intPtr)
        return ret


    @property
    def AnnotationsWidget(self)->'PdfAnnotationCollection':
        from spire.pdf.PdfAnnotationCollection import PdfAnnotationCollection
        """
    <summary>
        Gets the field collection.
    </summary>
        """
        GetDllLibPdf().PdfPageBase_get_AnnotationsWidget.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageBase_get_AnnotationsWidget.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageBase_get_AnnotationsWidget(self.Ptr)
        ret = None if intPtr==None else PdfAnnotationCollection(intPtr)
        return ret


    @AnnotationsWidget.setter
    def AnnotationsWidget(self, value:'PdfAnnotationCollection'):
        GetDllLibPdf().PdfPageBase_set_AnnotationsWidget.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfPageBase_set_AnnotationsWidget(self.Ptr, value.Ptr)

    @property

    def PagePieceInfo(self)->'PdfPieceInfo':
        """
    <summary>
        Get the page piece info.
    </summary>
        """
        GetDllLibPdf().PdfPageBase_get_PagePieceInfo.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageBase_get_PagePieceInfo.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageBase_get_PagePieceInfo(self.Ptr)
        ret = None if intPtr==None else PdfPieceInfo(intPtr)
        return ret


    @PagePieceInfo.setter
    def PagePieceInfo(self, value:'PdfPieceInfo'):
        GetDllLibPdf().PdfPageBase_set_PagePieceInfo.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfPageBase_set_PagePieceInfo(self.Ptr, value.Ptr)

    @property

    def BackgroundColor(self)->'Color':
        """
    <summary>
        Gets or sets page's background color.
    </summary>
        """
        GetDllLibPdf().PdfPageBase_get_BackgroundColor.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageBase_get_BackgroundColor.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageBase_get_BackgroundColor(self.Ptr)
        ret = None if intPtr==None else Color(intPtr)
        return ret


    @BackgroundColor.setter
    def BackgroundColor(self, value:'Color'):
        GetDllLibPdf().PdfPageBase_set_BackgroundColor.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfPageBase_set_BackgroundColor(self.Ptr, value.Ptr)

    @property
    def BackgroudOpacity(self)->float:
        """

        """
        GetDllLibPdf().PdfPageBase_get_BackgroudOpacity.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageBase_get_BackgroudOpacity.restype=c_float
        ret = GetDllLibPdf().PdfPageBase_get_BackgroudOpacity(self.Ptr)
        return ret

    @BackgroudOpacity.setter
    def BackgroudOpacity(self, value:float):
        GetDllLibPdf().PdfPageBase_set_BackgroudOpacity.argtypes=[c_void_p, c_float]
        GetDllLibPdf().PdfPageBase_set_BackgroudOpacity(self.Ptr, value)

    @property

    def BackgroundRegion(self)->'RectangleF':
        """
    <summary>
        The position and size of the background 
    </summary>
        """
        GetDllLibPdf().PdfPageBase_get_BackgroundRegion.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageBase_get_BackgroundRegion.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageBase_get_BackgroundRegion(self.Ptr)
        ret = None if intPtr==None else RectangleF(intPtr)
        return ret


    @BackgroundRegion.setter
    def BackgroundRegion(self, value:'RectangleF'):
        GetDllLibPdf().PdfPageBase_set_BackgroundRegion.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfPageBase_set_BackgroundRegion(self.Ptr, value.Ptr)

    @property

    def ImagesInfo(self)->List['PdfImageInfo']:
        """
    <summary>
        Gets the information about the extracted image.
    </summary>
        """
        GetDllLibPdf().PdfPageBase_get_ImagesInfo.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageBase_get_ImagesInfo.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().PdfPageBase_get_ImagesInfo(self.Ptr)
        ret = GetObjVectorFromArray(intPtrArray, PdfImageInfo)
        return ret


    @property

    def Canvas(self)->'PdfCanvas':
        """
    <summary>
        Gets the graphics of the .
    </summary>
        """
        GetDllLibPdf().PdfPageBase_get_Canvas.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageBase_get_Canvas.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageBase_get_Canvas(self.Ptr)
        ret = None if intPtr==None else PdfCanvas(intPtr)
        return ret


    @property

    def Section(self)->'PdfSection':
        """
    <summary>
        Gets the parent section of the page.
    </summary>
        """
        GetDllLibPdf().PdfPageBase_get_Section.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageBase_get_Section.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageBase_get_Section(self.Ptr)
        ret = None if intPtr==None else PdfSection(intPtr)
        return ret


    @property

    def Document(self)->'PdfDocumentBase':
        """

        """
        GetDllLibPdf().PdfPageBase_get_Document.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageBase_get_Document.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageBase_get_Document(self.Ptr)
        ret = None if intPtr==None else PdfDocumentBase(intPtr)
        return ret


    @property
    def DefaultLayerIndex(self)->int:
        """
    <summary>
        Gets or sets index of the default layer.
    </summary>
        """
        GetDllLibPdf().PdfPageBase_get_DefaultLayerIndex.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageBase_get_DefaultLayerIndex.restype=c_int
        ret = GetDllLibPdf().PdfPageBase_get_DefaultLayerIndex(self.Ptr)
        return ret

    @DefaultLayerIndex.setter
    def DefaultLayerIndex(self, value:int):
        GetDllLibPdf().PdfPageBase_set_DefaultLayerIndex.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfPageBase_set_DefaultLayerIndex(self.Ptr, value)

    @property

    def Size(self)->'SizeF':
        """
    <summary>
        Gets the size of the page.
    </summary>
        """
        GetDllLibPdf().PdfPageBase_get_Size.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageBase_get_Size.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageBase_get_Size(self.Ptr)
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @property

    def ActualSize(self)->'SizeF':
        """
    <summary>
        Gets the actual size of the page.
    </summary>
        """
        GetDllLibPdf().PdfPageBase_get_ActualSize.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageBase_get_ActualSize.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageBase_get_ActualSize(self.Ptr)
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @property

    def Rotation(self)->'PdfPageRotateAngle':
        """

        """
        GetDllLibPdf().PdfPageBase_get_Rotation.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageBase_get_Rotation.restype=c_int
        ret = GetDllLibPdf().PdfPageBase_get_Rotation(self.Ptr)
        objwraped = PdfPageRotateAngle(ret)
        return objwraped

    @Rotation.setter
    def Rotation(self, value:'PdfPageRotateAngle'):
        GetDllLibPdf().PdfPageBase_set_Rotation.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfPageBase_set_Rotation(self.Ptr, value.value)

    @property

    def BackgroundImage(self)->'Stream':
        """
    <summary>
        Gets or sets page's background image.
    </summary>
        """
        GetDllLibPdf().PdfPageBase_get_BackgroundImage.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageBase_get_BackgroundImage.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageBase_get_BackgroundImage(self.Ptr)
        ret = None if intPtr==None else Stream(intPtr)
        return ret


    @BackgroundImage.setter
    def BackgroundImage(self, value:'Stream'):
        GetDllLibPdf().PdfPageBase_set_BackgroundImage.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfPageBase_set_BackgroundImage(self.Ptr, value.Ptr)

    @property

    def PageLabel(self)->str:
        """
    <summary>
        Get the page label.
    </summary>
        """
        GetDllLibPdf().PdfPageBase_get_PageLabel.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageBase_get_PageLabel.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfPageBase_get_PageLabel(self.Ptr))
        return ret


    def IsBlank(self)->bool:
        """
    <summary>
        Returns page is blank flag for page's content.
    </summary>
        """
        GetDllLibPdf().PdfPageBase_IsBlank.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageBase_IsBlank.restype=c_bool
        ret = GetDllLibPdf().PdfPageBase_IsBlank(self.Ptr)
        return ret


    def GetClientSize(self)->'SizeF':
        """
    <summary>
        Returns a page size reduced by page margins and page template dimensions.
    </summary>
<remarks>It's the actual size of the page where some output can be performed.</remarks>
    <returns>Returns a page size reduced by page margins and page template dimensions.</returns>
        """
        GetDllLibPdf().PdfPageBase_GetClientSize.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageBase_GetClientSize.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageBase_GetClientSize(self.Ptr)
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @dispatch

    def ReplaceImage(self ,imageIndex:int,image:PdfImage):
        """
    <summary>
        Replace the Image at index's Position.
    </summary>
    <param name="imageIndex">The index of original image.</param>
    <param name="image">The new replace image.</param>
        """
        intPtrimage:c_void_p = image.Ptr

        GetDllLibPdf().PdfPageBase_ReplaceImage.argtypes=[c_void_p ,c_int,c_void_p]
        GetDllLibPdf().PdfPageBase_ReplaceImage(self.Ptr, imageIndex,intPtrimage)

    #@dispatch

    #def ReplaceImage(self ,originalImage:Image,image:PdfImage):
    #    """
    #<summary>
    #    Replace the Image through the original image.   
    #</summary>
    #<param name="originalImage">The original image</param>
    #<param name="image">The New Replace image</param>
    #    """
    #    intPtroriginalImage:c_void_p = originalImage.Ptr
    #    intPtrimage:c_void_p = image.Ptr

    #    GetDllLibPdf().PdfPageBase_ReplaceImageOI.argtypes=[c_void_p ,c_void_p,c_void_p]
    #    GetDllLibPdf().PdfPageBase_ReplaceImageOI(self.Ptr, intPtroriginalImage,intPtrimage)


    def CreateTemplate(self)->'PdfTemplate':
        """
    <summary>
        Creates a template from page content and all annotation appearances.
    </summary>
    <returns>The created template.</returns>
        """
        GetDllLibPdf().PdfPageBase_CreateTemplate.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageBase_CreateTemplate.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageBase_CreateTemplate(self.Ptr)
        ret = None if intPtr==None else PdfTemplate(intPtr)
        return ret


    @dispatch

    def FindText(self ,searchPatternText:str,isSearchWholeWord:bool)->PdfTextFindCollection:
        """
    <summary>
        Find text 
    </summary>
    <param name="searchPatternText"> The text intends to search. </param>
    <param name="isSearchWholeWord">
            Indicate the expected result is the whole word or not, which means, if it is true, only the word is exactly the same with the 
            searching word will be found;if it is false, any word including the searching word will be found. For instance,the text is "is this a pen?" 
            and the target is "is", if true, one result will be returned; if false, two results will be returned.
    </param>
    <returns></returns>
        """
        
        GetDllLibPdf().PdfPageBase_FindText.argtypes=[c_void_p ,c_wchar_p,c_bool]
        GetDllLibPdf().PdfPageBase_FindText.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageBase_FindText(self.Ptr, searchPatternText,isSearchWholeWord)
        ret = None if intPtr==None else PdfTextFindCollection(intPtr)
        return ret


    @dispatch

    def FindText(self ,searchPatternText:str)->PdfTextFindCollection:
        """
    <summary>
        Find text
    </summary>
    <param name="searchPatternText">string searchPatternText</param>
    <returns></returns>
        """
        
        GetDllLibPdf().PdfPageBase_FindTextS.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfPageBase_FindTextS.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageBase_FindTextS(self.Ptr, searchPatternText)
        ret = None if intPtr==None else PdfTextFindCollection(intPtr)
        return ret


    @dispatch

    def FindText(self ,searchPatternText:str,isSearchWholeWord:bool,ignoreCase:bool)->PdfTextFindCollection:
        """
    <summary>
        Find text
    </summary>
    <param name="searchPatternText"></param>
    <param name="isSearchWholeWord"></param>
    <param name="ignoreCase"></param>
    <returns></returns>
        """
        
        GetDllLibPdf().PdfPageBase_FindTextSII.argtypes=[c_void_p ,c_wchar_p,c_bool,c_bool]
        GetDllLibPdf().PdfPageBase_FindTextSII.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageBase_FindTextSII(self.Ptr, searchPatternText,isSearchWholeWord,ignoreCase)
        ret = None if intPtr==None else PdfTextFindCollection(intPtr)
        return ret


    @dispatch

    def FindText(self ,searchPatternText:str,parameter:TextFindParameter)->PdfTextFindCollection:
        """

        """
        enumparameter:c_int = parameter.value

        GetDllLibPdf().PdfPageBase_FindTextSP.argtypes=[c_void_p ,c_wchar_p,c_int]
        GetDllLibPdf().PdfPageBase_FindTextSP.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageBase_FindTextSP(self.Ptr, searchPatternText,enumparameter)
        ret = None if intPtr==None else PdfTextFindCollection(intPtr)
        return ret


    @dispatch

    def FindText(self ,searchPatternText:str,parameter:TextFindParameter,options:PdfTextFindOptions)->PdfTextFindCollection:
        """

        """
        enumparameter:c_int = parameter.value
        intPtroptions:c_void_p = options.Ptr

        GetDllLibPdf().PdfPageBase_FindTextSPO.argtypes=[c_void_p ,c_wchar_p,c_int,c_void_p]
        GetDllLibPdf().PdfPageBase_FindTextSPO.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageBase_FindTextSPO(self.Ptr, searchPatternText,enumparameter,intPtroptions)
        ret = None if intPtr==None else PdfTextFindCollection(intPtr)
        return ret


    @dispatch

    def FindText(self ,rectangleF:RectangleF,searchPatternText:str,parameter:TextFindParameter)->PdfTextFindCollection:
        """

        """
        intPtrrectangleF:c_void_p = rectangleF.Ptr
        enumparameter:c_int = parameter.value

        GetDllLibPdf().PdfPageBase_FindTextRSP.argtypes=[c_void_p ,c_void_p,c_wchar_p,c_int]
        GetDllLibPdf().PdfPageBase_FindTextRSP.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageBase_FindTextRSP(self.Ptr, intPtrrectangleF,searchPatternText,enumparameter)
        ret = None if intPtr==None else PdfTextFindCollection(intPtr)
        return ret


    @dispatch

    def FindText(self ,searchPatternText:str,isEmbedTable:bool,parameter:TextFindParameter)->PdfTextFindCollection:
        """

        """
        enumparameter:c_int = parameter.value

        GetDllLibPdf().PdfPageBase_FindTextSIP.argtypes=[c_void_p ,c_wchar_p,c_bool,c_int]
        GetDllLibPdf().PdfPageBase_FindTextSIP.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageBase_FindTextSIP(self.Ptr, searchPatternText,isEmbedTable,enumparameter)
        ret = None if intPtr==None else PdfTextFindCollection(intPtr)
        return ret



    def FindAllText(self)->'PdfTextFindCollection':
        """
    <summary>
        Find all text and position.
    </summary>
    <returns>All text find in the page.</returns>
        """
        GetDllLibPdf().PdfPageBase_FindAllText.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageBase_FindAllText.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageBase_FindAllText(self.Ptr)
        ret = None if intPtr==None else PdfTextFindCollection(intPtr)
        return ret


