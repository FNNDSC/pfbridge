import  os
from typing import Any
from    pydantic    import AnyHttpUrl, BaseSettings, AnyUrl
from    models      import relayModel
from    pftag       import pftag

class Pflink(BaseSettings):
    prodURL:str             = 'http://localhost:8050/api/v1/workflow'
    testURL:str             = 'http://localhost:8050/api/v1/testing'
    ignore_duplicate:bool   = True


class Analyses(BaseSettings):
    analyses: dict = {}

class DylldAnalysis(Pflink):
    pipelineName:str        = ''
    pluginName:str          = ''
    pluginVersion:str       = ''
    pluginArgs:str          = ''
    feedName:str            = 'pfbridge-%SeriesInstanceUID'

class PflinkAuth(Pflink):
    pflink_auth_url:str = "http://localhost:8050/api/v1/auth-token"
    pflink_username:str = "pflink"
    pflink_password:str = "pflink1234"
    token:str           = "invalid"  # will be generated while making POST request to pflink

class Pfdcm(BaseSettings):
    name:str            = "PFDCMLOCAL"
    PACSname:str        = "orthanc"
    CUBEandSwiftKey:str = "local"

class ServiceURLs(BaseSettings):
    urlCUBE:str             = "http://localhost:8000/api/v1/"
    urlOrthanc:str          = "http://localhost:8888"

class Vault(BaseSettings):
    locked:bool             = False
    vaultKey:str            = ''

class CredentialsCUBE(BaseSettings):
    usernameCUBE:str        = 'chris'
    passwordCUBE:str        = 'chris1234'

class CredentialsOrthanc(BaseSettings):
    usernameOrthanc:str     = ''
    passwordOrthanc:str     = ''

def vaultCheckLock(vault:Vault) -> None:
    if vault.vaultKey and not vault.locked:
        vault.locked        = True
        print("Vault check: key has already been set. Vault is now LOCKED.")

def analysis_decode(key:str) -> None:
    decode:pftag.Pftag  = pftag.Pftag({})
    addDict:bool = decode.lookupDict_add(
        [
            {
                'CUBE': {
                    'usernameCUBE': credentialsCUBE.usernameCUBE,
                    'passwordCUBE': credentialsCUBE.passwordCUBE,
                    'urlCUBE':      serviceURLs.urlCUBE
                }
            },
            {
                'orthanc': {
                    'usernameOrthanc':  credentialsOrthanc.usernameOrthanc,
                    'passwordOrthanc':  credentialsOrthanc.passwordOrthanc,
                    'urlOrthanc':       serviceURLs.urlOrthanc
                }
            },
            {
                'ignore': {
                    'time': '%timestamp'
                }
            }
        ]
    )
    for field in ["pluginArgs", "pipelineName", "pluginName", "feedName", "pluginVersion"]:
        d_decode:dict = decode(analyses.analyses[key].__getattribute__(field))
        analysisDecoded.__setattr__(field, d_decode["result"])

pflink              = Pflink()
analysis            = DylldAnalysis()
analysisDecoded     = DylldAnalysis()
vault               = Vault()
credentialsCUBE     = CredentialsCUBE()
credentialsOrthanc  = CredentialsOrthanc()
serviceURLs         = ServiceURLs()
pflinkAuth          = PflinkAuth()
pfdcm               = Pfdcm()
analyses            = Analyses()
analyses.analyses["dylld"] = analysisDecoded


