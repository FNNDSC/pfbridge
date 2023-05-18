# This script describes by way of demonstration various explicit examples of
# how to interact with the pfbridge API using curl -s.
#
#   $ source \$PWD/workflow
#
# MAKE SURE ANY ENV VARIABLES SET BY THIS ARE WHAT YOU WANT!
#
#     * Feb-2023
#     Develop/deploy.
#

###############################################################################
#_____________________________________________________________________________#
# E N V                                                                       #
#_____________________________________________________________________________#
# Set the following variables appropriately for your local setup.             #
###############################################################################

#
# pfbridge service
#
# In some envs, this MUST be an IP address!
export pfbridge=http://localhost:33333

###############################################################################
#_____________________________________________________________________________#
# H E L P                                                                     #
#_____________________________________________________________________________#
# Use pflink_help to get some in-line alias help.                             #
###############################################################################
pfbridge_help() {
  cat << EOM
  The following aliases are available:

  vault_check               - check the status of the vault

  pflinkURLs_get            - get the 'pflink' URLs with which 'pfbridge'
                              communicates
  testURL_set <URL>         - set the "test" URL of 'pflink'
  prodURL_set <URL>         - set the "production" URL of 'pflink'
  analysis_get              - get the details of an analysis (plugin name, username, etc)
  analysis_set <key> <val>  - set the analysis <key> to <val>
  relay <type> <STD> <SRD>  - relay the <STD> (StudyInstanceUID) and <SRD>
                              (SeriesInstanceUID) to 'pflink'. If <type> is
                              "test" then use the testing API, otherwise for
                              any other value of <type> use the production API.

  NB:
  * Set the 'pfbridge' environment variable (if needed):

    export pfbridge=http://localhost:33333

    (currently, \$pfbridge=$pfbridge)

  * Also, note that on startup, the 'pflink' production and test
    URLs can be specified in environment variables, e.g:

    export PRODURL=http://localhost:8050/workflow/
    export TESTURL=http://localhost:8050/testing/

    These are 'pflink' URLS!

  * Set an environment variable called VERBOSE (to any value) to
    trigger printing the actual curl command being used. Unset this
    variable to turn off verbose logging.

EOM
}


###############################################################################
#_____________________________________________________________________________#
# B U I L D                                                                   #
#_____________________________________________________________________________#
# Build the container image in a variety of difference contexts/use cases.    #
###############################################################################

build () {
# UID
# for fish:
# export UID=(id -u)
# for bash/zsh
export UID=$(id -u)
# Build (for fish shell syntax!)
docker build --build-arg UID=$UID -t local/pfbridge .
}

launch_quickndirty () {
# Quick 'n dirty run -- this is what you'll mostly do.
# Obviously change port mappings if needed (and in the Dockerfile)
docker run --rm -it                                                            \
        -p 33333:33333                                                         \
        local/pfbridge /start-reload.sh
}

launch_debug () {
# Run with support for source debugging
docker run --rm -it                                                            \
        -p 33333:33333                                                         \
        -v $PWD/pfbridge:/app:ro                                               \
        local/pfbridge /start-reload.sh
}

# To access the API swagger documentation, point a brower at:
export swaggerURL=":33333/docs"

randtime_generate () {
  range=$1
  shuf -i 1-$1 -n 1 | xargs -i% echo "scale = 4; %/1000"  | bc
}

###############################################################################
#_____________________________________________________________________________#
# V A U L T / c r e d e n t i a l l i n g                                     #
#_____________________________________________________________________________#
###############################################################################
# vaultKey and credentialling                                                 #
###############################################################################
#

