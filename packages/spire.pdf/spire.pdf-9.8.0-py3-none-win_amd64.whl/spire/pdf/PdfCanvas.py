from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfCanvas (SpireObject) :
    """
    <summary>
        The class representing a graphics context of the objects.
            It's used for performing simple graphics operations.
    </summary>
    """
    @dispatch

    def DrawString(self ,s:str,font:PdfFontBase,pen:PdfPen,layoutRectangle:RectangleF,format:PdfStringFormat,htmlTags:bool):
        """
    <summary>
        Draws the specified text string at the specified location and size
            with the specified Pen and Font objects. 
    </summary>
    <param name="s">The text string.</param>
    <param name="font">The font.</param>
    <param name="pen">The pen.</param>
    <param name="layoutRectangle">RectangleF structure that specifies the bounds of the drawn text.</param>
    <param name="format">The text string format.</param>
    <param name="htmlTags">whether the parsing of HTML tags</param>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrpen:c_void_p = pen.Ptr
        intPtrlayoutRectangle:c_void_p = layoutRectangle.Ptr
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfCanvas_DrawString.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_void_p,c_void_p,c_bool]
        GetDllLibPdf().PdfCanvas_DrawString(self.Ptr, s,intPtrfont,intPtrpen,intPtrlayoutRectangle,intPtrformat,htmlTags)

    @dispatch

    def DrawString(self ,s:str,font:PdfFontBase,pen:PdfPen,brush:PdfBrush,layoutRectangle:RectangleF,format:PdfStringFormat,htmlTags:bool):
        """
    <summary>
        Draws the specified text string at the specified location and size
            with the specified Pen, Brush and Font objects. 
    </summary>
    <param name="s">The text string.</param>
    <param name="font">The font.</param>
    <param name="pen">The pen.</param>
    <param name="brush">The brush.</param>
    <param name="layoutRectangle">RectangleF structure that specifies the bounds of the drawn text.</param>
    <param name="format">The text string format.</param>
    <param name="htmlTags">whether the parsing of HTML tags</param>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrpen:c_void_p = pen.Ptr
        intPtrbrush:c_void_p = brush.Ptr
        intPtrlayoutRectangle:c_void_p = layoutRectangle.Ptr
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfCanvas_DrawStringSFPBLFH.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_void_p,c_void_p,c_void_p,c_bool]
        GetDllLibPdf().PdfCanvas_DrawStringSFPBLFH(self.Ptr, s,intPtrfont,intPtrpen,intPtrbrush,intPtrlayoutRectangle,intPtrformat,htmlTags)


    def TranslateTransform(self ,offsetX:float,offsetY:float):
        """
    <summary>
        Translates the coordinates by specified coordinates.
    </summary>
    <param name="offsetX">The X value by which to translate
            coordinate system.</param>
    <param name="offsetY">The Y value by which to translate
            coordinate system.</param>
<property name="flag" value="Finished" />
        """
        
        GetDllLibPdf().PdfCanvas_TranslateTransform.argtypes=[c_void_p ,c_float,c_float]
        GetDllLibPdf().PdfCanvas_TranslateTransform(self.Ptr, offsetX,offsetY)


    def ScaleTransform(self ,scaleX:float,scaleY:float):
        """
    <summary>
        Scales the coordinates by specified coordinates.
    </summary>
    <param name="scaleX">The value by which to scale coordinate
            system in the X axis direction.</param>
    <param name="scaleY">The value by which to scale coordinate
            system in the Y axis direction.</param>
<property name="flag" value="Finished" />
        """
        
        GetDllLibPdf().PdfCanvas_ScaleTransform.argtypes=[c_void_p ,c_float,c_float]
        GetDllLibPdf().PdfCanvas_ScaleTransform(self.Ptr, scaleX,scaleY)

    @dispatch

    def RotateTransform(self ,angle:float,point:PointF):
        """
    <summary>
         Rotates the coordinate system in clockwise direction around specified point.
     </summary>
    <param name="angle">The angle of the rotation (in degrees).</param>
    <param name="angle">A System.Drawing.PointF that represents the center of the rotation. </param>
        """
        intPtrpoint:c_void_p = point.Ptr

        GetDllLibPdf().PdfCanvas_RotateTransform.argtypes=[c_void_p ,c_float,c_void_p]
        GetDllLibPdf().PdfCanvas_RotateTransform(self.Ptr, angle,intPtrpoint)

    @dispatch

    def RotateTransform(self ,angle:float):
        """
    <summary>
        Rotates the coordinate system in clockwise direction.
    </summary>
    <param name="angle">The angle of the rotation (in degrees).</param>
<property name="flag" value="Finished" />
        """
        
        GetDllLibPdf().PdfCanvas_RotateTransformA.argtypes=[c_void_p ,c_float]
        GetDllLibPdf().PdfCanvas_RotateTransformA(self.Ptr, angle)


    def SkewTransform(self ,angleX:float,angleY:float):
        """
    <summary>
        Skews the coordinate system axes.
    </summary>
    <param name="angleX">Skews the X axis by this angle (in
            degrees).</param>
    <param name="angleY">Skews the Y axis by this angle (in
            degrees).</param>
<property name="flag" value="Finished" />
        """
        
        GetDllLibPdf().PdfCanvas_SkewTransform.argtypes=[c_void_p ,c_float,c_float]
        GetDllLibPdf().PdfCanvas_SkewTransform(self.Ptr, angleX,angleY)

    @dispatch

    def DrawTemplate(self ,template:'PdfTemplate',location:PointF):
        """
    <summary>
        Draws a template using its original size, at the specified location.
    </summary>
    <param name="template"> object.</param>
    <param name="location">Location of the template.</param>
        """
        intPtrtemplate:c_void_p = template.Ptr
        intPtrlocation:c_void_p = location.Ptr

        GetDllLibPdf().PdfCanvas_DrawTemplate.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().PdfCanvas_DrawTemplate(self.Ptr, intPtrtemplate,intPtrlocation)

    @dispatch

    def DrawTemplate(self ,template:'PdfTemplate',location:PointF,size:SizeF):
        """
    <summary>
        Draws a template at the specified location and size.
    </summary>
    <param name="template"> object.</param>
    <param name="location">Location of the template.</param>
    <param name="size">Size of the template.</param>
        """
        intPtrtemplate:c_void_p = template.Ptr
        intPtrlocation:c_void_p = location.Ptr
        intPtrsize:c_void_p = size.Ptr

        GetDllLibPdf().PdfCanvas_DrawTemplateTLS.argtypes=[c_void_p ,c_void_p,c_void_p,c_void_p]
        GetDllLibPdf().PdfCanvas_DrawTemplateTLS(self.Ptr, intPtrtemplate,intPtrlocation,intPtrsize)

    def Flush(self):
        """
    <summary>
        Flashes this instance.
    </summary>
        """
        GetDllLibPdf().PdfCanvas_Flush.argtypes=[c_void_p]
        GetDllLibPdf().PdfCanvas_Flush(self.Ptr)


    def Save(self)->'PdfGraphicsState':
        """
    <summary>
        Saves the current state of this Graphics and identifies the saved state with a GraphicsState.
    </summary>
    <returns>This method returns a GraphicsState that represents the saved state of this Graphics. </returns>
<remarks>This method works similar to  method.</remarks>
        """
        GetDllLibPdf().PdfCanvas_Save.argtypes=[c_void_p]
        GetDllLibPdf().PdfCanvas_Save.restype=c_void_p
        intPtr = GetDllLibPdf().PdfCanvas_Save(self.Ptr)
        ret = None if intPtr==None else PdfGraphicsState(intPtr)
        return ret


    @dispatch
    def Restore(self):
        """
    <summary>
        Restores the last state of this Graphics.
    </summary>
        """
        GetDllLibPdf().PdfCanvas_Restore.argtypes=[c_void_p]
        GetDllLibPdf().PdfCanvas_Restore(self.Ptr)

    @dispatch

    def Restore(self ,state:PdfGraphicsState):
        """
    <summary>
        Restores the state of this Graphics to the state represented by a GraphicsState.
    </summary>
    <param name="state">GraphicsState that represents the state to which to restore this Graphics.</param>
<remarks>This method works similar to  method.</remarks>
        """
        intPtrstate:c_void_p = state.Ptr

        GetDllLibPdf().PdfCanvas_RestoreS.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfCanvas_RestoreS(self.Ptr, intPtrstate)

    @dispatch

    def SetClip(self ,rectangle:RectangleF):
        """
    <summary>
        Modifying the current clipping path by intersecting it with the current path.
    </summary>
    <param name="rectangle">Clip rectangle.</param>
        """
        intPtrrectangle:c_void_p = rectangle.Ptr

        GetDllLibPdf().PdfCanvas_SetClip.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfCanvas_SetClip(self.Ptr, intPtrrectangle)

    @dispatch

    def SetClip(self ,rectangle:RectangleF,mode:PdfFillMode):
        """
    <summary>
        Modifying the current clipping path by intersecting it with the current path.
    </summary>
    <param name="rectangle">Clip rectangle.</param>
    <param name="mode">The fill mode to determine which regions lie inside the clipping	path.</param>
        """
        intPtrrectangle:c_void_p = rectangle.Ptr
        enummode:c_int = mode.value

        GetDllLibPdf().PdfCanvas_SetClipRM.argtypes=[c_void_p ,c_void_p,c_int]
        GetDllLibPdf().PdfCanvas_SetClipRM(self.Ptr, intPtrrectangle,enummode)

    @dispatch

    def SetClip(self ,path:'PdfPath'):
        """
    <summary>
        Modifying the current clipping path by intersecting it with the current path.
    </summary>
    <param name="path">Clip path.</param>
        """
        intPtrpath:c_void_p = path.Ptr

        GetDllLibPdf().PdfCanvas_SetClipP.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfCanvas_SetClipP(self.Ptr, intPtrpath)

    @dispatch

    def SetClip(self ,path:'PdfPath',mode:PdfFillMode):
        """
    <summary>
        Modifying the current clipping path by intersecting it with the current path.
    </summary>
    <param name="path">Clip path.</param>
    <param name="mode">The fill mode to determine which regions lie inside the clipping	path.</param>
        """
        intPtrpath:c_void_p = path.Ptr
        enummode:c_int = mode.value

        GetDllLibPdf().PdfCanvas_SetClipPM.argtypes=[c_void_p ,c_void_p,c_int]
        GetDllLibPdf().PdfCanvas_SetClipPM(self.Ptr, intPtrpath,enummode)

    @dispatch

    def SetTransparency(self ,alpha:float):
        """
    <summary>
        Sets the transparency.
    </summary>
    <param name="alpha">The alpha value for both pen
            and brush operations.</param>
        """
        
        GetDllLibPdf().PdfCanvas_SetTransparency.argtypes=[c_void_p ,c_float]
        GetDllLibPdf().PdfCanvas_SetTransparency(self.Ptr, alpha)

    @dispatch

    def SetTransparency(self ,alphaPen:float,alphaBrush:float):
        """
    <summary>
        Sets the transparency.
    </summary>
    <param name="alphaPen">The alpha value for pen operations.</param>
    <param name="alphaBrush">The alpha value for brush operations.</param>
        """
        
        GetDllLibPdf().PdfCanvas_SetTransparencyAA.argtypes=[c_void_p ,c_float,c_float]
        GetDllLibPdf().PdfCanvas_SetTransparencyAA(self.Ptr, alphaPen,alphaBrush)

    @dispatch

    def SetTransparency(self ,alphaPen:float,alphaBrush:float,blendMode:PdfBlendMode):
        """
    <summary>
        Sets the transparency.
    </summary>
    <param name="alphaPen">The alpha value for pen operations.</param>
    <param name="alphaBrush">The alpha value for brush operations.</param>
    <param name="blendMode">The blend mode.</param>
        """
        enumblendMode:c_int = blendMode.value

        GetDllLibPdf().PdfCanvas_SetTransparencyAAB.argtypes=[c_void_p ,c_float,c_float,c_int]
        GetDllLibPdf().PdfCanvas_SetTransparencyAAB(self.Ptr, alphaPen,alphaBrush,enumblendMode)

    @property

    def Size(self)->'SizeF':
        """
    <summary>
        Gets the size of the canvas.
    </summary>
<remarks>Usually, this value is equal to the size of the object this graphics belongs to.</remarks>
        """
        GetDllLibPdf().PdfCanvas_get_Size.argtypes=[c_void_p]
        GetDllLibPdf().PdfCanvas_get_Size.restype=c_void_p
        intPtr = GetDllLibPdf().PdfCanvas_get_Size(self.Ptr)
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @property

    def ClientSize(self)->'SizeF':
        """
    <summary>
        Gets the size of the canvas reduced by margins and page templates.
    </summary>
<remarks>It indicates a size of the canvas reduced by margins and template dimensions.
            This value doesn't change when any custom clip is set.</remarks>
        """
        GetDllLibPdf().PdfCanvas_get_ClientSize.argtypes=[c_void_p]
        GetDllLibPdf().PdfCanvas_get_ClientSize.restype=c_void_p
        intPtr = GetDllLibPdf().PdfCanvas_get_ClientSize(self.Ptr)
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @property

    def ColorSpace(self)->'PdfColorSpace':
        """
    <summary>
        Gets or sets the current color space.
    </summary>
<remarks>The value change of this property has impact on the objects
            which will be drawn after the change.</remarks>
        """
        GetDllLibPdf().PdfCanvas_get_ColorSpace.argtypes=[c_void_p]
        GetDllLibPdf().PdfCanvas_get_ColorSpace.restype=c_int
        ret = GetDllLibPdf().PdfCanvas_get_ColorSpace(self.Ptr)
        objwraped = PdfColorSpace(ret)
        return objwraped

    @ColorSpace.setter
    def ColorSpace(self, value:'PdfColorSpace'):
        GetDllLibPdf().PdfCanvas_set_ColorSpace.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfCanvas_set_ColorSpace(self.Ptr, value.value)

    @dispatch

    def DrawLine(self ,pen:PdfPen,point1:PointF,point2:PointF):
        """
    <summary>
        Draws a line.
    </summary>
    <param name="pen">The pen.</param>
    <param name="point1">The point1.</param>
    <param name="point2">The point2.</param>
        """
        intPtrpen:c_void_p = pen.Ptr
        intPtrpoint1:c_void_p = point1.Ptr
        intPtrpoint2:c_void_p = point2.Ptr

        GetDllLibPdf().PdfCanvas_DrawLine.argtypes=[c_void_p ,c_void_p,c_void_p,c_void_p]
        GetDllLibPdf().PdfCanvas_DrawLine(self.Ptr, intPtrpen,intPtrpoint1,intPtrpoint2)

    @dispatch

    def DrawLine(self ,pen:PdfPen,x1:float,y1:float,x2:float,y2:float):
        """
    <summary>
        Draws a line.
    </summary>
    <param name="pen">The pen.</param>
    <param name="x1">The x1.</param>
    <param name="y1">The y1.</param>
    <param name="x2">The x2.</param>
    <param name="y2">The y2.</param>
        """
        intPtrpen:c_void_p = pen.Ptr

        GetDllLibPdf().PdfCanvas_DrawLinePXYXY.argtypes=[c_void_p ,c_void_p,c_float,c_float,c_float,c_float]
        GetDllLibPdf().PdfCanvas_DrawLinePXYXY(self.Ptr, intPtrpen,x1,y1,x2,y2)

    @dispatch

    def DrawRectangle(self ,pen:PdfPen,rectangle:RectangleF):
        """
    <summary>
        Draws a rectangle.
    </summary>
    <param name="pen">The pen.</param>
    <param name="rectangle">The rectangle.</param>
        """
        intPtrpen:c_void_p = pen.Ptr
        intPtrrectangle:c_void_p = rectangle.Ptr

        GetDllLibPdf().PdfCanvas_DrawRectangle.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().PdfCanvas_DrawRectangle(self.Ptr, intPtrpen,intPtrrectangle)

    @dispatch

    def DrawRectangle(self ,pen:PdfPen,x:float,y:float,width:float,height:float):
        """
    <summary>
        Draws a rectangle.
    </summary>
    <param name="pen">The pen.</param>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
    <param name="width">The width.</param>
    <param name="height">The height.</param>
        """
        intPtrpen:c_void_p = pen.Ptr

        GetDllLibPdf().PdfCanvas_DrawRectanglePXYWH.argtypes=[c_void_p ,c_void_p,c_float,c_float,c_float,c_float]
        GetDllLibPdf().PdfCanvas_DrawRectanglePXYWH(self.Ptr, intPtrpen,x,y,width,height)

    @dispatch

    def DrawRectangle(self ,brush:PdfBrush,rectangle:RectangleF):
        """
    <summary>
        Draws a rectangle.
    </summary>
    <param name="brush">The brush.</param>
    <param name="rectangle">The rectangle.</param>
        """
        intPtrbrush:c_void_p = brush.Ptr
        intPtrrectangle:c_void_p = rectangle.Ptr

        GetDllLibPdf().PdfCanvas_DrawRectangleBR.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().PdfCanvas_DrawRectangleBR(self.Ptr, intPtrbrush,intPtrrectangle)

    @dispatch

    def DrawRectangle(self ,brush:PdfBrush,x:float,y:float,width:float,height:float):
        """
    <summary>
        Draws a rectangle.
    </summary>
    <param name="brush">The brush.</param>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
    <param name="width">The width.</param>
    <param name="height">The height.</param>
        """
        intPtrbrush:c_void_p = brush.Ptr

        GetDllLibPdf().PdfCanvas_DrawRectangleBXYWH.argtypes=[c_void_p ,c_void_p,c_float,c_float,c_float,c_float]
        GetDllLibPdf().PdfCanvas_DrawRectangleBXYWH(self.Ptr, intPtrbrush,x,y,width,height)

    @dispatch

    def DrawRectangle(self ,pen:PdfPen,brush:PdfBrush,rectangle:RectangleF):
        """
    <summary>
        Draws a rectangle.
    </summary>
    <param name="pen">The pen.</param>
    <param name="brush">The brush.</param>
    <param name="rectangle">The rectangle.</param>
        """
        intPtrpen:c_void_p = pen.Ptr
        intPtrbrush:c_void_p = brush.Ptr
        intPtrrectangle:c_void_p = rectangle.Ptr

        GetDllLibPdf().PdfCanvas_DrawRectanglePBR.argtypes=[c_void_p ,c_void_p,c_void_p,c_void_p]
        GetDllLibPdf().PdfCanvas_DrawRectanglePBR(self.Ptr, intPtrpen,intPtrbrush,intPtrrectangle)

    @dispatch

    def DrawRectangle(self ,pen:PdfPen,brush:PdfBrush,x:float,y:float,width:float,height:float):
        """
    <summary>
        Draws a rectangle.
    </summary>
    <param name="pen">The pen.</param>
    <param name="brush">The brush.</param>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
    <param name="width">The width.</param>
    <param name="height">The height.</param>
        """
        intPtrpen:c_void_p = pen.Ptr
        intPtrbrush:c_void_p = brush.Ptr

        GetDllLibPdf().PdfCanvas_DrawRectanglePBXYWH.argtypes=[c_void_p ,c_void_p,c_void_p,c_float,c_float,c_float,c_float]
        GetDllLibPdf().PdfCanvas_DrawRectanglePBXYWH(self.Ptr, intPtrpen,intPtrbrush,x,y,width,height)

    @dispatch

    def DrawEllipse(self ,pen:PdfPen,rectangle:RectangleF):
        """
    <summary>
        Draws an ellipse.
    </summary>
    <param name="pen">The pen.</param>
    <param name="rectangle">The rectangle.</param>
        """
        intPtrpen:c_void_p = pen.Ptr
        intPtrrectangle:c_void_p = rectangle.Ptr

        GetDllLibPdf().PdfCanvas_DrawEllipse.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().PdfCanvas_DrawEllipse(self.Ptr, intPtrpen,intPtrrectangle)

    @dispatch

    def DrawEllipse(self ,pen:PdfPen,x:float,y:float,width:float,height:float):
        """
    <summary>
        Draws an ellipse.
    </summary>
    <param name="pen">The pen.</param>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
    <param name="width">The width.</param>
    <param name="height">The height.</param>
        """
        intPtrpen:c_void_p = pen.Ptr

        GetDllLibPdf().PdfCanvas_DrawEllipsePXYWH.argtypes=[c_void_p ,c_void_p,c_float,c_float,c_float,c_float]
        GetDllLibPdf().PdfCanvas_DrawEllipsePXYWH(self.Ptr, intPtrpen,x,y,width,height)

    @dispatch

    def DrawEllipse(self ,brush:PdfBrush,rectangle:RectangleF):
        """
    <summary>
        Draws an ellipse.
    </summary>
    <param name="brush">The brush.</param>
    <param name="rectangle">The rectangle.</param>
        """
        intPtrbrush:c_void_p = brush.Ptr
        intPtrrectangle:c_void_p = rectangle.Ptr

        GetDllLibPdf().PdfCanvas_DrawEllipseBR.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().PdfCanvas_DrawEllipseBR(self.Ptr, intPtrbrush,intPtrrectangle)

    @dispatch

    def DrawEllipse(self ,brush:PdfBrush,x:float,y:float,width:float,height:float):
        """
    <summary>
        Draws an ellipse.
    </summary>
    <param name="brush">The brush.</param>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
    <param name="width">The width.</param>
    <param name="height">The height.</param>
        """
        intPtrbrush:c_void_p = brush.Ptr

        GetDllLibPdf().PdfCanvas_DrawEllipseBXYWH.argtypes=[c_void_p ,c_void_p,c_float,c_float,c_float,c_float]
        GetDllLibPdf().PdfCanvas_DrawEllipseBXYWH(self.Ptr, intPtrbrush,x,y,width,height)

    @dispatch

    def DrawEllipse(self ,pen:PdfPen,brush:PdfBrush,rectangle:RectangleF):
        """
    <summary>
        Draws an ellipse.
    </summary>
    <param name="pen">The pen.</param>
    <param name="brush">The brush.</param>
    <param name="rectangle">The rectangle.</param>
        """
        intPtrpen:c_void_p = pen.Ptr
        intPtrbrush:c_void_p = brush.Ptr
        intPtrrectangle:c_void_p = rectangle.Ptr

        GetDllLibPdf().PdfCanvas_DrawEllipsePBR.argtypes=[c_void_p ,c_void_p,c_void_p,c_void_p]
        GetDllLibPdf().PdfCanvas_DrawEllipsePBR(self.Ptr, intPtrpen,intPtrbrush,intPtrrectangle)

    @dispatch

    def DrawEllipse(self ,pen:PdfPen,brush:PdfBrush,x:float,y:float,width:float,height:float):
        """
    <summary>
        Draws an ellipse.
    </summary>
    <param name="pen">The pen.</param>
    <param name="brush">The brush.</param>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
    <param name="width">The width.</param>
    <param name="height">The height.</param>
        """
        intPtrpen:c_void_p = pen.Ptr
        intPtrbrush:c_void_p = brush.Ptr

        GetDllLibPdf().PdfCanvas_DrawEllipsePBXYWH.argtypes=[c_void_p ,c_void_p,c_void_p,c_float,c_float,c_float,c_float]
        GetDllLibPdf().PdfCanvas_DrawEllipsePBXYWH(self.Ptr, intPtrpen,intPtrbrush,x,y,width,height)

    @dispatch

    def DrawArc(self ,pen:PdfPen,rectangle:RectangleF,startAngle:float,sweepAngle:float):
        """
    <summary>
        Draws an arc.
    </summary>
    <param name="pen">The pen.</param>
    <param name="rectangle">The rectangle.</param>
    <param name="startAngle">The start angle.</param>
    <param name="sweepAngle">The sweep angle.</param>
        """
        intPtrpen:c_void_p = pen.Ptr
        intPtrrectangle:c_void_p = rectangle.Ptr

        GetDllLibPdf().PdfCanvas_DrawArc.argtypes=[c_void_p ,c_void_p,c_void_p,c_float,c_float]
        GetDllLibPdf().PdfCanvas_DrawArc(self.Ptr, intPtrpen,intPtrrectangle,startAngle,sweepAngle)

    @dispatch

    def DrawArc(self ,pen:PdfPen,x:float,y:float,width:float,height:float,startAngle:float,sweepAngle:float):
        """
    <summary>
        Draws an arc.
    </summary>
    <param name="pen">The pen.</param>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
    <param name="width">The width.</param>
    <param name="height">The height.</param>
    <param name="startAngle">The start angle.</param>
    <param name="sweepAngle">The sweep angle.</param>
        """
        intPtrpen:c_void_p = pen.Ptr

        GetDllLibPdf().PdfCanvas_DrawArcPXYWHSS.argtypes=[c_void_p ,c_void_p,c_float,c_float,c_float,c_float,c_float,c_float]
        GetDllLibPdf().PdfCanvas_DrawArcPXYWHSS(self.Ptr, intPtrpen,x,y,width,height,startAngle,sweepAngle)

    @dispatch

    def DrawPie(self ,pen:PdfPen,rectangle:RectangleF,startAngle:float,sweepAngle:float):
        """
    <summary>
        Draws a pie.
    </summary>
    <param name="pen">The pen.</param>
    <param name="rectangle">The rectangle.</param>
    <param name="startAngle">The start angle.</param>
    <param name="sweepAngle">The sweep angle.</param>
        """
        intPtrpen:c_void_p = pen.Ptr
        intPtrrectangle:c_void_p = rectangle.Ptr

        GetDllLibPdf().PdfCanvas_DrawPie.argtypes=[c_void_p ,c_void_p,c_void_p,c_float,c_float]
        GetDllLibPdf().PdfCanvas_DrawPie(self.Ptr, intPtrpen,intPtrrectangle,startAngle,sweepAngle)

    @dispatch

    def DrawPie(self ,pen:PdfPen,x:float,y:float,width:float,height:float,startAngle:float,sweepAngle:float):
        """
    <summary>
        Draws a pie.
    </summary>
    <param name="pen">The pen.</param>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
    <param name="width">The width.</param>
    <param name="height">The height.</param>
    <param name="startAngle">The start angle.</param>
    <param name="sweepAngle">The sweep angle.</param>
        """
        intPtrpen:c_void_p = pen.Ptr

        GetDllLibPdf().PdfCanvas_DrawPiePXYWHSS.argtypes=[c_void_p ,c_void_p,c_float,c_float,c_float,c_float,c_float,c_float]
        GetDllLibPdf().PdfCanvas_DrawPiePXYWHSS(self.Ptr, intPtrpen,x,y,width,height,startAngle,sweepAngle)

    @dispatch

    def DrawPie(self ,brush:PdfBrush,rectangle:RectangleF,startAngle:float,sweepAngle:float):
        """
    <summary>
        Draws a pie.
    </summary>
    <param name="brush">The brush.</param>
    <param name="rectangle">The rectangle.</param>
    <param name="startAngle">The start angle.</param>
    <param name="sweepAngle">The sweep angle.</param>
        """
        intPtrbrush:c_void_p = brush.Ptr
        intPtrrectangle:c_void_p = rectangle.Ptr

        GetDllLibPdf().PdfCanvas_DrawPieBRSS.argtypes=[c_void_p ,c_void_p,c_void_p,c_float,c_float]
        GetDllLibPdf().PdfCanvas_DrawPieBRSS(self.Ptr, intPtrbrush,intPtrrectangle,startAngle,sweepAngle)

    @dispatch

    def DrawPie(self ,brush:PdfBrush,x:float,y:float,width:float,height:float,startAngle:float,sweepAngle:float):
        """
    <summary>
        Draws a pie.
    </summary>
    <param name="brush">The brush.</param>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
    <param name="width">The width.</param>
    <param name="height">The height.</param>
    <param name="startAngle">The start angle.</param>
    <param name="sweepAngle">The sweep angle.</param>
        """
        intPtrbrush:c_void_p = brush.Ptr

        GetDllLibPdf().PdfCanvas_DrawPieBXYWHSS.argtypes=[c_void_p ,c_void_p,c_float,c_float,c_float,c_float,c_float,c_float]
        GetDllLibPdf().PdfCanvas_DrawPieBXYWHSS(self.Ptr, intPtrbrush,x,y,width,height,startAngle,sweepAngle)

    @dispatch

    def DrawPie(self ,pen:PdfPen,brush:PdfBrush,rectangle:RectangleF,startAngle:float,sweepAngle:float):
        """
    <summary>
        Draws a pie.
    </summary>
    <param name="pen">The pen.</param>
    <param name="brush">The brush.</param>
    <param name="rectangle">The rectangle.</param>
    <param name="startAngle">The start angle.</param>
    <param name="sweepAngle">The sweep angle.</param>
        """
        intPtrpen:c_void_p = pen.Ptr
        intPtrbrush:c_void_p = brush.Ptr
        intPtrrectangle:c_void_p = rectangle.Ptr

        GetDllLibPdf().PdfCanvas_DrawPiePBRSS.argtypes=[c_void_p ,c_void_p,c_void_p,c_void_p,c_float,c_float]
        GetDllLibPdf().PdfCanvas_DrawPiePBRSS(self.Ptr, intPtrpen,intPtrbrush,intPtrrectangle,startAngle,sweepAngle)

    @dispatch

    def DrawPie(self ,pen:PdfPen,brush:PdfBrush,x:float,y:float,width:float,height:float,startAngle:float,sweepAngle:float):
        """
    <summary>
        Draws a pie.
    </summary>
    <param name="pen">The pen.</param>
    <param name="brush">The brush.</param>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
    <param name="width">The width.</param>
    <param name="height">The height.</param>
    <param name="startAngle">The start angle.</param>
    <param name="sweepAngle">The sweep angle.</param>
        """
        intPtrpen:c_void_p = pen.Ptr
        intPtrbrush:c_void_p = brush.Ptr

        GetDllLibPdf().PdfCanvas_DrawPiePBXYWHSS.argtypes=[c_void_p ,c_void_p,c_void_p,c_float,c_float,c_float,c_float,c_float,c_float]
        GetDllLibPdf().PdfCanvas_DrawPiePBXYWHSS(self.Ptr, intPtrpen,intPtrbrush,x,y,width,height,startAngle,sweepAngle)

