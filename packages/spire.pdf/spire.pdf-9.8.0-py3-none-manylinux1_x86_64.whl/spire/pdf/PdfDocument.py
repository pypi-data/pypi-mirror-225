from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfDocument (SpireObject) :
    """

    """
    @dispatch
    def __init__(self):
        GetDllLibPdf().PdfDocument_Create.restype = c_void_p
        intPtr = GetDllLibPdf().PdfDocument_Create()
        super(PdfDocument, self).__init__(intPtr)
    @dispatch
    def __init__(self, filename:str):
        GetDllLibPdf().PdfDocument_CreatePdfDocumentF.argtypes=[c_wchar_p]
        GetDllLibPdf().PdfDocument_CreatePdfDocumentF.restype = c_void_p
        intPtr = GetDllLibPdf().PdfDocument_CreatePdfDocumentF(filename)
        super(PdfDocument, self).__init__(intPtr)
    @dispatch
    def __init__(self, filename:str, password:str):
        GetDllLibPdf().PdfDocument_CreatePdfDocumentFP.argtypes=[c_wchar_p,c_wchar_p]
        GetDllLibPdf().PdfDocument_CreatePdfDocumentFP.restype = c_void_p
        intPtr = GetDllLibPdf().PdfDocument_CreatePdfDocumentFP(filename,password)
        super(PdfDocument, self).__init__(intPtr)
    @dispatch
    def __init__(self, stream:Stream):
        intPtrstream:c_void_p = stream.Ptr
        GetDllLibPdf().PdfDocument_CreatePdfDocumentS.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_CreatePdfDocumentS.restype = c_void_p
        intPtr = GetDllLibPdf().PdfDocument_CreatePdfDocumentS(intPtrstream)
        super(PdfDocument, self).__init__(intPtr)
    @dispatch
    def __init__(self, stream:Stream, password:str):
        intPtrstream:c_void_p = stream.Ptr
        GetDllLibPdf().PdfDocument_CreatePdfDocumentSP.argtypes=[c_void_p,c_wchar_p]
        GetDllLibPdf().PdfDocument_CreatePdfDocumentSP.restype = c_void_p
        intPtr = GetDllLibPdf().PdfDocument_CreatePdfDocumentSP(intPtrstream,password)
        super(PdfDocument, self).__init__(intPtr)
    def __del__(self):
        GetDllLibPdf().PdfDocument_Dispose.argtypes = [c_void_p]
        GetDllLibPdf().PdfDocument_Dispose(self.Ptr)
        super(PdfDocument, self).__del__()
#    @dispatch
#
#    def LoadFromBytes(self ,bytes:'Byte[]',password:str):
#        """
#    <summary>
#        Initializes a new instance of the  class.
#    </summary>
#    <param name="bytes">The byte array with the file content.</param>
#    <param name="password">The password (user or owner) of the encrypted document.</param>
#        """
#        #arraybytes:ArrayTypebytes = ""
#        countbytes = len(bytes)
#        ArrayTypebytes = c_void_p * countbytes
#        arraybytes = ArrayTypebytes()
#        for i in range(0, countbytes):
#            arraybytes[i] = bytes[i].Ptr
#
#
#        GetDllLibPdf().PdfDocument_LoadFromBytes.argtypes=[c_void_p ,ArrayTypebytes,c_wchar_p]
#        GetDllLibPdf().PdfDocument_LoadFromBytes(self.Ptr, arraybytes,password)


    @dispatch

    def LoadFromStream(self ,stream:Stream,password:str):
        """
    <summary>
        Initializes a new instance.
    </summary>
    <param name="stream">The stream with the file.</param>
    <param name="password">The password (user or owner) of the encrypted document.</param>
        """
        intPtrstream:c_void_p = stream.Ptr

        GetDllLibPdf().PdfDocument_LoadFromStreamSP.argtypes=[c_void_p ,c_void_p,c_wchar_p]
        GetDllLibPdf().PdfDocument_LoadFromStreamSP(self.Ptr, intPtrstream,password)

    @dispatch

    def CreateBooklet(self ,fileName:str,width:float,height:float,bothSides:bool):
        """
    <summary>
        Thie method creates a booklet
    </summary>
    <param name="fileName">The loaded document filename.</param>
    <param name="width">The page width</param>
    <param name="height">The page height</param>
    <param name="bothSides">if set to <c>true</c> if the result in document should be printed</param>
        """
        
        GetDllLibPdf().PdfDocument_CreateBooklet.argtypes=[c_void_p ,c_wchar_p,c_float,c_float,c_bool]
        GetDllLibPdf().PdfDocument_CreateBooklet(self.Ptr, fileName,width,height,bothSides)

    @dispatch

    #def CreateBooklet(self ,fileName:str,width:float,height:float,bothSides:bool,beginDrawPage:DrawPageInBookletEventHandler,endDrawPage:DrawPageInBookletEventHandler):
    #    """
    #<summary>
    #    Thie method creates a booklet
    #</summary>
    #<param name="fileName">The loaded document filename.</param>
    #<param name="width">The page width</param>
    #<param name="height">The page height</param>
    #<param name="bothSides">if set to <c>true</c> if the result in document should be printed</param>
    #<param name="beginDrawPage">Delegate for handling event when the begin drawing page in a booklet.</param>
    #<param name="endDrawPage">Delegate for handling event when the end drawing page in a booklet.</param>
    #    """
    #    intPtrbeginDrawPage:c_void_p = beginDrawPage.Ptr
    #    intPtrendDrawPage:c_void_p = endDrawPage.Ptr

    #    GetDllLibPdf().PdfDocument_CreateBookletFWHBBE.argtypes=[c_void_p ,c_wchar_p,c_float,c_float,c_bool,c_void_p,c_void_p]
    #    GetDllLibPdf().PdfDocument_CreateBookletFWHBBE(self.Ptr, fileName,width,height,bothSides,intPtrbeginDrawPage,intPtrendDrawPage)


    def VerifySignature(self ,signName:str)->bool:
        """
    <summary>
        Verify pdf document regarding signature.
    </summary>
    <param name="signName">Signature field name.</param>
    <returns>Signature is validated return true,otherwise false</returns>
        """
        
        GetDllLibPdf().PdfDocument_VerifySignature.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfDocument_VerifySignature.restype=c_bool
        ret = GetDllLibPdf().PdfDocument_VerifySignature(self.Ptr, signName)
        return ret

#
#    def GetSignatureContent(self ,signName:str)->List['Byte']:
#        """
#    <summary>
#        Get pdf document regarding signature.
#    </summary>
#    <param name="signName">Signature field name.</param>
#        """
#        
#        GetDllLibPdf().PdfDocument_GetSignatureContent.argtypes=[c_void_p ,c_wchar_p]
#        GetDllLibPdf().PdfDocument_GetSignatureContent.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().PdfDocument_GetSignatureContent(self.Ptr, signName)
#        ret = GetObjVectorFromArray(intPtrArray, Byte)
#        return ret


    @staticmethod

    def IsPasswordProtected(fileName:str)->bool:
        """
    <summary>
        Whether the file is password protected.
    </summary>
    <param name="fileName">The file name</param>
    <returns>if password protected,return true,or false</returns>
        """
        
        GetDllLibPdf().PdfDocument_IsPasswordProtected.argtypes=[ c_wchar_p]
        GetDllLibPdf().PdfDocument_IsPasswordProtected.restype=c_bool
        ret = GetDllLibPdf().PdfDocument_IsPasswordProtected( fileName)
        return ret

    def HasExtendedRight(self)->bool:
        """
    <summary>
        Indicates whthere contains extended right.
    </summary>
        """
        GetDllLibPdf().PdfDocument_HasExtendedRight.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_HasExtendedRight.restype=c_bool
        ret = GetDllLibPdf().PdfDocument_HasExtendedRight(self.Ptr)
        return ret

    def RemoveExtendedRight(self):
        """
    <summary>
        Removes the extended right.
    </summary>
        """
        GetDllLibPdf().PdfDocument_RemoveExtendedRight.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_RemoveExtendedRight(self.Ptr)

    @dispatch

    def SaveToStream(self ,stream:Stream):
        """
    <summary>
        Save the document to the specified stream.
    </summary>
    <param name="stream">
            The stream which default saved to the FileFormat.PDF format.
    </param>
        """
        intPtrstream:c_void_p = stream.Ptr

        GetDllLibPdf().PdfDocument_SaveToStream.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfDocument_SaveToStream(self.Ptr, intPtrstream)

