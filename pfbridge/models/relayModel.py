str_description = """

    The data models/schemas for comms with `pfbridge`.

"""

from    pydantic            import BaseModel, Field
from    typing              import Optional, List, Dict, Any
from    datetime            import datetime
from    enum                import Enum
from    pathlib             import Path
import  pudb
from    config              import settings


class pacsService(BaseModel):
    """Name of the PACS service provider"""
    provider:str                    = settings.pfdcm.PACSname
class pfdcmService(BaseModel):
    """Name of the PFDCM service provider -- relevant to ChRIS"""
    provider:str                    = settings.pfdcm.name

class CUBEandSwiftKey(BaseModel):
    """Lookup key for CUBE and swift information -- relevant to ChRIS"""
    key:str                         = settings.pfdcm.CUBEandSwiftKey

class db(BaseModel):
    """Path of the ChRIS managed PACS filesystem database"""
    path:str                        = '/home/dicom/log'

class DICOMfile(BaseModel):
    """Explicit extention of DICOMS -- relevant to ChRIS"""
    extension:str                   = 'dcm'

class pfdcmInfo(BaseModel):
    pfdcm_service:str               = pfdcmService().provider
    PACS_service:str                = pacsService().provider
    cube_service:str                = CUBEandSwiftKey().key
    swift_service:str               = CUBEandSwiftKey().key
    dicom_file_extension:str        = DICOMfile().extension
    db_log_path:str                 = db().path

class PACSqueryCore(BaseModel):
    """The PACS Query model"""
    AccessionNumber                     : str   = ""
    PatientID                           : str   = ""
    PatientName                         : str   = ""
    PatientBirthDate                    : str   = ""
    PatientAge                          : str   = ""
    PatientSex                          : str   = ""
    StudyDate                           : str   = ""
    StudyDescription                    : str   = ""
    StudyInstanceUID                    : str   = ""
    Modality                            : str   = ""
    ModalitiesInStudy                   : str   = ""
    PerformedStationAETitle             : str   = ""
    NumberOfSeriesRelatedInstances      : str   = ""
    InstanceNumber                      : str   = ""
    SeriesDate                          : str   = ""
    SeriesDescription                   : str   = ""
    SeriesInstanceUID                   : str   = ""
    ProtocolName                        : str   = ""
    AcquisitionProtocolDescription      : str   = ""
    AcquisitionProtocolName             : str   = ""

class analysisModel(BaseModel):
    feed_name:str                  = ""
    plugin_name:str                = ""
    plugin_version:str             = ""
    plugin_params:str              = ""
    pipeline_name:str              = ""

class cubeUserModel(BaseModel):
    username:str                   = settings.credentialsCUBE.usernameCUBE
    password:str                   = settings.credentialsCUBE.passwordCUBE

class pflinkInput(BaseModel):
    ignore_duplicate:bool           = settings.pflink.ignore_duplicate
    pfdcm_info:pfdcmInfo            = pfdcmInfo()
    PACS_directive:PACSqueryCore    = PACSqueryCore()
    workflow_info:analysisModel     = analysisModel()
    cube_user_info:cubeUserModel    = cubeUserModel()

class clientPayload(BaseModel):
    imageMeta:PACSqueryCore         = PACSqueryCore()
    analyzeFunction:str             = ''

class pflinkError(BaseModel):
    """
    A model returned when a pflink connection error has been flagged
    """
    error:str                       = ""
    URL:str                         = ""
    help:str                        = ""

class pflinkURLs(BaseModel):
    productionURL:str               = settings.pflink.prodURL
    testingURL:str                  = settings.pflink.testURL
    authURL:str                     = settings.pflinkAuth.pflink_auth_url

class serviceURLs(BaseModel):
    urlCUBE:str                     = settings.serviceURLs.urlCUBE
    urlOrthanc:str                  = settings.serviceURLs.urlOrthanc

class pflinkResponseSchema(BaseModel):
    """
    The Workflow status response model. This is the return from pflink.
    """
    status: bool                    = False
    workflow_state: str             = ""
    state_progress: str             = "0%"
    feed_id: str                    = ""
    feed_name: str                  = ""
    message: str                    = ""
    duplicates: list[dict]          = None
    error: str                      = ""
    workflow_progress_perc: int     = 0

class clientResponseSchema(BaseModel):
    """
    The response ultimately received by the client. This is a modified
    subset of the pflinkResponseSchema
    """
    Status:bool                     = False
    State:str                       = ''
    ProgressPerc:int                = 0
    ErrorWorkflow:str               = ''
    ModelViolation:Any              = None
    ErrorComms:pflinkError          = pflinkError()
