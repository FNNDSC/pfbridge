# `pfbridge`

[![Build](https://github.com/FNNDSC/pfbridge/actions/workflows/build.yml/badge.svg)](https://github.com/FNNDSC/pfbridge/actions/workflows/build.yml)

*a rather simple relay bridge between two communicating entities -- intended as a translator within the ChRIS ecosystem between a clinical service and a CUBE controlling service*

## Abstract

`pfbridge` was developed to "bridge" communication between one service to another. On one side, an origin point is a program or service that has some basic metadata that defines a _function_ to apply to some _data_. The "data" in this case is typically some medical image defined by a set of DICOM tags, and the "function" to apply is the name of a set of operations that are ultimately managed by CUBE. Controlling CUBE and shepherding its progress is a controller service called `pflink`. The `pflink` API requires more verbose data that is not really relevant to the original service -- for example a typical `pflink` payload contains information about several other services that are of no concern or interest to the originator.

Thus, `pfbridge` was conceived as a intermediary to buffer the originator from implementation details of concern. It accepts a much reduced `http` `POST` body, and repackages this body into the more detailed `pflink` body. Then, `pfbridge` transmits (or relays) this to `pflink` and captures the `pflink` response. Before returning this response to the original caller, `pfbridge` simplifies the response to return only success and status (and possible error) information.

## JSON input to `pfbridge`

A client calls the appropriate `pfbridge` API endpont (`/api/v1/analyze/`) with a `POST` modeled by

```json
{
  "imageMeta": {
    "AccessionNumber": "",
    "PatientID": "",
    "PatientName": "",
    "PatientBirthDate": "",
    "PatientAge": "",
    "PatientSex": "",
    "StudyDate": "",
    "StudyDescription": "",
    "StudyInstanceUID": "",
    "Modality": "",
    "ModalitiesInStudy": "",
    "PerformedStationAETitle": "",
    "NumberOfSeriesRelatedInstances": "",
    "InstanceNumber": "",
    "SeriesDate": "",
    "SeriesDescription": "",
    "SeriesInstanceUID": "",
    "ProtocolName": "",
    "AcquisitionProtocolDescription": "",
    "AcquisitionProtocolName": ""
  },
  "analyzeFunction": ""
}
```

The `imageMeta` contains fields corresponding to DICOM tag keys that are used to query a PACS for an image (or image set) to analyze with the named `analyzeFunction`. Only `imageMeta` fields that relevant to a particular image need be explicitly specified, so for example:

```json
{
  "imageMeta": {
    "StudyInstanceUID": "123456789",
    "SeriesInstanceUID": "123456789",
  },
  "analyzeFunction": "dylld"
}
```

Will apply the `dylld` `analyzeFunction` to the image with the specified `StudyInstanceUID` and `SeriesInstanceUID`.

## JSON return from `pfbridge`

After `pfbridge` relays this JSON to `pflink`, it returns to the caller:

```json
{
  "Status": true|false,
  "State": "",
  "Progress": "%",
  "ErrorWorkflow": "",
  "ModelViolation": null,
  "ErrorComms": {
    "error": "",
    "URL": "",
    "help": ""
  }
}
```

The `Status` is a `boolean` on the status of the workflow. If it has failed, i.e. `false`, then the client should examine the `ErrorWorkflow` and `ErrorComms`. If is operational, i.e. `true`, then the client can read the current state of analysis in `State` with a `Progress` showing the progress within that state as a percentage, for example

```json
{
  "Status": true,
  "State": "Registering image to ChRIS",
  "Progress": "50%",
  "ErrorWorkflow": "",
  "ModelViolation": null,
  "ErrorComms": {
    "error": "",
    "URL": "",
    "help": ""
  }
}
```

## Getting and using

### Build

Build the latest docker image

```bash
# Pull repo...
gh repo clone FNNDSC/pfbridge
# Enter the repo...
cd pfbridge

# Set some vars
set UID (id -u) # THIS IF FOR FISH SHELLs
# export UID=$(id -u)  # THIS IS FOR BASH SHELLs
export PROXY="http://10.41.13.4:3128"

# Here we build an image called local/pfbridge
# Using --no-cache is a good idea to force the image to build all from scratch
docker build --no-cache --build-arg http_proxy=$PROXY --build-arg UID=$UID -t local/pfbridge .

# If you're not behind a proxy, then
docker build --no-cache --build-arg UID=$UID -t local/pfbridge .
```

## Deploy as background process

Several `pfbridge` runtime variables can be set at start time, as defined by these models:

```python
class Pflink(BaseSettings):
    prodURL:str             = 'http://localhost:8050/workflow/'
    testURL:str             = 'http://localhost:8050/testing/'

class DylldAnalysis(Pflink):
    pluginName:str          = 'pl-dylld'
    pluginArgs:str          = ''
    clinicalUser:str        = 'radstar'
    feedName:str            = 'dylld-%SeriesInstanceUID'
```

These can be set at start time by passing them in the environment to `docker`. Note the settings class reads environment variables in a case insensitive manner.

```bash
# Set the workflow and testing URLs of the pflink instance
# to which we are bridging
export PRODURL=http://localhost:8050/workflow
export TESTURL=http://localhost:8050/testing

# For daemon, or background mode:
docker run --env PRODURL=$PRODURL --env TESTURL=$TESTURL                        \
               --name pfbridge  --rm -it  -d                                    \
               -p 33333:33333                                                   \
               local/pfbridge /start-reload.sh
```

### "Hello, `pfbridge`, you're looking good"

Using [httpie](https://httpie.org/), let's ask `pfbridge` about itself


```bash
http :33333/api/v1/about/
```

and say `hello` with some info about the system on which `pfbridge` is running:

```bash
http :33333/api/v1/hello/ echoBack=="Hello, World!"
```

For full exemplar documented examples, see `pfbridge/workflow.sh` in this repository as well as `HOWTORUN`. Also consult the `pfbridge/pfbridge.sh` script for more details.

### API swagger

Full API swagger is available. Once you have started `pfbridge`, and assuming that the machine hosting the container is `localhost`, navigate to [http://localhost:33333/docs](http://localhost:33333/docs) .


## Development

To debug code within `pfbridge` from a containerized instance, perform volume mappings in an interactive session:

```bash
# Set the workflow and testing URLs of the pflink instance
# to which we are bridging
export PRODURL=http://localhost:8050/workflow
export TESTURL=http://localhost:8050/testing

# Run with support for source debugging
docker run --name pfbridge  --rm -it                                              	\
        -p 33333:33333 	                                                                \
        -v $PWD/pfbridge:/app:ro                                                  	\
        local/pfbridge /start-reload.sh
```

## Using the helper `workflow.sh` script commands

The `workflow.sh` script can be sourced in `bash`/`zsh` to provide full CLI helper functions for complete access to the API.

```bash
cd pfbridge/pfbridge
# Assuming bash/zsh:
source workflow.sh
```
The following commands are defined:

* `pflinkURLs_get`: Get the `pflink` links.
* `testURL_set <URL>`: Set the `pflink` test URL.
* `prodURL_set <URL>`: Set the `pflink` production URL.
* `analysis_get`: Get the `analysis` relevant data.
* `analysis_set <key> <value>`: Set `analysis` relevant data.
* `relay <type> <StudyInstanceUID> <SeriesInstanceUID>`: Relay an analysis to perform.

## Tests

Proper tests coming soon. For now you can use the `workflow.sh` script to do some rudimentary testing. Successive calls to `relay test <study> <series>` will return to the caller all the major states through which `pflink` transits. Assuming you have fired up an instance of `pfbridge`:

```bash

# You can check how the `pflink` URLs are currently configured with:
❯ pflinkURLs_get
{
  "productionURL": "http://localhost:8050/workflow/",
  "testingURL": "http://localhost:8050/testing/"
}

# This assumes of course that you have a `pflink` instance running on `localhost:8050`.
# Let's assume not and try and hit the `testing` URL:
# Here we use two numeric arguments that correspond to the
# StudyInstanceUID and SeriesInstanceUID of a dummy test:

❯ relay test 1234567 1234567
{
  "Status": "Comms failure",
  "Progress": "n/a",
  "ErrorWorkflow": "n/a",
  "ErrorComms": {
    "error": "All connection attempts failed",
    "URL": "http://localhost:8050/testing/",
    "help": "Please check that the pflink URL is correct"
  }
}

# If we in fact get `pflink` properly up, we can test the testing URL:
❯ relay test 1234567 1234567
{
  "Status": "Initializing workflow",
  "Progress": "0%",
  "ErrorWorkflow": "",
  "ErrorComms": {
    "error": "",
    "URL": "",
    "help": ""
  }
}

❯ relay test 1234567 1234567
{
  "Status": "Pulling image for analysis",
  "Progress": "25%",
  "ErrorWorkflow": "",
  "ErrorComms": {
    "error": "",
    "URL": "",
    "help": ""
  }
}

❯ relay test 1234567 1234567
{
  "Status": "Pulling image for analysis",
  "Progress": "50%",
  "ErrorWorkflow": "",
  "ErrorComms": {
    "error": "",
    "URL": "",
    "help": ""
  }
}


```

_-30-_
