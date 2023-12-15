#!/usr/bin/env bash
# =========================================================
SYNOPSIS="
NAME
    setup.sh

SYNOPSIS
    setup.sh [-h]                   \\
             [-U <pfbridgeUrl>]     \\
             [-P <pflinkUrl>]       \\
             [-v <vaultKey>]        \\
             [-u <cubeUsername>]    \\
             [-p <cubePassword>]    \\
             [-o <orthancUsername>] \\
             [-r <orthancPassword>] \\
DESC
    setup.sh is a helper script to override various Base
    Settings inside pfbridge such as service endpoints of
    pflink and analysis related settings such as username
    and password of CUBE and orthanc. We can also define
    new analysis function and configure values to keys
    such as plugin name, version, args; feed name and
    pipeline

ARGS
    [-h]
    If specified, print this synapsis text of setup.sh.

    [-U <pfbridgeUrl>]
    If specified, uses this url (complete service address)
    as service address to submit curl requests to pfbridge.
    Default value is http://localhost:33333/api/v1.

    [-P <pflinkUrl>]
    If specified, use this url (complete service address)
    to override existing pflink urls in the base settings.
    Default value is http://localhost:8050/api/v1.

    [-v <vaultKey>]
    If specified, use this combination as a vault key
    to get/set various analysis related settings.
    Default value is 1234.

    [-u <cubeUsername>]
    If specified, use this string to set CUBE username.
    Default value is 'chris'.

    [-p <cubePassword>]
    If specified, use this string to set CUBE password.
    Default value is 'chris1234'.

    [-o <orthancUsername>]
    If specified, use this string to set orthanc username.
    Default value is 'orthanc'.

    [-r <orthancPassword>]
    If specified, use this string to set orthanc password.
    Default value is 'orthanc'.

EXAMPLES
    $ ./setup.sh -U http://localhost:33333/api/v1 \\
                 -P http://localhost:8050/api/v1  \\
                 -v 1234                          \\
                 -u chris                         \\
                 -p chris1234                     \\
                 -o orthanc                       \\
                 -r orthanc                       \\
                 -n default                       \\
                 -l pl-simpledsapp                \\
                 -f default-%PatientID-%SeriesInstanceUID-%SeriesDescription

"

# =========================================================
# STEP 0:  CONFIGURATION
# =========================================================
#
#
URL='http://localhost:33333/api/v1'
PFLINK_URL='http://localhost:8050/api/v1'
VAULTKEY='1234'
USERNAMECUBE='chris'
PASSWORDCUBE='chris1234'
USERNAMEORTHANC='orthanc'
PASSWORDORTHANC='orthanc'
NAME='default'
FEEDNAME="$NAME-%PatientID-%SeriesInstanceUID-%SeriesDescription"
PLUGIN='pl-simpledsapp'
VERSION='2.1.0'
ARGS=''
PIPELINE=''

while getopts "U:P:v:u:p:o:r:n:l:f:s:a:e:h" opt; do
    case $opt in
        h) printf "%s" "$SYNOPSIS"; exit 1                ;;

        U) URL=$2                                         ;;

        P) PFLINK_URL=$OPTARG                             ;;

        v) VAULTKEY=$OPTARG                               ;;

        u) USERNAMECUBE=$OPTARG                           ;;

        p) PASSWORDCUBE=$OPTARG                           ;;

        o) USERNAMEORTHANC=$OPTARG                        ;;

        r) PASSWORDORTHANC=$OPTARG                        ;;

        n) NAME=$OPTARG                                   ;;

        l) PLUGIN=$OPTARG                                 ;;

        f) FEEDNAME=$OPTARG                               ;;

        s) VERSION=$OPTARG                                ;;

        a) ARGS=$OPTARG                                   ;;

        e) PIPELINE=$OPTARG                               ;;

        *) exit 0                                         ;;

    esac
done

#
# =========================================================
echo "STEP 1: CURL request to update existing pflink test URL"
# =========================================================
curl -s -X 'PUT' \
  "$URL/pflink/testURL/?URL=$PFLINK_URL/testing" \
  -H 'accept: application/json' | jq

# =========================================================
echo "STEP 2: CURL request to update existing pflink prod URL"
# =========================================================
curl -s -X 'PUT' \
  "$URL/pflink/prodURL/?URL=$PFLINK_URL/workflow" \
  -H 'accept: application/json' | jq

# =========================================================
echo "STEP 3: CURL request to update existing pflink auth URL"
# =========================================================
curl -s -X 'PUT' \
  "$URL/pflink/authURL/?URL=$PFLINK_URL/auth-token" \
  -H 'accept: application/json' | jq

# =========================================================  
echo "STEP 4: CURL request to set the vault key"
# =========================================================
curl -s -X 'PUT' \
  "$URL/vaultKey/?key=$VAULTKEY" \
  -H 'accept: application/json' | jq

# =========================================================
echo "STEP 5: CURL request to set CUBE credentials"
# =========================================================
curl -s -X 'POST' \
  "$URL/credentials/CUBE/?vaultKey=$VAULTKEY" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "'$USERNAMECUBE'",
  "password": "'$PASSWORDCUBE'"
}' | jq

# =========================================================
echo "STEP 6: CURL request to set orthanc credentials"
# =========================================================
curl -s -X 'POST' \
  "$URL/credentials/Orthanc/?vaultKey=$VAULTKEY" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "'$USERNAMEORTHANC'",
  "password": "'$PASSWORDORTHANC'"
}' | jq

# =========================================================
echo "STEP 7: CURL request to set analysis feed name"
# =========================================================
curl -s -X 'PUT' \
  "$URL/analysis/?analysis_name=$NAME&key=analysisFeedName&value=$FEEDNAME" \
  -H 'accept: application/json' | jq

# =========================================================
echo "STEP 8: CURL request to set analysis plugin name"
# =========================================================
curl -s -X 'PUT' \
  "$URL/analysis/?analysis_name=$NAME&key=analysisPluginName&value=$PLUGIN" \
  -H 'accept: application/json' | jq

# =========================================================
echo "STEP 9: CURL request to set analysis plugin version"
# =========================================================
curl -s -X 'PUT' \
  "$URL/analysis/?analysis_name=$NAME&key=analysisPluginVersion&value=$VERSION" \
  -H 'accept: application/json' | jq

# =========================================================
echo "STEP 10: CURL request to set analysis plugin args"
# =========================================================
curl -s -X 'PUT' \
  "$URL/analysis/?analysis_name=$NAME&key=analysisPluginArgs&value=$ARGS" \
  -H 'accept: application/json' | jq

# =========================================================
echo "STEP 11: CURL request to set analysis pipeline name"
# =========================================================
curl -s -X 'PUT' \
  "$URL/analysis/?analysis_name=$NAME&key=analysisPipelineName&value=$PIPELINE" \
  -H 'accept: application/json' | jq

# =========================================================