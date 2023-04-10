str_description = """
    The main module for the service handler/system.

    This essentially creates the fastAPI app and adds
    route handlers.
"""

from    fastapi                 import FastAPI
from    fastapi.middleware.cors import CORSMiddleware
from    base.router             import helloRouter_create

from    routes.relayRouter      import router   as relay_router

from    os                      import path

import  pudb

with open(path.join(path.dirname(path.abspath(__file__)), 'ABOUT')) as f:
    str_about:str       = f.read()

with open(path.join(path.dirname(path.abspath(__file__)), 'VERSION')) as f:
    str_version:str     = f.read().strip()

tags_metadata:list = [
    {
        "name"          :   "Relay services",
        "description"   :
            """
            Provide simple API endpoints that will serve as relays for client
            payloads. These payloads are "repacked" and relayed along, while
            downstream replies are returned to the original client after some
            simplifcation.
            """
    },
    {
        "name"          :   "pfbridge environmental detail",
        "description"   :
            """
            Provide API GET endpoints that provide information about the
            service itself and the compute environment in which the service
            is deployed.
            """
    }
    ]

app = FastAPI(
    title           = 'pfbridge',
    version         = str_version,
    openapi_tags    = tags_metadata
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "OPTIONS"],
    allow_headers=["*"],
)

hello_router = helloRouter_create(
    name            = 'pfbridge_hello',
    version         = str_version,
    about           = str_about
)

app.include_router( relay_router,
                    prefix  = '/api/v1')

app.include_router( hello_router,
                    prefix  = '/api/v1')
