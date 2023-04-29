from    concurrent.futures  import  ProcessPoolExecutor, ThreadPoolExecutor, Future

from    fastapi             import  APIRouter, Query, Request
from    fastapi.encoders    import  jsonable_encoder
from    fastapi.concurrency import  run_in_threadpool
from    pydantic            import  BaseModel, Field
from    typing              import  Optional, List, Dict, Callable, Any

from    .jobController      import  jobber
import  asyncio
from    models              import  credentialModel
import  os
from    datetime            import  datetime

import  json
import  pudb
from    pudb.remote         import set_trace
from    config              import settings
import  httpx

from    lib                 import map

import  sys

def CUBElogin_set(
        payload             : credentialModel.credentials,
        request             : Request
) -> credentialModel.credentialsStatus:
    """
    Set the credentials for CUBE login

    Args:
        payload (credentialModel.credentials): the credentials model
        request (Request): client request data

    Returns:
        credentialModel.credentialsStatus: status of the setting operation
    """
    d_ret:credentialModel.credentialsStatus = credentialModel.credentialsStatus()
    settings.credentialsCUBE.usernameCUBE   = payload.username
    settings.credentialsCUBE.passwordCUBE   = payload.password
    d_ret.status                            = True
    d_ret.message                           = "CUBE credentials set successfully."
    return d_ret

def orthanclogin_set(
        payload             : credentialModel.credentials,
        request             : Request
) -> credentialModel.credentialsStatus:
    """
    Set the credentials for orthanc login

    Args:
        payload (credentialModel.credentials): the credentials model
        request (Request): client request data

    Returns:
        credentialModel.credentialsStatus: status of the setting operation
    """
    d_ret:credentialModel.credentialsStatus = credentialModel.credentialsStatus()
    settings.credentialsOrthanc.usernameOrthanc     = payload.username
    settings.credentialsOrthanc.passwordOrthanc     = payload.password
    d_ret.status                                    = True
    d_ret.message                                   = "Orthanc credentials set successfully."
    return d_ret
