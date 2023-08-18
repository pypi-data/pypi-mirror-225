from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfPens (SpireObject) :
    """
    <summary>
        The collection of the default pens.
    </summary>
    """
    @staticmethod

    def get_MediumSeaGreen()->'PdfPen':
        """
    <summary>
        Gets the MediumSeaGreen default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_MediumSeaGreen.argtypes=[]
        GetDllLibPdf().PdfPens_get_MediumSeaGreen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_MediumSeaGreen()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_MediumSlateBlue()->'PdfPen':
        """
    <summary>
        Gets the MediumSlateBlue default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_MediumSlateBlue.argtypes=[]
        GetDllLibPdf().PdfPens_get_MediumSlateBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_MediumSlateBlue()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_MediumSpringGreen()->'PdfPen':
        """
    <summary>
        Gets the MediumSpringGreen default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_MediumSpringGreen.argtypes=[]
        GetDllLibPdf().PdfPens_get_MediumSpringGreen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_MediumSpringGreen()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_MediumTurquoise()->'PdfPen':
        """
    <summary>
        Gets the MediumTurquoise default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_MediumTurquoise.argtypes=[]
        GetDllLibPdf().PdfPens_get_MediumTurquoise.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_MediumTurquoise()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_MediumVioletRed()->'PdfPen':
        """
    <summary>
        Gets the MediumVioletRed default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_MediumVioletRed.argtypes=[]
        GetDllLibPdf().PdfPens_get_MediumVioletRed.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_MediumVioletRed()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_MidnightBlue()->'PdfPen':
        """
    <summary>
        Gets the MidnightBlue default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_MidnightBlue.argtypes=[]
        GetDllLibPdf().PdfPens_get_MidnightBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_MidnightBlue()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_MintCream()->'PdfPen':
        """
    <summary>
        Gets the MintCream default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_MintCream.argtypes=[]
        GetDllLibPdf().PdfPens_get_MintCream.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_MintCream()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_MistyRose()->'PdfPen':
        """
    <summary>
        Gets the MistyRose default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_MistyRose.argtypes=[]
        GetDllLibPdf().PdfPens_get_MistyRose.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_MistyRose()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Moccasin()->'PdfPen':
        """
    <summary>
        Gets the Moccasin default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Moccasin.argtypes=[]
        GetDllLibPdf().PdfPens_get_Moccasin.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Moccasin()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_NavajoWhite()->'PdfPen':
        """
    <summary>
        Gets the NavajoWhite default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_NavajoWhite.argtypes=[]
        GetDllLibPdf().PdfPens_get_NavajoWhite.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_NavajoWhite()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Navy()->'PdfPen':
        """
    <summary>
        Gets the Navy default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Navy.argtypes=[]
        GetDllLibPdf().PdfPens_get_Navy.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Navy()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_OldLace()->'PdfPen':
        """
    <summary>
        Gets the OldLace default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_OldLace.argtypes=[]
        GetDllLibPdf().PdfPens_get_OldLace.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_OldLace()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Olive()->'PdfPen':
        """
    <summary>
        Gets the Olive default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Olive.argtypes=[]
        GetDllLibPdf().PdfPens_get_Olive.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Olive()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_OliveDrab()->'PdfPen':
        """
    <summary>
        Gets the OliveDrab default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_OliveDrab.argtypes=[]
        GetDllLibPdf().PdfPens_get_OliveDrab.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_OliveDrab()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Orange()->'PdfPen':
        """
    <summary>
        Gets the Orange default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Orange.argtypes=[]
        GetDllLibPdf().PdfPens_get_Orange.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Orange()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_OrangeRed()->'PdfPen':
        """
    <summary>
        Gets the OrangeRed default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_OrangeRed.argtypes=[]
        GetDllLibPdf().PdfPens_get_OrangeRed.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_OrangeRed()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Orchid()->'PdfPen':
        """
    <summary>
        Gets the Orchid default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Orchid.argtypes=[]
        GetDllLibPdf().PdfPens_get_Orchid.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Orchid()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_PaleGoldenrod()->'PdfPen':
        """
    <summary>
        Gets the PaleGoldenrod default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_PaleGoldenrod.argtypes=[]
        GetDllLibPdf().PdfPens_get_PaleGoldenrod.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_PaleGoldenrod()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_PaleGreen()->'PdfPen':
        """
    <summary>
        Gets the PaleGreen default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_PaleGreen.argtypes=[]
        GetDllLibPdf().PdfPens_get_PaleGreen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_PaleGreen()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_PaleTurquoise()->'PdfPen':
        """
    <summary>
        Gets the PaleTurquoise default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_PaleTurquoise.argtypes=[]
        GetDllLibPdf().PdfPens_get_PaleTurquoise.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_PaleTurquoise()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_PaleVioletRed()->'PdfPen':
        """
    <summary>
        Gets the PaleVioletRed default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_PaleVioletRed.argtypes=[]
        GetDllLibPdf().PdfPens_get_PaleVioletRed.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_PaleVioletRed()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_PapayaWhip()->'PdfPen':
        """
    <summary>
        Gets the PapayaWhip default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_PapayaWhip.argtypes=[]
        GetDllLibPdf().PdfPens_get_PapayaWhip.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_PapayaWhip()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_PeachPuff()->'PdfPen':
        """
    <summary>
        Gets the PeachPuff default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_PeachPuff.argtypes=[]
        GetDllLibPdf().PdfPens_get_PeachPuff.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_PeachPuff()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Peru()->'PdfPen':
        """
    <summary>
        Gets the Peru default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Peru.argtypes=[]
        GetDllLibPdf().PdfPens_get_Peru.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Peru()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Pink()->'PdfPen':
        """
    <summary>
        Gets the Pink default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Pink.argtypes=[]
        GetDllLibPdf().PdfPens_get_Pink.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Pink()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Plum()->'PdfPen':
        """
    <summary>
        Gets the Plum default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Plum.argtypes=[]
        GetDllLibPdf().PdfPens_get_Plum.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Plum()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_PowderBlue()->'PdfPen':
        """
    <summary>
        Gets the PowderBlue default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_PowderBlue.argtypes=[]
        GetDllLibPdf().PdfPens_get_PowderBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_PowderBlue()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Purple()->'PdfPen':
        """
    <summary>
        Gets the Purple default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Purple.argtypes=[]
        GetDllLibPdf().PdfPens_get_Purple.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Purple()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Red()->'PdfPen':
        """
    <summary>
        Gets the Red default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Red.argtypes=[]
        GetDllLibPdf().PdfPens_get_Red.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Red()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_RosyBrown()->'PdfPen':
        """
    <summary>
        Gets the RosyBrown default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_RosyBrown.argtypes=[]
        GetDllLibPdf().PdfPens_get_RosyBrown.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_RosyBrown()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_RoyalBlue()->'PdfPen':
        """
    <summary>
        Gets the RoyalBlue default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_RoyalBlue.argtypes=[]
        GetDllLibPdf().PdfPens_get_RoyalBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_RoyalBlue()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_SaddleBrown()->'PdfPen':
        """
    <summary>
        Gets the SaddleBrown default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_SaddleBrown.argtypes=[]
        GetDllLibPdf().PdfPens_get_SaddleBrown.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_SaddleBrown()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Salmon()->'PdfPen':
        """
    <summary>
        Gets the Salmon default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Salmon.argtypes=[]
        GetDllLibPdf().PdfPens_get_Salmon.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Salmon()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_SandyBrown()->'PdfPen':
        """
    <summary>
        Gets the SandyBrown default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_SandyBrown.argtypes=[]
        GetDllLibPdf().PdfPens_get_SandyBrown.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_SandyBrown()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_SeaGreen()->'PdfPen':
        """
    <summary>
        Gets the SeaGreen default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_SeaGreen.argtypes=[]
        GetDllLibPdf().PdfPens_get_SeaGreen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_SeaGreen()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_SeaShell()->'PdfPen':
        """
    <summary>
        Gets the SeaShell default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_SeaShell.argtypes=[]
        GetDllLibPdf().PdfPens_get_SeaShell.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_SeaShell()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Sienna()->'PdfPen':
        """
    <summary>
        Gets the Sienna default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Sienna.argtypes=[]
        GetDllLibPdf().PdfPens_get_Sienna.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Sienna()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Silver()->'PdfPen':
        """
    <summary>
        Gets the Silver default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Silver.argtypes=[]
        GetDllLibPdf().PdfPens_get_Silver.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Silver()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_SkyBlue()->'PdfPen':
        """
    <summary>
        Gets the SkyBlue default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_SkyBlue.argtypes=[]
        GetDllLibPdf().PdfPens_get_SkyBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_SkyBlue()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_SlateBlue()->'PdfPen':
        """
    <summary>
        Gets the SlateBlue default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_SlateBlue.argtypes=[]
        GetDllLibPdf().PdfPens_get_SlateBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_SlateBlue()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_SlateGray()->'PdfPen':
        """
    <summary>
        Gets the SlateGray default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_SlateGray.argtypes=[]
        GetDllLibPdf().PdfPens_get_SlateGray.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_SlateGray()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Snow()->'PdfPen':
        """
    <summary>
        Gets the Snow default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Snow.argtypes=[]
        GetDllLibPdf().PdfPens_get_Snow.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Snow()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_SpringGreen()->'PdfPen':
        """
    <summary>
        Gets the SpringGreen default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_SpringGreen.argtypes=[]
        GetDllLibPdf().PdfPens_get_SpringGreen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_SpringGreen()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_SteelBlue()->'PdfPen':
        """
    <summary>
        Gets the SteelBlue default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_SteelBlue.argtypes=[]
        GetDllLibPdf().PdfPens_get_SteelBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_SteelBlue()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Tan()->'PdfPen':
        """
    <summary>
        Gets the Tan default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Tan.argtypes=[]
        GetDllLibPdf().PdfPens_get_Tan.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Tan()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Teal()->'PdfPen':
        """
    <summary>
        Gets the Teal default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Teal.argtypes=[]
        GetDllLibPdf().PdfPens_get_Teal.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Teal()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Thistle()->'PdfPen':
        """
    <summary>
        Gets the Thistle default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Thistle.argtypes=[]
        GetDllLibPdf().PdfPens_get_Thistle.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Thistle()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Tomato()->'PdfPen':
        """
    <summary>
        Gets the Tomato default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Tomato.argtypes=[]
        GetDllLibPdf().PdfPens_get_Tomato.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Tomato()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Transparent()->'PdfPen':
        """
    <summary>
        Gets the Transparent default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Transparent.argtypes=[]
        GetDllLibPdf().PdfPens_get_Transparent.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Transparent()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Turquoise()->'PdfPen':
        """
    <summary>
        Gets the Turquoise default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Turquoise.argtypes=[]
        GetDllLibPdf().PdfPens_get_Turquoise.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Turquoise()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Violet()->'PdfPen':
        """
    <summary>
        Gets the Violet default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Violet.argtypes=[]
        GetDllLibPdf().PdfPens_get_Violet.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Violet()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Wheat()->'PdfPen':
        """
    <summary>
        Gets the Wheat default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Wheat.argtypes=[]
        GetDllLibPdf().PdfPens_get_Wheat.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Wheat()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_White()->'PdfPen':
        """
    <summary>
        Gets the White default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_White.argtypes=[]
        GetDllLibPdf().PdfPens_get_White.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_White()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_WhiteSmoke()->'PdfPen':
        """
    <summary>
        Gets the WhiteSmoke default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_WhiteSmoke.argtypes=[]
        GetDllLibPdf().PdfPens_get_WhiteSmoke.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_WhiteSmoke()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Yellow()->'PdfPen':
        """
    <summary>
        Gets the Yellow default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Yellow.argtypes=[]
        GetDllLibPdf().PdfPens_get_Yellow.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Yellow()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_YellowGreen()->'PdfPen':
        """
    <summary>
        Gets the YellowGreen default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_YellowGreen.argtypes=[]
        GetDllLibPdf().PdfPens_get_YellowGreen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_YellowGreen()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_AliceBlue()->'PdfPen':
        """
    <summary>
        Gets the AliceBlue pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_AliceBlue.argtypes=[]
        GetDllLibPdf().PdfPens_get_AliceBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_AliceBlue()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_AntiqueWhite()->'PdfPen':
        """
    <summary>
        Gets the antique white pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_AntiqueWhite.argtypes=[]
        GetDllLibPdf().PdfPens_get_AntiqueWhite.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_AntiqueWhite()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Aqua()->'PdfPen':
        """
    <summary>
        Gets the Aqua default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Aqua.argtypes=[]
        GetDllLibPdf().PdfPens_get_Aqua.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Aqua()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Aquamarine()->'PdfPen':
        """
    <summary>
        Gets the Aquamarine default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Aquamarine.argtypes=[]
        GetDllLibPdf().PdfPens_get_Aquamarine.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Aquamarine()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Azure()->'PdfPen':
        """
    <summary>
        Gets the Azure default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Azure.argtypes=[]
        GetDllLibPdf().PdfPens_get_Azure.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Azure()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Beige()->'PdfPen':
        """
    <summary>
        Gets the Beige default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Beige.argtypes=[]
        GetDllLibPdf().PdfPens_get_Beige.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Beige()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Bisque()->'PdfPen':
        """
    <summary>
        Gets the Bisque default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Bisque.argtypes=[]
        GetDllLibPdf().PdfPens_get_Bisque.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Bisque()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Black()->'PdfPen':
        """
    <summary>
        Gets the Black default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Black.argtypes=[]
        GetDllLibPdf().PdfPens_get_Black.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Black()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_BlanchedAlmond()->'PdfPen':
        """
    <summary>
        Gets the BlanchedAlmond default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_BlanchedAlmond.argtypes=[]
        GetDllLibPdf().PdfPens_get_BlanchedAlmond.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_BlanchedAlmond()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Blue()->'PdfPen':
        """
    <summary>
        Gets the Blue default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Blue.argtypes=[]
        GetDllLibPdf().PdfPens_get_Blue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Blue()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_BlueViolet()->'PdfPen':
        """
    <summary>
        Gets the BlueViolet default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_BlueViolet.argtypes=[]
        GetDllLibPdf().PdfPens_get_BlueViolet.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_BlueViolet()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Brown()->'PdfPen':
        """
    <summary>
        Gets the Brown default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Brown.argtypes=[]
        GetDllLibPdf().PdfPens_get_Brown.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Brown()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_BurlyWood()->'PdfPen':
        """
    <summary>
        Gets the BurlyWood default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_BurlyWood.argtypes=[]
        GetDllLibPdf().PdfPens_get_BurlyWood.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_BurlyWood()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_CadetBlue()->'PdfPen':
        """
    <summary>
        Gets the CadetBlue default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_CadetBlue.argtypes=[]
        GetDllLibPdf().PdfPens_get_CadetBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_CadetBlue()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Chartreuse()->'PdfPen':
        """
    <summary>
        Gets the Chartreuse default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Chartreuse.argtypes=[]
        GetDllLibPdf().PdfPens_get_Chartreuse.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Chartreuse()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Chocolate()->'PdfPen':
        """
    <summary>
        Gets the Chocolate default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Chocolate.argtypes=[]
        GetDllLibPdf().PdfPens_get_Chocolate.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Chocolate()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Coral()->'PdfPen':
        """
    <summary>
        Gets the Coral default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Coral.argtypes=[]
        GetDllLibPdf().PdfPens_get_Coral.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Coral()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_CornflowerBlue()->'PdfPen':
        """
    <summary>
        Gets the CornflowerBlue default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_CornflowerBlue.argtypes=[]
        GetDllLibPdf().PdfPens_get_CornflowerBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_CornflowerBlue()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Cornsilk()->'PdfPen':
        """
    <summary>
        Gets the Corn silk default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Cornsilk.argtypes=[]
        GetDllLibPdf().PdfPens_get_Cornsilk.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Cornsilk()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Crimson()->'PdfPen':
        """
    <summary>
        Gets the Crimson default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Crimson.argtypes=[]
        GetDllLibPdf().PdfPens_get_Crimson.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Crimson()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Cyan()->'PdfPen':
        """
    <summary>
        Gets the Cyan default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Cyan.argtypes=[]
        GetDllLibPdf().PdfPens_get_Cyan.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Cyan()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_DarkBlue()->'PdfPen':
        """
    <summary>
        Gets the DarkBlue default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_DarkBlue.argtypes=[]
        GetDllLibPdf().PdfPens_get_DarkBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_DarkBlue()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_DarkCyan()->'PdfPen':
        """
    <summary>
        Gets the DarkCyan default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_DarkCyan.argtypes=[]
        GetDllLibPdf().PdfPens_get_DarkCyan.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_DarkCyan()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_DarkGoldenrod()->'PdfPen':
        """
    <summary>
        Gets the DarkGoldenrod default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_DarkGoldenrod.argtypes=[]
        GetDllLibPdf().PdfPens_get_DarkGoldenrod.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_DarkGoldenrod()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_DarkGray()->'PdfPen':
        """
    <summary>
        Gets the DarkGray default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_DarkGray.argtypes=[]
        GetDllLibPdf().PdfPens_get_DarkGray.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_DarkGray()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_DarkGreen()->'PdfPen':
        """
    <summary>
        Gets the DarkGreen default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_DarkGreen.argtypes=[]
        GetDllLibPdf().PdfPens_get_DarkGreen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_DarkGreen()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_DarkKhaki()->'PdfPen':
        """
    <summary>
        Gets the DarkKhaki default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_DarkKhaki.argtypes=[]
        GetDllLibPdf().PdfPens_get_DarkKhaki.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_DarkKhaki()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_DarkMagenta()->'PdfPen':
        """
    <summary>
        Gets the DarkMagenta default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_DarkMagenta.argtypes=[]
        GetDllLibPdf().PdfPens_get_DarkMagenta.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_DarkMagenta()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_DarkOliveGreen()->'PdfPen':
        """
    <summary>
        Gets the DarkOliveGreen default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_DarkOliveGreen.argtypes=[]
        GetDllLibPdf().PdfPens_get_DarkOliveGreen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_DarkOliveGreen()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_DarkOrange()->'PdfPen':
        """
    <summary>
        Gets the DarkOrange default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_DarkOrange.argtypes=[]
        GetDllLibPdf().PdfPens_get_DarkOrange.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_DarkOrange()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_DarkOrchid()->'PdfPen':
        """
    <summary>
        Gets the DarkOrchid default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_DarkOrchid.argtypes=[]
        GetDllLibPdf().PdfPens_get_DarkOrchid.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_DarkOrchid()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_DarkRed()->'PdfPen':
        """
    <summary>
        Gets the DarkRed default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_DarkRed.argtypes=[]
        GetDllLibPdf().PdfPens_get_DarkRed.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_DarkRed()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_DarkSalmon()->'PdfPen':
        """
    <summary>
        Gets the DarkSalmon default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_DarkSalmon.argtypes=[]
        GetDllLibPdf().PdfPens_get_DarkSalmon.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_DarkSalmon()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_DarkSeaGreen()->'PdfPen':
        """
    <summary>
        Gets the DarkSeaGreen default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_DarkSeaGreen.argtypes=[]
        GetDllLibPdf().PdfPens_get_DarkSeaGreen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_DarkSeaGreen()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_DarkSlateBlue()->'PdfPen':
        """
    <summary>
        Gets the DarkSlateBlue default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_DarkSlateBlue.argtypes=[]
        GetDllLibPdf().PdfPens_get_DarkSlateBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_DarkSlateBlue()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_DarkSlateGray()->'PdfPen':
        """
    <summary>
        Gets the DarkSlateGray default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_DarkSlateGray.argtypes=[]
        GetDllLibPdf().PdfPens_get_DarkSlateGray.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_DarkSlateGray()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_DarkTurquoise()->'PdfPen':
        """
    <summary>
        Gets the DarkTurquoise default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_DarkTurquoise.argtypes=[]
        GetDllLibPdf().PdfPens_get_DarkTurquoise.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_DarkTurquoise()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_DarkViolet()->'PdfPen':
        """
    <summary>
        Gets the DarkViolet default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_DarkViolet.argtypes=[]
        GetDllLibPdf().PdfPens_get_DarkViolet.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_DarkViolet()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_DeepPink()->'PdfPen':
        """
    <summary>
        Gets the DeepPink default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_DeepPink.argtypes=[]
        GetDllLibPdf().PdfPens_get_DeepPink.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_DeepPink()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_DeepSkyBlue()->'PdfPen':
        """
    <summary>
        Gets the DeepSkyBlue default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_DeepSkyBlue.argtypes=[]
        GetDllLibPdf().PdfPens_get_DeepSkyBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_DeepSkyBlue()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_DimGray()->'PdfPen':
        """
    <summary>
        Gets the DimGray default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_DimGray.argtypes=[]
        GetDllLibPdf().PdfPens_get_DimGray.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_DimGray()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_DodgerBlue()->'PdfPen':
        """
    <summary>
        Gets the DodgerBlue default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_DodgerBlue.argtypes=[]
        GetDllLibPdf().PdfPens_get_DodgerBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_DodgerBlue()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Firebrick()->'PdfPen':
        """
    <summary>
        Gets the Firebrick default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Firebrick.argtypes=[]
        GetDllLibPdf().PdfPens_get_Firebrick.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Firebrick()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_FloralWhite()->'PdfPen':
        """
    <summary>
        Gets the FloralWhite default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_FloralWhite.argtypes=[]
        GetDllLibPdf().PdfPens_get_FloralWhite.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_FloralWhite()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_ForestGreen()->'PdfPen':
        """
    <summary>
        Gets the ForestGreen default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_ForestGreen.argtypes=[]
        GetDllLibPdf().PdfPens_get_ForestGreen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_ForestGreen()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Fuchsia()->'PdfPen':
        """
    <summary>
        Gets the Fuchsia default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Fuchsia.argtypes=[]
        GetDllLibPdf().PdfPens_get_Fuchsia.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Fuchsia()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Gainsboro()->'PdfPen':
        """
    <summary>
        Gets the Gainsborough default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Gainsboro.argtypes=[]
        GetDllLibPdf().PdfPens_get_Gainsboro.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Gainsboro()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_GhostWhite()->'PdfPen':
        """
    <summary>
        Gets the GhostWhite default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_GhostWhite.argtypes=[]
        GetDllLibPdf().PdfPens_get_GhostWhite.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_GhostWhite()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Gold()->'PdfPen':
        """
    <summary>
        Gets the Gold default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Gold.argtypes=[]
        GetDllLibPdf().PdfPens_get_Gold.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Gold()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Goldenrod()->'PdfPen':
        """
    <summary>
        Gets the Goldenrod default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Goldenrod.argtypes=[]
        GetDllLibPdf().PdfPens_get_Goldenrod.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Goldenrod()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Gray()->'PdfPen':
        """
    <summary>
        Gets the Gray default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Gray.argtypes=[]
        GetDllLibPdf().PdfPens_get_Gray.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Gray()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Green()->'PdfPen':
        """
    <summary>
        Gets the Green default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Green.argtypes=[]
        GetDllLibPdf().PdfPens_get_Green.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Green()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_GreenYellow()->'PdfPen':
        """
    <summary>
        Gets the GreenYellow default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_GreenYellow.argtypes=[]
        GetDllLibPdf().PdfPens_get_GreenYellow.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_GreenYellow()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Honeydew()->'PdfPen':
        """
    <summary>
        Gets the Honeydew default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Honeydew.argtypes=[]
        GetDllLibPdf().PdfPens_get_Honeydew.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Honeydew()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_HotPink()->'PdfPen':
        """
    <summary>
        Gets the HotPink default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_HotPink.argtypes=[]
        GetDllLibPdf().PdfPens_get_HotPink.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_HotPink()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_IndianRed()->'PdfPen':
        """
    <summary>
        Gets the IndianRed default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_IndianRed.argtypes=[]
        GetDllLibPdf().PdfPens_get_IndianRed.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_IndianRed()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Indigo()->'PdfPen':
        """
    <summary>
        Gets the Indigo default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Indigo.argtypes=[]
        GetDllLibPdf().PdfPens_get_Indigo.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Indigo()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Ivory()->'PdfPen':
        """
    <summary>
        Gets the Ivory default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Ivory.argtypes=[]
        GetDllLibPdf().PdfPens_get_Ivory.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Ivory()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Khaki()->'PdfPen':
        """
    <summary>
        Gets the Khaki default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Khaki.argtypes=[]
        GetDllLibPdf().PdfPens_get_Khaki.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Khaki()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Lavender()->'PdfPen':
        """
    <summary>
        Gets the Lavender default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Lavender.argtypes=[]
        GetDllLibPdf().PdfPens_get_Lavender.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Lavender()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_LavenderBlush()->'PdfPen':
        """
    <summary>
        Gets the LavenderBlush default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_LavenderBlush.argtypes=[]
        GetDllLibPdf().PdfPens_get_LavenderBlush.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_LavenderBlush()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_LawnGreen()->'PdfPen':
        """
    <summary>
        Gets the LawnGreen default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_LawnGreen.argtypes=[]
        GetDllLibPdf().PdfPens_get_LawnGreen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_LawnGreen()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_LemonChiffon()->'PdfPen':
        """
    <summary>
        Gets the LemonChiffon default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_LemonChiffon.argtypes=[]
        GetDllLibPdf().PdfPens_get_LemonChiffon.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_LemonChiffon()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_LightBlue()->'PdfPen':
        """
    <summary>
        Gets the LightBlue default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_LightBlue.argtypes=[]
        GetDllLibPdf().PdfPens_get_LightBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_LightBlue()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_LightCoral()->'PdfPen':
        """
    <summary>
        Gets the LightCoral default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_LightCoral.argtypes=[]
        GetDllLibPdf().PdfPens_get_LightCoral.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_LightCoral()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_LightCyan()->'PdfPen':
        """
    <summary>
        Gets the LightCyan default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_LightCyan.argtypes=[]
        GetDllLibPdf().PdfPens_get_LightCyan.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_LightCyan()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_LightGoldenrodYellow()->'PdfPen':
        """
    <summary>
        Gets the LightGoldenrodYellow default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_LightGoldenrodYellow.argtypes=[]
        GetDllLibPdf().PdfPens_get_LightGoldenrodYellow.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_LightGoldenrodYellow()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_LightGray()->'PdfPen':
        """
    <summary>
        Gets the LightGray default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_LightGray.argtypes=[]
        GetDllLibPdf().PdfPens_get_LightGray.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_LightGray()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_LightGreen()->'PdfPen':
        """
    <summary>
        Gets the LightGreen default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_LightGreen.argtypes=[]
        GetDllLibPdf().PdfPens_get_LightGreen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_LightGreen()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_LightPink()->'PdfPen':
        """
    <summary>
        Gets the LightPink default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_LightPink.argtypes=[]
        GetDllLibPdf().PdfPens_get_LightPink.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_LightPink()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_LightSalmon()->'PdfPen':
        """
    <summary>
        Gets the LightSalmon default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_LightSalmon.argtypes=[]
        GetDllLibPdf().PdfPens_get_LightSalmon.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_LightSalmon()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_LightSeaGreen()->'PdfPen':
        """
    <summary>
        Gets the LightSeaGreen default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_LightSeaGreen.argtypes=[]
        GetDllLibPdf().PdfPens_get_LightSeaGreen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_LightSeaGreen()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_LightSkyBlue()->'PdfPen':
        """
    <summary>
        Gets the LightSkyBlue default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_LightSkyBlue.argtypes=[]
        GetDllLibPdf().PdfPens_get_LightSkyBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_LightSkyBlue()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_LightSlateGray()->'PdfPen':
        """
    <summary>
        Gets the LightSlateGray default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_LightSlateGray.argtypes=[]
        GetDllLibPdf().PdfPens_get_LightSlateGray.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_LightSlateGray()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_LightSteelBlue()->'PdfPen':
        """
    <summary>
        Gets the LightSteelBlue default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_LightSteelBlue.argtypes=[]
        GetDllLibPdf().PdfPens_get_LightSteelBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_LightSteelBlue()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_LightYellow()->'PdfPen':
        """
    <summary>
        Gets the LightYellow default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_LightYellow.argtypes=[]
        GetDllLibPdf().PdfPens_get_LightYellow.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_LightYellow()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Lime()->'PdfPen':
        """
    <summary>
        Gets the Lime default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Lime.argtypes=[]
        GetDllLibPdf().PdfPens_get_Lime.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Lime()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_LimeGreen()->'PdfPen':
        """
    <summary>
        Gets the LimeGreen default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_LimeGreen.argtypes=[]
        GetDllLibPdf().PdfPens_get_LimeGreen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_LimeGreen()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Linen()->'PdfPen':
        """
    <summary>
        Gets the Linen default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Linen.argtypes=[]
        GetDllLibPdf().PdfPens_get_Linen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Linen()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Magenta()->'PdfPen':
        """
    <summary>
        Gets the Magenta default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Magenta.argtypes=[]
        GetDllLibPdf().PdfPens_get_Magenta.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Magenta()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_Maroon()->'PdfPen':
        """
    <summary>
        Gets the Maroon default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_Maroon.argtypes=[]
        GetDllLibPdf().PdfPens_get_Maroon.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_Maroon()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_MediumAquamarine()->'PdfPen':
        """
    <summary>
        Gets the MediumAquamarine default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_MediumAquamarine.argtypes=[]
        GetDllLibPdf().PdfPens_get_MediumAquamarine.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_MediumAquamarine()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_MediumBlue()->'PdfPen':
        """
    <summary>
        Gets the MediumBlue default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_MediumBlue.argtypes=[]
        GetDllLibPdf().PdfPens_get_MediumBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_MediumBlue()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_MediumOrchid()->'PdfPen':
        """
    <summary>
        Gets the MediumOrchid default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_MediumOrchid.argtypes=[]
        GetDllLibPdf().PdfPens_get_MediumOrchid.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_MediumOrchid()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @staticmethod

    def get_MediumPurple()->'PdfPen':
        """
    <summary>
        Gets the MediumPurple default pen.
    </summary>
        """
        #GetDllLibPdf().PdfPens_get_MediumPurple.argtypes=[]
        GetDllLibPdf().PdfPens_get_MediumPurple.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPens_get_MediumPurple()
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