vaultKey_set() {
  CMD=$(echo curl -s -X 'PUT'                         \
  "$pfbridge/api/v1/vaultKey/?key=$1"                 \
  -H "accept: application/json")
  if (( ${#VERBOSE} )) ; then echo $CMD ; fi
  echo "$CMD" | sh | jq
}

vault_check() {
  CMD=$(echo curl -s -X 'GET'                         \
  "$pfbridge/api/v1/vaultKey/"                        \
  -H "accept: application/json")
  if (( ${#VERBOSE} )) ; then echo $CMD ; fi
  echo "$CMD" | sh | jq
}

credentials_get() {
  SERVICE=$1
  KEY=$2
  CMD=$(echo curl -s -X 'GET'                             \
  "$pfbridge/api/v1/credentials/$SERVICE/?vaultKey=$KEY"  \
  -H "accept: application/json")
  if (( ${#VERBOSE} )) ; then echo $CMD ; fi
  echo "$CMD" | sh | jq
}

credentials_set() {
  SERVICE=$1
  KEY=$2
  USER=$3
  PASSWORD=$4
  CMD=$(echo curl -s -X 'POST'                            \
  "$pfbridge/api/v1/credentials/$SERVICE/?vaultKey=$KEY"  \
  -H "accept: application/json"                           \
  -H \"Content-Type: application/json\"                   \
  -d ''\''{
     "username": "'$USER'",
     "password": "'$PASSWORD'"
  }'\''')
  if (( ${#VERBOSE} )) ; then echo $CMD ; fi
  echo "$CMD" | sh | jq
}

###############################################################################
#_____________________________________________________________________________#
# G E T / P U T  pflink URLs                                                  #
#_____________________________________________________________________________#
###############################################################################
# Relay and echo back to the test API endpoint of pflink                      #
###############################################################################
#

pflinkURLs_get() {
  CMD=$(echo curl -s -X 'GET'                         \
  \"$pfbridge/api/v1/pflink/\"                        \
  -H \"accept: application/json\"                     \
  )
  if (( ${#VERBOSE} )) ; then echo $CMD ; fi
  echo "$CMD" | sh | jq
}

testURL_set() {
  URL=$1
  CMD=$(echo curl -s -X 'PUT'                         \
  "$pfbridge/api/v1/pflink/testURL/?URL=$URL"         \
  -H "accept: application/json"                       \
  )
  if (( ${#VERBOSE} )) ; then echo $CMD ; fi
  echo "$CMD" | sh | jq
}

prodURL_set() {
  URL=$1
  CMD=$(echo curl -s -X 'PUT'                         \
  "$pfbridge/api/v1/pflink/prodURL/?URL=$URL"         \
  -H "accept: application/json"                       \
  )
  if (( ${#VERBOSE} )) ; then echo $CMD ; fi
  echo "$CMD" | sh | jq
}

analysis_get() {
  KEY=$1
  if (( ${KEY} )) ; then
    QUERY="?vaultKey=$KEY"
  else
    QUERY=""
  fi
  CMD=$(echo curl -s -X 'GET'                         \
  \"$pfbridge/api/v1/analysis/$QUERY\"                \
  -H \"accept: application/json\"                     \
  )
  if (( ${#VERBOSE} )) ; then echo $CMD ; fi
  echo "$CMD" | sh | jq
}

analysis_set() {
  KEY=$1
  VAL=$2
  CMD=$(echo curl -s -X 'PUT'                         \
  "$pfbridge/api/v1/analysis/?key=$KEY\&value=$VAL"   \
  -H "accept: application/json"                       \
  )
  if (( ${#VERBOSE} )) ; then echo $CMD ; fi
  echo "$CMD" | sh | jq
}

###############################################################################
#_____________________________________________________________________________#
# R E L A Y                                                                   #
#_____________________________________________________________________________#
###############################################################################
# Relay payloads to the workflow API endpoint of pflink                       #
###############################################################################
#

relay () {
  Type=$1 # 'test' or anything else
  StudyInstanceUID=$2
  SeriesInstanceUID=$3
  PACSDIRECTIVE='{
        "AccessionNumber": "",
        "PatientID": "",
        "PatientName": "",
        "PatientBirthDate": "",
        "PatientAge": "",
        "PatientSex": "",
        "StudyDate": "",
        "StudyDescription": "",
        "StudyInstanceUID": "'$StudyInstanceUID'",
        "Modality": "",
        "ModalitiesInStudy": "",
        "PerformedStationAETitle": "",
        "NumberOfSeriesRelatedInstances": "",
        "InstanceNumber": "",
        "SeriesDate": "",
        "SeriesDescription": "",
        "SeriesInstanceUID": "'$SeriesInstanceUID'",
        "ProtocolName": "",
        "AcquisitionProtocolDescription": "",
        "AcquisitionProtocolName": ""
  }'
  QUERY=''
  if [[ $Type == 'test' ]] ; then QUERY='?test=true' ; fi
  CMD=$(echo curl -s -X 'POST'            \
  \"$pfbridge/api/v1/analyze/$QUERY\" \
  -H \"accept: application/json\"         \
  -H \"Content-Type: application/json\"   \
  -d ''\''{
  "imageMeta": '$PACSDIRECTIVE',
    "analyzeFunction": "dylld"
  }'\''')
  if (( ${#VERBOSE} )) ; then echo "$CMD" ; fi
  echo "$CMD" | sh | jq
}

#
# And we're done!
# _-30-_
#
