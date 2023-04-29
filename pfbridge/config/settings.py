import  os
from    pydantic    import BaseSettings
from    models      import relayModel

class Pflink(BaseSettings):
    prodURL:str             = 'http://localhost:8050/api/v1/workflow'
    testURL:str             = 'http://localhost:8050/api/v1/testing'

class DylldAnalysis(Pflink):
    pipelineName:str        = ''
    pluginName:str          = 'pl-dylld'
    pluginVersion:str       = '4.4.28'
    pluginArgs:str          = '--pattern **/*dcm --CUBEurl http://cube-next.tch.harvard.edu/api/v1/ --CUBEuser %usernameCUBE --CUBEpassword %passwordCUBE --orthancURL http://10.72.8.224:8042 --orthancuser %usernameOrthanc --orthancpassword %passwordOrthanc'
    clinicalUser:str        = '%usernameCUBE'
    feedName:str            = 'dylld-%SeriesInstanceUID'

class Vault(BaseSettings):
    locked:bool             = False
    vaultKey:str            = ''

class CredentialsCUBE(BaseSettings):
    usernameCUBE:str        = ''
    passwordCUBE:str        = ''

class CredentialsOrthanc(BaseSettings):
    usernameOrthanc:str     = ''
    passwordOrthanc:str     = ''

pflink              = Pflink()
analysis            = DylldAnalysis()
vault               = Vault()
credentialsCUBE     = CredentialsCUBE()
credentialsOrthanc  = CredentialsOrthanc()