from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfSubmitAction (  PdfFormAction) :
    """
    <summary>
        Represents Pdf form's submit action.
    </summary>
<remarks>This type of action allows a user to go to a resource on the Internet, tipically a hypertext link. </remarks>
    """
    @property

    def Url(self)->str:
        """
<value>An string value specifying the full URI for the internet resource. </value>
        """
        GetDllLibPdf().PdfSubmitAction_get_Url.argtypes=[c_void_p]
        GetDllLibPdf().PdfSubmitAction_get_Url.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfSubmitAction_get_Url(self.Ptr))
        return ret


    @property

    def HttpMethod(self)->'HttpMethod':
        """
    <summary>
        Gets or sets the HTTP method.
    </summary>
<value>The HTTP method.</value>
        """
        GetDllLibPdf().PdfSubmitAction_get_HttpMethod.argtypes=[c_void_p]
        GetDllLibPdf().PdfSubmitAction_get_HttpMethod.restype=c_int
        ret = GetDllLibPdf().PdfSubmitAction_get_HttpMethod(self.Ptr)
        objwraped = HttpMethod(ret)
        return objwraped

    @HttpMethod.setter
    def HttpMethod(self, value:'HttpMethod'):
        GetDllLibPdf().PdfSubmitAction_set_HttpMethod.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfSubmitAction_set_HttpMethod(self.Ptr, value.value)

    @property
    def CanonicalDateTimeFormat(self)->bool:
        """
    <summary>
        If set, any submitted field values representing dates are converted to the 
            standard format. The interpretation of a form field as a date is not specified 
            explicitly in the field itself but only in the JavaScript code that processes it.
    </summary>
<value>
  <c>true</c> if use canonical date time format when submit data; otherwise, <c>false</c>.
            </value>
        """
        GetDllLibPdf().PdfSubmitAction_get_CanonicalDateTimeFormat.argtypes=[c_void_p]
        GetDllLibPdf().PdfSubmitAction_get_CanonicalDateTimeFormat.restype=c_bool
        ret = GetDllLibPdf().PdfSubmitAction_get_CanonicalDateTimeFormat(self.Ptr)
        return ret

    @CanonicalDateTimeFormat.setter
    def CanonicalDateTimeFormat(self, value:bool):
        GetDllLibPdf().PdfSubmitAction_set_CanonicalDateTimeFormat.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfSubmitAction_set_CanonicalDateTimeFormat(self.Ptr, value)

    @property
    def SubmitCoordinates(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether to submit mouse pointer coordinates. If set, 
            the coordinates of the mouse click that caused the submit-form action are transmitted 
            as part of the form data. 
    </summary>
<value>
  <c>true</c> if submit coordinates; otherwise, <c>false</c>.</value>
        """
        GetDllLibPdf().PdfSubmitAction_get_SubmitCoordinates.argtypes=[c_void_p]
        GetDllLibPdf().PdfSubmitAction_get_SubmitCoordinates.restype=c_bool
        ret = GetDllLibPdf().PdfSubmitAction_get_SubmitCoordinates(self.Ptr)
        return ret

    @SubmitCoordinates.setter
    def SubmitCoordinates(self, value:bool):
        GetDllLibPdf().PdfSubmitAction_set_SubmitCoordinates.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfSubmitAction_set_SubmitCoordinates(self.Ptr, value)

    @property
    def IncludeNoValueFields(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether to submit fields without value.
            If set, all fields designated by the Fields collection and the 
            flag are submitted, regardless of whether they have a value. For fields without a 
            value, only the field name is transmitted.
    </summary>
<value>
  <c>true</c> if submit fields without value or the empty ones; otherwise, <c>false</c>.
            </value>
        """
        GetDllLibPdf().PdfSubmitAction_get_IncludeNoValueFields.argtypes=[c_void_p]
        GetDllLibPdf().PdfSubmitAction_get_IncludeNoValueFields.restype=c_bool
        ret = GetDllLibPdf().PdfSubmitAction_get_IncludeNoValueFields(self.Ptr)
        return ret

    @IncludeNoValueFields.setter
    def IncludeNoValueFields(self, value:bool):
        GetDllLibPdf().PdfSubmitAction_set_IncludeNoValueFields.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfSubmitAction_set_IncludeNoValueFields(self.Ptr, value)

    @property
    def IncludeIncrementalUpdates(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether to submit form's incremental updates.
            Meaningful only when the form is being submitted in Forms Data Format.
            If set, the submitted FDF file includes the contents of all incremental 
            updates to the underlying PDF document. If clear, the incremental updates are 
            not included.
    </summary>
<value>
  <c>true</c> if incremental updates should be submitted; otherwise, <c>false</c>.
            </value>
        """
        GetDllLibPdf().PdfSubmitAction_get_IncludeIncrementalUpdates.argtypes=[c_void_p]
        GetDllLibPdf().PdfSubmitAction_get_IncludeIncrementalUpdates.restype=c_bool
        ret = GetDllLibPdf().PdfSubmitAction_get_IncludeIncrementalUpdates(self.Ptr)
        return ret

    @IncludeIncrementalUpdates.setter
    def IncludeIncrementalUpdates(self, value:bool):
        GetDllLibPdf().PdfSubmitAction_set_IncludeIncrementalUpdates.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfSubmitAction_set_IncludeIncrementalUpdates(self.Ptr, value)

    @property
    def IncludeAnnotations(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether to submit annotations.
            Meaningful only when the form is being submitted in Forms Data Format.
            If set, the submitted FDF file includes all markup annotations in the 
            underlying PDF document. If clear, markup annotations are not included.
    </summary>
<value>
  <c>true</c> if annotations should be submitted; otherwise, <c>false</c>.</value>
        """
        GetDllLibPdf().PdfSubmitAction_get_IncludeAnnotations.argtypes=[c_void_p]
        GetDllLibPdf().PdfSubmitAction_get_IncludeAnnotations.restype=c_bool
        ret = GetDllLibPdf().PdfSubmitAction_get_IncludeAnnotations(self.Ptr)
        return ret

    @IncludeAnnotations.setter
    def IncludeAnnotations(self, value:bool):
        GetDllLibPdf().PdfSubmitAction_set_IncludeAnnotations.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfSubmitAction_set_IncludeAnnotations(self.Ptr, value)

    @property
    def ExcludeNonUserAnnotations(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether to exclude non user annotations form submit 
            data stream. Meaningful only when the form is being submitted in Forms Data Format 
            and the  property is set to true.
    </summary>
<value>
  <c>true</c> if non user annotations should be excluded; otherwise, <c>false</c>.
            </value>
        """
        GetDllLibPdf().PdfSubmitAction_get_ExcludeNonUserAnnotations.argtypes=[c_void_p]
        GetDllLibPdf().PdfSubmitAction_get_ExcludeNonUserAnnotations.restype=c_bool
        ret = GetDllLibPdf().PdfSubmitAction_get_ExcludeNonUserAnnotations(self.Ptr)
        return ret

    @ExcludeNonUserAnnotations.setter
    def ExcludeNonUserAnnotations(self, value:bool):
        GetDllLibPdf().PdfSubmitAction_set_ExcludeNonUserAnnotations.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfSubmitAction_set_ExcludeNonUserAnnotations(self.Ptr, value)

    @property
    def EmbedForm(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether to include form to submit data stream.
            Meaningful only when the form is being submitted in Forms Data Format.
            If set, the  property is a file name containing an embedded file 
            stream representing the PDF file from which the FDF is being submitted.
    </summary>
<value>
  <c>true</c> if form should be embedded to submit stream; otherwise, <c>false</c>.</value>
        """
        GetDllLibPdf().PdfSubmitAction_get_EmbedForm.argtypes=[c_void_p]
        GetDllLibPdf().PdfSubmitAction_get_EmbedForm.restype=c_bool
        ret = GetDllLibPdf().PdfSubmitAction_get_EmbedForm(self.Ptr)
        return ret

    @EmbedForm.setter
    def EmbedForm(self, value:bool):
        GetDllLibPdf().PdfSubmitAction_set_EmbedForm.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfSubmitAction_set_EmbedForm(self.Ptr, value)

    @property

    def DataFormat(self)->'SubmitDataFormat':
        """
    <summary>
        Gets or sets the submit data format.
    </summary>
<value>The submit data format.</value>
        """
        GetDllLibPdf().PdfSubmitAction_get_DataFormat.argtypes=[c_void_p]
        GetDllLibPdf().PdfSubmitAction_get_DataFormat.restype=c_int
        ret = GetDllLibPdf().PdfSubmitAction_get_DataFormat(self.Ptr)
        objwraped = SubmitDataFormat(ret)
        return objwraped

    @DataFormat.setter
    def DataFormat(self, value:'SubmitDataFormat'):
        GetDllLibPdf().PdfSubmitAction_set_DataFormat.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfSubmitAction_set_DataFormat(self.Ptr, value.value)

    @property
    def Include(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether fields contained in Fields
            collection will be included for submitting.
    </summary>
<value>
  <c>true</c> if include; otherwise, <c>false</c>.</value>
<remarks>
            If Include property is true, only the fields in this collection will be submitted.
            If Include property is false, the fields in this collection are not submitted
            and only the remaining form fields are submitted.
            If the collection is null or empty, then all the form fields are reset
            and the Include property is ignored.
            If the field has Export property set to false it will be not included for 
            submitting in any case.
            </remarks>
        """
        GetDllLibPdf().PdfSubmitAction_get_Include.argtypes=[c_void_p]
        GetDllLibPdf().PdfSubmitAction_get_Include.restype=c_bool
        ret = GetDllLibPdf().PdfSubmitAction_get_Include(self.Ptr)
        return ret

    @Include.setter
    def Include(self, value:bool):
        GetDllLibPdf().PdfSubmitAction_set_Include.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfSubmitAction_set_Include(self.Ptr, value)

