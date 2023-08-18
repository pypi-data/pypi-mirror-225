from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfPath (  PdfFillElement) :
    @dispatch
    def __init__(self):
        GetDllLibPdf().PdfPath_CreatePdfPath.restype = c_void_p
        intPtr = GetDllLibPdf().PdfPath_CreatePdfPath()
        super(PdfPath, self).__init__(intPtr)

    @dispatch
    def __init__(self, pen:PdfPen):
        ptrPen:c_void_p = pen.Ptr
        GetDllLibPdf().PdfPath_CreatePdfPathP.argtypes=[c_void_p]
        GetDllLibPdf().PdfPath_CreatePdfPathP.restype = c_void_p
        intPtr = GetDllLibPdf().PdfPath_CreatePdfPathP(ptrPen)
        super(PdfPath, self).__init__(intPtr)

    @dispatch
    def __init__(self, brush:PdfBrush):
        ptrBrush:c_void_p = brush.Ptr
        GetDllLibPdf().PdfPath_CreatePdfPathB.argtypes=[c_void_p]
        GetDllLibPdf().PdfPath_CreatePdfPathB.restype = c_void_p
        intPtr = GetDllLibPdf().PdfPath_CreatePdfPathB(ptrBrush)
        super(PdfPath, self).__init__(intPtr)

    @dispatch
    def __init__(self, brush:PdfBrush,fillMode:PdfFillMode ):
        ptrBrush:c_void_p = brush.Ptr
        enumMode:c_int = fillMode.value

        GetDllLibPdf().PdfPath_CreatePdfPathBF.argtypes=[c_void_p,c_int]
        GetDllLibPdf().PdfPath_CreatePdfPathBF.restype = c_void_p
        intPtr = GetDllLibPdf().PdfPath_CreatePdfPathBF(ptrBrush,enumMode)
        super(PdfPath, self).__init__(intPtr)

    @dispatch
    def __init__(self,  pen:PdfPen,brush:PdfBrush,fillMode:PdfFillMode ):
        ptrPen:c_void_p = pen.Ptr
        ptrBrush:c_void_p = brush.Ptr
        enumMode:c_int = fillMode.value

        GetDllLibPdf().PdfPath_CreatePdfPathPBF.argtypes=[c_void_p,c_void_p,c_int]
        GetDllLibPdf().PdfPath_CreatePdfPathPBF.restype = c_void_p
        intPtr = GetDllLibPdf().PdfPath_CreatePdfPathPBF(ptrPen,ptrBrush,enumMode)
        super(PdfPath, self).__init__(intPtr)
    """
    <summary>
        Implements graphics path, which is a sequence of primitive graphics elements.
    </summary>
    """
    @property

    def FillMode(self)->'PdfFillMode':
        """
    <summary>
        Gets or sets the fill mode.
    </summary>
        """
        GetDllLibPdf().PdfPath_get_FillMode.argtypes=[c_void_p]
        GetDllLibPdf().PdfPath_get_FillMode.restype=c_int
        ret = GetDllLibPdf().PdfPath_get_FillMode(self.Ptr)
        objwraped = PdfFillMode(ret)
        return objwraped

    @FillMode.setter
    def FillMode(self, value:'PdfFillMode'):
        GetDllLibPdf().PdfPath_set_FillMode.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfPath_set_FillMode(self.Ptr, value.value)

#    @property
#
#    def PathPoints(self)->List['PointF']:
#        """
#    <summary>
#        Gets the path points.
#    </summary>
#        """
#        GetDllLibPdf().PdfPath_get_PathPoints.argtypes=[c_void_p]
#        GetDllLibPdf().PdfPath_get_PathPoints.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().PdfPath_get_PathPoints(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, PointF)
#        return ret


