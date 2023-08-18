from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfPaperSizes (SpireObject) :
    """
    <summary>
        Represents information about page size.
            The PaperSize's width and height,unit:in hundredths of an inch.
    </summary>
    """
#    @staticmethod
#
#    def Letter()->'PaperSize':
#        """
#    <summary>
#        Letter format.
#    </summary>
#        """
#        #GetDllLibPdf().PdfPaperSizes_Letter.argtypes=[]
#        GetDllLibPdf().PdfPaperSizes_Letter.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPaperSizes_Letter()
#        ret = None if intPtr==None else PaperSize(intPtr)
#        return ret
#


#    @staticmethod
#
#    def Note()->'PaperSize':
#        """
#    <summary>
#        Note format.
#    </summary>
#        """
#        #GetDllLibPdf().PdfPaperSizes_Note.argtypes=[]
#        GetDllLibPdf().PdfPaperSizes_Note.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPaperSizes_Note()
#        ret = None if intPtr==None else PaperSize(intPtr)
#        return ret
#


#    @staticmethod
#
#    def Legal()->'PaperSize':
#        """
#    <summary>
#        Legal format.
#    </summary>
#        """
#        #GetDllLibPdf().PdfPaperSizes_Legal.argtypes=[]
#        GetDllLibPdf().PdfPaperSizes_Legal.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPaperSizes_Legal()
#        ret = None if intPtr==None else PaperSize(intPtr)
#        return ret
#


#    @staticmethod
#
#    def A0()->'PaperSize':
#        """
#    <summary>
#        A0 format.
#    </summary>
#        """
#        #GetDllLibPdf().PdfPaperSizes_A0.argtypes=[]
#        GetDllLibPdf().PdfPaperSizes_A0.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPaperSizes_A0()
#        ret = None if intPtr==None else PaperSize(intPtr)
#        return ret
#


#    @staticmethod
#
#    def A1()->'PaperSize':
#        """
#    <summary>
#        A1 format.
#    </summary>
#        """
#        #GetDllLibPdf().PdfPaperSizes_A1.argtypes=[]
#        GetDllLibPdf().PdfPaperSizes_A1.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPaperSizes_A1()
#        ret = None if intPtr==None else PaperSize(intPtr)
#        return ret
#


#    @staticmethod
#
#    def A2()->'PaperSize':
#        """
#    <summary>
#        A2 format.
#    </summary>
#        """
#        #GetDllLibPdf().PdfPaperSizes_A2.argtypes=[]
#        GetDllLibPdf().PdfPaperSizes_A2.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPaperSizes_A2()
#        ret = None if intPtr==None else PaperSize(intPtr)
#        return ret
#


#    @staticmethod
#
#    def A3()->'PaperSize':
#        """
#    <summary>
#        A3 format.
#    </summary>
#        """
#        #GetDllLibPdf().PdfPaperSizes_A3.argtypes=[]
#        GetDllLibPdf().PdfPaperSizes_A3.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPaperSizes_A3()
#        ret = None if intPtr==None else PaperSize(intPtr)
#        return ret
#


#    @staticmethod
#
#    def A4()->'PaperSize':
#        """
#    <summary>
#        A4 format.
#    </summary>
#        """
#        #GetDllLibPdf().PdfPaperSizes_A4.argtypes=[]
#        GetDllLibPdf().PdfPaperSizes_A4.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPaperSizes_A4()
#        ret = None if intPtr==None else PaperSize(intPtr)
#        return ret
#


#    @staticmethod
#
#    def A5()->'PaperSize':
#        """
#    <summary>
#        A5 format.
#    </summary>
#        """
#        #GetDllLibPdf().PdfPaperSizes_A5.argtypes=[]
#        GetDllLibPdf().PdfPaperSizes_A5.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPaperSizes_A5()
#        ret = None if intPtr==None else PaperSize(intPtr)
#        return ret
#


#    @staticmethod
#
#    def A6()->'PaperSize':
#        """
#    <summary>
#        A6 format.
#    </summary>
#        """
#        #GetDllLibPdf().PdfPaperSizes_A6.argtypes=[]
#        GetDllLibPdf().PdfPaperSizes_A6.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPaperSizes_A6()
#        ret = None if intPtr==None else PaperSize(intPtr)
#        return ret
#


