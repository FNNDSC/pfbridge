import  os
from typing import Any
from    pydantic    import AnyHttpUrl, BaseSettings, AnyUrl
from    models      import relayModel
from    pftag       import pftag

class Pflink(BaseSettings):
    prodURL:str             = 'http://localhost:8050/api/v1/workflow'
    testURL:str             = 'http://localhost:8050/api/v1/testing'

class DylldAnalysis(Pflink):
    pipelineName:str        = ''
    pluginName:str          = 'pl-dylld'
    pluginVersion:str       = '4.4.28'
    pluginArgs:str          = '--pattern **/*dcm --CUBEurl %urlCUBE --CUBEuser %usernameCUBE --CUBEpassword %passwordCUBE --orthancURL %urlOrthanc --orthancuser %usernameOrthanc --orthancpassword %passwordOrthanc'
    clinicalUser:str        = '%usernameCUBE'
    feedName:str            = 'dylld-%SeriesInstanceUID'

class PflinkAuth(Pflink):
    pflink_auth_url:str = "http://localhost:8050/api/v1/auth-token"
    pflink_username:str = "pflink"
    pflink_password:str = "pflink1234"
    token:str           = "" # will be generated while making POST request to pflink


class ServiceURLs(BaseSettings):
    urlCUBE:str             = "http://localhost:8000/api/v1/"
    urlOrthanc:str          = "http://localhost:8888"

class Vault(BaseSettings):
    locked:bool             = False
    vaultKey:str            = ''

class CredentialsCUBE(BaseSettings):
    usernameCUBE:str        = ''
    passwordCUBE:str        = ''

class CredentialsOrthanc(BaseSettings):
    usernameOrthanc:str     = ''
    passwordOrthanc:str     = ''

def vaultCheckLock(vault:Vault) -> None:
    if vault.vaultKey and not vault.locked:
        vault.locked        = True
        print("Vault check: key has already been set. Vault is now LOCKED.")

def analysis_decode() -> None:
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
            }
        ]
    )
    for field in ['pluginArgs', 'clinicalUser']:
        d_decode:dict = decode(analysis.__getattribute__(field))
        if d_decode['status']:
            analysisDecoded.__setattr__(field, d_decode['result'])

pflink              = Pflink()
analysis            = DylldAnalysis()
analysisDecoded     = DylldAnalysis()
vault               = Vault()
credentialsCUBE     = CredentialsCUBE()
credentialsOrthanc  = CredentialsOrthanc()
serviceURLs         = ServiceURLs()
pflinkAuth          = PflinkAuth()