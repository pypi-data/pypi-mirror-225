from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class ZipWriter (  Stream) :
    """
    <summary>
        ZipWriter defines an abstract class to write entries into a ZIP file.
            To add a file, first call AddEntry with the relative path, then
            write the content of the file into the stream.
    </summary>
    """

    def AddEntry(self ,relativePath:str):
        """
    <summary>
        Adds an entry to the ZIP file (only writes the header, to write
            the content use Stream methods).
    </summary>
    <param name="relativePath">The relative path of the entry in the ZIP
            file.</param>
        """
        
        GetDllLibPdf().ZipWriter_AddEntry.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().ZipWriter_AddEntry(self.Ptr, relativePath)