#    @dispatch
#
#    def SaveToStream(self ,fileformat:FileFormat)->List[Stream]:
#        """
#    <summary>
#        Convert the document to streams with the file format.
#    </summary>
#    <param name="fileformat">The file format.</param>
#    <returns>
#            The format file streams.
#            FileFormat.PDF:return only one stream(PDF support paging).
#            FileFormat.XPS:return only one stream(XPS support paging).
#            FileFormat.DOC:return only one stream(DOC support paging).
#            FileFormat.DOCX:return only one stream(DOCX support paging).
#            FileFormat.XLSX:return only one stream(XLSX support paging).
#            FileFormat.PCL:return only one stream(PCL support paging).
#            FileFormat.POSTSCRIPT:return only one stream(POSTSCRIPT support paging).
#            FileFormat.HTML:return only one stream(HTML support paging).
#            FileFormat.SVG:return multiple streams(SVG not support paging,one stream to one page).
#            </returns>
#        """
#        enumfileformat:c_int = fileformat.value
#
#        GetDllLibPdf().PdfDocument_SaveToStreamF.argtypes=[c_void_p ,c_int]
#        GetDllLibPdf().PdfDocument_SaveToStreamF.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().PdfDocument_SaveToStreamF(self.Ptr, enumfileformat)
#        ret = GetObjVectorFromArray(intPtrArray, Stream)
#        return ret