#    @dispatch
#
#    def DrawPolygon(self ,pen:PdfPen,points:'PointF[]'):
#        """
#    <summary>
#        Draws a polygon.
#    </summary>
#    <param name="pen">The pen.</param>
#    <param name="points">The points.</param>
#        """
#        intPtrpen:c_void_p = pen.Ptr
#        #arraypoints:ArrayTypepoints = ""
#        countpoints = len(points)
#        ArrayTypepoints = c_void_p * countpoints
#        arraypoints = ArrayTypepoints()
#        for i in range(0, countpoints):
#            arraypoints[i] = points[i].Ptr
#
#
#        GetDllLibPdf().PdfCanvas_DrawPolygon.argtypes=[c_void_p ,c_void_p,ArrayTypepoints]
#        GetDllLibPdf().PdfCanvas_DrawPolygon(self.Ptr, intPtrpen,arraypoints)


#    @dispatch
#
#    def DrawPolygon(self ,brush:PdfBrush,points:'PointF[]'):
#        """
#    <summary>
#        Draws a polygon.
#    </summary>
#    <param name="brush">The brush.</param>
#    <param name="points">The points.</param>
#        """
#        intPtrbrush:c_void_p = brush.Ptr
#        #arraypoints:ArrayTypepoints = ""
#        countpoints = len(points)
#        ArrayTypepoints = c_void_p * countpoints
#        arraypoints = ArrayTypepoints()
#        for i in range(0, countpoints):
#            arraypoints[i] = points[i].Ptr
#
#
#        GetDllLibPdf().PdfCanvas_DrawPolygonBP.argtypes=[c_void_p ,c_void_p,ArrayTypepoints]
#        GetDllLibPdf().PdfCanvas_DrawPolygonBP(self.Ptr, intPtrbrush,arraypoints)


