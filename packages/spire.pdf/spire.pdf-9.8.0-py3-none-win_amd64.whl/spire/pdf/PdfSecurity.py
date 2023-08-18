from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfSecurity (SpireObject) :
    """
    <summary>
        Represents the security settings of the PDF document.
    </summary>
    """
    @property

    def OwnerPassword(self)->str:
        """
    <summary>
        Gets the owner password.
    </summary>
        """
        GetDllLibPdf().PdfSecurity_get_OwnerPassword.argtypes=[c_void_p]
        GetDllLibPdf().PdfSecurity_get_OwnerPassword.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfSecurity_get_OwnerPassword(self.Ptr))
        return ret


    @property

    def UserPassword(self)->str:
        """
    <summary>
        Gets the user password.
    </summary>
        """
        GetDllLibPdf().PdfSecurity_get_UserPassword.argtypes=[c_void_p]
        GetDllLibPdf().PdfSecurity_get_UserPassword.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfSecurity_get_UserPassword(self.Ptr))
        return ret


    @property
    def OriginalEncrypt(self)->bool:
        """
    <summary>
        Indicate whether this pdf document was encrypted originally or not. 
    </summary>
        """
        GetDllLibPdf().PdfSecurity_get_OriginalEncrypt.argtypes=[c_void_p]
        GetDllLibPdf().PdfSecurity_get_OriginalEncrypt.restype=c_bool
        ret = GetDllLibPdf().PdfSecurity_get_OriginalEncrypt(self.Ptr)
        return ret

    @dispatch
    def DecryptUserPassWord(self):
        """
    <summary>
        Decrypt user password
    </summary>
        """
        GetDllLibPdf().PdfSecurity_DecryptUserPassWord.argtypes=[c_void_p]
        GetDllLibPdf().PdfSecurity_DecryptUserPassWord(self.Ptr)

    @dispatch

    def DecryptUserPassWord(self ,ownerPassword:str):
        """
    <summary>
        Decrypt user password.
    </summary>
    <param name="ownerPassword">The ownerPassword</param>
        """
        
        GetDllLibPdf().PdfSecurity_DecryptUserPassWordO.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfSecurity_DecryptUserPassWordO(self.Ptr, ownerPassword)


    def DecryptOwnerPassWord(self ,ownerPassword:str):
        """
    <summary>
        Decrypt all password.
    </summary>
    <param name="ownerPassword">The ownerPassword</param>
        """
        
        GetDllLibPdf().PdfSecurity_DecryptOwnerPassWord.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfSecurity_DecryptOwnerPassWord(self.Ptr, ownerPassword)

    @dispatch

    def Encrypt(self ,openPassword:str):
        """
    <summary>
        To Encrypt the PDF document with open password.
            Note:If set empty string value to open password, it indicates that the PDF document can be operated without providing corresponding password. 
            Note: the document owner password should not be exist.
    </summary>
    <param name="openPassword">The open password</param>
        """
        
        GetDllLibPdf().PdfSecurity_Encrypt.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfSecurity_Encrypt(self.Ptr, openPassword)

    @dispatch

    def Encrypt(self ,permissionPassword:str,permissions:PdfPermissionsFlags):
        """
    <summary>
        To Encrypt the PDF document with permission password and permissions.
            Note:The Permission password can't be empty string.
    </summary>
    <param name="permissionPassword">The permission password</param>
    <param name="permissions">A set of flags specifying which operations are permitted when the document is opened with user access</param>
        """
        enumpermissions:c_int = permissions.value

        GetDllLibPdf().PdfSecurity_EncryptPP.argtypes=[c_void_p ,c_wchar_p,c_int]
        GetDllLibPdf().PdfSecurity_EncryptPP(self.Ptr, permissionPassword,enumpermissions)

    @dispatch

    def Encrypt(self ,openPassword:str,permissionPassword:str,permissions:PdfPermissionsFlags,keySize:PdfEncryptionKeySize):
        """
    <summary>
        To Encrypt the PDF document and set the encryption key size and permissions.
            Note:If set empty string value to open password or permission password, it indicates that the PDF document can be operated without providing corresponding password. 
    </summary>
    <param name="openPassword">The open password</param>
    <param name="permissionPassword">The permission password</param>
    <param name="permissions">A set of flags specifying which operations are permitted when the document is opened with user access</param>
    <param name="keySize">The bit length of the encryption key</param>
    <returns></returns>
        """
        enumpermissions:c_int = permissions.value
        enumkeySize:c_int = keySize.value

        GetDllLibPdf().PdfSecurity_EncryptOPPK.argtypes=[c_void_p ,c_wchar_p,c_wchar_p,c_int,c_int]
        GetDllLibPdf().PdfSecurity_EncryptOPPK(self.Ptr, openPassword,permissionPassword,enumpermissions,enumkeySize)

    @dispatch

    def Encrypt(self ,openPassword:str,permissionPassword:str,permissions:PdfPermissionsFlags,keySize:PdfEncryptionKeySize,originalPermissionPassword:str):
        """
    <summary>
        To Encrypt the PDF document with open password and permission password,and set the encryption key size and permissions.
            Note:If set empty string value to open password or permission password, it indicates that the PDF document can be operated without providing corresponding password. 
    </summary>
    <param name="openPassword">The open password</param>
    <param name="permissionPassword">The permission password</param>
    <param name="permissions">A set of flags specifying which operations are permitted when the document is opened with user access</param>
    <param name="keySize">The bit length of the encryption key</param>
    <param name="originalPermissionPassword">The original permissionPassword of the document</param>
        """
        enumpermissions:c_int = permissions.value
        enumkeySize:c_int = keySize.value

        GetDllLibPdf().PdfSecurity_EncryptOPPKO.argtypes=[c_void_p ,c_wchar_p,c_wchar_p,c_int,c_int,c_wchar_p]
        GetDllLibPdf().PdfSecurity_EncryptOPPKO(self.Ptr, openPassword,permissionPassword,enumpermissions,enumkeySize,originalPermissionPassword)

    @property

    def Permissions(self)->'PdfPermissionsFlags':
        """
    <summary>
        Gets the document's permission flags
    </summary>
        """
        GetDllLibPdf().PdfSecurity_get_Permissions.argtypes=[c_void_p]
        GetDllLibPdf().PdfSecurity_get_Permissions.restype=c_int
        ret = GetDllLibPdf().PdfSecurity_get_Permissions(self.Ptr)
        objwraped = PdfPermissionsFlags(ret)
        return objwraped

    @property

    def KeySize(self)->'PdfEncryptionKeySize':
        """
    <summary>
        Gets the size of the key.
    </summary>
        """
        GetDllLibPdf().PdfSecurity_get_KeySize.argtypes=[c_void_p]
        GetDllLibPdf().PdfSecurity_get_KeySize.restype=c_int
        ret = GetDllLibPdf().PdfSecurity_get_KeySize(self.Ptr)
        objwraped = PdfEncryptionKeySize(ret)
        return objwraped