#    @dispatch
#
#    def SaveToStream(self ,startIndex:int,endIndex:int,fileformat:FileFormat)->List[Stream]:
#        """
#    <summary>
#        Convert the document to streams with the file format.
#    </summary>
#    <param name="startIndex">The start index.</param>
#    <param name="endIndex">The end index.</param>
#    <param name="fileformat">The file format.</param>
#    <returns>
#            The format file streams.
#            FileFormat.PDF:return only one stream(PDF support paging).
#            FileFormat.XPS:return only one stream(XPS support paging).
#            FileFormat.DOC:return only one stream(DOC support paging).
#            FileFormat.DOCX:return only one stream(DOCX support paging).
#            FileFormat.XLSX:return only one stream(XLSX support paging).
#            FileFormat.PCL:return only one stream(PCL support paging).
#            FileFormat.POSTSCRIPT:return only one stream(POSTSCRIPT support paging).
#            FileFormat.HTML:return only one stream(HTML support paging).
#            FileFormat.SVG:return multiple streams(SVG not support paging,one stream to one page).
#            </returns>
#        """
#        enumfileformat:c_int = fileformat.value
#
#        GetDllLibPdf().PdfDocument_SaveToStreamSEF.argtypes=[c_void_p ,c_int,c_int,c_int]
#        GetDllLibPdf().PdfDocument_SaveToStreamSEF.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().PdfDocument_SaveToStreamSEF(self.Ptr, startIndex,endIndex,enumfileformat)
#        ret = GetObjVectorFromArray(intPtrArray, Stream)
#        return ret


    @dispatch

    def SaveToStream(self ,stream:Stream,fileformat:FileFormat):
        """
    <summary>
        Convert the document to an stream with the file format.
    </summary>
    <param name="stream">
            The stream with the file format.
    </param>
    <param name="fileformat">
            The file format.
            FileFormat.SVG is not supported, because SVG file has no paging,so can't be saved to a stream.
    </param>
        """
        intPtrstream:c_void_p = stream.Ptr
        enumfileformat:c_int = fileformat.value

        GetDllLibPdf().PdfDocument_SaveToStreamSF.argtypes=[c_void_p ,c_void_p,c_int]
        GetDllLibPdf().PdfDocument_SaveToStreamSF(self.Ptr, intPtrstream,enumfileformat)

    @dispatch

    def SaveToFile(self ,filename:str):
        """
    <summary>
        Saves PDF document to file.
    </summary>
    <param name="filename">A relative or absolute path for the file</param>
        """
        
        GetDllLibPdf().PdfDocument_SaveToFile.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfDocument_SaveToFile(self.Ptr, filename)

    @dispatch

    def SaveToFile(self ,filename:str,fileFormat:FileFormat):
        """
    <summary>
        Saves PDF document to file.
    </summary>
    <param name="filename">A relative or absolute path for the file</param>
    <param name="fileFormat">File format for the file</param>
        """
        enumfileFormat:c_int = fileFormat.value

        GetDllLibPdf().PdfDocument_SaveToFileFF.argtypes=[c_void_p ,c_wchar_p,c_int]
        GetDllLibPdf().PdfDocument_SaveToFileFF(self.Ptr, filename,enumfileFormat)

    @dispatch

    def SaveToFile(self ,filename:str,startIndex:int,endIndex:int,fileFormat:FileFormat):
        """
    <summary>
        Saves PDF document to PDF or other Format files.
            Current only supports save PDF document to SVG and PDF
    </summary>
    <param name="filename">A relative or absolute path for the file</param>
    <param name="startIndex">The start page index.The index starts at 0</param>
    <param name="endIndex">The end page index.</param>
    <param name="fileFormat">File format for the file</param>
        """
        enumfileFormat:c_int = fileFormat.value

        GetDllLibPdf().PdfDocument_SaveToFileFSEF.argtypes=[c_void_p ,c_wchar_p,c_int,c_int,c_int]
        GetDllLibPdf().PdfDocument_SaveToFileFSEF(self.Ptr, filename,startIndex,endIndex,enumfileFormat)

    @dispatch

    def SaveAsImage(self ,pageIndex:int)->Stream:
        """
    <summary>
        Saves PDF document page as image
    </summary>
    <param name="pageIndex">Page with page index to save as image</param>
    <returns>Returns  page as Image</returns>
        """
        
        GetDllLibPdf().PdfDocument_SaveAsImage.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfDocument_SaveAsImage.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_SaveAsImage(self.Ptr, pageIndex)
        ret = None if intPtr==None else Stream(intPtr)
        return ret


    #@dispatch

    #def SaveAsImage(self ,pageIndex:int,dpiX:int,dpiY:int)->Image:
    #    """
    #<summary>
    #    Saves PDF document page as image,Set image Dpi
    #</summary>
    #<param name="pageIndex">Page with page index to save as image</param>
    #<param name="dpiX">Pictures X resolution</param>
    #<param name="dpiY">Pictures Y resolution</param>
    #<returns>Returns  page as Image</returns>
    #    """
        
    #    GetDllLibPdf().PdfDocument_SaveAsImagePDD.argtypes=[c_void_p ,c_int,c_int,c_int]
    #    GetDllLibPdf().PdfDocument_SaveAsImagePDD.restype=c_void_p
    #    intPtr = GetDllLibPdf().PdfDocument_SaveAsImagePDD(self.Ptr, pageIndex,dpiX,dpiY)
    #    ret = None if intPtr==None else Image(intPtr)
    #    return ret


    #@dispatch

    #def SaveAsImage(self ,pageIndex:int,type:PdfImageType,dpiX:int,dpiY:int)->Image:
    #    """
    #<summary>
    #    Saves PDF document page as image,Set PdfImageType and image Dpi
    #</summary>
    #<param name="pageIndex">Page index</param>
    #<param name="type">PdfImageType type </param>
    #<param name="dpiX">
    #        X resolution
    #</param>
    #<param name="dpiY">
    #        Y resolution
    #</param>
    #<returns>Returns  page as Image</returns>
    #    """
    #    enumtype:c_int = type.value

    #    GetDllLibPdf().PdfDocument_SaveAsImagePTDD.argtypes=[c_void_p ,c_int,c_int,c_int,c_int]
    #    GetDllLibPdf().PdfDocument_SaveAsImagePTDD.restype=c_void_p
    #    intPtr = GetDllLibPdf().PdfDocument_SaveAsImagePTDD(self.Ptr, pageIndex,enumtype,dpiX,dpiY)
    #    ret = None if intPtr==None else Image(intPtr)
    #    return ret


    @dispatch

    def SaveAsImage(self ,pageIndex:int,type:PdfImageType)->Stream:
        """
    <summary>
        Saves PDF document page as image
    </summary>
    <param name="pageIndex">Page index</param>
    <param name="type">PdfImageType type </param>
    <returns>Returns  page as Image</returns>
        """
        enumtype:c_int = type.value

        GetDllLibPdf().PdfDocument_SaveAsImagePT.argtypes=[c_void_p ,c_int,c_int]
        GetDllLibPdf().PdfDocument_SaveAsImagePT.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_SaveAsImagePT(self.Ptr, pageIndex,enumtype)
        ret = None if intPtr==None else Stream(intPtr)
        return ret



    def Clone(self)->'SpireObject':
        """
    <summary>
        Creates a new object that is a copy of the current instance.
    </summary>
<value>A new object that is a copy of this instance.</value>
<remarks>The resulting clone must be of the same type as or a compatible type to the original instance.</remarks>
        """
        GetDllLibPdf().PdfDocument_Clone.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_Clone.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_Clone(self.Ptr)
        ret = None if intPtr==None else SpireObject(intPtr)
        return ret


    @dispatch

    def AppendPage(self ,PdfDocument):
        """
    <summary>
        Appends the specified loaded document to this one.
    </summary>
    <param name="doc">The loaded document.</param>
        """
        intPtrdoc:c_void_p = PdfDocument.Ptr

        GetDllLibPdf().PdfDocument_AppendPage.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfDocument_AppendPage(self.Ptr, intPtrdoc)

    @dispatch

    def AppendPage(self)->PdfPageBase:
        """
    <summary>
        Appends a new page to this one.
    </summary>
    <returns>The new page.</returns>
        """
        GetDllLibPdf().PdfDocument_AppendPage1.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_AppendPage1.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_AppendPage1(self.Ptr)
        ret = None if intPtr==None else PdfPageBase(intPtr)
        return ret


    @dispatch

    def InsertPage(self ,PdfDocument,page:PdfPageBase)->PdfPageBase:
        """
    <summary>
        Imports a page.
    </summary>
    <param name="ldDoc">The loaded document.</param>
    <param name="page">The page.</param>
    <returns>The page in the result document.</returns>
        """
        intPtrldDoc:c_void_p = PdfDocument.Ptr
        intPtrpage:c_void_p = page.Ptr

        GetDllLibPdf().PdfDocument_InsertPage.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().PdfDocument_InsertPage.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_InsertPage(self.Ptr, intPtrldDoc,intPtrpage)
        ret = None if intPtr==None else PdfPageBase(intPtr)
        return ret


    @dispatch

    def InsertPage(self ,PdfDocument,pageIndex:int)->PdfPageBase:
        """
    <summary>
        Imports a page.
    </summary>
    <param name="ldDoc">The loaded document.</param>
    <param name="pageIndex">Index of the page.</param>
    <returns>The page in the result document.</returns>
        """
        intPtrldDoc:c_void_p = PdfDocument.Ptr

        GetDllLibPdf().PdfDocument_InsertPageLP.argtypes=[c_void_p ,c_void_p,c_int]
        GetDllLibPdf().PdfDocument_InsertPageLP.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_InsertPageLP(self.Ptr, intPtrldDoc,pageIndex)
        ret = None if intPtr==None else PdfPageBase(intPtr)
        return ret


    @dispatch

    def InsertPage(self ,PdfDocument,pageIndex:int,resultPageIndex:int)->PdfPageBase:
        """
    <summary>
        Imports a page.
    </summary>
    <param name="ldDoc">The loaded document.</param>
    <param name="pageIndex">Index of the page.</param>
    <param name="resultPageIndex">The page index in the result document.</param>
    <returns>The page in the result document.</returns>
        """
        intPtrldDoc:c_void_p = PdfDocument.Ptr

        GetDllLibPdf().PdfDocument_InsertPageLPR.argtypes=[c_void_p ,c_void_p,c_int,c_int]
        GetDllLibPdf().PdfDocument_InsertPageLPR.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_InsertPageLPR(self.Ptr, intPtrldDoc,pageIndex,resultPageIndex)
        ret = None if intPtr==None else PdfPageBase(intPtr)
        return ret



    def InsertPageRange(self ,PdfDocument,startIndex:int,endIndex:int)->PdfPageBase:
        """
    <summary>
        Imports a page range from a loaded document.
    </summary>
    <param name="ldDoc">The loaded document.</param>
    <param name="startIndex">The start page index.</param>
    <param name="endIndex">The end page index.</param>
    <returns>The last created page in the result document.</returns>
        """
        intPtrldDoc:c_void_p = PdfDocument.Ptr

        GetDllLibPdf().PdfDocument_InsertPageRange.argtypes=[c_void_p ,c_void_p,c_int,c_int]
        GetDllLibPdf().PdfDocument_InsertPageRange.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_InsertPageRange(self.Ptr, intPtrldDoc,startIndex,endIndex)
        ret = None if intPtr==None else PdfPageBase(intPtr)
        return ret


    @staticmethod

    def Merge(dest:PdfDocumentBase,sourceDocuments:List['SpireObject'])->PdfDocumentBase:
        """
    <summary>
        Merges the specified source documents and return destination document.
            ***It is recommended to use method "MergeFiles(string[] inputFiles, string outputFile)" or "MergeFiles(stream[] inputFiles, stream[] outputFile)",
            which automatically release srcFiles and mergeFils resources after merging.***
    </summary>
    <param name="dest">The destination document, where the other documents are merged into.
            If it's null a new document object will be created.</param>
    <param name="sourceDocuments">The source documents.</param>
    <returns>The document containing merged documents.</returns>
        """
        intPtrdest:c_void_p = dest.Ptr
        #arraysourceDocuments:ArrayTypesourceDocuments = ""
        countsourceDocuments = len(sourceDocuments)
        ArrayTypesourceDocuments = c_void_p * countsourceDocuments
        arraysourceDocuments = ArrayTypesourceDocuments()
        for i in range(0, countsourceDocuments):
            arraysourceDocuments[i] = sourceDocuments[i].Ptr


        GetDllLibPdf().PdfDocument_Merge.argtypes=[ c_void_p,ArrayTypesourceDocuments]
        GetDllLibPdf().PdfDocument_Merge.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_Merge( intPtrdest,arraysourceDocuments)
        ret = None if intPtr==None else PdfDocumentBase(intPtr)
        return ret


    @staticmethod
    @dispatch

    def MergeFiles(inputFiles:List[str])->PdfDocumentBase:
        """
    <summary>
        Merges the PDF documents specified by the paths.
            ***It is recommended to use method "MergeFiles(string[] inputFiles, string outputFile)" or "MergeFiles(stream[] inputFiles, stream[] outputFile)",
            which automatically release srcFiles and mergeFils resources after merging.***
    </summary>
    <param name="paths">The array of string paths.</param>
    <returns>A new PDF document containing all merged documents.</returns>
        """
        #arrayinputFiles:ArrayTypeinputFiles = ""
        countinputFiles = len(inputFiles)
        ArrayTypeinputFiles = c_wchar_p * countinputFiles
        arrayinputFiles = ArrayTypeinputFiles()
        for i in range(0, countinputFiles):
            arrayinputFiles[i] = inputFiles[i]


        GetDllLibPdf().PdfDocument_MergeFiles.argtypes=[c_void_p, ArrayTypeinputFiles,c_int]
        GetDllLibPdf().PdfDocument_MergeFiles.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_MergeFiles(None, arrayinputFiles,len(inputFiles))
        ret = None if intPtr==None else PdfDocumentBase(intPtr)
        return ret


    @staticmethod
    @dispatch

    def MergeFiles(streams:List[Stream])->PdfDocumentBase:
        """
    <summary>
        Merges the PDF documents specified by the Stream.
            ***It is recommended to use method "MergeFiles(string[] inputFiles, string outputFile)" or "MergeFiles(stream[] inputFiles, stream[] outputFile)",
            which automatically release srcFiles and mergeFils resources after merging.***
    </summary>
    <param name="streams"></param>
    <returns></returns>
        """
        #arraystreams:ArrayTypestreams = ""
        countstreams = len(streams)
        ArrayTypestreams = c_void_p * countstreams
        arraystreams = ArrayTypestreams()
        for i in range(0, countstreams):
            arraystreams[i] = streams[i].Ptr


        GetDllLibPdf().PdfDocument_MergeFilesS.argtypes=[c_void_p, ArrayTypestreams,c_int]
        GetDllLibPdf().PdfDocument_MergeFilesS.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_MergeFilesS(None, arraystreams,countstreams)
        ret = None if intPtr==None else PdfDocumentBase(intPtr)
        return ret
