str_description = """
    This module contains logic pertinent to the PACS setup "subsystem"
    of the `pfdcm` service.
"""

from    concurrent.futures  import  ProcessPoolExecutor, ThreadPoolExecutor, Future

from    fastapi             import  APIRouter, Query, Request
from    fastapi.encoders    import  jsonable_encoder
from    fastapi.concurrency import  run_in_threadpool
from    pydantic            import  BaseModel, Field
from    typing              import  Optional, List, Dict, Callable, Any

from    .jobController      import  jobber
import  asyncio
from    models              import  relayModel
import  os
from    datetime            import  datetime

import  json
import  pudb
from    pudb.remote         import set_trace
from    config              import settings
import  httpx

from    lib                 import map

import  sys
from    loguru              import logger
LOG             = logger.debug

logger_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> │ "
    "<level>{level: <5}</level> │ "
    "<yellow>{name: >28}</yellow>::"
    "<cyan>{function: <30}</cyan> @"
    "<cyan>{line: <4}</cyan> ║ "
    "<level>{message}</level>"
)
logger.remove()
logger.opt(colors = True)
logger.add(sys.stderr, format=logger_format)
LOG     = logger.info


threadpool: ThreadPoolExecutor      = ThreadPoolExecutor()
processpool: ProcessPoolExecutor    = ProcessPoolExecutor()

def noop():
    """
    A dummy function that does nothing.
    """
    return {
        'status':   True
    }

def logToStdout(description:str, d_log:dict) -> None:
    """
    Simply "write" the d_log to console stdout

    Args:
        d_log (dict): some dictionary to log
    """
    LOG("\n%s\n%s" % (description, json.dumps(d_log, indent =4)))

def logEvent(payload:relayModel.clientPayload, request: Request)-> dict:
    """
    Output an "input" log event

    Args:
        request (Request): the incoming request

    Returns:
        dict: a log event
    """
    timestamp = lambda : '%s' % datetime.now()
    d_logEvent:dict      = {
        '_timestamp'        : timestamp(),
        'requestHost'       : request.client.host,
        'requestPort'       : str(request.client.port),
        'requestUserAgent'  : request.headers['user-agent'],
        'payload'           : json.loads(payload.json())
    }
    return d_logEvent

def commsFailed_handle(URL:str, e:Exception) -> relayModel.clientResponseSchema:
    """
    Handle a failed comms state

    Args:
        e (Exception): the comms failure

    Returns:
        relayModel.clientResponseSchema: a response with appropriate failure
                                         conditions
    """
    failedClient:relayModel.clientResponseSchema    = relayModel.clientResponseSchema()
    failedClient.Status         = "Comms failure"
    failedClient.Progress       = "n/a"
    failedClient.ErrorWorkflow  = "n/a"
    errorResponse:relayModel.pflinkError            = relayModel.pflinkError()
    errorResponse.URL           = URL
    errorResponse.error         = str(e)
    errorResponse.help          = "Please check that the pflink URL is correct"
    failedClient.ErrorComms     = errorResponse
    return failedClient

async def relayAndEchoBack(
        payload             : relayModel.clientPayload,
        request             : Request,
        test                : bool
) -> relayModel.clientResponseSchema:
    """
    Parse the incoming payload, expand to pflink needs,
    transmit, and return remote response.

    Args:
        payload (relayModel.clientPayload): the relay payload

    Returns:
        dict: the reponse from the remote server

    """
    boundary:map.Map            = map.Map(name = 'Leg Length Analysis')
    d_logEvent:dict             = logEvent(payload, request)
    logToStdout("Incoming", d_logEvent)
    toPflink:relayModel.pflinkInput = boundary.intoPflink_transform(payload)
    logToStdout("Transmitting", json.loads(toPflink.json()))
    URL:str                     = settings.pflink.testURL if test else settings.pflink.prodURL
    toClient:relayModel.clientResponseSchema    = relayModel.clientResponseSchema()
    async with httpx.AsyncClient() as client:
        try:
            response: httpx.Response = await client.post(
                    URL,
                    data = toPflink.json()
            )
            logToStdout("Reply", response.json())
            toClient:relayModel.clientResponseSchema = boundary.fromPflink_transform(response)
            logToStdout("Return", json.loads(toClient.json()))
        except Exception as e:
            toClient:relayModel.clientResponseSchema = commsFailed_handle(URL, e)
        return toClient

