from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfPrintSettings (SpireObject) :
    """
    <summary>
        The page print settings.
    </summary>
    """
    @property

    def PrinterName(self)->str:
        """
    <summary>
        Get or set the name of printer which is on printing pdf document.
    </summary>
        """
        GetDllLibPdf().PdfPrintSettings_get_PrinterName.argtypes=[c_void_p]
        GetDllLibPdf().PdfPrintSettings_get_PrinterName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfPrintSettings_get_PrinterName(self.Ptr))
        return ret


    @PrinterName.setter
    def PrinterName(self, value:str):
        GetDllLibPdf().PdfPrintSettings_set_PrinterName.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfPrintSettings_set_PrinterName(self.Ptr, value)

    @property

    def DocumentName(self)->str:
        """
    <summary>
         Get or set the document name to display (for example, in a print status dialog box or printer queue) while printing the document.
    </summary>
        """
        GetDllLibPdf().PdfPrintSettings_get_DocumentName.argtypes=[c_void_p]
        GetDllLibPdf().PdfPrintSettings_get_DocumentName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfPrintSettings_get_DocumentName(self.Ptr))
        return ret


    @DocumentName.setter
    def DocumentName(self, value:str):
        GetDllLibPdf().PdfPrintSettings_set_DocumentName.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfPrintSettings_set_DocumentName(self.Ptr, value)

#    @property
#
#    def PaperSize(self)->'PaperSize':
#        """
#    <summary>
#        Get or set the size of a piece of paper.
#    </summary>
#        """
#        GetDllLibPdf().PdfPrintSettings_get_PaperSize.argtypes=[c_void_p]
#        GetDllLibPdf().PdfPrintSettings_get_PaperSize.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPrintSettings_get_PaperSize(self.Ptr)
#        ret = None if intPtr==None else PaperSize(intPtr)
#        return ret
#


#    @PaperSize.setter
#    def PaperSize(self, value:'PaperSize'):
#        GetDllLibPdf().PdfPrintSettings_set_PaperSize.argtypes=[c_void_p, c_void_p]
#        GetDllLibPdf().PdfPrintSettings_set_PaperSize(self.Ptr, value.Ptr)


    @property

    def Copies(self)->'Int16':
        """
    <summary>
        Get or set the number of copies of the document to print.
    </summary>
        """
        GetDllLibPdf().PdfPrintSettings_get_Copies.argtypes=[c_void_p]
        GetDllLibPdf().PdfPrintSettings_get_Copies.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPrintSettings_get_Copies(self.Ptr)
        ret = None if intPtr==None else Int16(intPtr)
        return ret


    @Copies.setter
    def Copies(self, value:'Int16'):
        GetDllLibPdf().PdfPrintSettings_set_Copies.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfPrintSettings_set_Copies(self.Ptr, value.Ptr)

    @property
    def Color(self)->bool:
        """
    <summary>
        Get or set a value indicating whether the page should be printed in color.
            true if the page should be printed in color; otherwise, false. The default
            is determined by the printer.
    </summary>
        """
        GetDllLibPdf().PdfPrintSettings_get_Color.argtypes=[c_void_p]
        GetDllLibPdf().PdfPrintSettings_get_Color.restype=c_bool
        ret = GetDllLibPdf().PdfPrintSettings_get_Color(self.Ptr)
        return ret

    @Color.setter
    def Color(self, value:bool):
        GetDllLibPdf().PdfPrintSettings_set_Color.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfPrintSettings_set_Color(self.Ptr, value)

    @property
    def Collate(self)->bool:
        """
    <summary>
        Get or set a value indicating whether the printed document is collated.
    </summary>
        """
        GetDllLibPdf().PdfPrintSettings_get_Collate.argtypes=[c_void_p]
        GetDllLibPdf().PdfPrintSettings_get_Collate.restype=c_bool
        ret = GetDllLibPdf().PdfPrintSettings_get_Collate(self.Ptr)
        return ret

    @Collate.setter
    def Collate(self, value:bool):
        GetDllLibPdf().PdfPrintSettings_set_Collate.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfPrintSettings_set_Collate(self.Ptr, value)

    @property
    def Landscape(self)->bool:
        """
    <summary>
        Get or set a value indicating whether the page is printed in landscape or portrait orientation.
            Returns:
            True if the page should be printed in landscape orientation; otherwise, false.
    </summary>
        """
        GetDllLibPdf().PdfPrintSettings_get_Landscape.argtypes=[c_void_p]
        GetDllLibPdf().PdfPrintSettings_get_Landscape.restype=c_bool
        ret = GetDllLibPdf().PdfPrintSettings_get_Landscape(self.Ptr)
        return ret

    @Landscape.setter
    def Landscape(self, value:bool):
        GetDllLibPdf().PdfPrintSettings_set_Landscape.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfPrintSettings_set_Landscape(self.Ptr, value)

