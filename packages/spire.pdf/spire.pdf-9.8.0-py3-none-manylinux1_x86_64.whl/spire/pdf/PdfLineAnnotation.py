from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfLineAnnotation (  PdfAnnotation) :
    @dispatch
    def __init__(self, rectangle:RectangleF):
        ptrRec:c_void_p = rectangle.Ptr
        GetDllLibPdf().PdfLineAnnotation_CreatePdfLineAnnotationR.argtypes=[c_void_p]
        GetDllLibPdf().PdfLineAnnotation_CreatePdfLineAnnotationR.restype = c_void_p
        intPtr = GetDllLibPdf().PdfLineAnnotation_CreatePdfLineAnnotationR(ptrRec)
        super(PdfLineAnnotation, self).__init__(intPtr)

    @dispatch
    def __init__(self, linePoints:List[int]):
        countnewValues = len(linePoints)
        ArrayTypenewValues = c_int * countnewValues
        arraynewValues = ArrayTypenewValues()
        for i in range(0, countnewValues):
            arraynewValues[i] = linePoints[i]

        GetDllLibPdf().PdfLineAnnotation_CreatePdfLineAnnotationL.argtypes=[ArrayTypenewValues,c_int]
        GetDllLibPdf().PdfLineAnnotation_CreatePdfLineAnnotationL.restype = c_void_p
        intPtr = GetDllLibPdf().PdfLineAnnotation_CreatePdfLineAnnotationL(arraynewValues,countnewValues)
        super(PdfLineAnnotation, self).__init__(intPtr)

    @dispatch
    def __init__(self, linePoints:List[int],text:str):
        countnewValues = len(linePoints)
        ArrayTypenewValues = c_int * countnewValues
        arraynewValues = ArrayTypenewValues()
        for i in range(0, countnewValues):
            arraynewValues[i] = linePoints[i]

        GetDllLibPdf().PdfLineAnnotation_CreatePdfLineAnnotationLT.argtypes=[ArrayTypenewValues,c_wchar_p,c_int]
        GetDllLibPdf().PdfLineAnnotation_CreatePdfLineAnnotationLT.restype = c_void_p
        intPtr = GetDllLibPdf().PdfLineAnnotation_CreatePdfLineAnnotationLT(arraynewValues,text,countnewValues)
        super(PdfLineAnnotation, self).__init__(intPtr)
    """
    <summary>
        Represents a line annotation. 
    </summary>
    """
    @property
    def LineCaption(self)->bool:
        """
    <summary>
        Gets or sets whether the line annotation caption should be displayed.
    </summary>
<value>
  <c>true</c> if the line caption should be displayed, otherwise <c>false</c>.</value>
        """
        GetDllLibPdf().PdfLineAnnotation_get_LineCaption.argtypes=[c_void_p]
        GetDllLibPdf().PdfLineAnnotation_get_LineCaption.restype=c_bool
        ret = GetDllLibPdf().PdfLineAnnotation_get_LineCaption(self.Ptr)
        return ret

    @LineCaption.setter
    def LineCaption(self, value:bool):
        GetDllLibPdf().PdfLineAnnotation_set_LineCaption.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfLineAnnotation_set_LineCaption(self.Ptr, value)

    @property
    def LeaderLine(self)->int:
        """
    <summary>
        Gets or sets Leader Line 
    </summary>
        """
        GetDllLibPdf().PdfLineAnnotation_get_LeaderLine.argtypes=[c_void_p]
        GetDllLibPdf().PdfLineAnnotation_get_LeaderLine.restype=c_int
        ret = GetDllLibPdf().PdfLineAnnotation_get_LeaderLine(self.Ptr)
        return ret

    @LeaderLine.setter
    def LeaderLine(self, value:int):
        GetDllLibPdf().PdfLineAnnotation_set_LeaderLine.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfLineAnnotation_set_LeaderLine(self.Ptr, value)

    @property
    def LeaderLineExt(self)->int:
        """
    <summary>
        Gets or sets Leader Line Extension
    </summary>
        """
        GetDllLibPdf().PdfLineAnnotation_get_LeaderLineExt.argtypes=[c_void_p]
        GetDllLibPdf().PdfLineAnnotation_get_LeaderLineExt.restype=c_int
        ret = GetDllLibPdf().PdfLineAnnotation_get_LeaderLineExt(self.Ptr)
        return ret

    @LeaderLineExt.setter
    def LeaderLineExt(self, value:int):
        GetDllLibPdf().PdfLineAnnotation_set_LeaderLineExt.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfLineAnnotation_set_LeaderLineExt(self.Ptr, value)

    @property

    def lineBorder(self)->'LineBorder':
        """
    <summary>
        Gets or sets Border style of the Line Annotation.
    </summary>
<value>A  enumeration member specifying the border style for the line.</value>
        """
        GetDllLibPdf().PdfLineAnnotation_get_lineBorder.argtypes=[c_void_p]
        GetDllLibPdf().PdfLineAnnotation_get_lineBorder.restype=c_void_p
        intPtr = GetDllLibPdf().PdfLineAnnotation_get_lineBorder(self.Ptr)
        ret = None if intPtr==None else LineBorder(intPtr)
        return ret


    @lineBorder.setter
    def lineBorder(self, value:'LineBorder'):
        GetDllLibPdf().PdfLineAnnotation_set_lineBorder.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfLineAnnotation_set_lineBorder(self.Ptr, value.Ptr)

    @property

    def BeginLineStyle(self)->'PdfLineEndingStyle':
        """
    <summary>
        Gets or sets the style used for the beginning of the line. 
    </summary>
<value>A  enumeration member specifying the begin style for the line.</value>
        """
        GetDllLibPdf().PdfLineAnnotation_get_BeginLineStyle.argtypes=[c_void_p]
        GetDllLibPdf().PdfLineAnnotation_get_BeginLineStyle.restype=c_int
        ret = GetDllLibPdf().PdfLineAnnotation_get_BeginLineStyle(self.Ptr)
        objwraped = PdfLineEndingStyle(ret)
        return objwraped

    @BeginLineStyle.setter
    def BeginLineStyle(self, value:'PdfLineEndingStyle'):
        GetDllLibPdf().PdfLineAnnotation_set_BeginLineStyle.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfLineAnnotation_set_BeginLineStyle(self.Ptr, value.value)

    @property

    def EndLineStyle(self)->'PdfLineEndingStyle':
        """
    <summary>
        Gets or sets the style used for the end of the line. 
    </summary>
<value>A  enumeration member specifying the end style for the line.</value>
        """
        GetDllLibPdf().PdfLineAnnotation_get_EndLineStyle.argtypes=[c_void_p]
        GetDllLibPdf().PdfLineAnnotation_get_EndLineStyle.restype=c_int
        ret = GetDllLibPdf().PdfLineAnnotation_get_EndLineStyle(self.Ptr)
        objwraped = PdfLineEndingStyle(ret)
        return objwraped

    @EndLineStyle.setter
    def EndLineStyle(self, value:'PdfLineEndingStyle'):
        GetDllLibPdf().PdfLineAnnotation_set_EndLineStyle.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfLineAnnotation_set_EndLineStyle(self.Ptr, value.value)

    @property

    def CaptionType(self)->'PdfLineCaptionType':
        """
    <summary>
        Gets or sets the line caption text type.
    </summary>
<value>A  enumeration member specifying the line caption type.</value>
        """
        GetDllLibPdf().PdfLineAnnotation_get_CaptionType.argtypes=[c_void_p]
        GetDllLibPdf().PdfLineAnnotation_get_CaptionType.restype=c_int
        ret = GetDllLibPdf().PdfLineAnnotation_get_CaptionType(self.Ptr)
        objwraped = PdfLineCaptionType(ret)
        return objwraped

    @CaptionType.setter
    def CaptionType(self, value:'PdfLineCaptionType'):
        GetDllLibPdf().PdfLineAnnotation_set_CaptionType.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfLineAnnotation_set_CaptionType(self.Ptr, value.value)

    @property

    def LineIntent(self)->'PdfLineIntent':
        """
    <summary>
        Gets or sets LineIntent
    </summary>
        """
        GetDllLibPdf().PdfLineAnnotation_get_LineIntent.argtypes=[c_void_p]
        GetDllLibPdf().PdfLineAnnotation_get_LineIntent.restype=c_int
        ret = GetDllLibPdf().PdfLineAnnotation_get_LineIntent(self.Ptr)
        objwraped = PdfLineIntent(ret)
        return objwraped

    @LineIntent.setter
    def LineIntent(self, value:'PdfLineIntent'):
        GetDllLibPdf().PdfLineAnnotation_set_LineIntent.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfLineAnnotation_set_LineIntent(self.Ptr, value.value)

    @property

    def InnerLineColor(self)->'PdfRGBColor':
        """
    <summary>
        Gets or sets Inner Color of the PdfLine
    </summary>
        """
        GetDllLibPdf().PdfLineAnnotation_get_InnerLineColor.argtypes=[c_void_p]
        GetDllLibPdf().PdfLineAnnotation_get_InnerLineColor.restype=c_void_p
        intPtr = GetDllLibPdf().PdfLineAnnotation_get_InnerLineColor(self.Ptr)
        ret = None if intPtr==None else PdfRGBColor(intPtr)
        return ret


    @InnerLineColor.setter
    def InnerLineColor(self, value:'PdfRGBColor'):
        GetDllLibPdf().PdfLineAnnotation_set_InnerLineColor.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfLineAnnotation_set_InnerLineColor(self.Ptr, value.Ptr)

    @property

    def BackColor(self)->'PdfRGBColor':
        """
    <summary>
        Gets or sets Background Color of the PdfLine
    </summary>
        """
        GetDllLibPdf().PdfLineAnnotation_get_BackColor.argtypes=[c_void_p]
        GetDllLibPdf().PdfLineAnnotation_get_BackColor.restype=c_void_p
        intPtr = GetDllLibPdf().PdfLineAnnotation_get_BackColor(self.Ptr)
        ret = None if intPtr==None else PdfRGBColor(intPtr)
        return ret


    @BackColor.setter
    def BackColor(self, value:'PdfRGBColor'):
        GetDllLibPdf().PdfLineAnnotation_set_BackColor.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfLineAnnotation_set_BackColor(self.Ptr, value.Ptr)

    @property

    def Author(self)->str:
        """
    <summary>
        To specifying author
    </summary>
        """
        GetDllLibPdf().PdfLineAnnotation_get_Author.argtypes=[c_void_p]
        GetDllLibPdf().PdfLineAnnotation_get_Author.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfLineAnnotation_get_Author(self.Ptr))
        return ret


    @Author.setter
    def Author(self, value:str):
        GetDllLibPdf().PdfLineAnnotation_set_Author.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfLineAnnotation_set_Author(self.Ptr, value)

    @property

    def Subject(self)->str:
        """
    <summary>
        To specifying subject
    </summary>
        """
        GetDllLibPdf().PdfLineAnnotation_get_Subject.argtypes=[c_void_p]
        GetDllLibPdf().PdfLineAnnotation_get_Subject.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfLineAnnotation_get_Subject(self.Ptr))
        return ret


    @Subject.setter
    def Subject(self, value:str):
        GetDllLibPdf().PdfLineAnnotation_set_Subject.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfLineAnnotation_set_Subject(self.Ptr, value)


    def m_captionType(self)->'PdfLineCaptionType':
        """
    <summary>
        To specifying Caption Type
    </summary>
        """
        GetDllLibPdf().PdfLineAnnotation_m_captionType.argtypes=[c_void_p]
        GetDllLibPdf().PdfLineAnnotation_m_captionType.restype=c_int
        ret = GetDllLibPdf().PdfLineAnnotation_m_captionType(self.Ptr)
        objwraped = PdfLineCaptionType(ret)
        return objwraped