#    @property
#
#    def PathTypes(self)->List['Byte']:
#        """
#    <summary>
#        Gets the path point types.
#    </summary>
#        """
#        GetDllLibPdf().PdfPath_get_PathTypes.argtypes=[c_void_p]
#        GetDllLibPdf().PdfPath_get_PathTypes.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().PdfPath_get_PathTypes(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, Byte)
#        return ret


    @property
    def PointCount(self)->int:
        """
    <summary>
        Gets the point count.
    </summary>
        """
        GetDllLibPdf().PdfPath_get_PointCount.argtypes=[c_void_p]
        GetDllLibPdf().PdfPath_get_PointCount.restype=c_int
        ret = GetDllLibPdf().PdfPath_get_PointCount(self.Ptr)
        return ret

    @property

    def LastPoint(self)->'PointF':
        """
    <summary>
        Gets the last point.
    </summary>
        """
        GetDllLibPdf().PdfPath_get_LastPoint.argtypes=[c_void_p]
        GetDllLibPdf().PdfPath_get_LastPoint.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPath_get_LastPoint(self.Ptr)
        ret = None if intPtr==None else PointF(intPtr)
        return ret


    @dispatch

    def AddArc(self ,rectangle:RectangleF,startAngle:float,sweepAngle:float):
        """
    <summary>
        Adds an arc.
    </summary>
    <param name="rectangle">The boundaries of the arc.</param>
    <param name="startAngle">The start angle.</param>
    <param name="sweepAngle">The sweep angle.</param>
        """
        intPtrrectangle:c_void_p = rectangle.Ptr

        GetDllLibPdf().PdfPath_AddArc.argtypes=[c_void_p ,c_void_p,c_float,c_float]
        GetDllLibPdf().PdfPath_AddArc(self.Ptr, intPtrrectangle,startAngle,sweepAngle)

    @dispatch

    def AddArc(self ,x:float,y:float,width:float,height:float,startAngle:float,sweepAngle:float):
        """
    <summary>
        Adds an arc.
    </summary>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
    <param name="width">The width.</param>
    <param name="height">The height.</param>
    <param name="startAngle">The start angle.</param>
    <param name="sweepAngle">The sweep angle.</param>
        """
        
        GetDllLibPdf().PdfPath_AddArcXYWHSS.argtypes=[c_void_p ,c_float,c_float,c_float,c_float,c_float,c_float]
        GetDllLibPdf().PdfPath_AddArcXYWHSS(self.Ptr, x,y,width,height,startAngle,sweepAngle)

    @dispatch

    def AddBezier(self ,startPoint:PointF,firstControlPoint:PointF,secondControlPoint:PointF,endPoint:PointF):
        """
    <summary>
        Adds a bezier curve.
    </summary>
    <param name="startPoint">The start point.</param>
    <param name="firstControlPoint">The first control point.</param>
    <param name="secondControlPoint">The second control point.</param>
    <param name="endPoint">The end point.</param>
        """
        intPtrstartPoint:c_void_p = startPoint.Ptr
        intPtrfirstControlPoint:c_void_p = firstControlPoint.Ptr
        intPtrsecondControlPoint:c_void_p = secondControlPoint.Ptr
        intPtrendPoint:c_void_p = endPoint.Ptr

        GetDllLibPdf().PdfPath_AddBezier.argtypes=[c_void_p ,c_void_p,c_void_p,c_void_p,c_void_p]
        GetDllLibPdf().PdfPath_AddBezier(self.Ptr, intPtrstartPoint,intPtrfirstControlPoint,intPtrsecondControlPoint,intPtrendPoint)

    @dispatch

    def AddBezier(self ,startPointX:float,startPointY:float,firstControlPointX:float,firstControlPointY:float,secondControlPointX:float,secondControlPointY:float,endPointX:float,endPointY:float):
        """
    <summary>
        Adds a bezier curve.
    </summary>
    <param name="startPointX">The start point X.</param>
    <param name="startPointY">The start point Y.</param>
    <param name="firstControlPointX">The first control point X.</param>
    <param name="firstControlPointY">The first control point Y.</param>
    <param name="secondControlPointX">The second control point X.</param>
    <param name="secondControlPointY">The second control point Y.</param>
    <param name="endPointX">The end point X.</param>
    <param name="endPointY">The end point Y.</param>
        """
        
        GetDllLibPdf().PdfPath_AddBezierSSFFSSEE.argtypes=[c_void_p ,c_float,c_float,c_float,c_float,c_float,c_float,c_float,c_float]
        GetDllLibPdf().PdfPath_AddBezierSSFFSSEE(self.Ptr, startPointX,startPointY,firstControlPointX,firstControlPointY,secondControlPointX,secondControlPointY,endPointX,endPointY)

    @dispatch

    def AddEllipse(self ,rectangle:RectangleF):
        """
    <summary>
        Adds an ellipse.
    </summary>
    <param name="rectangle">The boundaries of the ellipse.</param>
        """
        intPtrrectangle:c_void_p = rectangle.Ptr

        GetDllLibPdf().PdfPath_AddEllipse.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfPath_AddEllipse(self.Ptr, intPtrrectangle)

    @dispatch

    def AddEllipse(self ,x:float,y:float,width:float,height:float):
        """
    <summary>
        Adds an ellipse.
    </summary>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
    <param name="width">The width.</param>
    <param name="height">The height.</param>
        """
        
        GetDllLibPdf().PdfPath_AddEllipseXYWH.argtypes=[c_void_p ,c_float,c_float,c_float,c_float]
        GetDllLibPdf().PdfPath_AddEllipseXYWH(self.Ptr, x,y,width,height)

    @dispatch

    def AddLine(self ,point1:PointF,point2:PointF):
        """
    <summary>
        Adds a line.
    </summary>
    <param name="point1">The point1.</param>
    <param name="point2">The point2.</param>
        """
        intPtrpoint1:c_void_p = point1.Ptr
        intPtrpoint2:c_void_p = point2.Ptr

        GetDllLibPdf().PdfPath_AddLine.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().PdfPath_AddLine(self.Ptr, intPtrpoint1,intPtrpoint2)

    @dispatch

    def AddLine(self ,x1:float,y1:float,x2:float,y2:float):
        """
    <summary>
        Adds a line.
    </summary>
    <param name="x1">The x1.</param>
    <param name="y1">The y1.</param>
    <param name="x2">The x2.</param>
    <param name="y2">The y2.</param>
        """
        
        GetDllLibPdf().PdfPath_AddLineXYXY.argtypes=[c_void_p ,c_float,c_float,c_float,c_float]
        GetDllLibPdf().PdfPath_AddLineXYXY(self.Ptr, x1,y1,x2,y2)

    @dispatch

    def AddPath(self ,path:'PdfPath'):
        """
    <summary>
        Appends the path specified to this one.
    </summary>
    <param name="path">The path, which should be appended.</param>
        """
        intPtrpath:c_void_p = path.Ptr

        GetDllLibPdf().PdfPath_AddPath.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfPath_AddPath(self.Ptr, intPtrpath)