#    @staticmethod
#
#    def A7()->'PaperSize':
#        """
#    <summary>
#        A7 format.
#    </summary>
#        """
#        #GetDllLibPdf().PdfPaperSizes_A7.argtypes=[]
#        GetDllLibPdf().PdfPaperSizes_A7.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPaperSizes_A7()
#        ret = None if intPtr==None else PaperSize(intPtr)
#        return ret
#


#    @staticmethod
#
#    def A8()->'PaperSize':
#        """
#    <summary>
#        A8 format.
#    </summary>
#        """
#        #GetDllLibPdf().PdfPaperSizes_A8.argtypes=[]
#        GetDllLibPdf().PdfPaperSizes_A8.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPaperSizes_A8()
#        ret = None if intPtr==None else PaperSize(intPtr)
#        return ret
#


#    @staticmethod
#
#    def A9()->'PaperSize':
#        """
#    <summary>
#        A9 format.
#    </summary>
#        """
#        #GetDllLibPdf().PdfPaperSizes_A9.argtypes=[]
#        GetDllLibPdf().PdfPaperSizes_A9.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPaperSizes_A9()
#        ret = None if intPtr==None else PaperSize(intPtr)
#        return ret
#


#    @staticmethod
#
#    def A10()->'PaperSize':
#        """
#    <summary>
#        A10 format.
#    </summary>
#        """
#        #GetDllLibPdf().PdfPaperSizes_A10.argtypes=[]
#        GetDllLibPdf().PdfPaperSizes_A10.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPaperSizes_A10()
#        ret = None if intPtr==None else PaperSize(intPtr)
#        return ret
#


#    @staticmethod
#
#    def B0()->'PaperSize':
#        """
#    <summary>
#        B0 format.
#    </summary>
#        """
#        #GetDllLibPdf().PdfPaperSizes_B0.argtypes=[]
#        GetDllLibPdf().PdfPaperSizes_B0.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPaperSizes_B0()
#        ret = None if intPtr==None else PaperSize(intPtr)
#        return ret
#


#    @staticmethod
#
#    def B1()->'PaperSize':
#        """
#    <summary>
#        B1 format.
#    </summary>
#        """
#        #GetDllLibPdf().PdfPaperSizes_B1.argtypes=[]
#        GetDllLibPdf().PdfPaperSizes_B1.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPaperSizes_B1()
#        ret = None if intPtr==None else PaperSize(intPtr)
#        return ret
#


#    @staticmethod
#
#    def B2()->'PaperSize':
#        """
#    <summary>
#        B2 format.
#    </summary>
#        """
#        #GetDllLibPdf().PdfPaperSizes_B2.argtypes=[]
#        GetDllLibPdf().PdfPaperSizes_B2.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPaperSizes_B2()
#        ret = None if intPtr==None else PaperSize(intPtr)
#        return ret
#


#    @staticmethod
#
#    def B3()->'PaperSize':
#        """
#    <summary>
#        B3 format.
#    </summary>
#        """
#        #GetDllLibPdf().PdfPaperSizes_B3.argtypes=[]
#        GetDllLibPdf().PdfPaperSizes_B3.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPaperSizes_B3()
#        ret = None if intPtr==None else PaperSize(intPtr)
#        return ret
#


#    @staticmethod
#
#    def B4()->'PaperSize':
#        """
#    <summary>
#        B4 format.
#    </summary>
#        """
#        #GetDllLibPdf().PdfPaperSizes_B4.argtypes=[]
#        GetDllLibPdf().PdfPaperSizes_B4.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPaperSizes_B4()
#        ret = None if intPtr==None else PaperSize(intPtr)
#        return ret
#


#    @staticmethod
#
#    def B5()->'PaperSize':
#        """
#    <summary>
#        B5 format.
#    </summary>
#        """
#        #GetDllLibPdf().PdfPaperSizes_B5.argtypes=[]
#        GetDllLibPdf().PdfPaperSizes_B5.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPaperSizes_B5()
#        ret = None if intPtr==None else PaperSize(intPtr)
#        return ret
#