#


    #@staticmethod
    #@dispatch

    #def MergeFiles(firstInputFile:str,secInputFile:str)->PdfDocumentBase:
    #    """
    #<summary>
    #    Merges the PDF documents specified by the paths.
    #</summary>
    #<param name="firstInputFile"></param>
    #<param name="secInputFile"></param>
    #<returns>A new PDF document containing all merged documents.</returns>
    #    """
        
    #    GetDllLibPdf().PdfDocument_MergeFilesFS.argtypes=[ c_wchar_p,c_wchar_p]
    #    GetDllLibPdf().PdfDocument_MergeFilesFS.restype=c_void_p
    #    intPtr = GetDllLibPdf().PdfDocument_MergeFilesFS( firstInputFile,secInputFile)
    #    ret = None if intPtr==None else PdfDocumentBase(intPtr)
    #    return ret


    @staticmethod
    @dispatch

    def MergeFiles(inputFiles:List[str],outputFile:str):
        """
    <summary>
        Merge the PDF documents.
    </summary>
    <param name="inputFiles">The input PDF documents.</param>
    <param name="outputFile">The output PDF document.</param>
        """
        #arrayinputFiles:ArrayTypeinputFiles = ""
        countinputFiles = len(inputFiles)
        ArrayTypeinputFiles = c_wchar_p * countinputFiles
        arrayinputFiles = ArrayTypeinputFiles()
        for i in range(0, countinputFiles):
            arrayinputFiles[i] = inputFiles[i]


        GetDllLibPdf().PdfDocument_MergeFilesIO.argtypes=[ ArrayTypeinputFiles,c_int,c_wchar_p]
        GetDllLibPdf().PdfDocument_MergeFilesIO( arrayinputFiles,countinputFiles,outputFile)

#    @staticmethod
#    @dispatch
#
#    def MergeFiles(inputFiles:'Stream[]',outputFile:Stream):
#        """
#    <summary>
#        Merge the PDF documents.
#    </summary>
#    <param name="inputFiles">The input PDF documents.</param>
#    <param name="outputFile">The output PDF document.</param>
#        """
#        #arrayinputFiles:ArrayTypeinputFiles = ""
#        countinputFiles = len(inputFiles)
#        ArrayTypeinputFiles = c_void_p * countinputFiles
#        arrayinputFiles = ArrayTypeinputFiles()
#        for i in range(0, countinputFiles):
#            arrayinputFiles[i] = inputFiles[i].Ptr
#
#        intPtroutputFile:c_void_p = outputFile.Ptr
#
#        GetDllLibPdf().PdfDocument_MergeFilesIO1.argtypes=[ ArrayTypeinputFiles,c_void_p]
#        GetDllLibPdf().PdfDocument_MergeFilesIO1( arrayinputFiles,intPtroutputFile)


    @dispatch

    def Split(self ,destFilePattern:str):
        """
    <summary>
        Splits a PDF file to many PDF files, each of them consists of one page from the source file.
    </summary>
    <param name="destFilePattern">Template for destination file names.</param>
<remarks>
            Each destination file will have 'destFileName{0***}' name,
            where *** is an optional format string for the number of the
            page inside of the source document.
            </remarks>
        """
        
        GetDllLibPdf().PdfDocument_Split.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfDocument_Split(self.Ptr, destFilePattern)

    @dispatch

    def Split(self ,destFilePattern:str,startNumber:int):
        """
    <summary>
        Splits a PDF file to many PDF files, each of them consists of
            one page from the source file.
    </summary>
    <param name="destFilePattern">Template for destination file
            names.</param>
    <param name="startNumber">The number that is use as a start
            point for the page numbering.</param>
<remarks>
            Each destination file will have 'destFileName{0***}' name,
            where *** is an optional format string for the number of the
            page inside of the source document.
            </remarks>
        """
        
        GetDllLibPdf().PdfDocument_SplitDS.argtypes=[c_void_p ,c_wchar_p,c_int]
        GetDllLibPdf().PdfDocument_SplitDS(self.Ptr, destFilePattern,startNumber)

    def RemoveDocumentJavaScript(self)->bool:
        """
    <summary>
        remove document's javaScript
    </summary>
    <returns>if True remove succesfully,else remove the failure or document doesn't have JavaScript</returns>
        """
        GetDllLibPdf().PdfDocument_RemoveDocumentJavaScript.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_RemoveDocumentJavaScript.restype=c_bool
        ret = GetDllLibPdf().PdfDocument_RemoveDocumentJavaScript(self.Ptr)
        return ret