#    @dispatch
#
#    def AddPath(self ,pathPoints:'PointF[]',pathTypes:'Byte[]'):
#        """
#    <summary>
#        Appends the path specified by the points and their types to this one.
#    </summary>
#    <param name="pathPoints">The points.</param>
#    <param name="pathTypes">The path point types.</param>
#        """
#        #arraypathPoints:ArrayTypepathPoints = ""
#        countpathPoints = len(pathPoints)
#        ArrayTypepathPoints = c_void_p * countpathPoints
#        arraypathPoints = ArrayTypepathPoints()
#        for i in range(0, countpathPoints):
#            arraypathPoints[i] = pathPoints[i].Ptr
#
#        #arraypathTypes:ArrayTypepathTypes = ""
#        countpathTypes = len(pathTypes)
#        ArrayTypepathTypes = c_void_p * countpathTypes
#        arraypathTypes = ArrayTypepathTypes()
#        for i in range(0, countpathTypes):
#            arraypathTypes[i] = pathTypes[i].Ptr
#
#
#        GetDllLibPdf().PdfPath_AddPathPP.argtypes=[c_void_p ,ArrayTypepathPoints,ArrayTypepathTypes]
#        GetDllLibPdf().PdfPath_AddPathPP(self.Ptr, arraypathPoints,arraypathTypes)


    @dispatch

    def AddPie(self ,rectangle:RectangleF,startAngle:float,sweepAngle:float):
        """
    <summary>
        Appends the pie to this path.
    </summary>
    <param name="rectangle">The rectangle.</param>
    <param name="startAngle">The start angle.</param>
    <param name="sweepAngle">The sweep angle.</param>
        """
        intPtrrectangle:c_void_p = rectangle.Ptr

        GetDllLibPdf().PdfPath_AddPie.argtypes=[c_void_p ,c_void_p,c_float,c_float]
        GetDllLibPdf().PdfPath_AddPie(self.Ptr, intPtrrectangle,startAngle,sweepAngle)

    @dispatch

    def AddPie(self ,x:float,y:float,width:float,height:float,startAngle:float,sweepAngle:float):
        """
    <summary>
        Appends the pie to this path.
    </summary>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
    <param name="width">The width.</param>
    <param name="height">The height.</param>
    <param name="startAngle">The start angle.</param>
    <param name="sweepAngle">The sweep angle.</param>
        """
        
        GetDllLibPdf().PdfPath_AddPieXYWHSS.argtypes=[c_void_p ,c_float,c_float,c_float,c_float,c_float,c_float]
        GetDllLibPdf().PdfPath_AddPieXYWHSS(self.Ptr, x,y,width,height,startAngle,sweepAngle)

