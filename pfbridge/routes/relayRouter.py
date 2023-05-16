str_description = """
    This route module handles logic pertaining to associating
    routes to actual logic in the controller module. For the
    most part, this module mostly has route method defintions
    and UI swagger for documentation.

    In most methods, the actual logic is simply a call out
    to the real method in the controller module that performs
    the application logic.
"""


from    fastapi             import  APIRouter, Query, HTTPException, BackgroundTasks, Request
from    typing              import  List, Dict, Any, Union

from    models              import  relayModel, credentialModel
from    controllers         import  relayController
from    routes              import  credentialRouter

from    config              import  settings
from    pftag               import  pftag
import  pudb

router          = APIRouter()
router.tags     = ['Relay services']

@router.put(
    '/pflink/testURL/',
    response_model  = relayModel.pflinkURLs,
    summary         = '''
    PUT a new value for the pflink testing URL endpoint.
    '''
)
def testURL_update(URL:str) -> relayModel.pflinkURLs:
    """
    Description
    -----------

    Update the internal *testing* URL endpoint of the `pflink` controller.
    Note that any updates PUT here will *NOT* persist across restarts
    of `pfbridge` -- on restart these will revert to startup/environement
    settings.

    Args:
    -----
    * `URL` (str): A URL.

    Returns:
    --------
    * `relayModel.pflinkURLs`: the updated set of pflinks
    """
    settings.pflink.testURL         = URL
    update:relayModel.pflinkURLs    = relayModel.pflinkURLs()
    update.productionURL            = settings.pflink.prodURL
    update.testingURL               = settings.pflink.testURL
    update.authURL                  = settings.pflinkAuth.pflink_auth_url
    return update

@router.put(
    '/pflink/prodURL/',
    response_model  = relayModel.pflinkURLs,
    summary         = '''
    PUT a new value for the pflink testing URL endpoint.
    '''
)
def prodURL_update(URL:str) -> relayModel.pflinkURLs:
    """
    Description
    -----------

    Update the internal *production* URL endpoint of the `pflink` controller.
    Note that any updates PUT here will *NOT* persist across restarts
    of `pfbridge` -- on restart these will revert to startup/environement
    settings.

    Args:
    -----
    * `URL` (str): A URL.

    Returns:
    --------
    * `relayModel.pflinkURLs`: the updated set of pflinks
    """
    settings.pflink.prodURL         = URL
    update:relayModel.pflinkURLs    = relayModel.pflinkURLs()
    update.productionURL            = settings.pflink.prodURL
    update.testingURL               = settings.pflink.testURL
    update.authURL                  = settings.pflinkAuth.pflink_auth_url
    return update

@router.put(
    '/pflink/authURL/',
    response_model  = relayModel.pflinkURLs,
    summary         = '''
    PUT a new value for the pflink auth URL endpoint.
    '''
)
def authURL_update(URL:str) -> relayModel.pflinkURLs:
    """
    Description
    -----------

    Update the internal *auth token* URL endpoint of the `pflink` controller.
    Note that any updates PUT here will *NOT* persist across restarts
    of `pfbridge` -- on restart these will revert to startup/environement
    settings.

    Args:
    -----
    * `URL` (str): A URL.

    Returns:
    --------
    * `relayModel.pflinkURLs`: the updated set of pflinks
    """
    settings.pflinkAuth.pflink_auth_url         = URL
    update:relayModel.pflinkURLs                = relayModel.pflinkURLs()
    update.productionURL                        = settings.pflink.prodURL
    update.testingURL                           = settings.pflink.testURL
    update.authURL                              = settings.pflinkAuth.pflink_auth_url
    return update

@router.get(
    '/pflink/URLs/',
    response_model  = relayModel.pflinkURLs,
    summary         = '''
    GET the internal pflink URLs.
    '''
)
def urls_retFromModel() -> relayModel.pflinkURLs:
    """
    Description
    -----------

    Simply return the URLs to the `pfbridge` with which this
    `pflink` will communicate. These URLs are typically defined
    in the environment of `pfbridge`, but can also be set with
    an appropriate PUT. Note that runtime changes to these URLs
    are _NOT_ preserved on restart!

    Returns
    -------
    * `relayModel.pflinkURLs`: The model URLs
    """
    current:relayModel.pflinkURLs   = relayModel.pflinkURLs()
    current.productionURL           = settings.pflink.prodURL
    current.testingURL              = settings.pflink.testURL
    current.authURL                 = settings.pflinkAuth.pflink_auth_url
    return current

@router.get(
    '/service/URLs/',
    response_model  = relayModel.serviceURLs,
    summary         = '''
    GET the URLs for services such as CUBE and orthanc.
    '''
)
def serviceUrls_retFromModel() -> relayModel.serviceURLs:
    """
    Description
    -----------

    Simply return the serviceURLs, i.e. `CUBE` and `orthanc` URLs.

    These URLs are typically defined in the `pfbridge` environment,
    but can also be set with an appropriate PUT. Note that runtime
    changes to these URLs are _NOT_ preserved on restart!

    Returns
    -------
    * `relayModel.serviceURLs`: The model URLs
    """
    current:relayModel.serviceURLs  = relayModel.serviceURLs()
    current.urlCUBE                 = settings.serviceURLs.urlCUBE
    current.urlOrthanc              = settings.serviceURLs.urlOrthanc
    return current

