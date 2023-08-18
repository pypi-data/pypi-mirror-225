from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class UOFTranslator (  IUOFTranslator) :
    """
    <summary>
        This is a abstract class base Translator, it provides common functions.
    </summary>
<author>linwei</author>
<modifier>linyaohu</modifier>
    """

    def GetFileGuidName(self ,isOoxToUof:bool,isInput:bool)->str:
        """

        """
        
        GetDllLibPdf().UOFTranslator_GetFileGuidName.argtypes=[c_void_p ,c_bool,c_bool]
        GetDllLibPdf().UOFTranslator_GetFileGuidName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().UOFTranslator_GetFileGuidName(self.Ptr, isOoxToUof,isInput))
        return ret


#    @staticmethod
#
#    def GetXPathDoc(xslname:str,location:str)->'XPathDocument':
#        """
#
#        """
#        
#        GetDllLibPdf().UOFTranslator_GetXPathDoc.argtypes=[ c_wchar_p,c_wchar_p]
#        GetDllLibPdf().UOFTranslator_GetXPathDoc.restype=c_void_p
#        intPtr = GetDllLibPdf().UOFTranslator_GetXPathDoc( xslname,location)
#        ret = None if intPtr==None else XPathDocument(intPtr)
#        return ret
#


#
#    def AddProgressMessageListener(self ,listener:'EventHandler'):
#        """
#
#        """
#        intPtrlistener:c_void_p = listener.Ptr
#
#        GetDllLibPdf().UOFTranslator_AddProgressMessageListener.argtypes=[c_void_p ,c_void_p]
#        GetDllLibPdf().UOFTranslator_AddProgressMessageListener(self.Ptr, intPtrlistener)


#
#    def AddFeedbackMessageListener(self ,listener:'EventHandler'):
#        """
#
#        """
#        intPtrlistener:c_void_p = listener.Ptr
#
#        GetDllLibPdf().UOFTranslator_AddFeedbackMessageListener.argtypes=[c_void_p ,c_void_p]
#        GetDllLibPdf().UOFTranslator_AddFeedbackMessageListener(self.Ptr, intPtrlistener)



    def UofToOox(self ,inputStream:'Stream',outputStream:'Stream'):
        """

        """
        intPtrinputStream:c_void_p = inputStream.Ptr
        intPtroutputStream:c_void_p = outputStream.Ptr

        GetDllLibPdf().UOFTranslator_UofToOox.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().UOFTranslator_UofToOox(self.Ptr, intPtrinputStream,intPtroutputStream)


    def OoxToUof(self ,inputStream:'Stream',outputStream:'Stream'):
        """

        """
        intPtrinputStream:c_void_p = inputStream.Ptr
        intPtroutputStream:c_void_p = outputStream.Ptr

        GetDllLibPdf().UOFTranslator_OoxToUof.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().UOFTranslator_OoxToUof(self.Ptr, intPtrinputStream,intPtroutputStream)

#    @staticmethod
#
#    def GetChartData(chartTypeNode:'XmlNode',nm:'XmlNamespaceManager')->'DataTable':
#        """
#    <summary>
#         get the embeded chart data
#    </summary>
#    <param name="chartTypeNode">chart type node (eg:c:barChart)</param>
#    <param name="nm">name space</param>
#    <returns>chart data</returns>
#        """
#        intPtrchartTypeNode:c_void_p = chartTypeNode.Ptr
#        intPtrnm:c_void_p = nm.Ptr
#
#        GetDllLibPdf().UOFTranslator_GetChartData.argtypes=[ c_void_p,c_void_p]
#        GetDllLibPdf().UOFTranslator_GetChartData.restype=c_void_p
#        intPtr = GetDllLibPdf().UOFTranslator_GetChartData( intPtrchartTypeNode,intPtrnm)
#        ret = None if intPtr==None else DataTable(intPtr)
#        return ret
#


#    @staticmethod
#    @dispatch
#
#    def GetSeriesName(series:'XmlNodeList',nm:'XmlNamespaceManager')->List[str]:
#        """
#    <summary>
#         get the series name
#    </summary>
#    <param name="series">series node</param>
#    <param name="nm">name space</param>
#    <returns>series name</returns>
#        """
#        intPtrseries:c_void_p = series.Ptr
#        intPtrnm:c_void_p = nm.Ptr
#
#        GetDllLibPdf().UOFTranslator_GetSeriesName.argtypes=[ c_void_p,c_void_p]
#        GetDllLibPdf().UOFTranslator_GetSeriesName.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().UOFTranslator_GetSeriesName( intPtrseries,intPtrnm)
#        ret = GetVectorFromArray(intPtrArray, c_wchar_p)
#        return ret


