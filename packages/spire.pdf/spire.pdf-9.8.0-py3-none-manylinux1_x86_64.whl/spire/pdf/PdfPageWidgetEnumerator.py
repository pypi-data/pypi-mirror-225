from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfPageWidgetEnumerator (  IEnumerator) :
    """
    <summary>
        Implements enumerator to the loaded page collection.
    </summary>
    """
    @property

    def Current(self)->'SpireObject':
        """
    <summary>
        Gets the current element in the collection.
    </summary>
<value></value>
    <returns>The current element in the collection.</returns>
<exception cref="T:System.InvalidOperationException">
            The enumerator is positioned before the first element of the collection
            or after the last element. </exception>
        """
        GetDllLibPdf().PdfPageWidgetEnumerator_get_Current.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageWidgetEnumerator_get_Current.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPageWidgetEnumerator_get_Current(self.Ptr)
        ret = None if intPtr==None else SpireObject(intPtr)
        return ret


    def MoveNext(self)->bool:
        """
    <summary>
        Advances the enumerator to the next element of the collection.
    </summary>
    <returns>
            true if the enumerator was successfully advanced to the next element;
            false if the enumerator has passed the end of the collection.
            </returns>
<exception cref="T:System.InvalidOperationException">
            The collection was modified after the enumerator was created. </exception>
        """
        GetDllLibPdf().PdfPageWidgetEnumerator_MoveNext.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageWidgetEnumerator_MoveNext.restype=c_bool
        ret = GetDllLibPdf().PdfPageWidgetEnumerator_MoveNext(self.Ptr)
        return ret

    def Reset(self):
        """
    <summary>
        Sets the enumerator to its initial position,
            which is before the first element in the collection.
    </summary>
<exception cref="T:System.InvalidOperationException">
            The collection was modified after the enumerator was created. </exception>
        """
        GetDllLibPdf().PdfPageWidgetEnumerator_Reset.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageWidgetEnumerator_Reset(self.Ptr)

