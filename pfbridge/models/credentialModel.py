str_description = """

    Data models/schemas for housing potentially sensitive information.

    Each model contains a "vaultKey" -- akin to a password -- that needs
    to be passed to the API in order to GET/PUT any data in these models.

    This approach is not airtight.

"""

from    pydantic            import BaseModel, Field
from    typing              import Optional, List, Dict, Any
from    datetime            import datetime
from    enum                import Enum
from    pathlib             import Path
import  pudb
from    config              import settings

class vaultKey(BaseModel):
    """
    Simply a "key" and a "value"
    """
    vaultKey:str                    = ""

class vaultStatus(BaseModel):
    locked:bool                     = False
    description:str                 = "unlocked"

class credentialsStatus(BaseModel):
    status:bool                     = False
    message:str                     = ""

class credentials(BaseModel):
    """
    A simple class to hold sensitive data, including the
    usernames and passwords for various backend services.

    This is not by default super secure, and read/write
    access is governed by the `vaultKey`.

    Access (GET/PUT) to the usernames and passwords needs
    a `vaultKey` token passed in the URL. This `vaultKey`
    is empty on startup, and needs to be set _once_. Once
    set it cannot be retrieved, but can be reset in the API.
    """
    username:str                    = ""
    password:str                    = ""

