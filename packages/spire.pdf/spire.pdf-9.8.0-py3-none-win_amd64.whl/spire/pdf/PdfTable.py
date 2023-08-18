from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfTable (  PdfLayoutWidget) :
    @dispatch
    def __init__(self):
        GetDllLibPdf().PdfTable_CreatePdfTable.restype = c_void_p
        intPtr = GetDllLibPdf().PdfTable_CreatePdfTable()
        super(PdfTable, self).__init__(intPtr)
    """
    <summary>
        Represents fast table with few features.
    </summary>
    """
    @property

    def Columns(self)->'PdfColumnCollection':
        """
    <summary>
        Gets the columns.
    </summary>
<value>The table column collection</value>
        """
        GetDllLibPdf().PdfTable_get_Columns.argtypes=[c_void_p]
        GetDllLibPdf().PdfTable_get_Columns.restype=c_void_p
        intPtr = GetDllLibPdf().PdfTable_get_Columns(self.Ptr)
        ret = None if intPtr==None else PdfColumnCollection(intPtr)
        return ret


    @property

    def Rows(self)->'PdfRowCollection':
        """
    <summary>
        Gets the rows.
    </summary>
        """
        GetDllLibPdf().PdfTable_get_Rows.argtypes=[c_void_p]
        GetDllLibPdf().PdfTable_get_Rows.restype=c_void_p
        intPtr = GetDllLibPdf().PdfTable_get_Rows(self.Ptr)
        ret = None if intPtr==None else PdfRowCollection(intPtr)
        return ret


    @property

    def DataSource(self)->'SpireObject':
        """
    <summary>
        Gets or sets the data source.
    </summary>
        """
        GetDllLibPdf().PdfTable_get_DataSource.argtypes=[c_void_p]
        GetDllLibPdf().PdfTable_get_DataSource.restype=c_void_p
        intPtr = GetDllLibPdf().PdfTable_get_DataSource(self.Ptr)
        ret = None if intPtr==None else SpireObject(intPtr)
        return ret


    @DataSource.setter
    def DataSource(self, value:List[str]):
        countinputFiles = len(value)
        ArrayTypeinputFiles = c_wchar_p * countinputFiles
        arrayinputFiles = ArrayTypeinputFiles()
        for i in range(0, countinputFiles):
            arrayinputFiles[i] = value[i]

        GetDllLibPdf().PdfTable_set_DataSource.argtypes=[c_void_p, c_wchar_p, c_int]
        GetDllLibPdf().PdfTable_set_DataSource(self.Ptr, arrayinputFiles,countinputFiles)

    def SetDataSource(self, value:List[str]):
        countinputFiles = len(value)
        ArrayTypeinputFiles = c_wchar_p * countinputFiles
        arrayinputFiles = ArrayTypeinputFiles()
        for i in range(0, countinputFiles):
            arrayinputFiles[i] = value[i]

        GetDllLibPdf().PdfTable_set_DataSource.argtypes=[c_void_p, c_wchar_p, c_int]
        GetDllLibPdf().PdfTable_set_DataSource(self.Ptr, arrayinputFiles,countinputFiles)

    @property

    def DataMember(self)->str:
        """
    <summary>
        Gets or sets the data member.
    </summary>
<value>The data member.</value>
        """
        GetDllLibPdf().PdfTable_get_DataMember.argtypes=[c_void_p]
        GetDllLibPdf().PdfTable_get_DataMember.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfTable_get_DataMember(self.Ptr))
        return ret


    @DataMember.setter
    def DataMember(self, value:str):
        GetDllLibPdf().PdfTable_set_DataMember.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfTable_set_DataMember(self.Ptr, value)

    @property

    def DataSourceType(self)->'PdfTableDataSourceType':
        """
    <summary>
        Gets or sets the datasource type of the PdfTable
    </summary>
        """
        GetDllLibPdf().PdfTable_get_DataSourceType.argtypes=[c_void_p]
        GetDllLibPdf().PdfTable_get_DataSourceType.restype=c_int
        ret = GetDllLibPdf().PdfTable_get_DataSourceType(self.Ptr)
        objwraped = PdfTableDataSourceType(ret)
        return objwraped

    @DataSourceType.setter
    def DataSourceType(self, value:'PdfTableDataSourceType'):
        GetDllLibPdf().PdfTable_set_DataSourceType.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfTable_set_DataSourceType(self.Ptr, value.value)

    @property

    def Style(self)->'PdfTableStyle':
        """
    <summary>
        Gets or sets the properties.
    </summary>
        """
        GetDllLibPdf().PdfTable_get_Style.argtypes=[c_void_p]
        GetDllLibPdf().PdfTable_get_Style.restype=c_void_p
        intPtr = GetDllLibPdf().PdfTable_get_Style(self.Ptr)
        ret = None if intPtr==None else PdfTableStyle(intPtr)
        return ret


    @Style.setter
    def Style(self, value:'PdfTableStyle'):
        GetDllLibPdf().PdfTable_set_Style.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfTable_set_Style(self.Ptr, value.Ptr)

    @property
    def IgnoreSorting(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether
            PdfTable should ignore sorting in data table.
    </summary>
        """
        GetDllLibPdf().PdfTable_get_IgnoreSorting.argtypes=[c_void_p]
        GetDllLibPdf().PdfTable_get_IgnoreSorting.restype=c_bool
        ret = GetDllLibPdf().PdfTable_get_IgnoreSorting(self.Ptr)
        return ret

    @IgnoreSorting.setter
    def IgnoreSorting(self, value:bool):
        GetDllLibPdf().PdfTable_set_IgnoreSorting.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfTable_set_IgnoreSorting(self.Ptr, value)

    @property
    def AllowCrossPages(self)->bool:
        """
    <summary>
        Gets a value Indicates whether can cross a page.
    </summary>
        """
        GetDllLibPdf().PdfTable_get_AllowCrossPages.argtypes=[c_void_p]
        GetDllLibPdf().PdfTable_get_AllowCrossPages.restype=c_bool
        ret = GetDllLibPdf().PdfTable_get_AllowCrossPages(self.Ptr)
        return ret

    @AllowCrossPages.setter
    def AllowCrossPages(self, value:bool):
        GetDllLibPdf().PdfTable_set_AllowCrossPages.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfTable_set_AllowCrossPages(self.Ptr, value)


    def add_BeginRowLayout(self ,value:'BeginRowLayoutEventHandler'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().PdfTable_add_BeginRowLayout.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfTable_add_BeginRowLayout(self.Ptr, intPtrvalue)


    def remove_BeginRowLayout(self ,value:'BeginRowLayoutEventHandler'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().PdfTable_remove_BeginRowLayout.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfTable_remove_BeginRowLayout(self.Ptr, intPtrvalue)


    def add_EndRowLayout(self ,value:'EndRowLayoutEventHandler'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().PdfTable_add_EndRowLayout.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfTable_add_EndRowLayout(self.Ptr, intPtrvalue)


    def remove_EndRowLayout(self ,value:'EndRowLayoutEventHandler'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().PdfTable_remove_EndRowLayout.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfTable_remove_EndRowLayout(self.Ptr, intPtrvalue)


    def add_BeginCellLayout(self ,value:'BeginCellLayoutEventHandler'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().PdfTable_add_BeginCellLayout.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfTable_add_BeginCellLayout(self.Ptr, intPtrvalue)


    def remove_BeginCellLayout(self ,value:'BeginCellLayoutEventHandler'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().PdfTable_remove_BeginCellLayout.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfTable_remove_BeginCellLayout(self.Ptr, intPtrvalue)


    def add_EndCellLayout(self ,value:'EndCellLayoutEventHandler'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().PdfTable_add_EndCellLayout.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfTable_add_EndCellLayout(self.Ptr, intPtrvalue)


    def remove_EndCellLayout(self ,value:'EndCellLayoutEventHandler'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().PdfTable_remove_EndCellLayout.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfTable_remove_EndCellLayout(self.Ptr, intPtrvalue)


    def add_QueryNextRow(self ,value:'QueryNextRowEventHandler'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().PdfTable_add_QueryNextRow.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfTable_add_QueryNextRow(self.Ptr, intPtrvalue)


    def remove_QueryNextRow(self ,value:'QueryNextRowEventHandler'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().PdfTable_remove_QueryNextRow.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfTable_remove_QueryNextRow(self.Ptr, intPtrvalue)


    def add_QueryColumnCount(self ,value:'QueryColumnCountEventHandler'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().PdfTable_add_QueryColumnCount.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfTable_add_QueryColumnCount(self.Ptr, intPtrvalue)


    def remove_QueryColumnCount(self ,value:'QueryColumnCountEventHandler'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().PdfTable_remove_QueryColumnCount.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfTable_remove_QueryColumnCount(self.Ptr, intPtrvalue)


    def add_QueryRowCount(self ,value:'QueryRowCountEventHandler'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().PdfTable_add_QueryRowCount.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfTable_add_QueryRowCount(self.Ptr, intPtrvalue)


    def remove_QueryRowCount(self ,value:'QueryRowCountEventHandler'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().PdfTable_remove_QueryRowCount.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfTable_remove_QueryRowCount(self.Ptr, intPtrvalue)

    @dispatch

    def Draw(self ,graphics:'PdfCanvas',location:PointF,width:float):
        """
    <summary>
        Draws an element on the Graphics.
    </summary>
    <param name="graphics">Graphics context where the element should be printed.</param>
    <param name="location">The location of the element.</param>
    <param name="width">The width of the table.</param>
        """
        intPtrgraphics:c_void_p = graphics.Ptr
        intPtrlocation:c_void_p = location.Ptr

        GetDllLibPdf().PdfTable_Draw.argtypes=[c_void_p ,c_void_p,c_void_p,c_float]
        GetDllLibPdf().PdfTable_Draw(self.Ptr, intPtrgraphics,intPtrlocation,width)

    @dispatch

    def Draw(self ,graphics:'PdfCanvas',x:float,y:float,width:float):
        """
    <summary>
        Draws an element on the Graphics.
    </summary>
    <param name="graphics">Graphics context where the element should be printed.</param>
    <param name="x">X co-ordinate of the element.</param>
    <param name="y">Y co-ordinate of the element.</param>
    <param name="width">The width of the table.</param>
        """
        intPtrgraphics:c_void_p = graphics.Ptr

        GetDllLibPdf().PdfTable_DrawGXYW.argtypes=[c_void_p ,c_void_p,c_float,c_float,c_float]
        GetDllLibPdf().PdfTable_DrawGXYW(self.Ptr, intPtrgraphics,x,y,width)

    @dispatch

    def Draw(self ,graphics:'PdfCanvas',bounds:RectangleF):
        """
    <summary>
        Draws an element on the Graphics.
    </summary>
    <param name="graphics">Graphics context where the element should be printed.</param>
    <param name="bounds">The bounds.</param>
        """
        intPtrgraphics:c_void_p = graphics.Ptr
        intPtrbounds:c_void_p = bounds.Ptr

        GetDllLibPdf().PdfTable_DrawGB.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().PdfTable_DrawGB(self.Ptr, intPtrgraphics,intPtrbounds)

    @dispatch

    def Draw(self ,page:'PdfNewPage',location:PointF)->PdfTableLayoutResult:
        """
    <summary>
        Draws the table starting from the specified page.
    </summary>
    <param name="page">The page.</param>
    <param name="location">The location.</param>
    <returns>The results of the lay outing.</returns>
        """
        intPtrpage:c_void_p = page.Ptr
        intPtrlocation:c_void_p = location.Ptr

        GetDllLibPdf().PdfTable_DrawPL.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().PdfTable_DrawPL.restype=c_void_p
        intPtr = GetDllLibPdf().PdfTable_DrawPL(self.Ptr, intPtrpage,intPtrlocation)
        ret = None if intPtr==None else PdfTableLayoutResult(intPtr)
        return ret


    @dispatch

    def Draw(self ,page:'PdfNewPage',location:PointF,format:PdfTableLayoutFormat)->PdfTableLayoutResult:
        """
    <summary>
        Draws the table starting from the specified page.
    </summary>
    <param name="page">The page.</param>
    <param name="location">The location.</param>
    <param name="format">The format.</param>
    <returns>The results of the lay outing.</returns>
        """
        intPtrpage:c_void_p = page.Ptr
        intPtrlocation:c_void_p = location.Ptr
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfTable_DrawPLF.argtypes=[c_void_p ,c_void_p,c_void_p,c_void_p]
        GetDllLibPdf().PdfTable_DrawPLF.restype=c_void_p
        intPtr = GetDllLibPdf().PdfTable_DrawPLF(self.Ptr, intPtrpage,intPtrlocation,intPtrformat)
        ret = None if intPtr==None else PdfTableLayoutResult(intPtr)
        return ret


    @dispatch

    def Draw(self ,page:'PdfNewPage',bounds:RectangleF)->PdfTableLayoutResult:
        """
    <summary>
        Draws the table starting from the specified page.
    </summary>
    <param name="page">The page.</param>
    <param name="bounds">The bounds.</param>
    <returns>The results of the lay outing.</returns>
        """
        intPtrpage:c_void_p = page.Ptr
        intPtrbounds:c_void_p = bounds.Ptr

        GetDllLibPdf().PdfTable_DrawPB.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().PdfTable_DrawPB.restype=c_void_p
        intPtr = GetDllLibPdf().PdfTable_DrawPB(self.Ptr, intPtrpage,intPtrbounds)
        ret = None if intPtr==None else PdfTableLayoutResult(intPtr)
        return ret


    @dispatch

    def Draw(self ,page:'PdfNewPage',bounds:RectangleF,format:PdfTableLayoutFormat)->PdfTableLayoutResult:
        """
    <summary>
        Draws the table starting from the specified page.
    </summary>
    <param name="page">The page.</param>
    <param name="bounds">The bounds.</param>
    <param name="format">The format.</param>
    <returns>The results of the lay outing.</returns>
        """
        intPtrpage:c_void_p = page.Ptr
        intPtrbounds:c_void_p = bounds.Ptr
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfTable_DrawPBF.argtypes=[c_void_p ,c_void_p,c_void_p,c_void_p]
        GetDllLibPdf().PdfTable_DrawPBF.restype=c_void_p
        intPtr = GetDllLibPdf().PdfTable_DrawPBF(self.Ptr, intPtrpage,intPtrbounds,intPtrformat)
        ret = None if intPtr==None else PdfTableLayoutResult(intPtr)
        return ret


    @dispatch

    def Draw(self ,page:'PdfNewPage',x:float,y:float)->PdfTableLayoutResult:
        """
    <summary>
        Draws the table starting from the specified page.
    </summary>
    <param name="page">The page.</param>
    <param name="x">The x coordinate.</param>
    <param name="y">The y coordinate.</param>
    <returns>The results of the lay outing.</returns>
        """
        intPtrpage:c_void_p = page.Ptr

        GetDllLibPdf().PdfTable_DrawPXY.argtypes=[c_void_p ,c_void_p,c_float,c_float]
        GetDllLibPdf().PdfTable_DrawPXY.restype=c_void_p
        intPtr = GetDllLibPdf().PdfTable_DrawPXY(self.Ptr, intPtrpage,x,y)
        ret = None if intPtr==None else PdfTableLayoutResult(intPtr)
        return ret


    @dispatch

    def Draw(self ,page:'PdfNewPage',x:float,y:float,format:PdfTableLayoutFormat)->PdfTableLayoutResult:
        """
    <summary>
        Draws the table starting from the specified page.
    </summary>
    <param name="page">The page.</param>
    <param name="x">The x coordinate.</param>
    <param name="y">The y coordinate.</param>
    <param name="format">The format.</param>
    <returns>The results of the lay outing.</returns>
        """
        intPtrpage:c_void_p = page.Ptr
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfTable_DrawPXYF.argtypes=[c_void_p ,c_void_p,c_float,c_float,c_void_p]
        GetDllLibPdf().PdfTable_DrawPXYF.restype=c_void_p
        intPtr = GetDllLibPdf().PdfTable_DrawPXYF(self.Ptr, intPtrpage,x,y,intPtrformat)
        ret = None if intPtr==None else PdfTableLayoutResult(intPtr)
        return ret


    @dispatch

    def Draw(self ,page:'PdfNewPage',x:float,y:float,width:float)->PdfTableLayoutResult:
        """
    <summary>
        Draws the table starting from the specified page.
    </summary>
    <param name="page">The page.</param>
    <param name="x">The x coordinate.</param>
    <param name="y">The y coordinate.</param>
    <param name="width">The width.</param>
    <returns>The results of the lay outing.</returns>
        """
        intPtrpage:c_void_p = page.Ptr

        GetDllLibPdf().PdfTable_DrawPXYW.argtypes=[c_void_p ,c_void_p,c_float,c_float,c_float]
        GetDllLibPdf().PdfTable_DrawPXYW.restype=c_void_p
        intPtr = GetDllLibPdf().PdfTable_DrawPXYW(self.Ptr, intPtrpage,x,y,width)
        ret = None if intPtr==None else PdfTableLayoutResult(intPtr)
        return ret


    @dispatch

    def Draw(self ,page:'PdfNewPage',x:float,y:float,width:float,format:PdfTableLayoutFormat)->PdfTableLayoutResult:
        """
    <summary>
        Draws the table starting from the specified page.
    </summary>
    <param name="page">The page.</param>
    <param name="x">The x coordinate.</param>
    <param name="y">The y coordinate.</param>
    <param name="width">The width.</param>
    <param name="format">The format.</param>
    <returns>The results of the lay outing.</returns>
        """
        intPtrpage:c_void_p = page.Ptr
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfTable_DrawPXYWF.argtypes=[c_void_p ,c_void_p,c_float,c_float,c_float,c_void_p]
        GetDllLibPdf().PdfTable_DrawPXYWF.restype=c_void_p
        intPtr = GetDllLibPdf().PdfTable_DrawPXYWF(self.Ptr, intPtrpage,x,y,width,intPtrformat)
        ret = None if intPtr==None else PdfTableLayoutResult(intPtr)
        return ret


    @dispatch

    def Draw(self ,graphics:'PdfCanvas',x:float,y:float):
        """
    <summary>
        Draws an element on the Graphics.
    </summary>
    <param name="graphics">Graphics context where the element should be printed.</param>
    <param name="x">X co-ordinate of the element.</param>
    <param name="y">Y co-ordinate of the element.</param>
        """
        intPtrgraphics:c_void_p = graphics.Ptr

        GetDllLibPdf().PdfTable_DrawGXY.argtypes=[c_void_p ,c_void_p,c_float,c_float]
        GetDllLibPdf().PdfTable_DrawGXY(self.Ptr, intPtrgraphics,x,y)

