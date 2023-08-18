from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfBrushes (SpireObject) :
    """
    <summary>
        Represents the collection of immutable default brushes.
    </summary>
    """
    @staticmethod

    def get_MediumPurple()->'PdfBrush':
        """
    <summary>
        Gets the MediumPurple default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_MediumPurple.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_MediumPurple.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_MediumPurple()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_MediumSeaGreen()->'PdfBrush':
        """
    <summary>
        Gets the MediumSeaGreen default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_MediumSeaGreen.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_MediumSeaGreen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_MediumSeaGreen()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_MediumSlateBlue()->'PdfBrush':
        """
    <summary>
        Gets the MediumSlateBlue default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_MediumSlateBlue.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_MediumSlateBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_MediumSlateBlue()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_MediumSpringGreen()->'PdfBrush':
        """
    <summary>
        Gets the MediumSpringGreen default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_MediumSpringGreen.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_MediumSpringGreen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_MediumSpringGreen()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_MediumTurquoise()->'PdfBrush':
        """
    <summary>
        Gets the MediumTurquoise default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_MediumTurquoise.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_MediumTurquoise.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_MediumTurquoise()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_MediumVioletRed()->'PdfBrush':
        """
    <summary>
        Gets the MediumVioletRed default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_MediumVioletRed.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_MediumVioletRed.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_MediumVioletRed()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_MidnightBlue()->'PdfBrush':
        """
    <summary>
        Gets the MidnightBlue default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_MidnightBlue.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_MidnightBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_MidnightBlue()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_MintCream()->'PdfBrush':
        """
    <summary>
        Gets the MintCream default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_MintCream.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_MintCream.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_MintCream()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_MistyRose()->'PdfBrush':
        """
    <summary>
        Gets the MistyRose default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_MistyRose.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_MistyRose.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_MistyRose()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Moccasin()->'PdfBrush':
        """
    <summary>
        Gets the Moccasin default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Moccasin.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Moccasin.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Moccasin()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_NavajoWhite()->'PdfBrush':
        """
    <summary>
        Gets the NavajoWhite default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_NavajoWhite.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_NavajoWhite.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_NavajoWhite()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Navy()->'PdfBrush':
        """
    <summary>
        Gets the Navy default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Navy.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Navy.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Navy()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_OldLace()->'PdfBrush':
        """
    <summary>
        Gets the OldLace default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_OldLace.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_OldLace.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_OldLace()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Olive()->'PdfBrush':
        """
    <summary>
        Gets the Olive default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Olive.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Olive.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Olive()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_OliveDrab()->'PdfBrush':
        """
    <summary>
        Gets the OliveDrab default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_OliveDrab.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_OliveDrab.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_OliveDrab()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Orange()->'PdfBrush':
        """
    <summary>
        Gets the Orange default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Orange.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Orange.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Orange()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_OrangeRed()->'PdfBrush':
        """
    <summary>
        Gets the OrangeRed default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_OrangeRed.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_OrangeRed.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_OrangeRed()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Orchid()->'PdfBrush':
        """
    <summary>
        Gets the Orchid default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Orchid.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Orchid.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Orchid()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_PaleGoldenrod()->'PdfBrush':
        """
    <summary>
        Gets the PaleGoldenrod default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_PaleGoldenrod.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_PaleGoldenrod.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_PaleGoldenrod()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_PaleGreen()->'PdfBrush':
        """
    <summary>
        Gets the PaleGreen default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_PaleGreen.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_PaleGreen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_PaleGreen()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_PaleTurquoise()->'PdfBrush':
        """
    <summary>
        Gets the PaleTurquoise default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_PaleTurquoise.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_PaleTurquoise.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_PaleTurquoise()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_PaleVioletRed()->'PdfBrush':
        """
    <summary>
        Gets the PaleVioletRed default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_PaleVioletRed.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_PaleVioletRed.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_PaleVioletRed()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_PapayaWhip()->'PdfBrush':
        """
    <summary>
        Gets the PapayaWhip default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_PapayaWhip.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_PapayaWhip.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_PapayaWhip()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_PeachPuff()->'PdfBrush':
        """
    <summary>
        Gets the PeachPuff default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_PeachPuff.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_PeachPuff.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_PeachPuff()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Peru()->'PdfBrush':
        """
    <summary>
        Gets the Peru default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Peru.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Peru.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Peru()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Pink()->'PdfBrush':
        """
    <summary>
        Gets the Pink default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Pink.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Pink.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Pink()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Plum()->'PdfBrush':
        """
    <summary>
        Gets the Plum default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Plum.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Plum.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Plum()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_PowderBlue()->'PdfBrush':
        """
    <summary>
        Gets the PowderBlue default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_PowderBlue.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_PowderBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_PowderBlue()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Purple()->'PdfBrush':
        """
    <summary>
        Gets the Purple default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Purple.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Purple.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Purple()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Red()->'PdfBrush':
        """
    <summary>
        Gets the Red default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Red.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Red.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Red()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_RosyBrown()->'PdfBrush':
        """
    <summary>
        Gets the RosyBrown default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_RosyBrown.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_RosyBrown.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_RosyBrown()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_RoyalBlue()->'PdfBrush':
        """
    <summary>
        Gets the RoyalBlue default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_RoyalBlue.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_RoyalBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_RoyalBlue()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_SaddleBrown()->'PdfBrush':
        """
    <summary>
        Gets the SaddleBrown default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_SaddleBrown.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_SaddleBrown.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_SaddleBrown()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Salmon()->'PdfBrush':
        """
    <summary>
        Gets the Salmon default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Salmon.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Salmon.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Salmon()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_SandyBrown()->'PdfBrush':
        """
    <summary>
        Gets the SandyBrown default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_SandyBrown.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_SandyBrown.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_SandyBrown()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_SeaGreen()->'PdfBrush':
        """
    <summary>
        Gets the SeaGreen default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_SeaGreen.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_SeaGreen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_SeaGreen()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_SeaShell()->'PdfBrush':
        """
    <summary>
        Gets the SeaShell default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_SeaShell.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_SeaShell.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_SeaShell()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Sienna()->'PdfBrush':
        """
    <summary>
        Gets the Sienna default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Sienna.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Sienna.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Sienna()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Silver()->'PdfBrush':
        """
    <summary>
        Gets the Silver default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Silver.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Silver.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Silver()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_SkyBlue()->'PdfBrush':
        """
    <summary>
        Gets the SkyBlue default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_SkyBlue.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_SkyBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_SkyBlue()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_SlateBlue()->'PdfBrush':
        """
    <summary>
        Gets the SlateBlue default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_SlateBlue.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_SlateBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_SlateBlue()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_SlateGray()->'PdfBrush':
        """
    <summary>
        Gets the SlateGray default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_SlateGray.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_SlateGray.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_SlateGray()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Snow()->'PdfBrush':
        """
    <summary>
        Gets the Snow default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Snow.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Snow.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Snow()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_SpringGreen()->'PdfBrush':
        """
    <summary>
        Gets the SpringGreen default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_SpringGreen.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_SpringGreen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_SpringGreen()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_SteelBlue()->'PdfBrush':
        """
    <summary>
        Gets the SteelBlue default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_SteelBlue.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_SteelBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_SteelBlue()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Tan()->'PdfBrush':
        """
    <summary>
        Gets the Tan default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Tan.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Tan.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Tan()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Teal()->'PdfBrush':
        """
    <summary>
        Gets the Teal default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Teal.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Teal.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Teal()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Thistle()->'PdfBrush':
        """
    <summary>
        Gets the Thistle default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Thistle.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Thistle.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Thistle()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Tomato()->'PdfBrush':
        """
    <summary>
        Gets the Tomato default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Tomato.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Tomato.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Tomato()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Transparent()->'PdfBrush':
        """
    <summary>
        Gets the Transparent default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Transparent.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Transparent.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Transparent()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Turquoise()->'PdfBrush':
        """
    <summary>
        Gets the Turquoise default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Turquoise.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Turquoise.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Turquoise()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Violet()->'PdfBrush':
        """
    <summary>
        Gets the Violet default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Violet.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Violet.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Violet()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Wheat()->'PdfBrush':
        """
    <summary>
        Gets the Wheat default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Wheat.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Wheat.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Wheat()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_White()->'PdfBrush':
        """
    <summary>
        Gets the White default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_White.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_White.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_White()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_WhiteSmoke()->'PdfBrush':
        """
    <summary>
        Gets the WhiteSmoke default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_WhiteSmoke.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_WhiteSmoke.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_WhiteSmoke()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Yellow()->'PdfBrush':
        """
    <summary>
        Gets the Yellow default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Yellow.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Yellow.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Yellow()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_YellowGreen()->'PdfBrush':
        """
    <summary>
        Gets the YellowGreen default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_YellowGreen.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_YellowGreen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_YellowGreen()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_AliceBlue()->'PdfBrush':
        """
    <summary>
        Gets the AliceBlue brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_AliceBlue.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_AliceBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_AliceBlue()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_AntiqueWhite()->'PdfBrush':
        """
    <summary>
        Gets the antique white brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_AntiqueWhite.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_AntiqueWhite.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_AntiqueWhite()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Aqua()->'PdfBrush':
        """
    <summary>
        Gets the Aqua default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Aqua.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Aqua.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Aqua()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Aquamarine()->'PdfBrush':
        """
    <summary>
        Gets the Aquamarine default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Aquamarine.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Aquamarine.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Aquamarine()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Azure()->'PdfBrush':
        """
    <summary>
        Gets the Azure default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Azure.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Azure.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Azure()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Beige()->'PdfBrush':
        """
    <summary>
        Gets the Beige default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Beige.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Beige.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Beige()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Bisque()->'PdfBrush':
        """
    <summary>
        Gets the Bisque default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Bisque.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Bisque.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Bisque()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Black()->'PdfBrush':
        """
    <summary>
        Gets the Black default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Black.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Black.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Black()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_BlanchedAlmond()->'PdfBrush':
        """
    <summary>
        Gets the BlanchedAlmond default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_BlanchedAlmond.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_BlanchedAlmond.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_BlanchedAlmond()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Blue()->'PdfBrush':
        """
    <summary>
        Gets the Blue default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Blue.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Blue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Blue()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_BlueViolet()->'PdfBrush':
        """
    <summary>
        Gets the BlueViolet default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_BlueViolet.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_BlueViolet.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_BlueViolet()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Brown()->'PdfBrush':
        """
    <summary>
        Gets the Brown default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Brown.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Brown.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Brown()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_BurlyWood()->'PdfBrush':
        """
    <summary>
        Gets the BurlyWood default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_BurlyWood.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_BurlyWood.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_BurlyWood()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_CadetBlue()->'PdfBrush':
        """
    <summary>
        Gets the CadetBlue default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_CadetBlue.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_CadetBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_CadetBlue()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Chartreuse()->'PdfBrush':
        """
    <summary>
        Gets the Chartreuse default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Chartreuse.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Chartreuse.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Chartreuse()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Chocolate()->'PdfBrush':
        """
    <summary>
        Gets the Chocolate default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Chocolate.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Chocolate.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Chocolate()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Coral()->'PdfBrush':
        """
    <summary>
        Gets the Coral default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Coral.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Coral.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Coral()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_CornflowerBlue()->'PdfBrush':
        """
    <summary>
        Gets the CornflowerBlue default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_CornflowerBlue.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_CornflowerBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_CornflowerBlue()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Cornsilk()->'PdfBrush':
        """
    <summary>
        Gets the Corn silk default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Cornsilk.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Cornsilk.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Cornsilk()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Crimson()->'PdfBrush':
        """
    <summary>
        Gets the Crimson default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Crimson.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Crimson.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Crimson()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Cyan()->'PdfBrush':
        """
    <summary>
        Gets the Cyan default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Cyan.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Cyan.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Cyan()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_DarkBlue()->'PdfBrush':
        """
    <summary>
        Gets the DarkBlue default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_DarkBlue.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_DarkBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_DarkBlue()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_DarkCyan()->'PdfBrush':
        """
    <summary>
        Gets the DarkCyan default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_DarkCyan.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_DarkCyan.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_DarkCyan()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_DarkGoldenrod()->'PdfBrush':
        """
    <summary>
        Gets the DarkGoldenrod default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_DarkGoldenrod.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_DarkGoldenrod.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_DarkGoldenrod()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_DarkGray()->'PdfBrush':
        """
    <summary>
        Gets the DarkGray default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_DarkGray.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_DarkGray.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_DarkGray()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_DarkGreen()->'PdfBrush':
        """
    <summary>
        Gets the DarkGreen default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_DarkGreen.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_DarkGreen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_DarkGreen()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_DarkKhaki()->'PdfBrush':
        """
    <summary>
        Gets the DarkKhaki default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_DarkKhaki.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_DarkKhaki.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_DarkKhaki()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_DarkMagenta()->'PdfBrush':
        """
    <summary>
        Gets the DarkMagenta default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_DarkMagenta.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_DarkMagenta.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_DarkMagenta()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_DarkOliveGreen()->'PdfBrush':
        """
    <summary>
        Gets the DarkOliveGreen default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_DarkOliveGreen.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_DarkOliveGreen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_DarkOliveGreen()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_DarkOrange()->'PdfBrush':
        """
    <summary>
        Gets the DarkOrange default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_DarkOrange.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_DarkOrange.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_DarkOrange()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_DarkOrchid()->'PdfBrush':
        """
    <summary>
        Gets the DarkOrchid default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_DarkOrchid.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_DarkOrchid.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_DarkOrchid()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_DarkRed()->'PdfBrush':
        """
    <summary>
        Gets the DarkRed default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_DarkRed.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_DarkRed.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_DarkRed()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_DarkSalmon()->'PdfBrush':
        """
    <summary>
        Gets the DarkSalmon default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_DarkSalmon.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_DarkSalmon.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_DarkSalmon()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_DarkSeaGreen()->'PdfBrush':
        """
    <summary>
        Gets the DarkSeaGreen default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_DarkSeaGreen.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_DarkSeaGreen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_DarkSeaGreen()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_DarkSlateBlue()->'PdfBrush':
        """
    <summary>
        Gets the DarkSlateBlue default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_DarkSlateBlue.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_DarkSlateBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_DarkSlateBlue()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_DarkSlateGray()->'PdfBrush':
        """
    <summary>
        Gets the DarkSlateGray default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_DarkSlateGray.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_DarkSlateGray.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_DarkSlateGray()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_DarkTurquoise()->'PdfBrush':
        """
    <summary>
        Gets the DarkTurquoise default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_DarkTurquoise.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_DarkTurquoise.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_DarkTurquoise()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_DarkViolet()->'PdfBrush':
        """
    <summary>
        Gets the DarkViolet default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_DarkViolet.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_DarkViolet.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_DarkViolet()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_DeepPink()->'PdfBrush':
        """
    <summary>
        Gets the DeepPink default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_DeepPink.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_DeepPink.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_DeepPink()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_DeepSkyBlue()->'PdfBrush':
        """
    <summary>
        Gets the DeepSkyBlue default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_DeepSkyBlue.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_DeepSkyBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_DeepSkyBlue()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_DimGray()->'PdfBrush':
        """
    <summary>
        Gets the DimGray default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_DimGray.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_DimGray.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_DimGray()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_DodgerBlue()->'PdfBrush':
        """
    <summary>
        Gets the DodgerBlue default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_DodgerBlue.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_DodgerBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_DodgerBlue()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Firebrick()->'PdfBrush':
        """
    <summary>
        Gets the Firebrick default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Firebrick.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Firebrick.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Firebrick()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_FloralWhite()->'PdfBrush':
        """
    <summary>
        Gets the FloralWhite default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_FloralWhite.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_FloralWhite.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_FloralWhite()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_ForestGreen()->'PdfBrush':
        """
    <summary>
        Gets the ForestGreen default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_ForestGreen.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_ForestGreen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_ForestGreen()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Fuchsia()->'PdfBrush':
        """
    <summary>
        Gets the Fuchsia default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Fuchsia.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Fuchsia.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Fuchsia()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Gainsboro()->'PdfBrush':
        """
    <summary>
        Gets the Gainsborough default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Gainsboro.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Gainsboro.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Gainsboro()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_GhostWhite()->'PdfBrush':
        """
    <summary>
        Gets the GhostWhite default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_GhostWhite.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_GhostWhite.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_GhostWhite()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Gold()->'PdfBrush':
        """
    <summary>
        Gets the Gold default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Gold.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Gold.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Gold()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Goldenrod()->'PdfBrush':
        """
    <summary>
        Gets the Goldenrod default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Goldenrod.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Goldenrod.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Goldenrod()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Gray()->'PdfBrush':
        """
    <summary>
        Gets the Gray default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Gray.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Gray.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Gray()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Green()->'PdfBrush':
        """
    <summary>
        Gets the Green default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Green.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Green.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Green()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_GreenYellow()->'PdfBrush':
        """
    <summary>
        Gets the GreenYellow default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_GreenYellow.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_GreenYellow.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_GreenYellow()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Honeydew()->'PdfBrush':
        """
    <summary>
        Gets the Honeydew default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Honeydew.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Honeydew.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Honeydew()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_HotPink()->'PdfBrush':
        """
    <summary>
        Gets the HotPink default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_HotPink.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_HotPink.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_HotPink()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_IndianRed()->'PdfBrush':
        """
    <summary>
        Gets the IndianRed default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_IndianRed.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_IndianRed.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_IndianRed()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Indigo()->'PdfBrush':
        """
    <summary>
        Gets the Indigo default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Indigo.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Indigo.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Indigo()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Ivory()->'PdfBrush':
        """
    <summary>
        Gets the Ivory default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Ivory.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Ivory.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Ivory()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Khaki()->'PdfBrush':
        """
    <summary>
        Gets the Khaki default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Khaki.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Khaki.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Khaki()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Lavender()->'PdfBrush':
        """
    <summary>
        Gets the Lavender default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Lavender.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Lavender.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Lavender()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_LavenderBlush()->'PdfBrush':
        """
    <summary>
        Gets the LavenderBlush default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_LavenderBlush.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_LavenderBlush.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_LavenderBlush()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_LawnGreen()->'PdfBrush':
        """
    <summary>
        Gets the LawnGreen default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_LawnGreen.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_LawnGreen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_LawnGreen()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_LemonChiffon()->'PdfBrush':
        """
    <summary>
        Gets the LemonChiffon default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_LemonChiffon.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_LemonChiffon.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_LemonChiffon()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_LightBlue()->'PdfBrush':
        """
    <summary>
        Gets the LightBlue default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_LightBlue.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_LightBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_LightBlue()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_LightCoral()->'PdfBrush':
        """
    <summary>
        Gets the LightCoral default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_LightCoral.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_LightCoral.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_LightCoral()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_LightCyan()->'PdfBrush':
        """
    <summary>
        Gets the LightCyan default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_LightCyan.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_LightCyan.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_LightCyan()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_LightGoldenrodYellow()->'PdfBrush':
        """
    <summary>
        Gets the LightGoldenrodYellow default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_LightGoldenrodYellow.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_LightGoldenrodYellow.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_LightGoldenrodYellow()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_LightGray()->'PdfBrush':
        """
    <summary>
        Gets the LightGray default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_LightGray.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_LightGray.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_LightGray()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_LightGreen()->'PdfBrush':
        """
    <summary>
        Gets the LightGreen default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_LightGreen.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_LightGreen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_LightGreen()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_LightPink()->'PdfBrush':
        """
    <summary>
        Gets the LightPink default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_LightPink.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_LightPink.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_LightPink()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_LightSalmon()->'PdfBrush':
        """
    <summary>
        Gets the LightSalmon default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_LightSalmon.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_LightSalmon.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_LightSalmon()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_LightSeaGreen()->'PdfBrush':
        """
    <summary>
        Gets the LightSeaGreen default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_LightSeaGreen.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_LightSeaGreen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_LightSeaGreen()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_LightSkyBlue()->'PdfBrush':
        """
    <summary>
        Gets the LightSkyBlue default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_LightSkyBlue.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_LightSkyBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_LightSkyBlue()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_LightSlateGray()->'PdfBrush':
        """
    <summary>
        Gets the LightSlateGray default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_LightSlateGray.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_LightSlateGray.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_LightSlateGray()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_LightSteelBlue()->'PdfBrush':
        """
    <summary>
        Gets the LightSteelBlue default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_LightSteelBlue.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_LightSteelBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_LightSteelBlue()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_LightYellow()->'PdfBrush':
        """
    <summary>
        Gets the LightYellow default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_LightYellow.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_LightYellow.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_LightYellow()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Lime()->'PdfBrush':
        """
    <summary>
        Gets the Lime default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Lime.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Lime.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Lime()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_LimeGreen()->'PdfBrush':
        """
    <summary>
        Gets the LimeGreen default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_LimeGreen.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_LimeGreen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_LimeGreen()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Linen()->'PdfBrush':
        """
    <summary>
        Gets the Linen default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Linen.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Linen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Linen()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Magenta()->'PdfBrush':
        """
    <summary>
        Gets the Magenta default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Magenta.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Magenta.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Magenta()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_Maroon()->'PdfBrush':
        """
    <summary>
        Gets the Maroon default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_Maroon.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_Maroon.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_Maroon()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_MediumAquamarine()->'PdfBrush':
        """
    <summary>
        Gets the MediumAquamarine default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_MediumAquamarine.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_MediumAquamarine.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_MediumAquamarine()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_MediumBlue()->'PdfBrush':
        """
    <summary>
        Gets the MediumBlue default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_MediumBlue.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_MediumBlue.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_MediumBlue()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @staticmethod

    def get_MediumOrchid()->'PdfBrush':
        """
    <summary>
        Gets the MediumOrchid default brush.
    </summary>
        """
        #GetDllLibPdf().PdfBrushes_get_MediumOrchid.argtypes=[]
        GetDllLibPdf().PdfBrushes_get_MediumOrchid.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrushes_get_MediumOrchid()
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