#
#    def Preview(self ,printPreviewControl:'PrintPreviewControl'):
#        """
#    <summary>
#        Print preview.
#    </summary>
#    <param name="printPreviewControl">Print preview control</param>
#        """
#        intPtrprintPreviewControl:c_void_p = printPreviewControl.Ptr
#
#        GetDllLibPdf().PdfDocument_Preview.argtypes=[c_void_p ,c_void_p]
#        GetDllLibPdf().PdfDocument_Preview(self.Ptr, intPtrprintPreviewControl)


    #@dispatch

    #def Print(self ,printSettings:'PdfPrintSettings'):
    #    """
    #<summary>
    #    Print document.
    #</summary>
    #<param name="printSettings">The print settings.</param>
    #    """
    #    intPtrprintSettings:c_void_p = printSettings.Ptr

    #    GetDllLibPdf().PdfDocument_Print.argtypes=[c_void_p ,c_void_p]
    #    GetDllLibPdf().PdfDocument_Print(self.Ptr, intPtrprintSettings)

    #@property

    #def PrintSettings(self)->'PdfPrintSettings':
    #    """
    #<summary>
    #    Get the print settings.
    #</summary>
    #    """
    #    GetDllLibPdf().PdfDocument_get_PrintSettings.argtypes=[c_void_p]
    #    GetDllLibPdf().PdfDocument_get_PrintSettings.restype=c_void_p
    #    intPtr = GetDllLibPdf().PdfDocument_get_PrintSettings(self.Ptr)
    #    ret = None if intPtr==None else PdfPrintSettings(intPtr)
    #    return ret


    #@dispatch
    #def Print(self):
    #    """
    #<summary>
    #    Print document.
    #</summary>
    #    """
    #    GetDllLibPdf().PdfDocument_Print1.argtypes=[c_void_p]
    #    GetDllLibPdf().PdfDocument_Print1(self.Ptr)

    def Close(self):
        """
    <summary>
        Closes the document.
    </summary>
<remarks>The document is disposed after calling the Close method. So, the document can not be saved if Close method was invoked.</remarks>
        """
        GetDllLibPdf().PdfDocument_Close.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_Close(self.Ptr)

    def Dispose(self):
        """
    <summary>
        Releases unmanaged resources and performs other cleanup operations before the
             is reclaimed by garbage collection.
    </summary>
        """
        GetDllLibPdf().PdfDocument_Dispose.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_Dispose(self.Ptr)

    @staticmethod

    def SetCustomFontsFolders(fontPath:str):
        """
    <summary>
        Set the path to the folder where the custom font is located.
    </summary>
    <param name="fontPath">the folder path.</param>
        """
        
        GetDllLibPdf().PdfDocument_SetCustomFontsFolders.argtypes=[ c_wchar_p]
        GetDllLibPdf().PdfDocument_SetCustomFontsFolders( fontPath)

    @staticmethod
    def ClearCustomFontsFolders():
        """
    <summary>
        Clear the path of the folder where the custom font is located.
    </summary>
        """
        #GetDllLibPdf().PdfDocument_ClearCustomFontsFolders.argtypes=[]
        GetDllLibPdf().PdfDocument_ClearCustomFontsFolders()

    @property
    def UseHighQualityImage(self)->bool:
        """
    <summary>
        Indicates whether to use the high qulity image when convert document
    </summary>
        """
        GetDllLibPdf().PdfDocument_get_UseHighQualityImage.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_UseHighQualityImage.restype=c_bool
        ret = GetDllLibPdf().PdfDocument_get_UseHighQualityImage(self.Ptr)
        return ret

    @UseHighQualityImage.setter
    def UseHighQualityImage(self, value:bool):
        GetDllLibPdf().PdfDocument_set_UseHighQualityImage.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfDocument_set_UseHighQualityImage(self.Ptr, value)

    @property

    def SetPdfToHtmlParameter(self)->'PdfToHtmlParameter':
        """

        """
        GetDllLibPdf().PdfDocument_get_SetPdfToHtmlParameter.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_SetPdfToHtmlParameter.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_get_SetPdfToHtmlParameter(self.Ptr)
        ret = None if intPtr==None else PdfToHtmlParameter(intPtr)
        return ret


    @SetPdfToHtmlParameter.setter
    def SetPdfToHtmlParameter(self, value:'PdfToHtmlParameter'):
        GetDllLibPdf().PdfDocument_set_SetPdfToHtmlParameter.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfDocument_set_SetPdfToHtmlParameter(self.Ptr, value.Ptr)

    @property
    def AllowCreateForm(self)->bool:
        """
    <summary>
        Get or Set Allow Create Form.
    </summary>
        """
        GetDllLibPdf().PdfDocument_get_AllowCreateForm.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_AllowCreateForm.restype=c_bool
        ret = GetDllLibPdf().PdfDocument_get_AllowCreateForm(self.Ptr)
        return ret

    @AllowCreateForm.setter
    def AllowCreateForm(self, value:bool):
        GetDllLibPdf().PdfDocument_set_AllowCreateForm.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfDocument_set_AllowCreateForm(self.Ptr, value)

    @property
    def UsePsDirectlyForConvert(self)->bool:
        """

        """
        GetDllLibPdf().PdfDocument_get_UsePsDirectlyForConvert.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_UsePsDirectlyForConvert.restype=c_bool
        ret = GetDllLibPdf().PdfDocument_get_UsePsDirectlyForConvert(self.Ptr)
        return ret

    @UsePsDirectlyForConvert.setter
    def UsePsDirectlyForConvert(self, value:bool):
        GetDllLibPdf().PdfDocument_set_UsePsDirectlyForConvert.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfDocument_set_UsePsDirectlyForConvert(self.Ptr, value)

    @property
    def UseInvariantCulture(self)->bool:
        """
    <summary>
        Indicates whether use invariant culture mode to convert pdf document.
    </summary>
        """
        GetDllLibPdf().PdfDocument_get_UseInvariantCulture.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_UseInvariantCulture.restype=c_bool
        ret = GetDllLibPdf().PdfDocument_get_UseInvariantCulture(self.Ptr)
        return ret

    @UseInvariantCulture.setter
    def UseInvariantCulture(self, value:bool):
        GetDllLibPdf().PdfDocument_set_UseInvariantCulture.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfDocument_set_UseInvariantCulture(self.Ptr, value)

    @property

    def ConvertOptions(self)->'PdfConvertOptions':
        """
    <summary>
        Set some options when do convert operation.
    </summary>
        """
        GetDllLibPdf().PdfDocument_get_ConvertOptions.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_ConvertOptions.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_get_ConvertOptions(self.Ptr)
        ret = None if intPtr==None else PdfConvertOptions(intPtr)
        return ret


    @property

    def PDFStandard(self)->'PdfDocumentBase':
        """
    <summary>
        Set,Get Current active pdf object 
    </summary>
        """
        GetDllLibPdf().PdfDocument_get_PDFStandard.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_PDFStandard.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_get_PDFStandard(self.Ptr)
        ret = None if intPtr==None else PdfDocumentBase(intPtr)
        return ret


    @PDFStandard.setter
    def PDFStandard(self, value:'PdfDocumentBase'):
        GetDllLibPdf().PdfDocument_set_PDFStandard.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfDocument_set_PDFStandard(self.Ptr, value.Ptr)

    @property

    def Conformance(self)->'PdfConformanceLevel':
        """
    <summary>
        Get document PdfConformanceLevel
    </summary>
        """
        GetDllLibPdf().PdfDocument_get_Conformance.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_Conformance.restype=c_int
        ret = GetDllLibPdf().PdfDocument_get_Conformance(self.Ptr)
        objwraped = PdfConformanceLevel(ret)
        return objwraped

    @property

    def Attachments(self)->PdfAttachmentCollection:
        """
    <summary>
        Gets the collection of document attachments displayed on a PDF page.
    </summary>
        """
        GetDllLibPdf().PdfDocument_get_Attachments.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_Attachments.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_get_Attachments(self.Ptr)
        ret = None if intPtr==None else PdfAttachmentCollection(intPtr)
        return ret





    @property

    def ColorSpace(self)->'PdfColorSpace':
        """
    <summary>
        Gets or sets the color space for page that will be created.
    </summary>
        """
        GetDllLibPdf().PdfDocument_get_ColorSpace.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_ColorSpace.restype=c_int
        ret = GetDllLibPdf().PdfDocument_get_ColorSpace(self.Ptr)
        objwraped = PdfColorSpace(ret)
        return objwraped

    @ColorSpace.setter
    def ColorSpace(self, value:'PdfColorSpace'):
        GetDllLibPdf().PdfDocument_set_ColorSpace.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfDocument_set_ColorSpace(self.Ptr, value.value)

    @property

    def DocumentInformation(self)->'PdfDocumentInformation':
        """
    <summary>
        Gets or sets document's information and properties.
    </summary>
        """
        GetDllLibPdf().PdfDocument_get_DocumentInformation.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_DocumentInformation.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_get_DocumentInformation(self.Ptr)
        ret = None if intPtr==None else PdfDocumentInformation(intPtr)
        return ret


    @property

    def JavaScripts(self)->'PdfDocumentActions':
        """
    <summary>
        Gets the additional document's actions.
    </summary>
        """
        GetDllLibPdf().PdfDocument_get_JavaScripts.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_JavaScripts.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_get_JavaScripts(self.Ptr)
        ret = None if intPtr==None else PdfDocumentActions(intPtr)
        return ret


    @property

    def Form(self)->'PdfForm':
        """
    <summary>
        Gets the loaded form.
    </summary>
        """
        GetDllLibPdf().PdfDocument_get_Form.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_Form.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_get_Form(self.Ptr)
        ret = None if intPtr==None else PdfForm(intPtr)
        return ret


    @property

    def PageLabels(self)->'PdfPageLabels':
        """
    <summary>
        Page labels.
    </summary>
        """
        GetDllLibPdf().PdfDocument_get_PageLabels.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_PageLabels.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_get_PageLabels(self.Ptr)
        ret = None if intPtr==None else PdfPageLabels(intPtr)
        return ret


    @PageLabels.setter
    def PageLabels(self, value:'PdfPageLabels'):
        GetDllLibPdf().PdfDocument_set_PageLabels.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfDocument_set_PageLabels(self.Ptr, value.Ptr)

    @property

    def DocumentPieceInfo(self)->'PdfPieceInfo':
        """
    <summary>
        Gets or set the document piece info.
    </summary>
        """
        GetDllLibPdf().PdfDocument_get_DocumentPieceInfo.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_DocumentPieceInfo.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_get_DocumentPieceInfo(self.Ptr)
        ret = None if intPtr==None else PdfPieceInfo(intPtr)
        return ret


    @DocumentPieceInfo.setter
    def DocumentPieceInfo(self, value:'PdfPieceInfo'):
        GetDllLibPdf().PdfDocument_set_DocumentPieceInfo.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfDocument_set_DocumentPieceInfo(self.Ptr, value.Ptr)

    @property

    def Pages(self)->PdfPageCollection:
        """
    <summary>
        Gets the pages.
    </summary>
        """
        GetDllLibPdf().PdfDocument_get_Pages.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_Pages.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_get_Pages(self.Ptr)
        ret = None if intPtr==None else PdfPageCollection(intPtr)
        return ret


    @property

    def UsedFonts(self)->List['PdfUsedFont']:
        """
    <summary>
        Gets the fonts which are available in the PDF document.
    </summary>
<value>Retruns the fonts which are used in the PDF document.</value>
        """
        GetDllLibPdf().PdfDocument_get_UsedFonts.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_UsedFonts.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().PdfDocument_get_UsedFonts(self.Ptr)
        ret = GetObjVectorFromArray(intPtrArray, PdfUsedFont)
        return ret


    @property

    def CompressionLevel(self)->'PdfCompressionLevel':
        """
    <summary>
        Gets or sets the desired level of stream compression.
    </summary>
<remarks>All new objects should be compressed with this level of the compression.</remarks>
        """
        GetDllLibPdf().PdfDocument_get_CompressionLevel.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_CompressionLevel.restype=c_int
        ret = GetDllLibPdf().PdfDocument_get_CompressionLevel(self.Ptr)
        objwraped = PdfCompressionLevel(ret)
        return objwraped

    @CompressionLevel.setter
    def CompressionLevel(self, value:'PdfCompressionLevel'):
        GetDllLibPdf().PdfDocument_set_CompressionLevel.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfDocument_set_CompressionLevel(self.Ptr, value.value)

    @property

    def PageSettings(self)->'PdfPageSettings':
        """

        """
        GetDllLibPdf().PdfDocument_get_PageSettings.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_PageSettings.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_get_PageSettings(self.Ptr)
        ret = None if intPtr==None else PdfPageSettings(intPtr)
        return ret


    @PageSettings.setter
    def PageSettings(self, value:'PdfPageSettings'):
        GetDllLibPdf().PdfDocument_set_PageSettings.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfDocument_set_PageSettings(self.Ptr, value.Ptr)

    @property

    def Sections(self)->'PdfSectionCollection':
        """

        """
        GetDllLibPdf().PdfDocument_get_Sections.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_Sections.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_get_Sections(self.Ptr)
        ret = None if intPtr==None else PdfSectionCollection(intPtr)
        return ret


    @property

    def FileInfo(self)->'PdfFileInfo':
        """

        """
        GetDllLibPdf().PdfDocument_get_FileInfo.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_FileInfo.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_get_FileInfo(self.Ptr)
        ret = None if intPtr==None else PdfFileInfo(intPtr)
        return ret


    @FileInfo.setter
    def FileInfo(self, value:'PdfFileInfo'):
        GetDllLibPdf().PdfDocument_set_FileInfo.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfDocument_set_FileInfo(self.Ptr, value.Ptr)

    @property

    def Security(self)->'PdfSecurity':
        """
    <summary>
        Gets the security parameters of the document.
    </summary>
        """
        GetDllLibPdf().PdfDocument_get_Security.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_Security.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_get_Security(self.Ptr)
        ret = None if intPtr==None else PdfSecurity(intPtr)
        return ret


    @property

    def ViewerPreferences(self)->'PdfViewerPreferences':
        """
    <summary>
        Gets or sets a viewer preferences object controlling the way the document is to be 
            presented on the screen or in print.
    </summary>
        """
        GetDllLibPdf().PdfDocument_get_ViewerPreferences.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_ViewerPreferences.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_get_ViewerPreferences(self.Ptr)
        ret = None if intPtr==None else PdfViewerPreferences(intPtr)
        return ret


    @ViewerPreferences.setter
    def ViewerPreferences(self, value:'PdfViewerPreferences'):
        GetDllLibPdf().PdfDocument_set_ViewerPreferences.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfDocument_set_ViewerPreferences(self.Ptr, value.Ptr)

    @property

    def AfterOpenAction(self)->'PdfGoToAction':
        """
    <summary>
        Gets or sets the action to execute when the document is opened. 
    </summary>
        """
        GetDllLibPdf().PdfDocument_get_AfterOpenAction.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_AfterOpenAction.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_get_AfterOpenAction(self.Ptr)
        ret = None if intPtr==None else PdfGoToAction(PdfDestination(intPtr))
        return ret


    @AfterOpenAction.setter
    def AfterOpenAction(self, value:PdfAction):
        if value is None :
            GetDllLibPdf().PdfDocument_set_AfterOpenActionN.argtypes=[c_void_p]
            GetDllLibPdf().PdfDocument_set_AfterOpenActionN(self.Ptr) 
        else :
            GetDllLibPdf().PdfDocument_set_AfterOpenAction.argtypes=[c_void_p, c_void_p]
            GetDllLibPdf().PdfDocument_set_AfterOpenAction(self.Ptr, value.Ptr)

    @property

    def AfterPrintAction(self)->'PdfJavaScriptAction':
        """
    <summary>
        Gets or sets the action to be performed after the document is printed.
    </summary>
<value>A  object specifying the action to be executed after the document is printed. .</value>
        """
        GetDllLibPdf().PdfDocument_get_AfterPrintAction.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_AfterPrintAction.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_get_AfterPrintAction(self.Ptr)
        ret = None if intPtr==None else PdfJavaScriptAction(intPtr)
        return ret


    @AfterPrintAction.setter
    def AfterPrintAction(self, value:'PdfJavaScriptAction'):
        GetDllLibPdf().PdfDocument_set_AfterPrintAction.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfDocument_set_AfterPrintAction(self.Ptr, value.Ptr)

    @property

    def AfterSaveAction(self)->'PdfJavaScriptAction':
        """
    <summary>
        Gets or sets the jave script action to be performed after the document is saved.
    </summary>
<value>A  object specifying the action to be executed after the document is saved.</value>
        """
        GetDllLibPdf().PdfDocument_get_AfterSaveAction.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_AfterSaveAction.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_get_AfterSaveAction(self.Ptr)
        ret = None if intPtr==None else PdfJavaScriptAction(intPtr)
        return ret


    @AfterSaveAction.setter
    def AfterSaveAction(self, value:'PdfJavaScriptAction'):
        GetDllLibPdf().PdfDocument_set_AfterSaveAction.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfDocument_set_AfterSaveAction(self.Ptr, value.Ptr)

    @property

    def BeforeCloseAction(self)->'PdfJavaScriptAction':
        """
    <summary>
        Gets or sets the action to be performed before the document is closed.
    </summary>
<value>A  object specifying the action to be executed before the document is closed. </value>
        """
        GetDllLibPdf().PdfDocument_get_BeforeCloseAction.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_BeforeCloseAction.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_get_BeforeCloseAction(self.Ptr)
        ret = None if intPtr==None else PdfJavaScriptAction(intPtr)
        return ret


    @BeforeCloseAction.setter
    def BeforeCloseAction(self, value:'PdfJavaScriptAction'):
        GetDllLibPdf().PdfDocument_set_BeforeCloseAction.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfDocument_set_BeforeCloseAction(self.Ptr, value.Ptr)

    @property

    def BeforePrintAction(self)->'PdfJavaScriptAction':
        """
    <summary>
        Gets or sets the action to be performed before the document is printed.
    </summary>
<value>A  object specifying the action to be executed before the document is printed. </value>
        """
        GetDllLibPdf().PdfDocument_get_BeforePrintAction.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_BeforePrintAction.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_get_BeforePrintAction(self.Ptr)
        ret = None if intPtr==None else PdfJavaScriptAction(intPtr)
        return ret


    @BeforePrintAction.setter
    def BeforePrintAction(self, value:'PdfJavaScriptAction'):
        GetDllLibPdf().PdfDocument_set_BeforePrintAction.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfDocument_set_BeforePrintAction(self.Ptr, value.Ptr)

    @property

    def BeforeSaveAction(self)->'PdfJavaScriptAction':
        """
    <summary>
        Gets or sets the java script action to be performed before the document is saved.
    </summary>
<value>A  object specifying the action to be executed before the document is saved. </value>
        """
        GetDllLibPdf().PdfDocument_get_BeforeSaveAction.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_BeforeSaveAction.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_get_BeforeSaveAction(self.Ptr)
        ret = None if intPtr==None else PdfJavaScriptAction(intPtr)
        return ret


    @BeforeSaveAction.setter
    def BeforeSaveAction(self, value:'PdfJavaScriptAction'):
        GetDllLibPdf().PdfDocument_set_BeforeSaveAction.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfDocument_set_BeforeSaveAction(self.Ptr, value.Ptr)

    @property

    def XmpMetaData(self)->'XmpMetadata':
        """

        """
        GetDllLibPdf().PdfDocument_get_XmpMetaData.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_XmpMetaData.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_get_XmpMetaData(self.Ptr)
        ret = None if intPtr==None else XmpMetadata(intPtr)
        return ret


    @property

    def Template(self)->'PdfDocumentTemplate':
        """
    <summary>
        Gets the template of pdf document
    </summary>
        """
        GetDllLibPdf().PdfDocument_get_Template.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_Template.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_get_Template(self.Ptr)
        ret = None if intPtr==None else PdfDocumentTemplate(intPtr)
        return ret


    @staticmethod
    def get_EnableFontCache()->bool:
        """
    <summary>
        Indicates whether enable font cache.
    </summary>
        """
        #GetDllLibPdf().PdfDocument_get_EnableFontCache.argtypes=[]
        GetDllLibPdf().PdfDocument_get_EnableFontCache.restype=c_bool
        ret = GetDllLibPdf().PdfDocument_get_EnableFontCache()
        return ret

    @staticmethod
    def set_EnableFontCache( value:bool):
        GetDllLibPdf().PdfDocument_set_EnableFontCache.argtypes=[ c_bool]
        GetDllLibPdf().PdfDocument_set_EnableFontCache( value)

    @property

    def Tag(self)->'SpireObject':
        """

        """
        GetDllLibPdf().PdfDocument_get_Tag.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_Tag.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_get_Tag(self.Ptr)
        ret = None if intPtr==None else SpireObject(intPtr)
        return ret


    @Tag.setter
    def Tag(self, value:'SpireObject'):
        GetDllLibPdf().PdfDocument_set_Tag.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfDocument_set_Tag(self.Ptr, value.Ptr)

    @property
    def IsEncrypted(self)->bool:
        """
    <summary>
        Indicates the document is encrypted or not.
    </summary>
        """
        GetDllLibPdf().PdfDocument_get_IsEncrypted.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_IsEncrypted.restype=c_bool
        ret = GetDllLibPdf().PdfDocument_get_IsEncrypted(self.Ptr)
        return ret

    @property
    def IsPortfolio(self)->bool:
        """
    <summary>
        Indicates the document is a PDF Portfolio or not.
    </summary>
        """
        GetDllLibPdf().PdfDocument_get_IsPortfolio.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_IsPortfolio.restype=c_bool
        ret = GetDllLibPdf().PdfDocument_get_IsPortfolio(self.Ptr)
        return ret

    @property

    def Layers(self)->'PdfLayerCollection':
        """
    <summary>
        Optional content properties
    </summary>
        """
        GetDllLibPdf().PdfDocument_get_Layers.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_Layers.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_get_Layers(self.Ptr)
        ret = None if intPtr==None else PdfLayerCollection(intPtr)
        return ret


    @property

    def Collection(self)->'Collections_PdfCollection':
        """
    <summary>
        The pdf collections.
    </summary>
        """
        GetDllLibPdf().PdfDocument_get_Collection.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_Collection.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_get_Collection(self.Ptr)
        ret = None if intPtr==None else Collections_PdfCollection(intPtr)
        return ret


    @dispatch

    def LoadFromFile(self ,filename:str):
        """
    <summary>
        Initializes a new instance of the class.
    </summary>
    <param name="filename">The path to source pdf file.</param>
<remarks>This constructor imports an existing pdf file into the document object. It automatically populates the Pages collection with the pages of the given document. </remarks>
        """
        
        GetDllLibPdf().PdfDocument_LoadFromFile.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfDocument_LoadFromFile(self.Ptr, filename)

    @dispatch

    def LoadFromFile(self ,filename:str,password:str):
        """
    <summary>
        Initializes a new instance of the  class.
    </summary>
    <param name="filename">The path to source PDF document.</param>
    <param name="password">The password (user or owner) of the encrypted document.</param>
        """
        
        GetDllLibPdf().PdfDocument_LoadFromFileFP.argtypes=[c_void_p ,c_wchar_p,c_wchar_p]
        GetDllLibPdf().PdfDocument_LoadFromFileFP.restype=IntPtrWithTypeName
        intPtr = GetDllLibPdf().PdfDocument_LoadFromFileFP(self.Ptr, filename,password)
        emessage = PtrToStr(intPtr.typeName)
        if emessage != None :
            print(emessage)

    @dispatch

    def LoadFromFile(self ,fileName:str,fileFormat:FileFormat):
        """

        """
        enumfileFormat:c_int = fileFormat.value

        GetDllLibPdf().PdfDocument_LoadFromFileFF.argtypes=[c_void_p ,c_wchar_p,c_int]
        GetDllLibPdf().PdfDocument_LoadFromFileFF(self.Ptr, fileName,enumfileFormat)