#
#    def AddPolygon(self ,points:'PointF[]'):
#        """
#    <summary>
#        Append the closed polygon to this path.
#    </summary>
#    <param name="points">The points of the polygon.</param>
#        """
#        #arraypoints:ArrayTypepoints = ""
#        countpoints = len(points)
#        ArrayTypepoints = c_void_p * countpoints
#        arraypoints = ArrayTypepoints()
#        for i in range(0, countpoints):
#            arraypoints[i] = points[i].Ptr
#
#
#        GetDllLibPdf().PdfPath_AddPolygon.argtypes=[c_void_p ,ArrayTypepoints]
#        GetDllLibPdf().PdfPath_AddPolygon(self.Ptr, arraypoints)


    @dispatch

    def AddRectangle(self ,rectangle:RectangleF):
        """
    <summary>
        Appends the rectangle to this path.
    </summary>
    <param name="rectangle">The rectangle.</param>
        """
        intPtrrectangle:c_void_p = rectangle.Ptr

        GetDllLibPdf().PdfPath_AddRectangle.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfPath_AddRectangle(self.Ptr, intPtrrectangle)

    @dispatch

    def AddRectangle(self ,x:float,y:float,width:float,height:float):
        """
    <summary>
        Appends the rectangle to this path.
    </summary>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
    <param name="width">The width.</param>
    <param name="height">The height.</param>
        """
        
        GetDllLibPdf().PdfPath_AddRectangleXYWH.argtypes=[c_void_p ,c_float,c_float,c_float,c_float]
        GetDllLibPdf().PdfPath_AddRectangleXYWH(self.Ptr, x,y,width,height)

    def StartFigure(self):
        """
    <summary>
        Starts a new figure.
    </summary>
<remarks>The next added primitive will start a new figure.</remarks>
        """
        GetDllLibPdf().PdfPath_StartFigure.argtypes=[c_void_p]
        GetDllLibPdf().PdfPath_StartFigure(self.Ptr)

    def CloseFigure(self):
        """
    <summary>
        Closes the last figure.
    </summary>
        """
        GetDllLibPdf().PdfPath_CloseFigure.argtypes=[c_void_p]
        GetDllLibPdf().PdfPath_CloseFigure(self.Ptr)

    def CloseAllFigures(self):
        """
    <summary>
        Closes all non-closed figures.
    </summary>
        """
        GetDllLibPdf().PdfPath_CloseAllFigures.argtypes=[c_void_p]
        GetDllLibPdf().PdfPath_CloseAllFigures(self.Ptr)


    def GetLastPoint(self)->'PointF':
        """
    <summary>
        Gets the last point.
    </summary>
    <returns>The last point.</returns>
        """
        GetDllLibPdf().PdfPath_GetLastPoint.argtypes=[c_void_p]
        GetDllLibPdf().PdfPath_GetLastPoint.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPath_GetLastPoint(self.Ptr)
        ret = None if intPtr==None else PointF(intPtr)
        return ret


