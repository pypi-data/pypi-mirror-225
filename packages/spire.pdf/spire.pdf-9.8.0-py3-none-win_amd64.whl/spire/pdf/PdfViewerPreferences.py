from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfViewerPreferences (SpireObject) :
    """
    <summary>
        Defines the way the document is to be presented on the screen or in print.
    </summary>
    """
    @property
    def CenterWindow(self)->bool:
        """
    <summary>
        A flag specifying whether to position the documents window in the center of the screen.
    </summary>
        """
        GetDllLibPdf().PdfViewerPreferences_get_CenterWindow.argtypes=[c_void_p]
        GetDllLibPdf().PdfViewerPreferences_get_CenterWindow.restype=c_bool
        ret = GetDllLibPdf().PdfViewerPreferences_get_CenterWindow(self.Ptr)
        return ret

    @CenterWindow.setter
    def CenterWindow(self, value:bool):
        GetDllLibPdf().PdfViewerPreferences_set_CenterWindow.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfViewerPreferences_set_CenterWindow(self.Ptr, value)

    @property
    def BookMarkExpandOrCollapse(self)->bool:
        return true

    @BookMarkExpandOrCollapse.setter
    def BookMarkExpandOrCollapse(self, value:bool):
        GetDllLibPdf().PdfViewerPreferences_set_BookMarkExpandOrCollapse.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfViewerPreferences_set_BookMarkExpandOrCollapse(self.Ptr, value)

    @property
    def DisplayTitle(self)->bool:
        """
    <summary>
        A flag specifying whether the windows title bar should display the document title taken 
            from the Title entry of the document information dictionary. If false, the title bar 
            should instead display the name of the Pdf file containing the document.
    </summary>
        """
        GetDllLibPdf().PdfViewerPreferences_get_DisplayTitle.argtypes=[c_void_p]
        GetDllLibPdf().PdfViewerPreferences_get_DisplayTitle.restype=c_bool
        ret = GetDllLibPdf().PdfViewerPreferences_get_DisplayTitle(self.Ptr)
        return ret

    @DisplayTitle.setter
    def DisplayTitle(self, value:bool):
        GetDllLibPdf().PdfViewerPreferences_set_DisplayTitle.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfViewerPreferences_set_DisplayTitle(self.Ptr, value)

    @property
    def FitWindow(self)->bool:
        """
    <summary>
        A flag specifying whether to resize the documents window to fit the size of the first 
            displayed page.
    </summary>
        """
        GetDllLibPdf().PdfViewerPreferences_get_FitWindow.argtypes=[c_void_p]
        GetDllLibPdf().PdfViewerPreferences_get_FitWindow.restype=c_bool
        ret = GetDllLibPdf().PdfViewerPreferences_get_FitWindow(self.Ptr)
        return ret

    @FitWindow.setter
    def FitWindow(self, value:bool):
        GetDllLibPdf().PdfViewerPreferences_set_FitWindow.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfViewerPreferences_set_FitWindow(self.Ptr, value)

    @property
    def HideMenubar(self)->bool:
        """
    <summary>
        A flag specifying whether to hide the viewer applications menu bar when the 
            document is active.
    </summary>
        """
        GetDllLibPdf().PdfViewerPreferences_get_HideMenubar.argtypes=[c_void_p]
        GetDllLibPdf().PdfViewerPreferences_get_HideMenubar.restype=c_bool
        ret = GetDllLibPdf().PdfViewerPreferences_get_HideMenubar(self.Ptr)
        return ret

    @HideMenubar.setter
    def HideMenubar(self, value:bool):
        GetDllLibPdf().PdfViewerPreferences_set_HideMenubar.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfViewerPreferences_set_HideMenubar(self.Ptr, value)

    @property
    def HideToolbar(self)->bool:
        """
    <summary>
        A flag specifying whether to hide the viewer applications tool bars when the document is active.
    </summary>
        """
        GetDllLibPdf().PdfViewerPreferences_get_HideToolbar.argtypes=[c_void_p]
        GetDllLibPdf().PdfViewerPreferences_get_HideToolbar.restype=c_bool
        ret = GetDllLibPdf().PdfViewerPreferences_get_HideToolbar(self.Ptr)
        return ret

    @HideToolbar.setter
    def HideToolbar(self, value:bool):
        GetDllLibPdf().PdfViewerPreferences_set_HideToolbar.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfViewerPreferences_set_HideToolbar(self.Ptr, value)

    @property
    def HideWindowUI(self)->bool:
        """
    <summary>
        A flag specifying whether to hide user interface elements in the documents window 
            (such as scroll bars and navigation controls), leaving only the documents contents displayed.
    </summary>
        """
        GetDllLibPdf().PdfViewerPreferences_get_HideWindowUI.argtypes=[c_void_p]
        GetDllLibPdf().PdfViewerPreferences_get_HideWindowUI.restype=c_bool
        ret = GetDllLibPdf().PdfViewerPreferences_get_HideWindowUI(self.Ptr)
        return ret

    @HideWindowUI.setter
    def HideWindowUI(self, value:bool):
        GetDllLibPdf().PdfViewerPreferences_set_HideWindowUI.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfViewerPreferences_set_HideWindowUI(self.Ptr, value)

    @property

    def PageMode(self)->'PdfPageMode':
        """
    <summary>
        A name object specifying how the document should be displayed when opened.
    </summary>
        """
        GetDllLibPdf().PdfViewerPreferences_get_PageMode.argtypes=[c_void_p]
        GetDllLibPdf().PdfViewerPreferences_get_PageMode.restype=c_int
        ret = GetDllLibPdf().PdfViewerPreferences_get_PageMode(self.Ptr)
        objwraped = PdfPageMode(ret)
        return objwraped

    @PageMode.setter
    def PageMode(self, value:'PdfPageMode'):
        GetDllLibPdf().PdfViewerPreferences_set_PageMode.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfViewerPreferences_set_PageMode(self.Ptr, value.value)

    @property

    def PageLayout(self)->'PdfPageLayout':
        """
    <summary>
        A name object specifying the page layout to be used when the document is opened.
    </summary>
        """
        GetDllLibPdf().PdfViewerPreferences_get_PageLayout.argtypes=[c_void_p]
        GetDllLibPdf().PdfViewerPreferences_get_PageLayout.restype=c_int
        ret = GetDllLibPdf().PdfViewerPreferences_get_PageLayout(self.Ptr)
        objwraped = PdfPageLayout(ret)
        return objwraped

    @PageLayout.setter
    def PageLayout(self, value:'PdfPageLayout'):
        GetDllLibPdf().PdfViewerPreferences_set_PageLayout.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfViewerPreferences_set_PageLayout(self.Ptr, value.value)

    @property

    def PrintScaling(self)->'PrintScalingMode':
        """
    <summary>
        Gets or Set the page scaling option to be selected 
            when a print dialog is displayed for this document.
    </summary>
        """
        GetDllLibPdf().PdfViewerPreferences_get_PrintScaling.argtypes=[c_void_p]
        GetDllLibPdf().PdfViewerPreferences_get_PrintScaling.restype=c_int
        ret = GetDllLibPdf().PdfViewerPreferences_get_PrintScaling(self.Ptr)
        objwraped = PrintScalingMode(ret)
        return objwraped

    @PrintScaling.setter
    def PrintScaling(self, value:'PrintScalingMode'):
        GetDllLibPdf().PdfViewerPreferences_set_PrintScaling.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfViewerPreferences_set_PrintScaling(self.Ptr, value.value)