#    @property
#
#    def PrintController(self)->'PrintController':
#        """
#    <summary>
#        Get or set the print controller that guides the printing process.
#    </summary>
#        """
#        GetDllLibPdf().PdfPrintSettings_get_PrintController.argtypes=[c_void_p]
#        GetDllLibPdf().PdfPrintSettings_get_PrintController.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPrintSettings_get_PrintController(self.Ptr)
#        ret = None if intPtr==None else PrintController(intPtr)
#        return ret
#


#    @PrintController.setter
#    def PrintController(self, value:'PrintController'):
#        GetDllLibPdf().PdfPrintSettings_set_PrintController.argtypes=[c_void_p, c_void_p]
#        GetDllLibPdf().PdfPrintSettings_set_PrintController(self.Ptr, value.Ptr)


    @property
    def CanDuplex(self)->bool:
        """
    <summary>
        Get a value indicating whether the printer supports double-sided printing.
    </summary>
        """
        GetDllLibPdf().PdfPrintSettings_get_CanDuplex.argtypes=[c_void_p]
        GetDllLibPdf().PdfPrintSettings_get_CanDuplex.restype=c_bool
        ret = GetDllLibPdf().PdfPrintSettings_get_CanDuplex(self.Ptr)
        return ret

#    @property
#
#    def Duplex(self)->'Duplex':
#        """
#    <summary>
#         Get or set the printer setting for double-sided printing.
#    </summary>
#        """
#        GetDllLibPdf().PdfPrintSettings_get_Duplex.argtypes=[c_void_p]
#        GetDllLibPdf().PdfPrintSettings_get_Duplex.restype=c_int
#        ret = GetDllLibPdf().PdfPrintSettings_get_Duplex(self.Ptr)
#        objwraped = Duplex(ret)
#        return objwraped


