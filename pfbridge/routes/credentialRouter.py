from    fastapi             import  APIRouter, Query, HTTPException, BackgroundTasks, Request
from    typing              import  List, Dict, Any

from    models              import  credentialModel
from    controllers         import  credentialController

from    config              import  settings

import  pudb

router          = APIRouter()
router.tags     = ['Credentialling services']

@router.put(
    '/vaultKey/',
    response_model  = credentialModel.vaultStatus,
    summary         = '''
    PUT a new vault key.
    '''
)
def vaultKey_set(key:str) -> credentialModel.vaultStatus:
    """
    Description
    -----------

    A vault `key` is simply a string (like a password), and can be set with
    a call to this API endpoint.

    Note that a vault key can only be set _once_, and once set cannot be reset
    without a server restart. All subsequent calls to "priviledged" data
    structures (like user credentialling) need to supply the vaultKey to unlock
    the data.

    Args:
    -----
    * `key` (str): A key string.

    Returns:
    --------
    * `credentialModel.vaultStatus`: a status response.
    """
    vaultStatus     = credentialModel.vaultStatus()
    if settings.vault.locked:
        vaultStatus.locked          = True
        vaultStatus.description     = "The vault is already locked and you cannot set a new key. Restart the server to reset."
    else:
        settings.vault.vaultKey     = key
        settings.vault.locked       = True
        vaultStatus.locked          = True
        vaultStatus.description     = "The vault is now locked. Use the vaultKey to access priviledged data."
    return vaultStatus

@router.get(
    '/vaultKey/',
    response_model  = credentialModel.vaultStatus,
    summary         = '''
    Return the vault status.
    '''
)
def vaultKey_statusGet() -> credentialModel.vaultStatus:
    """
    Description
    -----------

    Simply return the status of the vault. This will inform the client
    if the vault is locked (and has a key), or if the vault is unlocked
    and so a key can be specified.

    Returns
    -------
    * `credentialModel.vaultStatus`: a status response.
    """
    vaultStatus     = credentialModel.vaultStatus()
    if settings.vault.locked:
        vaultStatus.locked          = True
        vaultStatus.description     = "The vault is already locked. Restart the server to reset."
    else:
        vaultStatus.locked          = False
        vaultStatus.description     = "The vault is unlocked. You can set a key ONCE."
    return vaultStatus

def credentialAccess_check(vaultKey:str) \
    -> credentialModel.credentialsStatus:
    d_status:credentialModel.credentialsStatus = credentialModel.credentialsStatus()
    if not settings.vault.locked:
        d_status.status     = False
        d_status.message    = "The vault has not been locked and no key set. No access is possible."
    elif vaultKey != settings.vault.vaultKey:
        d_status.status     = False
        d_status.message    = "Incorrect vaultKey! No access is possible."
    else:
        d_status.status     = True
        d_status.message    = "vaultKey OK!"
    return d_status

@router.post(
    '/credentials/CUBE/',
    response_model  = credentialModel.credentialsStatus,
    summary         = '''
    POST a set of login credentials for CUBE
    '''
)
def CUBElogin_set(
    credentials     : credentialModel.credentials,
    request         : Request,
    vaultKey:str    = ''
) -> credentialModel.credentialsStatus:
    """
    Description
    -----------
    Set (override) the username and password for logging into CUBE. In order to
    actually perform the operation, the correct `vaultKey` must be passed.

    """
    d_ret:credentialModel.credentialsStatus = credentialModel.credentialsStatus()
    d_ret = credentialAccess_check(vaultKey)
    if not d_ret.status: return d_ret

    d_ret = credentialController.CUBElogin_set(
        credentials, request
    )
    return d_ret

@router.get(
    '/credentials/CUBE/',
    # For not well understood reasons, adding this response model will only ever
    # return the first model even if the second is explicitly returned.
    # response_model  = credentialModel.credentials | credentialModel.credentialsStatus,
    summary         = '''
    Return the CUBE login credentials (or status on failure).
    '''
)
def CUBElogin_get(
    vaultKey:str = ""
) -> credentialModel.credentialsStatus | credentialModel.credentials:
    """
    Description
    -----------

    Return the CUBE login credentials.

    Returns
    -------
    * `credentialModel.vaultStatus`: a status response.
    """
    d_status:credentialModel.credentialsStatus  = credentialModel.credentialsStatus()
    d_credentials:credentialModel.credentials   = credentialModel.credentials()
    d_status = credentialAccess_check(vaultKey)
    if not d_status.status: return d_status

    d_credentials.username  = settings.credentialsCUBE.usernameCUBE
    d_credentials.password  = settings.credentialsCUBE.passwordCUBE
    return d_credentials

@router.post(
    '/credentials/Orthanc/',
    response_model  = credentialModel.credentialsStatus,
    summary         = '''
    POST a set of login credentials for Orthanc
    '''
)
def orthanclogin_set(
    credentials     : credentialModel.credentials,
    request         : Request,
    vaultKey:str    = ''
) -> credentialModel.credentialsStatus:
    """
    Description
    -----------
    Set (override) the username and password for logging into CUBE. In order to
    actually perform the operation, the correct `vaultKey` must be passed.

    """
    d_ret:credentialModel.credentialsStatus = credentialModel.credentialsStatus()
    d_ret = credentialAccess_check(vaultKey)
    if not d_ret.status: return d_ret

    d_ret = credentialController.orthanclogin_set(
        credentials, request
    )
    return d_ret

@router.get(
    '/credentials/Orthanc/',
    # For not well understood reasons, adding this response model will only ever
    # return the first model even if the second is explicitly returned.
    # response_model  = credentialModel.credentials | credentialModel.credentialsStatus,
    summary         = '''
    Return the Orthanc login credentials (or status on failure).
    '''
)
def orthanclogin_get(
    vaultKey:str = ""
) -> credentialModel.credentialsStatus | credentialModel.credentials:
    """
    Description
    -----------

    Return the CUBE login credentials.

    Returns
    -------
    * `credentialModel.vaultStatus`: a status response.
    """
    d_status:credentialModel.credentialsStatus  = credentialModel.credentialsStatus()
    d_credentials:credentialModel.credentials   = credentialModel.credentials()
    d_status = credentialAccess_check(vaultKey)
    if not d_status.status: return d_status

    d_credentials.username  = settings.credentialsOrthanc.usernameOrthanc
    d_credentials.password  = settings.credentialsOrthanc.passwordOrthanc
    return d_credentials