#    @dispatch
#
#    def DrawPolygon(self ,pen:PdfPen,brush:PdfBrush,points:'PointF[]'):
#        """
#    <summary>
#        Draws a polygon.
#    </summary>
#    <param name="pen">The pen.</param>
#    <param name="brush">The brush.</param>
#    <param name="points">The points.</param>
#        """
#        intPtrpen:c_void_p = pen.Ptr
#        intPtrbrush:c_void_p = brush.Ptr
#        #arraypoints:ArrayTypepoints = ""
#        countpoints = len(points)
#        ArrayTypepoints = c_void_p * countpoints
#        arraypoints = ArrayTypepoints()
#        for i in range(0, countpoints):
#            arraypoints[i] = points[i].Ptr
#
#
#        GetDllLibPdf().PdfCanvas_DrawPolygonPBP.argtypes=[c_void_p ,c_void_p,c_void_p,ArrayTypepoints]
#        GetDllLibPdf().PdfCanvas_DrawPolygonPBP(self.Ptr, intPtrpen,intPtrbrush,arraypoints)


    @dispatch

    def DrawBezier(self ,pen:PdfPen,startPoint:PointF,firstControlPoint:PointF,secondControlPoint:PointF,endPoint:PointF):
        """
    <summary>
        Draws a bezier curve.
    </summary>
    <param name="pen">The pen.</param>
    <param name="startPoint">The start point.</param>
    <param name="firstControlPoint">The first control point.</param>
    <param name="secondControlPoint">The second control point.</param>
    <param name="endPoint">The end point.</param>
        """
        intPtrpen:c_void_p = pen.Ptr
        intPtrstartPoint:c_void_p = startPoint.Ptr
        intPtrfirstControlPoint:c_void_p = firstControlPoint.Ptr
        intPtrsecondControlPoint:c_void_p = secondControlPoint.Ptr
        intPtrendPoint:c_void_p = endPoint.Ptr

        GetDllLibPdf().PdfCanvas_DrawBezier.argtypes=[c_void_p ,c_void_p,c_void_p,c_void_p,c_void_p,c_void_p]
        GetDllLibPdf().PdfCanvas_DrawBezier(self.Ptr, intPtrpen,intPtrstartPoint,intPtrfirstControlPoint,intPtrsecondControlPoint,intPtrendPoint)

    @dispatch

    def DrawBezier(self ,pen:PdfPen,startPointX:float,startPointY:float,firstControlPointX:float,firstControlPointY:float,secondControlPointX:float,secondControlPointY:float,endPointX:float,endPointY:float):
        """
    <summary>
        Draws a bezier curve.
    </summary>
    <param name="pen">The pen.</param>
    <param name="startPointX">The start point X.</param>
    <param name="startPointY">The start point Y.</param>
    <param name="firstControlPointX">The first control point X.</param>
    <param name="firstControlPointY">The first control point Y.</param>
    <param name="secondControlPointX">The second control point X.</param>
    <param name="secondControlPointY">The second control point Y.</param>
    <param name="endPointX">The end point X.</param>
    <param name="endPointY">The end point Y.</param>
        """
        intPtrpen:c_void_p = pen.Ptr

        GetDllLibPdf().PdfCanvas_DrawBezierPSSFFSSEE.argtypes=[c_void_p ,c_void_p,c_float,c_float,c_float,c_float,c_float,c_float,c_float,c_float]
        GetDllLibPdf().PdfCanvas_DrawBezierPSSFFSSEE(self.Ptr, intPtrpen,startPointX,startPointY,firstControlPointX,firstControlPointY,secondControlPointX,secondControlPointY,endPointX,endPointY)

    @dispatch

    def DrawPath(self ,pen:PdfPen,path:'PdfPath'):
        """
    <summary>
        Draws a path.
    </summary>
    <param name="pen">The pen.</param>
    <param name="path">The path.</param>
        """
        intPtrpen:c_void_p = pen.Ptr
        intPtrpath:c_void_p = path.Ptr

        GetDllLibPdf().PdfCanvas_DrawPath.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().PdfCanvas_DrawPath(self.Ptr, intPtrpen,intPtrpath)

    @dispatch

    def DrawPath(self ,brush:PdfBrush,path:'PdfPath'):
        """
    <summary>
        Draws a path.
    </summary>
    <param name="brush">The brush.</param>
    <param name="path">The path.</param>
        """
        intPtrbrush:c_void_p = brush.Ptr
        intPtrpath:c_void_p = path.Ptr

        GetDllLibPdf().PdfCanvas_DrawPathBP.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().PdfCanvas_DrawPathBP(self.Ptr, intPtrbrush,intPtrpath)


    @dispatch

    def DrawPath(self ,pen:PdfPen,brush:PdfBrush,path:'PdfPath'):
        """
    <summary>
        Draws a path.
    </summary>
    <param name="pen">The pen.</param>
    <param name="brush">The brush.</param>
    <param name="path">The path.</param>
        """
        intPtrpen:c_void_p = pen.Ptr
        intPtrbrush:c_void_p = brush.Ptr
        intPtrpath:c_void_p = path.Ptr

        GetDllLibPdf().PdfCanvas_DrawPathPBP.argtypes=[c_void_p ,c_void_p,c_void_p,c_void_p]
        GetDllLibPdf().PdfCanvas_DrawPathPBP(self.Ptr, intPtrpen,intPtrbrush,intPtrpath)

    @dispatch
    def DrawImage(self ,image,point:PointF):
        """
    <summary>
        Draws an image.
    </summary>
    <param name="image">The image.</param>
    <param name="point">The point.</param>
        """
        intPtrimage:c_void_p = image.Ptr
        intPtrpoint:c_void_p = point.Ptr

        GetDllLibPdf().PdfCanvas_DrawImage.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().PdfCanvas_DrawImage(self.Ptr, intPtrimage,intPtrpoint)

    @dispatch

    def DrawImage(self ,image,x:float,y:float):
        """
    <summary>
        Draws an image.
    </summary>
    <param name="image">The image.</param>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
        """
        intPtrimage:c_void_p = image.Ptr

        GetDllLibPdf().PdfCanvas_DrawImageIXY.argtypes=[c_void_p ,c_void_p,c_float,c_float]
        GetDllLibPdf().PdfCanvas_DrawImageIXY(self.Ptr, intPtrimage,x,y)

    @dispatch

    def DrawImage(self ,image,rectangle:RectangleF):
        """
    <summary>
        Draws an image.
    </summary>
    <param name="image">The image.</param>
    <param name="rectangle">The rectangle.</param>
        """
        intPtrimage:c_void_p = image.Ptr
        intPtrrectangle:c_void_p = rectangle.Ptr

        GetDllLibPdf().PdfCanvas_DrawImageIR.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().PdfCanvas_DrawImageIR(self.Ptr, intPtrimage,intPtrrectangle)

    @dispatch

    def DrawImage(self ,image,point:PointF,size:SizeF):
        """
    <summary>
        Draws an image.
    </summary>
    <param name="image">The image.</param>
    <param name="point">The point.</param>
    <param name="size">The size.</param>
        """
        intPtrimage:c_void_p = image.Ptr
        intPtrpoint:c_void_p = point.Ptr
        intPtrsize:c_void_p = size.Ptr

        GetDllLibPdf().PdfCanvas_DrawImageIPS.argtypes=[c_void_p ,c_void_p,c_void_p,c_void_p]
        GetDllLibPdf().PdfCanvas_DrawImageIPS(self.Ptr, intPtrimage,intPtrpoint,intPtrsize)

    @dispatch

    def DrawImage(self ,image,compressionQuality:int,point:PointF,size:SizeF):
        """
    <summary>
        Draws an image,recommending monochrome image.
    </summary>
    <param name="image">The image.</param>
    <param name="compressionQuality">The image compresson quality.</param>
    <param name="point">The point.</param>
    <param name="size">The size.</param>
        """
        intPtrimage:c_void_p = image.Ptr
        intPtrpoint:c_void_p = point.Ptr
        intPtrsize:c_void_p = size.Ptr

        GetDllLibPdf().PdfCanvas_DrawImageICPS.argtypes=[c_void_p ,c_void_p,c_int,c_void_p,c_void_p]
        GetDllLibPdf().PdfCanvas_DrawImageICPS(self.Ptr, intPtrimage,compressionQuality,intPtrpoint,intPtrsize)

    @dispatch

    def DrawImage(self ,image,x:float,y:float,width:float,height:float):
        """
    <summary>
        Draws an image.
    </summary>
    <param name="image">The image.</param>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
    <param name="width">The width.</param>
    <param name="height">The height.</param>
        """
        intPtrimage:c_void_p = image.Ptr

        GetDllLibPdf().PdfCanvas_DrawImageIXYWH.argtypes=[c_void_p ,c_void_p,c_float,c_float,c_float,c_float]
        GetDllLibPdf().PdfCanvas_DrawImageIXYWH(self.Ptr, intPtrimage,x,y,width,height)

    @dispatch

    def DrawImage(self ,image,compressionQuality:int,x:float,y:float,width:float,height:float):
        """
    <summary>
        Draws an image,recommending monochrome image
    </summary>
    <param name="image">The image.</param>
    <param name="compressionQuality">The image compresson quality.</param>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
    <param name="width">The width.</param>
    <param name="height">The height.</param>
        """
        intPtrimage:c_void_p = image.Ptr

        GetDllLibPdf().PdfCanvas_DrawImageICXYWH.argtypes=[c_void_p ,c_void_p,c_int,c_float,c_float,c_float,c_float]
        GetDllLibPdf().PdfCanvas_DrawImageICXYWH(self.Ptr, intPtrimage,compressionQuality,x,y,width,height)

    @dispatch

    def DrawString(self ,s:str,font:PdfFontBase,brush:PdfBrush,point:PointF):
        """
    <summary>
        Draws the specified text string at the specified location
            with the specified Brush and Font objects. 
    </summary>
    <param name="s">The text string.</param>
    <param name="font">The font.</param>
    <param name="brush">The brush.</param>
    <param name="point">The location point.</param>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrbrush:c_void_p = brush.Ptr
        intPtrpoint:c_void_p = point.Ptr

        GetDllLibPdf().PdfCanvas_DrawString.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_void_p]
        GetDllLibPdf().PdfCanvas_DrawString(self.Ptr, s,intPtrfont,intPtrbrush,intPtrpoint)

    @dispatch

    def DrawString(self ,s:str,font:PdfFontBase,brush:PdfBrush,point:PointF,format:PdfStringFormat):
        """
    <summary>
        Draws the specified text string at the specified location
            with the specified Brush and Font objects. 
    </summary>
    <param name="s">The text string.</param>
    <param name="font">The font.</param>
    <param name="brush">The brush.</param>
    <param name="point">The point.</param>
    <param name="format">The text string format.</param>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrbrush:c_void_p = brush.Ptr
        intPtrpoint:c_void_p = point.Ptr
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfCanvas_DrawStringSFBPF.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_void_p,c_void_p]
        GetDllLibPdf().PdfCanvas_DrawStringSFBPF(self.Ptr, s,intPtrfont,intPtrbrush,intPtrpoint,intPtrformat)

    @dispatch

    def DrawString(self ,s:str,font:PdfFontBase,brush:PdfBrush,x:float,y:float):
        """
    <summary>
        Draws the specified text string at the specified location
            with the specified Brush and Font objects. 
    </summary>
    <param name="s">The text string.</param>
    <param name="font">The font.</param>
    <param name="brush">The brush.</param>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrbrush:c_void_p = brush.Ptr

        GetDllLibPdf().PdfCanvas_DrawStringSFBXY.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_float,c_float]
        GetDllLibPdf().PdfCanvas_DrawStringSFBXY(self.Ptr, s,intPtrfont,intPtrbrush,x,y)

    @dispatch

    def DrawString(self ,s:str,font:PdfFontBase,brush:PdfBrush,x:float,y:float,format:PdfStringFormat):
        """
    <summary>
        Draws the specified text string at the specified location
            with the specified Brush and Font objects. 
    </summary>
    <param name="s">The text string.</param>
    <param name="font">The font.</param>
    <param name="brush">The brush.</param>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
    <param name="format">The text string format.</param>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrbrush:c_void_p = brush.Ptr
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfCanvas_DrawStringSFBXYF.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_float,c_float,c_void_p]
        GetDllLibPdf().PdfCanvas_DrawStringSFBXYF(self.Ptr, s,intPtrfont,intPtrbrush,x,y,intPtrformat)

    @dispatch

    def DrawString(self ,s:str,font:PdfFontBase,pen:PdfPen,point:PointF):
        """
    <summary>
        Draws the specified text string at the specified location
            with the specified Brush and Font objects. 
    </summary>
    <param name="s">The text string.</param>
    <param name="font">The font.</param>
    <param name="pen">The pen.</param>
    <param name="point">The location point.</param>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrpen:c_void_p = pen.Ptr
        intPtrpoint:c_void_p = point.Ptr

        GetDllLibPdf().PdfCanvas_DrawStringSFPP.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_void_p]
        GetDllLibPdf().PdfCanvas_DrawStringSFPP(self.Ptr, s,intPtrfont,intPtrpen,intPtrpoint)

    @dispatch

    def DrawString(self ,s:str,font:PdfFontBase,pen:PdfPen,point:PointF,format:PdfStringFormat):
        """
    <summary>
        Draws the specified text string at the specified location
            with the specified Brush and Font objects. 
    </summary>
    <param name="s">The text string.</param>
    <param name="font">The font.</param>
    <param name="pen">The pen.</param>
    <param name="point">The point.</param>
    <param name="format">The text string format.</param>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrpen:c_void_p = pen.Ptr
        intPtrpoint:c_void_p = point.Ptr
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfCanvas_DrawStringSFPPF.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_void_p,c_void_p]
        GetDllLibPdf().PdfCanvas_DrawStringSFPPF(self.Ptr, s,intPtrfont,intPtrpen,intPtrpoint,intPtrformat)

    @dispatch

    def DrawString(self ,s:str,font:PdfFontBase,pen:PdfPen,x:float,y:float):
        """
    <summary>
        Draws the specified text string at the specified location
            with the specified Brush and Font objects. 
    </summary>
    <param name="s">The text string.</param>
    <param name="font">The font.</param>
    <param name="pen">The pen.</param>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrpen:c_void_p = pen.Ptr

        GetDllLibPdf().PdfCanvas_DrawStringSFPXY.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_float,c_float]
        GetDllLibPdf().PdfCanvas_DrawStringSFPXY(self.Ptr, s,intPtrfont,intPtrpen,x,y)

    @dispatch

    def DrawString(self ,s:str,font:PdfFontBase,pen:PdfPen,x:float,y:float,format:PdfStringFormat):
        """
    <summary>
        Draws the specified text string at the specified location
            with the specified Brush and Font objects. 
    </summary>
    <param name="s">The text string.</param>
    <param name="font">The font.</param>
    <param name="pen">The pen.</param>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
    <param name="format">The text string format.</param>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrpen:c_void_p = pen.Ptr
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfCanvas_DrawStringSFPXYF.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_float,c_float,c_void_p]
        GetDllLibPdf().PdfCanvas_DrawStringSFPXYF(self.Ptr, s,intPtrfont,intPtrpen,x,y,intPtrformat)

    @dispatch

    def DrawString(self ,s:str,font:PdfFontBase,pen:PdfPen,brush:PdfBrush,point:PointF):
        """
    <summary>
        Draws the specified text string at the specified location
            with the specified Brush and Font objects. 
    </summary>
    <param name="s">The text string.</param>
    <param name="font">The font.</param>
    <param name="pen">The pen.</param>
    <param name="brush">The brush.</param>
    <param name="point">The location point.</param>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrpen:c_void_p = pen.Ptr
        intPtrbrush:c_void_p = brush.Ptr
        intPtrpoint:c_void_p = point.Ptr

        GetDllLibPdf().PdfCanvas_DrawStringSFPBP.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_void_p,c_void_p]
        GetDllLibPdf().PdfCanvas_DrawStringSFPBP(self.Ptr, s,intPtrfont,intPtrpen,intPtrbrush,intPtrpoint)

    @dispatch

    def DrawString(self ,s:str,font:PdfFontBase,pen:PdfPen,brush:PdfBrush,point:PointF,format:PdfStringFormat):
        """
    <summary>
        Draws the specified text string at the specified location
            with the specified Brush and Font objects. 
    </summary>
    <param name="s">The text string.</param>
    <param name="font">The font.</param>
    <param name="pen">The pen.</param>
    <param name="brush">The brush.</param>
    <param name="point">The point.</param>
    <param name="format">The text string format.</param>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrpen:c_void_p = pen.Ptr
        intPtrbrush:c_void_p = brush.Ptr
        intPtrpoint:c_void_p = point.Ptr
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfCanvas_DrawStringSFPBPF.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_void_p,c_void_p,c_void_p]
        GetDllLibPdf().PdfCanvas_DrawStringSFPBPF(self.Ptr, s,intPtrfont,intPtrpen,intPtrbrush,intPtrpoint,intPtrformat)

    @dispatch

    def DrawString(self ,s:str,font:PdfFontBase,pen:PdfPen,brush:PdfBrush,x:float,y:float,format:PdfStringFormat):
        """
    <summary>
        Draws the specified text string at the specified location
            with the specified Brush and Font objects. 
    </summary>
    <param name="s">The text string.</param>
    <param name="font">The font.</param>
    <param name="pen">The pen.</param>
    <param name="brush">The brush.</param>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
    <param name="format">The text string format.</param>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrpen:c_void_p = pen.Ptr
        intPtrbrush:c_void_p = brush.Ptr
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfCanvas_DrawStringSFPBXYF.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_void_p,c_float,c_float,c_void_p]
        GetDllLibPdf().PdfCanvas_DrawStringSFPBXYF(self.Ptr, s,intPtrfont,intPtrpen,intPtrbrush,x,y,intPtrformat)

    @dispatch

    def DrawString(self ,s:str,font:PdfFontBase,pen:PdfPen,brush:PdfBrush,x:float,y:float):
        """
    <summary>
        Draws the specified text string at the specified location
            with the specified Brush and Font objects. 
    </summary>
    <param name="s">The text string.</param>
    <param name="font">The font.</param>
    <param name="pen">The pen.</param>
    <param name="brush">The brush.</param>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrpen:c_void_p = pen.Ptr
        intPtrbrush:c_void_p = brush.Ptr

        GetDllLibPdf().PdfCanvas_DrawStringSFPBXY.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_void_p,c_float,c_float]
        GetDllLibPdf().PdfCanvas_DrawStringSFPBXY(self.Ptr, s,intPtrfont,intPtrpen,intPtrbrush,x,y)

    @dispatch

    def DrawString(self ,s:str,font:PdfFontBase,brush:PdfBrush,layoutRectangle:RectangleF):
        """
    <summary>
        Draws the specified text string at the specified location and size
            with the specified Brush and Font objects. 
    </summary>
    <param name="s">The text string.</param>
    <param name="font">The font.</param>
    <param name="brush">The brush.</param>
    <param name="layoutRectangle">RectangleF structure that specifies the bounds of the drawn text.</param>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrbrush:c_void_p = brush.Ptr
        intPtrlayoutRectangle:c_void_p = layoutRectangle.Ptr

        GetDllLibPdf().PdfCanvas_DrawStringSFBL.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_void_p]
        GetDllLibPdf().PdfCanvas_DrawStringSFBL(self.Ptr, s,intPtrfont,intPtrbrush,intPtrlayoutRectangle)

    @dispatch

    def DrawString(self ,s:str,font:PdfFontBase,brush:PdfBrush,layoutRectangle:RectangleF,format:PdfStringFormat):
        """
    <summary>
        Draws the specified text string at the specified location and size
            with the specified Brush and Font objects. 
    </summary>
    <param name="s">The text string.</param>
    <param name="font">The font.</param>
    <param name="brush">The brush.</param>
    <param name="layoutRectangle">RectangleF structure that specifies the bounds of the drawn text.</param>
    <param name="format">The text string format.</param>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrbrush:c_void_p = brush.Ptr
        intPtrlayoutRectangle:c_void_p = layoutRectangle.Ptr
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfCanvas_DrawStringSFBLF.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_void_p,c_void_p]
        GetDllLibPdf().PdfCanvas_DrawStringSFBLF(self.Ptr, s,intPtrfont,intPtrbrush,intPtrlayoutRectangle,intPtrformat)

    @dispatch

    def DrawString(self ,s:str,font:PdfFontBase,pen:PdfPen,layoutRectangle:RectangleF):
        """
    <summary>
        Draws the specified text string at the specified location and size
            with the specified Pen and Font objects. 
    </summary>
    <param name="s">The text string.</param>
    <param name="font">The font.</param>
    <param name="pen">The pen.</param>
    <param name="layoutRectangle">RectangleF structure that specifies the bounds of the drawn text.</param>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrpen:c_void_p = pen.Ptr
        intPtrlayoutRectangle:c_void_p = layoutRectangle.Ptr

        GetDllLibPdf().PdfCanvas_DrawStringSFPL.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_void_p]
        GetDllLibPdf().PdfCanvas_DrawStringSFPL(self.Ptr, s,intPtrfont,intPtrpen,intPtrlayoutRectangle)

    @dispatch

    def DrawString(self ,s:str,font:PdfFontBase,pen:PdfPen,layoutRectangle:RectangleF,format:PdfStringFormat):
        """
    <summary>
        Draws the specified text string at the specified location and size
            with the specified Pen and Font objects. 
    </summary>
    <param name="s">The text string.</param>
    <param name="font">The font.</param>
    <param name="pen">The pen.</param>
    <param name="layoutRectangle">RectangleF structure that specifies the bounds of the drawn text.</param>
    <param name="format">The text string format.</param>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrpen:c_void_p = pen.Ptr
        intPtrlayoutRectangle:c_void_p = layoutRectangle.Ptr
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfCanvas_DrawStringSFPLF.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_void_p,c_void_p]
        GetDllLibPdf().PdfCanvas_DrawStringSFPLF(self.Ptr, s,intPtrfont,intPtrpen,intPtrlayoutRectangle,intPtrformat)

    @dispatch

    def DrawString(self ,s:str,font:PdfFontBase,pen:PdfPen,brush:PdfBrush,layoutRectangle:RectangleF,format:PdfStringFormat):
        """
    <summary>
        Draws the specified text string at the specified location and size
            with the specified Pen, Brush and Font objects. 
    </summary>
    <param name="s">The text string.</param>
    <param name="font">The font.</param>
    <param name="pen">The pen.</param>
    <param name="brush">The brush.</param>
    <param name="layoutRectangle">RectangleF structure that specifies the bounds of the drawn text.</param>
    <param name="format">The text string format.</param>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrpen:c_void_p = pen.Ptr
        intPtrbrush:c_void_p = brush.Ptr
        intPtrlayoutRectangle:c_void_p = layoutRectangle.Ptr
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfCanvas_DrawStringSFPBLF.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_void_p,c_void_p,c_void_p]
        GetDllLibPdf().PdfCanvas_DrawStringSFPBLF(self.Ptr, s,intPtrfont,intPtrpen,intPtrbrush,intPtrlayoutRectangle,intPtrformat)

    @dispatch

    def DrawString(self ,s:str,font:PdfFontBase,brush:PdfBrush,point:PointF,htmlTags:bool):
        """
    <summary>
        Draws the specified text string at the specified location
            with the specified Brush and Font objects. 
    </summary>
    <param name="s">The text string.</param>
    <param name="font">The font.</param>
    <param name="brush">The brush.</param>
    <param name="point">The location point.</param>
    <param name="htmlTags">whether the parsing of HTML tags</param>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrbrush:c_void_p = brush.Ptr
        intPtrpoint:c_void_p = point.Ptr

        GetDllLibPdf().PdfCanvas_DrawStringSFBPH.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_void_p,c_bool]
        GetDllLibPdf().PdfCanvas_DrawStringSFBPH(self.Ptr, s,intPtrfont,intPtrbrush,intPtrpoint,htmlTags)

    @dispatch

    def DrawString(self ,s:str,font:PdfFontBase,brush:PdfBrush,point:PointF,format:PdfStringFormat,htmlTags:bool):
        """
    <summary>
        Draws the specified text string at the specified location
            with the specified Brush and Font objects. 
    </summary>
    <param name="s">The text string.</param>
    <param name="font">The font.</param>
    <param name="brush">The brush.</param>
    <param name="point">The point.</param>
    <param name="format">The text string format.</param>
    <param name="htmlTags">whether the parsing of HTML tags</param>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrbrush:c_void_p = brush.Ptr
        intPtrpoint:c_void_p = point.Ptr
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfCanvas_DrawStringSFBPFH.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_void_p,c_void_p,c_bool]
        GetDllLibPdf().PdfCanvas_DrawStringSFBPFH(self.Ptr, s,intPtrfont,intPtrbrush,intPtrpoint,intPtrformat,htmlTags)

    @dispatch

    def DrawString(self ,s:str,font:PdfFontBase,brush:PdfBrush,x:float,y:float,htmlTags:bool):
        """
    <summary>
        Draws the specified text string at the specified location
            with the specified Brush and Font objects. 
    </summary>
    <param name="s">The text string.</param>
    <param name="font">The font.</param>
    <param name="brush">The brush.</param>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
    <param name="htmlTags">whether the parsing of HTML tags</param>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrbrush:c_void_p = brush.Ptr

        GetDllLibPdf().PdfCanvas_DrawStringSFBXYH.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_float,c_float,c_bool]
        GetDllLibPdf().PdfCanvas_DrawStringSFBXYH(self.Ptr, s,intPtrfont,intPtrbrush,x,y,htmlTags)

    @dispatch

    def DrawString(self ,s:str,font:PdfFontBase,brush:PdfBrush,x:float,y:float,format:PdfStringFormat,htmlTags:bool):
        """
    <summary>
        Draws the specified text string at the specified location
            with the specified Brush and Font objects. 
    </summary>
    <param name="s">The text string.</param>
    <param name="font">The font.</param>
    <param name="brush">The brush.</param>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
    <param name="format">The text string format.</param>
    <param name="htmlTags">whether the parsing of HTML tags</param>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrbrush:c_void_p = brush.Ptr
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfCanvas_DrawStringSFBXYFH.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_float,c_float,c_void_p,c_bool]
        GetDllLibPdf().PdfCanvas_DrawStringSFBXYFH(self.Ptr, s,intPtrfont,intPtrbrush,x,y,intPtrformat,htmlTags)

    @dispatch

    def DrawString(self ,s:str,font:PdfFontBase,pen:PdfPen,point:PointF,htmlTags:bool):
        """
    <summary>
        Draws the specified text string at the specified location
            with the specified Brush and Font objects. 
    </summary>
    <param name="s">The text string.</param>
    <param name="font">The font.</param>
    <param name="pen">The pen.</param>
    <param name="point">The location point.</param>
    <param name="htmlTags">whether the parsing of HTML tags</param>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrpen:c_void_p = pen.Ptr
        intPtrpoint:c_void_p = point.Ptr

        GetDllLibPdf().PdfCanvas_DrawStringSFPPH.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_void_p,c_bool]
        GetDllLibPdf().PdfCanvas_DrawStringSFPPH(self.Ptr, s,intPtrfont,intPtrpen,intPtrpoint,htmlTags)

    @dispatch

    def DrawString(self ,s:str,font:PdfFontBase,pen:PdfPen,point:PointF,format:PdfStringFormat,htmlTags:bool):
        """
    <summary>
        Draws the specified text string at the specified location
            with the specified Brush and Font objects. 
    </summary>
    <param name="s">The text string.</param>
    <param name="font">The font.</param>
    <param name="pen">The pen.</param>
    <param name="point">The point.</param>
    <param name="format">The text string format.</param>
    <param name="htmlTags">whether the parsing of HTML tags</param>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrpen:c_void_p = pen.Ptr
        intPtrpoint:c_void_p = point.Ptr
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfCanvas_DrawStringSFPPFH.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_void_p,c_void_p,c_bool]
        GetDllLibPdf().PdfCanvas_DrawStringSFPPFH(self.Ptr, s,intPtrfont,intPtrpen,intPtrpoint,intPtrformat,htmlTags)

    @dispatch

    def DrawString(self ,s:str,font:PdfFontBase,pen:PdfPen,x:float,y:float,htmlTags:bool):
        """
    <summary>
        Draws the specified text string at the specified location
            with the specified Brush and Font objects. 
    </summary>
    <param name="s">The text string.</param>
    <param name="font">The font.</param>
    <param name="pen">The pen.</param>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
    <param name="htmlTags">whether the parsing of HTML tags</param>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrpen:c_void_p = pen.Ptr

        GetDllLibPdf().PdfCanvas_DrawStringSFPXYH.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_float,c_float,c_bool]
        GetDllLibPdf().PdfCanvas_DrawStringSFPXYH(self.Ptr, s,intPtrfont,intPtrpen,x,y,htmlTags)

    @dispatch

    def DrawString(self ,s:str,font:PdfFontBase,pen:PdfPen,x:float,y:float,format:PdfStringFormat,htmlTags:bool):
        """
    <summary>
        Draws the specified text string at the specified location
            with the specified Brush and Font objects. 
    </summary>
    <param name="s">The text string.</param>
    <param name="font">The font.</param>
    <param name="pen">The pen.</param>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
    <param name="format">The text string format.</param>
    <param name="htmlTags">whether the parsing of HTML tags</param>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrpen:c_void_p = pen.Ptr
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfCanvas_DrawStringSFPXYFH.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_float,c_float,c_void_p,c_bool]
        GetDllLibPdf().PdfCanvas_DrawStringSFPXYFH(self.Ptr, s,intPtrfont,intPtrpen,x,y,intPtrformat,htmlTags)

    @dispatch

    def DrawString(self ,s:str,font:PdfFontBase,pen:PdfPen,brush:PdfBrush,point:PointF,htmlTags:bool):
        """
    <summary>
        Draws the specified text string at the specified location
            with the specified Brush and Font objects. 
    </summary>
    <param name="s">The text string.</param>
    <param name="font">The font.</param>
    <param name="pen">The pen.</param>
    <param name="brush">The brush.</param>
    <param name="point">The location point.</param>
    <param name="htmlTags">whether the parsing of HTML tags</param>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrpen:c_void_p = pen.Ptr
        intPtrbrush:c_void_p = brush.Ptr
        intPtrpoint:c_void_p = point.Ptr

        GetDllLibPdf().PdfCanvas_DrawStringSFPBPH.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_void_p,c_void_p,c_bool]
        GetDllLibPdf().PdfCanvas_DrawStringSFPBPH(self.Ptr, s,intPtrfont,intPtrpen,intPtrbrush,intPtrpoint,htmlTags)

    @dispatch

    def DrawString(self ,s:str,font:PdfFontBase,pen:PdfPen,brush:PdfBrush,point:PointF,format:PdfStringFormat,htmlTags:bool):
        """
    <summary>
        Draws the specified text string at the specified location
            with the specified Brush and Font objects. 
    </summary>
    <param name="s">The text string.</param>
    <param name="font">The font.</param>
    <param name="pen">The pen.</param>
    <param name="brush">The brush.</param>
    <param name="point">The point.</param>
    <param name="format">The text string format.</param>
    <param name="htmlTags">whether the parsing of HTML tags</param>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrpen:c_void_p = pen.Ptr
        intPtrbrush:c_void_p = brush.Ptr
        intPtrpoint:c_void_p = point.Ptr
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfCanvas_DrawStringSFPBPFH.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_void_p,c_void_p,c_void_p,c_bool]
        GetDllLibPdf().PdfCanvas_DrawStringSFPBPFH(self.Ptr, s,intPtrfont,intPtrpen,intPtrbrush,intPtrpoint,intPtrformat,htmlTags)

    @dispatch

    def DrawString(self ,s:str,font:PdfFontBase,pen:PdfPen,brush:PdfBrush,x:float,y:float,format:PdfStringFormat,htmlTags:bool):
        """
    <summary>
        Draws the specified text string at the specified location
            with the specified Brush and Font objects. 
    </summary>
    <param name="s">The text string.</param>
    <param name="font">The font.</param>
    <param name="pen">The pen.</param>
    <param name="brush">The brush.</param>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
    <param name="format">The text string format.</param>
    <param name="htmlTags">whether the parsing of HTML tags</param>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrpen:c_void_p = pen.Ptr
        intPtrbrush:c_void_p = brush.Ptr
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfCanvas_DrawStringSFPBXYFH.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_void_p,c_float,c_float,c_void_p,c_bool]
        GetDllLibPdf().PdfCanvas_DrawStringSFPBXYFH(self.Ptr, s,intPtrfont,intPtrpen,intPtrbrush,x,y,intPtrformat,htmlTags)

    @dispatch

    def DrawString(self ,s:str,font:PdfFontBase,pen:PdfPen,brush:PdfBrush,x:float,y:float,htmlTags:bool):
        """
    <summary>
        Draws the specified text string at the specified location
            with the specified Brush and Font objects. 
    </summary>
    <param name="s">The text string.</param>
    <param name="font">The font.</param>
    <param name="pen">The pen.</param>
    <param name="brush">The brush.</param>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
    <param name="htmlTags">whether the parsing of HTML tags</param>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrpen:c_void_p = pen.Ptr
        intPtrbrush:c_void_p = brush.Ptr

        GetDllLibPdf().PdfCanvas_DrawStringSFPBXYH.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_void_p,c_float,c_float,c_bool]
        GetDllLibPdf().PdfCanvas_DrawStringSFPBXYH(self.Ptr, s,intPtrfont,intPtrpen,intPtrbrush,x,y,htmlTags)

    @dispatch

    def DrawString(self ,s:str,font:PdfFontBase,brush:PdfBrush,layoutRectangle:RectangleF,htmlTags:bool):
        """
    <summary>
        Draws the specified text string at the specified location and size
            with the specified Brush and Font objects. 
    </summary>
    <param name="s">The text string.</param>
    <param name="font">The font.</param>
    <param name="brush">The brush.</param>
    <param name="layoutRectangle">RectangleF structure that specifies the bounds of the drawn text.</param>
    <param name="htmlTags">whether the parsing of HTML tags</param>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrbrush:c_void_p = brush.Ptr
        intPtrlayoutRectangle:c_void_p = layoutRectangle.Ptr

        GetDllLibPdf().PdfCanvas_DrawStringSFBLH.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_void_p,c_bool]
        GetDllLibPdf().PdfCanvas_DrawStringSFBLH(self.Ptr, s,intPtrfont,intPtrbrush,intPtrlayoutRectangle,htmlTags)

    @dispatch

    def DrawString(self ,s:str,font:PdfFontBase,brush:PdfBrush,layoutRectangle:RectangleF,format:PdfStringFormat,htmlTags:bool):
        """
    <summary>
        Draws the specified text string at the specified location and size
            with the specified Brush and Font objects. 
    </summary>
    <param name="s">The text string.</param>
    <param name="font">The font.</param>
    <param name="brush">The brush.</param>
    <param name="layoutRectangle">RectangleF structure that specifies the bounds of the drawn text.</param>
    <param name="format">The text string format.</param>
    <param name="htmlTags">whether the parsing of HTML tags</param>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrbrush:c_void_p = brush.Ptr
        intPtrlayoutRectangle:c_void_p = layoutRectangle.Ptr
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfCanvas_DrawStringSFBLFH.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_void_p,c_void_p,c_bool]
        GetDllLibPdf().PdfCanvas_DrawStringSFBLFH(self.Ptr, s,intPtrfont,intPtrbrush,intPtrlayoutRectangle,intPtrformat,htmlTags)

    @dispatch

    def DrawString(self ,s:str,font:PdfFontBase,pen:PdfPen,layoutRectangle:RectangleF,htmlTags:bool):
        """
    <summary>
        Draws the specified text string at the specified location and size
            with the specified Pen and Font objects. 
    </summary>
    <param name="s">The text string.</param>
    <param name="font">The font.</param>
    <param name="pen">The pen.</param>
    <param name="layoutRectangle">RectangleF structure that specifies the bounds of the drawn text.</param>
    <param name="htmlTags">whether the parsing of HTML tags</param>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrpen:c_void_p = pen.Ptr
        intPtrlayoutRectangle:c_void_p = layoutRectangle.Ptr

        GetDllLibPdf().PdfCanvas_DrawStringSFPLH.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_void_p,c_bool]
        GetDllLibPdf().PdfCanvas_DrawStringSFPLH(self.Ptr, s,intPtrfont,intPtrpen,intPtrlayoutRectangle,htmlTags)

