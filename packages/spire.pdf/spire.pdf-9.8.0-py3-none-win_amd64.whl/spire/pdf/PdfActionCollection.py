from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfActionCollection (  PdfCollection) :
    """
    <summary>
        Represents collection of actions.
    </summary>
    """

    def Add(self ,action:'PdfAction')->int:
        """
    <summary>
        Adds the specified action.
    </summary>
    <param name="action">The action.</param>
    <returns>action</returns>
        """
        intPtraction:c_void_p = action.Ptr

        GetDllLibPdf().PdfActionCollection_Add.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfActionCollection_Add.restype=c_int
        ret = GetDllLibPdf().PdfActionCollection_Add(self.Ptr, intPtraction)
        return ret


    def Insert(self ,index:int,action:'PdfAction'):
        """
    <summary>
        Inserts the action at the specified position.
    </summary>
    <param name="index">The index.</param>
    <param name="action">The action.</param>
        """
        intPtraction:c_void_p = action.Ptr

        GetDllLibPdf().PdfActionCollection_Insert.argtypes=[c_void_p ,c_int,c_void_p]
        GetDllLibPdf().PdfActionCollection_Insert(self.Ptr, index,intPtraction)


    def IndexOf(self ,action:'PdfAction')->int:
        """
    <summary>
        Gets the index of the action.
    </summary>
    <param name="action">The action.</param>
    <returns>action</returns>
        """
        intPtraction:c_void_p = action.Ptr

        GetDllLibPdf().PdfActionCollection_IndexOf.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfActionCollection_IndexOf.restype=c_int
        ret = GetDllLibPdf().PdfActionCollection_IndexOf(self.Ptr, intPtraction)
        return ret


    def Contains(self ,action:'PdfAction')->bool:
        """
    <summary>
        Determines whether the action is contained within collection.
    </summary>
    <param name="action">The action.</param>
    <returns>
            Value, indicating the presents of the action in collection.
            </returns>
        """
        intPtraction:c_void_p = action.Ptr

        GetDllLibPdf().PdfActionCollection_Contains.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfActionCollection_Contains.restype=c_bool
        ret = GetDllLibPdf().PdfActionCollection_Contains(self.Ptr, intPtraction)
        return ret

    def Clear(self):
        """
    <summary>
        Clears this collection.
    </summary>
        """
        GetDllLibPdf().PdfActionCollection_Clear.argtypes=[c_void_p]
        GetDllLibPdf().PdfActionCollection_Clear(self.Ptr)


    def Remove(self ,action:'PdfAction'):
        """
    <summary>
        Removes the specified action.
    </summary>
    <param name="action">The action.</param>
        """
        intPtraction:c_void_p = action.Ptr

        GetDllLibPdf().PdfActionCollection_Remove.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfActionCollection_Remove(self.Ptr, intPtraction)


    def RemoveAt(self ,index:int):
        """
    <summary>
        Removes the action at the specified position.
    </summary>
    <param name="index">The index.</param>
        """
        
        GetDllLibPdf().PdfActionCollection_RemoveAt.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfActionCollection_RemoveAt(self.Ptr, index)