#    @staticmethod
#    @dispatch
#
#    def GetCategoryName(ser:'XmlNode',nm:'XmlNamespaceManager')->List[str]:
#        """
#    <summary>
#         get the category name
#    </summary>
#    <param name="ser">series node</param>
#    <param name="nm">name space</param>
#    <returns>category name</returns>
#        """
#        intPtrser:c_void_p = ser.Ptr
#        intPtrnm:c_void_p = nm.Ptr
#
#        GetDllLibPdf().UOFTranslator_GetCategoryName.argtypes=[ c_void_p,c_void_p]
#        GetDllLibPdf().UOFTranslator_GetCategoryName.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().UOFTranslator_GetCategoryName( intPtrser,intPtrnm)
#        ret = GetVectorFromArray(intPtrArray, c_wchar_p)
#        return ret


    @dispatch

    def GetSeriesName(self ,chartFile:str)->List[str]:
        """
    <summary>
         get the series' name
    </summary>
    <param name="chartFile">chart xml file</param>
    <returns>series' name</returns>
        """
        
        GetDllLibPdf().UOFTranslator_GetSeriesNameC.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().UOFTranslator_GetSeriesNameC.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().UOFTranslator_GetSeriesNameC(self.Ptr, chartFile)
        ret = GetStrVectorFromArray(intPtrArray, c_void_p)
        return ret

    @dispatch

    def GetCategoryName(self ,chartFile:str)->List[str]:
        """
    <summary>
        get the categories name
    </summary>
    <param name="chartFile">chart xml file</param>
    <returns>categories name</returns>
        """
        
        GetDllLibPdf().UOFTranslator_GetCategoryNameC.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().UOFTranslator_GetCategoryNameC.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().UOFTranslator_GetCategoryNameC(self.Ptr, chartFile)
        ret = GetStrVectorFromArray(intPtrArray, c_void_p)
        return ret

#    @staticmethod
#
#    def ChkChartTypeNodes(xdoc:'XmlDocument',nm:'XmlNamespaceManager')->'LinkedList1':
#        """
#    <summary>
#         Check the chart cotains how many chart Types (Combo type)
#    </summary>
#    <param name="xdoc">chart file</param>
#    <param name="nm">name space manager</param>
#    <returns>chart type nodes</returns>
#        """
#        intPtrxdoc:c_void_p = xdoc.Ptr
#        intPtrnm:c_void_p = nm.Ptr
#
#        GetDllLibPdf().UOFTranslator_ChkChartTypeNodes.argtypes=[ c_void_p,c_void_p]
#        GetDllLibPdf().UOFTranslator_ChkChartTypeNodes.restype=c_void_p
#        intPtr = GetDllLibPdf().UOFTranslator_ChkChartTypeNodes( intPtrxdoc,intPtrnm)
#        ret = None if intPtr==None else LinkedList1(intPtr)
#        return ret
#


#    @staticmethod
#
#    def GetTitleText(paragraphNode:'XmlNode',nm:'XmlNamespaceManager')->str:
#        """
#    <summary>
#        get the title's text
#    </summary>
#    <param name="paragraphNode">a:p</param>
#    <param name="nm">name sapce</param>
#    <returns>title</returns>
#        """
#        intPtrparagraphNode:c_void_p = paragraphNode.Ptr
#        intPtrnm:c_void_p = nm.Ptr
#
#        GetDllLibPdf().UOFTranslator_GetTitleText.argtypes=[ c_void_p,c_void_p]
#        GetDllLibPdf().UOFTranslator_GetTitleText.restype=c_void_p
#        ret = PtrToStr(GetDllLibPdf().UOFTranslator_GetTitleText( intPtrparagraphNode,intPtrnm))
#        return ret
#


#    @staticmethod
#
#    def ChkValueShownAsLabel(dLbls:'XmlNode',nm:'XmlNamespaceManager')->bool:
#        """
#
#        """
#        intPtrdLbls:c_void_p = dLbls.Ptr
#        intPtrnm:c_void_p = nm.Ptr
#
#        GetDllLibPdf().UOFTranslator_ChkValueShownAsLabel.argtypes=[ c_void_p,c_void_p]
#        GetDllLibPdf().UOFTranslator_ChkValueShownAsLabel.restype=c_bool
#        ret = GetDllLibPdf().UOFTranslator_ChkValueShownAsLabel( intPtrdLbls,intPtrnm)
#        return ret


    @staticmethod

    def ASSEMBLY_PATH()->str:
        """

        """
        #GetDllLibPdf().UOFTranslator_ASSEMBLY_PATH.argtypes=[]
        GetDllLibPdf().UOFTranslator_ASSEMBLY_PATH.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().UOFTranslator_ASSEMBLY_PATH())
        return ret


