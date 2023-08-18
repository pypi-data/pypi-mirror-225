from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Qt_HtmlConverter (SpireObject) :
    """
    <summary>
        Convert HTML to PDF with plugin. 
            <para>For more details, please check https://www.e-iceblue.com/Tutorials/Spire.PDF/Spire.PDF-Program-Guide/Convert-HTML-to-PDF-with-New-Plugin.html </para></summary>
    """
    @staticmethod

    def get_PluginPath()->str:
        """
    <summary>
        Sets the path of the folder which cantains the HTMLConverter.dll
            and other dll files required for conversion.
    </summary>
        """
        #GetDllLibPdf().Qt_HtmlConverter_get_PluginPath.argtypes=[]
        GetDllLibPdf().Qt_HtmlConverter_get_PluginPath.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Qt_HtmlConverter_get_PluginPath())
        return ret


    @staticmethod
    def set_PluginPath( value:str):
        GetDllLibPdf().Qt_HtmlConverter_set_PluginPath.argtypes=[ c_wchar_p]
        GetDllLibPdf().Qt_HtmlConverter_set_PluginPath( value)

    @staticmethod
    @dispatch

    def Convert(url:str,fileName:str):
        """
    <summary>
         Convert an html page to a pdf file. The Qt html engine plugin is required.
             During conversion, JavaScript is enabled, default timeout is 30 seconds.
             The page size of output pdf file is A4 and margin is 90 (left-right) and 72 (top-bottom).
     </summary>
    <param name="url">Url address of the html page.</param>
    <param name="fileName">The output pdf file name.</param>
            [Obsolete("This method may be removed in the future.")]
        
        """
        
        GetDllLibPdf().Qt_HtmlConverter_Convert.argtypes=[ c_wchar_p,c_wchar_p]
        GetDllLibPdf().Qt_HtmlConverter_Convert( url,fileName)

    @staticmethod
    @dispatch

    def Convert(url:str,stream:Stream):
        """
    <summary>
         Convert an html page to a pdf file. The Qt html engine plugin is required.
             During conversion, JavaScript is enabled, default timeout is 30 seconds.
             The page size of output pdf file is A4 and margin is 90 (left-right) and 72 (top-bottom).
     </summary>
    <param name="url">Url address of the html page.</param>
    <param name="stream">The output pdf Stream.</param>
            [Obsolete("This method may be removed in the future.")]
        
        """
        intPtrstream:c_void_p = stream.Ptr

        GetDllLibPdf().Qt_HtmlConverter_ConvertUS.argtypes=[ c_wchar_p,c_void_p]
        GetDllLibPdf().Qt_HtmlConverter_ConvertUS( url,intPtrstream)

    @staticmethod
    @dispatch

    def Convert(url:str,fileName:str,urlHtml:LoadHtmlType):
        """
    <summary>
        Convert an html page to a pdf file. The Qt html engine plugin is required.
            During conversion, JavaScript is enabled, default timeout is 30 seconds.
            The page size of output pdf file is A4 and margin is 90 (left-right) and 72 (top-bottom).
    </summary>
    <param name="url">Url address of the html page.</param>
    <param name="fileName">The output pdf file name.</param>
    <param name="urlHtml">the load htmlcode or url </param>
        """
        enumurlHtml:c_int = urlHtml.value

        GetDllLibPdf().Qt_HtmlConverter_ConvertUFU.argtypes=[ c_wchar_p,c_wchar_p,c_int]
        GetDllLibPdf().Qt_HtmlConverter_ConvertUFU( url,fileName,enumurlHtml)

    @staticmethod
    @dispatch

    def Convert(url:str,stream:Stream,urlHtml:LoadHtmlType):
        """
    <summary>
        Convert an html page to a pdf stream. The Qt html engine plugin is required.
            During conversion, JavaScript is enabled, default timeout is 30 seconds.
            The page size of output pdf file is A4 and margin is 90 (left-right) and 72 (top-bottom).
    </summary>
    <param name="url">Url address of the html page.</param>
    <param name="stream">The output pdf stream.</param>
    <param name="urlHtml">the load htmlcode or url </param>
        """
        intPtrstream:c_void_p = stream.Ptr
        enumurlHtml:c_int = urlHtml.value

        GetDllLibPdf().Qt_HtmlConverter_ConvertUSU.argtypes=[ c_wchar_p,c_void_p,c_int]
        GetDllLibPdf().Qt_HtmlConverter_ConvertUSU( url,intPtrstream,enumurlHtml)

    @staticmethod
    @dispatch

    def Convert(url:str,fileName:str,enableJavaScript:bool,timeout:int,pageSize:SizeF,margins:PdfMargins):
        """
    <summary>
         Convert an html page to a pdf file. The Qt html engine plugin is required.
     </summary>
    <param name="url">Url address of the html page.</param>
    <param name="fileName">The output pdf file name.</param>
    <param name="enableJavaScript">Indicates whether enable JavaScript.</param>
    <param name="timeout">The timeout of loading html.</param>
    <param name="pageSize">The page size of output pdf file.</param>
    <param name="margins">The margins of output pdf file.</param>
            [Obsolete("This method may be removed in the future.")]
        
        """
        intPtrpageSize:c_void_p = pageSize.Ptr
        intPtrmargins:c_void_p = margins.Ptr

        GetDllLibPdf().Qt_HtmlConverter_ConvertUFETPM.argtypes=[ c_wchar_p,c_wchar_p,c_bool,c_int,c_void_p,c_void_p]
        GetDllLibPdf().Qt_HtmlConverter_ConvertUFETPM( url,fileName,enableJavaScript,timeout,intPtrpageSize,intPtrmargins)

    @staticmethod
    @dispatch

    def Convert(url:str,stream:Stream,enableJavaScript:bool,timeout:int,pageSize:SizeF,margins:PdfMargins):
        """
    <summary>
         Convert an html page to a pdf stream. The Qt html engine plugin is required.
     </summary>
    <param name="url">Url address of the html page.</param>
    <param name="stream">The output pdf stream.</param>
    <param name="enableJavaScript">Indicates whether enable JavaScript.</param>
    <param name="timeout">The timeout of loading html.</param>
    <param name="pageSize">The page size of output pdf file.</param>
    <param name="margins">The margins of output pdf file.</param>
            [Obsolete("This method may be removed in the future.")]
        
        """
        intPtrstream:c_void_p = stream.Ptr
        intPtrpageSize:c_void_p = pageSize.Ptr
        intPtrmargins:c_void_p = margins.Ptr

        GetDllLibPdf().Qt_HtmlConverter_ConvertUSETPM.argtypes=[ c_wchar_p,c_void_p,c_bool,c_int,c_void_p,c_void_p]
        GetDllLibPdf().Qt_HtmlConverter_ConvertUSETPM( url,intPtrstream,enableJavaScript,timeout,intPtrpageSize,intPtrmargins)

    @staticmethod
    @dispatch

    def Convert(url:str,fileName:str,enableJavaScript:bool,timeout:int,pageSize:SizeF,margins:PdfMargins,urlHtml:LoadHtmlType):
        """
    <summary>
         Convert an html page to a pdf file. The Qt html engine plugin is required.
    </summary>
    <param name="url">Url address of the html page.</param>
    <param name="fileName">The output pdf file name.</param>
    <param name="enableJavaScript">Indicates whether enable JavaScript.</param>
    <param name="timeout">The timeout of loading html.</param>
    <param name="pageSize">The page size of output pdf file.</param>
    <param name="margins">The margins of output pdf file.</param>
    <param name="urlHtml">url or htmlcontent</param>
        """
        intPtrpageSize:c_void_p = pageSize.Ptr
        intPtrmargins:c_void_p = margins.Ptr
        enumurlHtml:c_int = urlHtml.value

        GetDllLibPdf().Qt_HtmlConverter_ConvertUFETPMU.argtypes=[ c_wchar_p,c_wchar_p,c_bool,c_int,c_void_p,c_void_p,c_int]
        GetDllLibPdf().Qt_HtmlConverter_ConvertUFETPMU( url,fileName,enableJavaScript,timeout,intPtrpageSize,intPtrmargins,enumurlHtml)

    @staticmethod
    @dispatch

    def Convert(url:str,stream:Stream,enableJavaScript:bool,timeout:int,pageSize:SizeF,margins:PdfMargins,urlHtml:LoadHtmlType):
        """
    <summary>
        Convert an html page to a pdf file. The Qt html engine plugin is required.
    </summary>
    <param name="url">Url address of the html page.</param>
    <param name="stream">The output pdf stream.</param>
    <param name="enableJavaScript">Indicates whether enable JavaScript.</param>
    <param name="timeout">The timeout of loading html.</param>
    <param name="pageSize">The page size of output pdf file.</param>
    <param name="margins">The margins of output pdf file.</param>
    <param name="urlHtml">url or htmlcontent</param>
        """
        intPtrstream:c_void_p = stream.Ptr
        intPtrpageSize:c_void_p = pageSize.Ptr
        intPtrmargins:c_void_p = margins.Ptr
        enumurlHtml:c_int = urlHtml.value

        GetDllLibPdf().Qt_HtmlConverter_ConvertUSETPMU.argtypes=[ c_wchar_p,c_void_p,c_bool,c_int,c_void_p,c_void_p,c_int]
        GetDllLibPdf().Qt_HtmlConverter_ConvertUSETPMU( url,intPtrstream,enableJavaScript,timeout,intPtrpageSize,intPtrmargins,enumurlHtml)