#    @staticmethod
#
#    def ArchE()->'PaperSize':
#        """
#    <summary>
#        ArchE format.
#    </summary>
#        """
#        #GetDllLibPdf().PdfPaperSizes_ArchE.argtypes=[]
#        GetDllLibPdf().PdfPaperSizes_ArchE.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPaperSizes_ArchE()
#        ret = None if intPtr==None else PaperSize(intPtr)
#        return ret
#


#    @staticmethod
#
#    def ArchD()->'PaperSize':
#        """
#    <summary>
#        ArchD format.
#    </summary>
#        """
#        #GetDllLibPdf().PdfPaperSizes_ArchD.argtypes=[]
#        GetDllLibPdf().PdfPaperSizes_ArchD.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPaperSizes_ArchD()
#        ret = None if intPtr==None else PaperSize(intPtr)
#        return ret
#


#    @staticmethod
#
#    def ArchC()->'PaperSize':
#        """
#    <summary>
#        ArchC format.
#    </summary>
#        """
#        #GetDllLibPdf().PdfPaperSizes_ArchC.argtypes=[]
#        GetDllLibPdf().PdfPaperSizes_ArchC.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPaperSizes_ArchC()
#        ret = None if intPtr==None else PaperSize(intPtr)
#        return ret
#


#    @staticmethod
#
#    def ArchB()->'PaperSize':
#        """
#    <summary>
#        ArchB format.
#    </summary>
#        """
#        #GetDllLibPdf().PdfPaperSizes_ArchB.argtypes=[]
#        GetDllLibPdf().PdfPaperSizes_ArchB.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPaperSizes_ArchB()
#        ret = None if intPtr==None else PaperSize(intPtr)
#        return ret
#


#    @staticmethod
#
#    def ArchA()->'PaperSize':
#        """
#    <summary>
#        ArchA format.
#    </summary>
#        """
#        #GetDllLibPdf().PdfPaperSizes_ArchA.argtypes=[]
#        GetDllLibPdf().PdfPaperSizes_ArchA.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPaperSizes_ArchA()
#        ret = None if intPtr==None else PaperSize(intPtr)
#        return ret
#


#    @staticmethod
#
#    def Flsa()->'PaperSize':
#        """
#    <summary>
#        The American Foolscap format.
#    </summary>
#        """
#        #GetDllLibPdf().PdfPaperSizes_Flsa.argtypes=[]
#        GetDllLibPdf().PdfPaperSizes_Flsa.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPaperSizes_Flsa()
#        ret = None if intPtr==None else PaperSize(intPtr)
#        return ret
#


#    @staticmethod
#
#    def HalfLetter()->'PaperSize':
#        """
#    <summary>
#        HalfLetter format.
#    </summary>
#        """
#        #GetDllLibPdf().PdfPaperSizes_HalfLetter.argtypes=[]
#        GetDllLibPdf().PdfPaperSizes_HalfLetter.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPaperSizes_HalfLetter()
#        ret = None if intPtr==None else PaperSize(intPtr)
#        return ret
#


#    @staticmethod
#
#    def Letter11x17()->'PaperSize':
#        """
#    <summary>
#        11x17 format.
#    </summary>
#        """
#        #GetDllLibPdf().PdfPaperSizes_Letter11x17.argtypes=[]
#        GetDllLibPdf().PdfPaperSizes_Letter11x17.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPaperSizes_Letter11x17()
#        ret = None if intPtr==None else PaperSize(intPtr)
#        return ret
#


#    @staticmethod
#
#    def Ledger()->'PaperSize':
#        """
#    <summary>
#        Ledger format.
#    </summary>
#        """
#        #GetDllLibPdf().PdfPaperSizes_Ledger.argtypes=[]
#        GetDllLibPdf().PdfPaperSizes_Ledger.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfPaperSizes_Ledger()
#        ret = None if intPtr==None else PaperSize(intPtr)
#        return ret
#


