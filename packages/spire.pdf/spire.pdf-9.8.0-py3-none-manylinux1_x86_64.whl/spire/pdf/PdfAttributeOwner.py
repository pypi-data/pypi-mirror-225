from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfAttributeOwner (SpireObject) :
    """
    <summary>
        The attribute owners.
    </summary>
    """
    @property

    def Name(self)->str:
        """
    <summary>
        The name of the application or plug-in extension owning the attribute data.
    </summary>
        """
        GetDllLibPdf().PdfAttributeOwner_get_Name.argtypes=[c_void_p]
        GetDllLibPdf().PdfAttributeOwner_get_Name.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfAttributeOwner_get_Name(self.Ptr))
        return ret


    @staticmethod

    def Layout()->'PdfAttributeOwner':
        """
    <summary>
        Attributes governing the layout of content.
    </summary>
        """
        #GetDllLibPdf().PdfAttributeOwner_Layout.argtypes=[]
        GetDllLibPdf().PdfAttributeOwner_Layout.restype=c_void_p
        intPtr = GetDllLibPdf().PdfAttributeOwner_Layout()
        ret = None if intPtr==None else PdfAttributeOwner(intPtr)
        return ret


    @staticmethod

    def List()->'PdfAttributeOwner':
        """
    <summary>
        Attributes governing the numbering of lists.
    </summary>
        """
        #GetDllLibPdf().PdfAttributeOwner_List.argtypes=[]
        GetDllLibPdf().PdfAttributeOwner_List.restype=c_void_p
        intPtr = GetDllLibPdf().PdfAttributeOwner_List()
        ret = None if intPtr==None else PdfAttributeOwner(intPtr)
        return ret


    @staticmethod

    def PrintField()->'PdfAttributeOwner':
        """
    <summary>
        Attributes governing Form structure elements for non-interactive form fields.
    </summary>
        """
        #GetDllLibPdf().PdfAttributeOwner_PrintField.argtypes=[]
        GetDllLibPdf().PdfAttributeOwner_PrintField.restype=c_void_p
        intPtr = GetDllLibPdf().PdfAttributeOwner_PrintField()
        ret = None if intPtr==None else PdfAttributeOwner(intPtr)
        return ret


    @staticmethod

    def Table()->'PdfAttributeOwner':
        """
    <summary>
        Attributes governing the organization of cells in tables.
    </summary>
        """
        #GetDllLibPdf().PdfAttributeOwner_Table.argtypes=[]
        GetDllLibPdf().PdfAttributeOwner_Table.restype=c_void_p
        intPtr = GetDllLibPdf().PdfAttributeOwner_Table()
        ret = None if intPtr==None else PdfAttributeOwner(intPtr)
        return ret


    @staticmethod

    def Xml_100()->'PdfAttributeOwner':
        """
    <summary>
        Additional attributes governing translation to XML, version 1.00
    </summary>
        """
        #GetDllLibPdf().PdfAttributeOwner_Xml_100.argtypes=[]
        GetDllLibPdf().PdfAttributeOwner_Xml_100.restype=c_void_p
        intPtr = GetDllLibPdf().PdfAttributeOwner_Xml_100()
        ret = None if intPtr==None else PdfAttributeOwner(intPtr)
        return ret


    @staticmethod

    def Html_320()->'PdfAttributeOwner':
        """
    <summary>
        Additional attributes governing translation to HTML, version 3.20
    </summary>
        """
        #GetDllLibPdf().PdfAttributeOwner_Html_320.argtypes=[]
        GetDllLibPdf().PdfAttributeOwner_Html_320.restype=c_void_p
        intPtr = GetDllLibPdf().PdfAttributeOwner_Html_320()
        ret = None if intPtr==None else PdfAttributeOwner(intPtr)
        return ret


    @staticmethod

    def Html_401()->'PdfAttributeOwner':
        """
    <summary>
        Additional attributes governing translation to HTML, version 4.01
    </summary>
        """
        #GetDllLibPdf().PdfAttributeOwner_Html_401.argtypes=[]
        GetDllLibPdf().PdfAttributeOwner_Html_401.restype=c_void_p
        intPtr = GetDllLibPdf().PdfAttributeOwner_Html_401()
        ret = None if intPtr==None else PdfAttributeOwner(intPtr)
        return ret


    @staticmethod

    def Oeb_100()->'PdfAttributeOwner':
        """
    <summary>
        Additional attributes governing translation to OEB, version 1.0
    </summary>
        """
        #GetDllLibPdf().PdfAttributeOwner_Oeb_100.argtypes=[]
        GetDllLibPdf().PdfAttributeOwner_Oeb_100.restype=c_void_p
        intPtr = GetDllLibPdf().PdfAttributeOwner_Oeb_100()
        ret = None if intPtr==None else PdfAttributeOwner(intPtr)
        return ret


    @staticmethod

    def Rtf_105()->'PdfAttributeOwner':
        """
    <summary>
        Additional attributes governing translation to Microsoft Rich Text Format, version 1.05
    </summary>
        """
        #GetDllLibPdf().PdfAttributeOwner_Rtf_105.argtypes=[]
        GetDllLibPdf().PdfAttributeOwner_Rtf_105.restype=c_void_p
        intPtr = GetDllLibPdf().PdfAttributeOwner_Rtf_105()
        ret = None if intPtr==None else PdfAttributeOwner(intPtr)
        return ret


    @staticmethod

    def Css_100()->'PdfAttributeOwner':
        """
    <summary>
        Additional attributes governing translation to a format using CSS, version 1.00
    </summary>
        """
        #GetDllLibPdf().PdfAttributeOwner_Css_100.argtypes=[]
        GetDllLibPdf().PdfAttributeOwner_Css_100.restype=c_void_p
        intPtr = GetDllLibPdf().PdfAttributeOwner_Css_100()
        ret = None if intPtr==None else PdfAttributeOwner(intPtr)
        return ret


    @staticmethod

    def Css_200()->'PdfAttributeOwner':
        """
    <summary>
        Additional attributes governing translation to a format using CSS, version 2.00
    </summary>
        """
        #GetDllLibPdf().PdfAttributeOwner_Css_200.argtypes=[]
        GetDllLibPdf().PdfAttributeOwner_Css_200.restype=c_void_p
        intPtr = GetDllLibPdf().PdfAttributeOwner_Css_200()
        ret = None if intPtr==None else PdfAttributeOwner(intPtr)
        return ret


