from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfPageSize (SpireObject) :
    """
    <summary>
        Represents information about page size.
    </summary>
    """
    @staticmethod

    def Letter()->'SizeF':
        """
    <summary>
        Letter format.
    </summary>
        """
        #GetDllLibPdf().PdfPageSize_Letter.argtypes=[]
        GetDllLibPdf().PdfPageSize_Letter.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageSize_Letter()
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @staticmethod

    def Note()->'SizeF':
        """
    <summary>
        Note format.
    </summary>
        """
        #GetDllLibPdf().PdfPageSize_Note.argtypes=[]
        GetDllLibPdf().PdfPageSize_Note.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageSize_Note()
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @staticmethod

    def Legal()->'SizeF':
        """
    <summary>
        Legal format.
    </summary>
        """
        #GetDllLibPdf().PdfPageSize_Legal.argtypes=[]
        GetDllLibPdf().PdfPageSize_Legal.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageSize_Legal()
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @staticmethod

    def A0()->'SizeF':
        """
    <summary>
        A0 format.
    </summary>
        """
        #GetDllLibPdf().PdfPageSize_A0.argtypes=[]
        GetDllLibPdf().PdfPageSize_A0.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageSize_A0()
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @staticmethod

    def A1()->'SizeF':
        """
    <summary>
        A1 format.
    </summary>
        """
        #GetDllLibPdf().PdfPageSize_A1.argtypes=[]
        GetDllLibPdf().PdfPageSize_A1.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageSize_A1()
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @staticmethod

    def A2()->'SizeF':
        """
    <summary>
        A2 format.
    </summary>
        """
        #GetDllLibPdf().PdfPageSize_A2.argtypes=[]
        GetDllLibPdf().PdfPageSize_A2.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageSize_A2()
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @staticmethod

    def A3()->'SizeF':
        """
    <summary>
        A3 format.
    </summary>
        """
        #GetDllLibPdf().PdfPageSize_A3.argtypes=[]
        GetDllLibPdf().PdfPageSize_A3.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageSize_A3()
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @staticmethod

    def A4()->'SizeF':
        """
    <summary>
        A4 format.
    </summary>
        """
        #GetDllLibPdf().PdfPageSize_A4.argtypes=[]
        GetDllLibPdf().PdfPageSize_A4.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageSize_A4()
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @staticmethod

    def A5()->'SizeF':
        """
    <summary>
        A5 format.
    </summary>
        """
        #GetDllLibPdf().PdfPageSize_A5.argtypes=[]
        GetDllLibPdf().PdfPageSize_A5.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageSize_A5()
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @staticmethod

    def A6()->'SizeF':
        """
    <summary>
        A6 format.
    </summary>
        """
        #GetDllLibPdf().PdfPageSize_A6.argtypes=[]
        GetDllLibPdf().PdfPageSize_A6.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageSize_A6()
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @staticmethod

    def A7()->'SizeF':
        """
    <summary>
        A7 format.
    </summary>
        """
        #GetDllLibPdf().PdfPageSize_A7.argtypes=[]
        GetDllLibPdf().PdfPageSize_A7.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageSize_A7()
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @staticmethod

    def A8()->'SizeF':
        """
    <summary>
        A8 format.
    </summary>
        """
        #GetDllLibPdf().PdfPageSize_A8.argtypes=[]
        GetDllLibPdf().PdfPageSize_A8.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageSize_A8()
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @staticmethod

    def A9()->'SizeF':
        """
    <summary>
        A9 format.
    </summary>
        """
        #GetDllLibPdf().PdfPageSize_A9.argtypes=[]
        GetDllLibPdf().PdfPageSize_A9.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageSize_A9()
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @staticmethod

    def A10()->'SizeF':
        """
    <summary>
        A10 format.
    </summary>
        """
        #GetDllLibPdf().PdfPageSize_A10.argtypes=[]
        GetDllLibPdf().PdfPageSize_A10.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageSize_A10()
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @staticmethod

    def B0()->'SizeF':
        """
    <summary>
        B0 format.
    </summary>
        """
        #GetDllLibPdf().PdfPageSize_B0.argtypes=[]
        GetDllLibPdf().PdfPageSize_B0.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageSize_B0()
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @staticmethod

    def B1()->'SizeF':
        """
    <summary>
        B1 format.
    </summary>
        """
        #GetDllLibPdf().PdfPageSize_B1.argtypes=[]
        GetDllLibPdf().PdfPageSize_B1.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageSize_B1()
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @staticmethod

    def B2()->'SizeF':
        """
    <summary>
        B2 format.
    </summary>
        """
        #GetDllLibPdf().PdfPageSize_B2.argtypes=[]
        GetDllLibPdf().PdfPageSize_B2.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageSize_B2()
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @staticmethod

    def B3()->'SizeF':
        """
    <summary>
        B3 format.
    </summary>
        """
        #GetDllLibPdf().PdfPageSize_B3.argtypes=[]
        GetDllLibPdf().PdfPageSize_B3.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageSize_B3()
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @staticmethod

    def B4()->'SizeF':
        """
    <summary>
        B4 format.
    </summary>
        """
        #GetDllLibPdf().PdfPageSize_B4.argtypes=[]
        GetDllLibPdf().PdfPageSize_B4.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageSize_B4()
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @staticmethod

    def B5()->'SizeF':
        """
    <summary>
        B5 format.
    </summary>
        """
        #GetDllLibPdf().PdfPageSize_B5.argtypes=[]
        GetDllLibPdf().PdfPageSize_B5.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageSize_B5()
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @staticmethod

    def ArchE()->'SizeF':
        """
    <summary>
        ArchE format.
    </summary>
        """
        #GetDllLibPdf().PdfPageSize_ArchE.argtypes=[]
        GetDllLibPdf().PdfPageSize_ArchE.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageSize_ArchE()
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @staticmethod

    def ArchD()->'SizeF':
        """
    <summary>
        ArchD format.
    </summary>
        """
        #GetDllLibPdf().PdfPageSize_ArchD.argtypes=[]
        GetDllLibPdf().PdfPageSize_ArchD.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageSize_ArchD()
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @staticmethod

    def ArchC()->'SizeF':
        """
    <summary>
        ArchC format.
    </summary>
        """
        #GetDllLibPdf().PdfPageSize_ArchC.argtypes=[]
        GetDllLibPdf().PdfPageSize_ArchC.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageSize_ArchC()
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @staticmethod

    def ArchB()->'SizeF':
        """
    <summary>
        ArchB format.
    </summary>
        """
        #GetDllLibPdf().PdfPageSize_ArchB.argtypes=[]
        GetDllLibPdf().PdfPageSize_ArchB.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageSize_ArchB()
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @staticmethod

    def ArchA()->'SizeF':
        """
    <summary>
        ArchA format.
    </summary>
        """
        #GetDllLibPdf().PdfPageSize_ArchA.argtypes=[]
        GetDllLibPdf().PdfPageSize_ArchA.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageSize_ArchA()
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @staticmethod

    def Flsa()->'SizeF':
        """
    <summary>
        The American Foolscap format.
    </summary>
        """
        #GetDllLibPdf().PdfPageSize_Flsa.argtypes=[]
        GetDllLibPdf().PdfPageSize_Flsa.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageSize_Flsa()
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @staticmethod

    def HalfLetter()->'SizeF':
        """
    <summary>
        HalfLetter format.
    </summary>
        """
        #GetDllLibPdf().PdfPageSize_HalfLetter.argtypes=[]
        GetDllLibPdf().PdfPageSize_HalfLetter.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageSize_HalfLetter()
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @staticmethod

    def Letter11x17()->'SizeF':
        """
    <summary>
        11x17 format.
    </summary>
        """
        #GetDllLibPdf().PdfPageSize_Letter11x17.argtypes=[]
        GetDllLibPdf().PdfPageSize_Letter11x17.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageSize_Letter11x17()
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @staticmethod

    def Ledger()->'SizeF':
        """
    <summary>
        Ledger format.
    </summary>
        """
        #GetDllLibPdf().PdfPageSize_Ledger.argtypes=[]
        GetDllLibPdf().PdfPageSize_Ledger.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageSize_Ledger()
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


