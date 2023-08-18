import os
SPIRE_PRODUCTNAME = ['SPIRE']

def MODIFY_SPIRE_PRODUCTNAME(new_string:str):
    global SPIRE_PRODUCTNAME
    SPIRE_PRODUCTNAME[0] = new_string

def USE_SPIRE_PRODUCTNAME()->str:
    global SPIRE_PRODUCTNAME
    return SPIRE_PRODUCTNAME[0]
#"PDF"
#"XLS"
#"DOC"
#"PRESENTATION"

def GETSPIREPRODUCT(f:str):
    parent_directory = os.path.dirname(f)
    grandparent_directory = os.path.dirname(parent_directory)
    MODIFY_SPIRE_PRODUCTNAME(os.path.basename(grandparent_directory).upper())
    return USE_SPIRE_PRODUCTNAME()