#    @Duplex.setter
#    def Duplex(self, value:'Duplex'):
#        GetDllLibPdf().PdfPrintSettings_set_Duplex.argtypes=[c_void_p, c_int]
#        GetDllLibPdf().PdfPrintSettings_set_Duplex(self.Ptr, value.value)


    @property

    def PrinterResolutionKind(self)->'PdfPrinterResolutionKind':
        """
    <summary>
         Get or set the printer resolution kind.
    </summary>
        """
        GetDllLibPdf().PdfPrintSettings_get_PrinterResolutionKind.argtypes=[c_void_p]
        GetDllLibPdf().PdfPrintSettings_get_PrinterResolutionKind.restype=c_int
        ret = GetDllLibPdf().PdfPrintSettings_get_PrinterResolutionKind(self.Ptr)
        objwraped = PdfPrinterResolutionKind(ret)
        return objwraped

    @PrinterResolutionKind.setter
    def PrinterResolutionKind(self, value:'PdfPrinterResolutionKind'):
        GetDllLibPdf().PdfPrintSettings_set_PrinterResolutionKind.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfPrintSettings_set_PrinterResolutionKind(self.Ptr, value.value)

    @property
    def PrintFromPage(self)->int:
        """
    <summary>
        Get the pagenumber which you choose as the start page to printing.
    </summary>
        """
        GetDllLibPdf().PdfPrintSettings_get_PrintFromPage.argtypes=[c_void_p]
        GetDllLibPdf().PdfPrintSettings_get_PrintFromPage.restype=c_int
        ret = GetDllLibPdf().PdfPrintSettings_get_PrintFromPage(self.Ptr)
        return ret

    @property
    def PrintToPage(self)->int:
        """
    <summary>
        Get the pagenumber which you choose as the final page to printing.
    </summary>
        """
        GetDllLibPdf().PdfPrintSettings_get_PrintToPage.argtypes=[c_void_p]
        GetDllLibPdf().PdfPrintSettings_get_PrintToPage.restype=c_int
        ret = GetDllLibPdf().PdfPrintSettings_get_PrintToPage(self.Ptr)
        return ret

    @property
    def IsValid(self)->bool:
        """
    <summary>
        Gets a value indicating whether the System.Drawing.Printing.PrinterSettings.PrinterName property designates a valid printer.
    </summary>
        """
        GetDllLibPdf().PdfPrintSettings_get_IsValid.argtypes=[c_void_p]
        GetDllLibPdf().PdfPrintSettings_get_IsValid.restype=c_bool
        ret = GetDllLibPdf().PdfPrintSettings_get_IsValid(self.Ptr)
        return ret

    @property

    def PrintPages(self)->List[int]:
        """
    <summary>
        Get the user has specified print pages.
    </summary>
        """
        GetDllLibPdf().PdfPrintSettings_get_PrintPages.argtypes=[c_void_p]
        GetDllLibPdf().PdfPrintSettings_get_PrintPages.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().PdfPrintSettings_get_PrintPages(self.Ptr)
        ret = GetVectorFromArray(intPtrArray, c_int)
        return ret


    def add_PaperSettings(self ,value:'PdfPaperSettingsEventHandler'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().PdfPrintSettings_add_PaperSettings.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfPrintSettings_add_PaperSettings(self.Ptr, intPtrvalue)


    def remove_PaperSettings(self ,value:'PdfPaperSettingsEventHandler'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().PdfPrintSettings_remove_PaperSettings.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfPrintSettings_remove_PaperSettings(self.Ptr, intPtrvalue)

#
#    def add_BeginPrint(self ,value:'PrintEventHandler'):
#        """
#
#        """
#        intPtrvalue:c_void_p = value.Ptr
#
#        GetDllLibPdf().PdfPrintSettings_add_BeginPrint.argtypes=[c_void_p ,c_void_p]
#        GetDllLibPdf().PdfPrintSettings_add_BeginPrint(self.Ptr, intPtrvalue)


#
#    def remove_BeginPrint(self ,value:'PrintEventHandler'):
#        """
#
#        """
#        intPtrvalue:c_void_p = value.Ptr
#
#        GetDllLibPdf().PdfPrintSettings_remove_BeginPrint.argtypes=[c_void_p ,c_void_p]
#        GetDllLibPdf().PdfPrintSettings_remove_BeginPrint(self.Ptr, intPtrvalue)


#
#    def add_EndPrint(self ,value:'PrintEventHandler'):
#        """
#
#        """
#        intPtrvalue:c_void_p = value.Ptr
#
#        GetDllLibPdf().PdfPrintSettings_add_EndPrint.argtypes=[c_void_p ,c_void_p]
#        GetDllLibPdf().PdfPrintSettings_add_EndPrint(self.Ptr, intPtrvalue)


#
#    def remove_EndPrint(self ,value:'PrintEventHandler'):
#        """
#
#        """
#        intPtrvalue:c_void_p = value.Ptr
#
#        GetDllLibPdf().PdfPrintSettings_remove_EndPrint.argtypes=[c_void_p ,c_void_p]
#        GetDllLibPdf().PdfPrintSettings_remove_EndPrint(self.Ptr, intPtrvalue)


#
#    def add_PrintPage(self ,value:'PrintPageEventHandler'):
#        """
#
#        """
#        intPtrvalue:c_void_p = value.Ptr
#
#        GetDllLibPdf().PdfPrintSettings_add_PrintPage.argtypes=[c_void_p ,c_void_p]
#        GetDllLibPdf().PdfPrintSettings_add_PrintPage(self.Ptr, intPtrvalue)


#
#    def remove_PrintPage(self ,value:'PrintPageEventHandler'):
#        """
#
#        """
#        intPtrvalue:c_void_p = value.Ptr
#
#        GetDllLibPdf().PdfPrintSettings_remove_PrintPage.argtypes=[c_void_p ,c_void_p]
#        GetDllLibPdf().PdfPrintSettings_remove_PrintPage(self.Ptr, intPtrvalue)


#
#    def add_QueryPageSettings(self ,value:'QueryPageSettingsEventHandler'):
#        """
#
#        """
#        intPtrvalue:c_void_p = value.Ptr
#
#        GetDllLibPdf().PdfPrintSettings_add_QueryPageSettings.argtypes=[c_void_p ,c_void_p]
#        GetDllLibPdf().PdfPrintSettings_add_QueryPageSettings(self.Ptr, intPtrvalue)


#
#    def remove_QueryPageSettings(self ,value:'QueryPageSettingsEventHandler'):
#        """
#
#        """
#        intPtrvalue:c_void_p = value.Ptr
#
#        GetDllLibPdf().PdfPrintSettings_remove_QueryPageSettings.argtypes=[c_void_p ,c_void_p]
#        GetDllLibPdf().PdfPrintSettings_remove_QueryPageSettings(self.Ptr, intPtrvalue)



    def SelectPageRange(self ,fromPage:int,toPage:int):
        """
    <summary>
        Set print page range.
    </summary>
    <param name="fromPage">From page.</param>
    <param name="toPage">To page.</param>
        """
        
        GetDllLibPdf().PdfPrintSettings_SelectPageRange.argtypes=[c_void_p ,c_int,c_int]
        GetDllLibPdf().PdfPrintSettings_SelectPageRange(self.Ptr, fromPage,toPage)


    def SelectSomePages(self ,pages:List[int]):
        """
    <summary>
        Set print some pages.
    </summary>
    <param name="pages">Selection pages.</param>
        """
        #arraypages:ArrayTypepages = ""
        countpages = len(pages)
        ArrayTypepages = c_int * countpages
        arraypages = ArrayTypepages()
        for i in range(0, countpages):
            arraypages[i] = pages[i]


        GetDllLibPdf().PdfPrintSettings_SelectSomePages.argtypes=[c_void_p ,ArrayTypepages]
        GetDllLibPdf().PdfPrintSettings_SelectSomePages(self.Ptr, arraypages)

    @dispatch
    def SelectSinglePageLayout(self):
        """
    <summary>
        Select one page to one paper layout.
            Default pageScalingMode = PdfSinglePageScalingMode.FitSize, autoPortraitOrLandscape = true, customScaling = 100f.
    </summary>
        """
        GetDllLibPdf().PdfPrintSettings_SelectSinglePageLayout.argtypes=[c_void_p]
        GetDllLibPdf().PdfPrintSettings_SelectSinglePageLayout(self.Ptr)

    @dispatch

    def SelectSinglePageLayout(self ,pageScalingMode:PdfSinglePageScalingMode):
        """
    <summary>
        Select one page to one paper layout.
    </summary>
    <param name="pageScalingMode">Page scaling mode.</param>
        """
        enumpageScalingMode:c_int = pageScalingMode.value

        GetDllLibPdf().PdfPrintSettings_SelectSinglePageLayoutP.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfPrintSettings_SelectSinglePageLayoutP(self.Ptr, enumpageScalingMode)

    @dispatch

    def SelectSinglePageLayout(self ,pageScalingMode:PdfSinglePageScalingMode,autoPortraitOrLandscape:bool):
        """
    <summary>
        Select one page to one paper layout.
    </summary>
    <param name="pageScalingMode">Page scaling mode.</param>
    <param name="autoPortraitOrLandscape">Indicating whether automatic portrait and landscape.</param>
        """
        enumpageScalingMode:c_int = pageScalingMode.value

        GetDllLibPdf().PdfPrintSettings_SelectSinglePageLayoutPA.argtypes=[c_void_p ,c_int,c_bool]
        GetDllLibPdf().PdfPrintSettings_SelectSinglePageLayoutPA(self.Ptr, enumpageScalingMode,autoPortraitOrLandscape)

    @dispatch

    def SelectSinglePageLayout(self ,pageScalingMode:PdfSinglePageScalingMode,autoPortraitOrLandscape:bool,customScaling:float):
        """
    <summary>
        Select one page to one paper layout.
    </summary>
    <param name="pageScalingMode">Page scaling mode.</param>
    <param name="autoPortraitOrLandscape">Indicating whether automatic portrait and landscape.</param>
    <param name="customScaling">Custom scaling(unit:percent),default value 100f.Valid only if pageScalingMode== PdfSinglePageScalingMode.CustomScale.</param>
        """
        enumpageScalingMode:c_int = pageScalingMode.value

        GetDllLibPdf().PdfPrintSettings_SelectSinglePageLayoutPAC.argtypes=[c_void_p ,c_int,c_bool,c_float]
        GetDllLibPdf().PdfPrintSettings_SelectSinglePageLayoutPAC(self.Ptr, enumpageScalingMode,autoPortraitOrLandscape,customScaling)

    @dispatch
    def SelectMultiPageLayout(self):
        """
    <summary>
        Select muti page to one paper layout.
            Default rows = 2, columns = 2, hasPageBorder = false, pageOrder = PdfMultiPageOrder.Horizontal.
    </summary>
        """
        GetDllLibPdf().PdfPrintSettings_SelectMultiPageLayout.argtypes=[c_void_p]
        GetDllLibPdf().PdfPrintSettings_SelectMultiPageLayout(self.Ptr)

    @dispatch

    def SelectMultiPageLayout(self ,rows:int):
        """
    <summary>
        Select muti page to one paper layout.
    </summary>
    <param name="rows">The number of rows for the paper layout.</param>
        """
        
        GetDllLibPdf().PdfPrintSettings_SelectMultiPageLayoutR.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfPrintSettings_SelectMultiPageLayoutR(self.Ptr, rows)

    @dispatch

    def SelectMultiPageLayout(self ,rows:int,columns:int):
        """
    <summary>
        Select muti page to one paper layout.
    </summary>
    <param name="rows">The number of rows for the paper layout.</param>
    <param name="columns">The number of columns for the paper layout.</param>
        """
        
        GetDllLibPdf().PdfPrintSettings_SelectMultiPageLayoutRC.argtypes=[c_void_p ,c_int,c_int]
        GetDllLibPdf().PdfPrintSettings_SelectMultiPageLayoutRC(self.Ptr, rows,columns)

    @dispatch

    def SelectMultiPageLayout(self ,rows:int,columns:int,hasPageBorder:bool):
        """
    <summary>
        Select muti page to one paper layout.
    </summary>
    <param name="rows">The number of rows for the paper layout.</param>
    <param name="columns">The number of columns for the paper layout.</param>
    <param name="hasPageBorder">A value indicating whether the pages has the page border.</param>
        """
        
        GetDllLibPdf().PdfPrintSettings_SelectMultiPageLayoutRCH.argtypes=[c_void_p ,c_int,c_int,c_bool]
        GetDllLibPdf().PdfPrintSettings_SelectMultiPageLayoutRCH(self.Ptr, rows,columns,hasPageBorder)

    @dispatch

    def SelectMultiPageLayout(self ,rows:int,columns:int,hasPageBorder:bool,pageOrder:PdfMultiPageOrder):
        """
    <summary>
        Select muti page to one paper layout.
    </summary>
    <param name="rows">The number of rows for the paper layout.</param>
    <param name="columns">The number of columns for the paper layout.</param>
    <param name="hasPageBorder">A value indicating whether the pages has the page border.</param>
    <param name="pageOrder">Multiple pages order.</param>
        """
        enumpageOrder:c_int = pageOrder.value

        GetDllLibPdf().PdfPrintSettings_SelectMultiPageLayoutRCHP.argtypes=[c_void_p ,c_int,c_int,c_bool,c_int]
        GetDllLibPdf().PdfPrintSettings_SelectMultiPageLayoutRCHP(self.Ptr, rows,columns,hasPageBorder,enumpageOrder)

    def SelectSplitPageLayout(self):
        """
    <summary>
        Select split page to muti paper layout.
    </summary>
        """
        GetDllLibPdf().PdfPrintSettings_SelectSplitPageLayout.argtypes=[c_void_p]
        GetDllLibPdf().PdfPrintSettings_SelectSplitPageLayout(self.Ptr)

    @dispatch
    def SelectBookletLayout(self):
        """
    <summary>
        Select booklet layout.
    </summary>
        """
        GetDllLibPdf().PdfPrintSettings_SelectBookletLayout.argtypes=[c_void_p]
        GetDllLibPdf().PdfPrintSettings_SelectBookletLayout(self.Ptr)

    @dispatch

    def SelectBookletLayout(self ,bookletSubset:PdfBookletSubsetMode):
        """
    <summary>
        Select booklet layout.
    </summary>
    <param name="bookletSubset">The mode of BookletSubset.</param>
        """
        enumbookletSubset:c_int = bookletSubset.value

        GetDllLibPdf().PdfPrintSettings_SelectBookletLayoutB.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfPrintSettings_SelectBookletLayoutB(self.Ptr, enumbookletSubset)

    @dispatch

    def SelectBookletLayout(self ,bookletBinding:PdfBookletBindingMode):
        """
    <summary>
        Select booklet layout.
    </summary>
    <param name="bookletBinding">The mode of BookletBinding.</param>
        """
        enumbookletBinding:c_int = bookletBinding.value

        GetDllLibPdf().PdfPrintSettings_SelectBookletLayoutB1.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfPrintSettings_SelectBookletLayoutB1(self.Ptr, enumbookletBinding)

    @dispatch

    def SelectBookletLayout(self ,bookletSubset:PdfBookletSubsetMode,bookletBinding:PdfBookletBindingMode):
        """
    <summary>
        Select booklet layout.
    </summary>
    <param name="bookletSubset">The mode of BookletSubset.</param>
    <param name="bookletBinding">The mode of BookletBinding.</param>
        """
        enumbookletSubset:c_int = bookletSubset.value
        enumbookletBinding:c_int = bookletBinding.value

        GetDllLibPdf().PdfPrintSettings_SelectBookletLayoutBB.argtypes=[c_void_p ,c_int,c_int]
        GetDllLibPdf().PdfPrintSettings_SelectBookletLayoutBB(self.Ptr, enumbookletSubset,enumbookletBinding)


    def SetPaperMargins(self ,top:int,bottom:int,left:int,right:int):
        """
    <summary>
        Set paper margins,measured in hundredths of an inch.
    </summary>
    <param name="top">Paper margin top(unit:hundredths of an inch).</param>
    <param name="bottom">Paper margin bottom(unit:hundredths of an inch).</param>
    <param name="left">Paper margin left(unit:hundredths of an inch).</param>
    <param name="right">Paper margin right(unit:hundredths of an inch).</param>
        """
        
        GetDllLibPdf().PdfPrintSettings_SetPaperMargins.argtypes=[c_void_p ,c_int,c_int,c_int,c_int]
        GetDllLibPdf().PdfPrintSettings_SetPaperMargins(self.Ptr, top,bottom,left,right)


    def PrintToFile(self ,fileName:str):
        """
    <summary>
        Set printing to file.
    </summary>
    <param name="fileName">File name.</param>
        """
        
        GetDllLibPdf().PdfPrintSettings_PrintToFile.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfPrintSettings_PrintToFile(self.Ptr, fileName)

    def Dispose(self):
        """
    <summary>
        Releases all resources used.
    </summary>
        """
        GetDllLibPdf().PdfPrintSettings_Dispose.argtypes=[c_void_p]
        GetDllLibPdf().PdfPrintSettings_Dispose(self.Ptr)

