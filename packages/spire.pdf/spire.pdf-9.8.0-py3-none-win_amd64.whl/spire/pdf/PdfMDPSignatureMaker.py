from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfMDPSignatureMaker (  PdfSignatureMaker) :
    """
    <summary>
        Pdf MDP (modification detection and prevention) signature maker.
            A document can contain only one MDP signature, it must be the first signed in the document.
            It enables the author to specify what changes are permitted to be made the document and 
            what changes invalidate the author’s signature.
    </summary>
    """
    @staticmethod
    def Level1Permissions()->int:
        """
    <summary>
        No changes to the document are permitted; 
            any change to the document invalidates the signature.
    </summary>
        """
        #GetDllLibPdf().PdfMDPSignatureMaker_Level1Permissions.argtypes=[]
        GetDllLibPdf().PdfMDPSignatureMaker_Level1Permissions.restype=c_int
        ret = GetDllLibPdf().PdfMDPSignatureMaker_Level1Permissions()
        return ret

    @staticmethod
    def Level2Permissions()->int:
        """
    <summary>
        Permitted changes are filling in forms, instantiating page templates, 
            and signing; other changes invalidate the signature.
    </summary>
        """
        #GetDllLibPdf().PdfMDPSignatureMaker_Level2Permissions.argtypes=[]
        GetDllLibPdf().PdfMDPSignatureMaker_Level2Permissions.restype=c_int
        ret = GetDllLibPdf().PdfMDPSignatureMaker_Level2Permissions()
        return ret

    @staticmethod
    def Level3Permissions()->int:
        """
    <summary>
        Permitted changes are the same as for 2, as well as annotation creation, 
            deletion, and modification; other changes invalidate the signature
    </summary>
        """
        #GetDllLibPdf().PdfMDPSignatureMaker_Level3Permissions.argtypes=[]
        GetDllLibPdf().PdfMDPSignatureMaker_Level3Permissions.restype=c_int
        ret = GetDllLibPdf().PdfMDPSignatureMaker_Level3Permissions()
        return ret