#    @dispatch
#
#    def LoadFromXPS(self ,xpsBytes:'Byte[]'):
#        """
#    <summary>
#        Load a xps bytes array.
#    </summary>
#    <param name="xpsBytes">the xps byte array</param>
#        """
#        #arrayxpsBytes:ArrayTypexpsBytes = ""
#        countxpsBytes = len(xpsBytes)
#        ArrayTypexpsBytes = c_void_p * countxpsBytes
#        arrayxpsBytes = ArrayTypexpsBytes()
#        for i in range(0, countxpsBytes):
#            arrayxpsBytes[i] = xpsBytes[i].Ptr
#
#
#        GetDllLibPdf().PdfDocument_LoadFromXPS.argtypes=[c_void_p ,ArrayTypexpsBytes]
#        GetDllLibPdf().PdfDocument_LoadFromXPS(self.Ptr, arrayxpsBytes)


    #@dispatch

    #def LoadFromXPS(self ,fileName:str):
    #    """
    #<summary>
    #    Load a xps file.
    #</summary>
    #<param name="fileName"></param>
    #    """
        
    #    GetDllLibPdf().PdfDocument_LoadFromXPSF.argtypes=[c_void_p ,c_wchar_p]
    #    GetDllLibPdf().PdfDocument_LoadFromXPSF(self.Ptr, fileName)

    #@dispatch

    #def LoadFromXPS(self ,xpsStream:Stream):
    #    """
    #<summary>
    #    Load a xps stream.
    #</summary>
    #<param name="xpsStream"></param>
    #    """
    #    intPtrxpsStream:c_void_p = xpsStream.Ptr

    #    GetDllLibPdf().PdfDocument_LoadFromXPSX.argtypes=[c_void_p ,c_void_p]
    #    GetDllLibPdf().PdfDocument_LoadFromXPSX(self.Ptr, intPtrxpsStream)

    @dispatch

    def LoadFromSvg(self ,fileName:str):
        """
    <summary>
        Load a svg file.
    </summary>
    <param name="fileName">A relative or absolute path for the svg file</param>
        """
        
        GetDllLibPdf().PdfDocument_LoadFromSvg.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfDocument_LoadFromSvg(self.Ptr, fileName)

    @dispatch

    def LoadFromSvg(self ,stream:Stream):
        """
    <summary>
        Load a svg stream.
    </summary>
    <param name="stream">A Svg file stream</param>
        """
        intPtrstream:c_void_p = stream.Ptr

        GetDllLibPdf().PdfDocument_LoadFromSvgS.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfDocument_LoadFromSvgS(self.Ptr, intPtrstream)

    #@dispatch

    #def LoadFromHTML(self ,url:str,enableJavaScript:bool,enableHyperlinks:bool,autoDetectPageBreak:bool):
    #    """
    #<summary>
    #    Load file from disk file.
    #</summary>
    #<param name="url">url address</param>
    #<param name="enableJavaScript">Enable javascrpit</param>
    #<param name="enableHyperlinks">Enable hyperlink</param>
    #<param name="autoDetectPageBreak">Auto detect page break</param>
    #    """
        
    #    GetDllLibPdf().PdfDocument_LoadFromHTML.argtypes=[c_void_p ,c_wchar_p,c_bool,c_bool,c_bool]
    #    GetDllLibPdf().PdfDocument_LoadFromHTML(self.Ptr, url,enableJavaScript,enableHyperlinks,autoDetectPageBreak)

    #@dispatch

    #def LoadFromHTML(self ,Url:str,enableJavaScript:bool,enableHyperlinks:bool,autoDetectPageBreak:bool,setting:PdfPageSettings):
    #    """
    #<summary>
    #     Load file from disk file.
    #</summary>
    #<param name="url">url address</param>
    #<param name="enableJavaScript">Enable javascrpit</param>
    #<param name="enableHyperlinks">Enable hyperlink</param>
    #<param name="autoDetectPageBreak">Auto detect page break</param>
    #<param name="Size">paper size</param>
    #<param name="layoutFormat">PdfHtmlLayoutFormat layoutFormat</param>
    #    """
    #    intPtrsetting:c_void_p = setting.Ptr

    #    GetDllLibPdf().PdfDocument_LoadFromHTMLUEEAS.argtypes=[c_void_p ,c_wchar_p,c_bool,c_bool,c_bool,c_void_p]
    #    GetDllLibPdf().PdfDocument_LoadFromHTMLUEEAS(self.Ptr, Url,enableJavaScript,enableHyperlinks,autoDetectPageBreak,intPtrsetting)

    #@dispatch

    #def LoadFromHTML(self ,Url:str,enableJavaScript:bool,enableHyperlinks:bool,autoDetectPageBreak:bool,setting:PdfPageSettings,layoutFormat:PdfHtmlLayoutFormat):
    #    """
    #<summary>
    #     Load file from disk file.
    #</summary>
    #<param name="url">url address</param>
    #<param name="enableJavaScript">Enable javascrpit</param>
    #<param name="enableHyperlinks">Enable hyperlink</param>
    #<param name="autoDetectPageBreak">Auto detect page break</param>
    #<param name="Size">paper size</param>
    #<param name="layoutFormat">PdfHtmlLayoutFormat layoutFormat</param>
    #    """
    #    intPtrsetting:c_void_p = setting.Ptr
    #    intPtrlayoutFormat:c_void_p = layoutFormat.Ptr

    #    GetDllLibPdf().PdfDocument_LoadFromHTMLUEEASL.argtypes=[c_void_p ,c_wchar_p,c_bool,c_bool,c_bool,c_void_p,c_void_p]
    #    GetDllLibPdf().PdfDocument_LoadFromHTMLUEEASL(self.Ptr, Url,enableJavaScript,enableHyperlinks,autoDetectPageBreak,intPtrsetting,intPtrlayoutFormat)

    #@dispatch

    #def LoadFromHTML(self ,url:str,enableJavaScript:bool,enableHyperlinks:bool,autoDetectPageBreak:bool,setting:PdfPageSettings,layoutFormat:PdfHtmlLayoutFormat,isLoadComplete:bool):
    #    """
    #<summary>
    #     Load file from disk file.
    #</summary>
    #<param name="url">url address</param>
    #<param name="enableJavaScript">Enable javascrpit</param>
    #<param name="enableHyperlinks">Enable hyperlink</param>
    #<param name="autoDetectPageBreak">Auto detect page break</param>
    #<param name="setting">Page setting</param>
    #<param name="layoutFormat">PdfHtmlLayoutFormat layoutFormat</param>
    #<param name="isLoadComplete">
    #        by default false, when load Html DOM timeout(PdfHtmlLayoutFormat.LoadHtmlTimeout),convert uncompleted Html DOM to pdf.
    #        if true,until Html DOM load completed,then convert to pdf. 
    #</param>
    #    """
    #    intPtrsetting:c_void_p = setting.Ptr
    #    intPtrlayoutFormat:c_void_p = layoutFormat.Ptr

    #    GetDllLibPdf().PdfDocument_LoadFromHTMLUEEASLI.argtypes=[c_void_p ,c_wchar_p,c_bool,c_bool,c_bool,c_void_p,c_void_p,c_bool]
    #    GetDllLibPdf().PdfDocument_LoadFromHTMLUEEASLI(self.Ptr, url,enableJavaScript,enableHyperlinks,autoDetectPageBreak,intPtrsetting,intPtrlayoutFormat,isLoadComplete)

    #@dispatch

    #def LoadFromHTML(self ,htmlSourceCode:str,autoDetectPageBreak:bool,setting:PdfPageSettings,layoutFormat:PdfHtmlLayoutFormat):
    #    """
    #<summary>
    #    Load htmlSourceCode to Pdf
    #</summary>
    #<param name="htmlSourceCode">htmlSourceCode</param>
    #<param name="autoDetectPageBreak">Auto detect page break</param>
    #<param name="setting">PdfPageSettings setting</param>
    #<param name="layoutFormat">PdfHtmlLayoutFormat layoutFormat</param>
    #    """
    #    intPtrsetting:c_void_p = setting.Ptr
    #    intPtrlayoutFormat:c_void_p = layoutFormat.Ptr

    #    GetDllLibPdf().PdfDocument_LoadFromHTMLHASL.argtypes=[c_void_p ,c_wchar_p,c_bool,c_void_p,c_void_p]
    #    GetDllLibPdf().PdfDocument_LoadFromHTMLHASL(self.Ptr, htmlSourceCode,autoDetectPageBreak,intPtrsetting,intPtrlayoutFormat)

    #@dispatch

    #def LoadFromHTML(self ,htmlSourceCode:str,autoDetectPageBreak:bool,setting:PdfPageSettings,layoutFormat:PdfHtmlLayoutFormat,isLoadComplete:bool):
    #    """
    #<summary>
    #    Load htmlSourceCode to Pdf
    #</summary>
    #<param name="htmlSourceCode">htmlSourceCode</param>
    #<param name="autoDetectPageBreak">Auto detect page break</param>
    #<param name="setting">PdfPageSettings setting</param>
    #<param name="layoutFormat">PdfHtmlLayoutFormat layoutFormat</param>
    #<param name="isLoadComplete">
    #        by default false, when load Html DOM timeout(PdfHtmlLayoutFormat.LoadHtmlTimeout),convert uncompleted Html DOM to pdf.
    #        if true,until Html DOM load completed,then convert to pdf. 
    #</param>
    #    """
    #    intPtrsetting:c_void_p = setting.Ptr
    #    intPtrlayoutFormat:c_void_p = layoutFormat.Ptr

    #    GetDllLibPdf().PdfDocument_LoadFromHTMLHASLI.argtypes=[c_void_p ,c_wchar_p,c_bool,c_void_p,c_void_p,c_bool]
    #    GetDllLibPdf().PdfDocument_LoadFromHTMLHASLI(self.Ptr, htmlSourceCode,autoDetectPageBreak,intPtrsetting,intPtrlayoutFormat,isLoadComplete)