@router.put(
    '/service/URL/CUBE/',
    response_model  = relayModel.serviceURLs,
    summary         = '''
    PUT a new value for the CUBE service URL.
    '''
)
def urlCUBE_update(URL:str) -> relayModel.serviceURLs:
    """
    Description
    -----------

    Update the internal CUBE URL endpoint.

    Note that any updates PUT here will *NOT* persist across restarts
    of `pfbridge` -- on restart these will revert to startup/environement
    settings.

    Args:
    -----
    * `URL` (str): A URL.

    Returns:
    --------
    * `relayModel.serviceURLs`: the updated set of service URLs
    """
    settings.serviceURLs.urlCUBE    = URL
    update:relayModel.serviceURLs   = relayModel.serviceURLs()
    update.urlCUBE                  = URL
    return update

@router.put(
    '/service/URL/Orthanc/',
    response_model  = relayModel.serviceURLs,
    summary         = '''
    PUT a new value for the Orthanc service URL.
    '''
)
def urlOrthanc_update(URL:str) -> relayModel.serviceURLs:
    """
    Description
    -----------

    Update the internal Orthanc URL endpoint.

    Note that any updates PUT here will *NOT* persist across restarts
    of `pfbridge` -- on restart these will revert to startup/environement
    settings.

    Args:
    -----
    * `URL` (str): A URL.

    Returns:
    --------
    * `relayModel.serviceURLs`: the updated set of service URLs
    """
    settings.serviceURLs.urlOrthanc = URL
    update:relayModel.serviceURLs   = relayModel.serviceURLs()
    update.urlOrthanc               = URL
    return update

@router.put(
    '/analysis/',
    response_model  = settings.DylldAnalysis,
    summary         = '''
    PUT internal Analysis settings.
    '''
)
def analysis_update(
    key     = '',
    value   = ''
) -> settings.DylldAnalysis:
    """
    Description
    -----------

    Simply update `analysis` settings class values -- key/value updates
    are specified in query parameters. Note that any changes to the base
    settings values are only valid in this running instance of `pfbridge`!
    Replicas will not be updated, nor will any changes persist post
    restart!

    Valid keys are:

    * `analysisPipelineName` -- the name of an analysis pipeline to run (unused)
    * `analysisPluginName` -- the name of the plugin to run
    * `analysisPluginArgs` -- args to pass to the plugin
    * `analysisPluginVersion` -- the plugin version to run
    * `clinicalUser` -- the name of the clinical user; this is the name within ChRIS.
    * `analysisFeedName`  -- the template feed name

    Returns
    -------
    * `settings.Analysis`: The current Analysis settings
    """
    match key:
        case 'analysisPipelineName':
            settings.analysis.pipelineName  = value
        case 'analysisPluginName':
            settings.analysis.pluginName    = value
        case 'analysisPluginArgs':
            settings.analysis.pluginArgs    = value
        case 'analysisPluginVersion':
            settings.analysis.pluginVersion = value
        case 'clinicalUser':
            settings.analysis.clinicalUser  = value
        case 'analysisFeedName':
            settings.analysis.feedName      = value
    return settings.analysis

@router.get(
    '/analysis/',
    response_model  = settings.DylldAnalysis,
    summary         = '''
    GET the internal Analysis settings.
    '''
)
def analysisValues_get(vaultKey:str = "") -> settings.DylldAnalysis:
    """
    Description
    -----------

    Simply return the `analysis` settings class values. If the optional
    `vaultKey` is provided, then unlock the vault and return any values
    with sensitive information decoded.

    Returns
    -------
    * `settings.Analysis`: The current Analysis settings
    """
    values:settings.DylldAnalysis   = settings.analysis
    if vaultKey:
        d_vaultAccess:credentialModel.credentialsStatus = credentialModel.credentialsStatus()
        d_vaultAccess = credentialRouter.credentialAccess_check(vaultKey)
        if d_vaultAccess.status:
            settings.analysis_decode()
            values = settings.analysisDecoded
    return values

@router.post(
    '/analyze/',
    response_model  = relayModel.clientResponseSchema,
    summary         = '''
    POST an image and analysis directive that is relayed (after some
    internal processing) to a remote service.
    '''
)
async def workflow_do(
    relayPayload    : relayModel.clientPayload,
    request         : Request,
    test:bool       = False
) -> relayModel.clientResponseSchema:
    """
    Description
    -----------

    Main API entry-point that controls an analysis on an image
    data set and immediately returns a status update to the
    caller. Multiple calls with the same payload return current
    status of the workflow (or its completion).

    Send a `?test=true` boolean query parameter to use the `pflink`
    test API that simply returns the progressive stages for a workflow.

    ```
    class clientPayload(BaseModel):
        imageMeta:dict                  = PACSqueryCore()
        analyzeFunction:str             = ''
    ```

    where imageMeta defines the DICOM tags specifying the image to
    analyze and the `analyzeFunction` the analysis to perform by
    the ChRIS system.

    ```
    class PACSqueryCore(BaseModel):
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
    ```

    A response on the status of the workflow is immediately returned.

    """
    # pudb.set_trace()
    d_ret:relayModel.clientResponseSchema = await relayController.relayAndEchoBack(
            relayPayload, request, test
    )
    return d_ret

