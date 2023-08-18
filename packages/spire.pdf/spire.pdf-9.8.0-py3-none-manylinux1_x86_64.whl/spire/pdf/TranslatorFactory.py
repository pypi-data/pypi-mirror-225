from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class TranslatorFactory (SpireObject) :
    """
    <summary>
        Translator factory which can judeg the input file type and initialize
    </summary>
<author>linyaohu</author>
    """
    @staticmethod

    def CheckUOFFileType(srcFileName:str)->'DocType':
        """
    <summary>
        check uof file type
    </summary>
    <param name="srcFileName">source file name</param>
    <returns>document type</returns>
        """
        
        GetDllLibPdf().TranslatorFactory_CheckUOFFileType.argtypes=[ c_wchar_p]
        GetDllLibPdf().TranslatorFactory_CheckUOFFileType.restype=c_int
        ret = GetDllLibPdf().TranslatorFactory_CheckUOFFileType( srcFileName)
        objwraped = DocType(ret)
        return objwraped