#    @dispatch
#
#    def LoadFromBytes(self ,bytes:'Byte[]'):
#        """
#    <summary>
#        Initializes a new instance of the  class.
#    </summary>
#    <param name="bytes">The byte array with the file content.</param>
#        """
#        #arraybytes:ArrayTypebytes = ""
#        countbytes = len(bytes)
#        ArrayTypebytes = c_void_p * countbytes
#        arraybytes = ArrayTypebytes()
#        for i in range(0, countbytes):
#            arraybytes[i] = bytes[i].Ptr
#
#
#        GetDllLibPdf().PdfDocument_LoadFromBytesB.argtypes=[c_void_p ,ArrayTypebytes]
#        GetDllLibPdf().PdfDocument_LoadFromBytesB(self.Ptr, arraybytes)


    @dispatch

    def LoadFromStream(self ,stream:Stream):
        """
    <summary>
        Initializes a new instance of the  class.
    </summary>
    <param name="stream">The stream with the file.</param>
        """
        intPtrstream:c_void_p = stream.Ptr

        GetDllLibPdf().PdfDocument_LoadFromStreamS.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfDocument_LoadFromStreamS(self.Ptr, intPtrstream)

    @property
    def Bookmarks(self)->PdfBookmarkCollection:
        """
    <summary>
        Gets the bookmarks.
    </summary>
        """
        GetDllLibPdf().PdfDocument_get_Bookmarks.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocument_get_Bookmarks.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocument_get_Bookmarks(self.Ptr)
        ret = None if intPtr==None else PdfBookmarkCollection(intPtr)
        return ret