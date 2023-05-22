#!/usr/bin/env bash
SYNOPSIS="
This is testing
"

# =========================================================
# STEP 0:  CONFIGURATION
# =========================================================
#
#
URL='http://localhost:33333/api/v1'
PFLINK_URL='http://192.168.0.14:8050/api/v1'
VAULTKEY='1234'
USERNAMECUBE='chris'
PASSWORDCUBE='chris1234'
USERNAMEORTHANC='orthanc'
PASSWORDORTHANC='orthanc'

while getopts "U:P:v:u:p:o:r:h" opt; do
    case $opt in
        h) printf "%s" "$SYNOPSIS"; exit 1                ;;

        U) URL=$2                                         ;;

        P) PFLINK_URL=$OPTARG                             ;;

        v) VAULTKEY=$OPTARG                               ;;

        u) USERNAMECUBE=$OPTARG                           ;;

        p) PASSWORDCUBE=$OPTARG                           ;;

        o) USERNAMEORTHANC=$OPTARG                        ;;

        r) PASSWORDORTHANC=$OPTARG                        ;;

        *) exit 0                                         ;;

    esac
done

#
# ==========================================================
# STEP 1: CURL request to update existing `pflink` test URL
# ==========================================================
curl -X 'PUT' \
  "$URL/pflink/testURL/?URL=$PFLINK_URL/testing" \
  -H 'accept: application/json' | jq

# =========================================================
# STEP 2: CURL request to update existing `pflink` prod URL
# =========================================================
curl -X 'PUT' \
  "$URL/pflink/prodURL/?URL=$PFLINK_URL/workflow" \
  -H 'accept: application/json' | jq

# =========================================================
# STEP 3: CURL request to update existing `pflink` auth URL  
# =========================================================
curl -X 'PUT' \
  "$URL/pflink/authURL/?URL=$PFLINK_URL/auth-token" \
  -H 'accept: application/json' | jq

# =========================================================  
# STEP 4: CURL request to set the vault key
# =========================================================
curl -X 'PUT' \
  "$URL/vaultKey/?key=$VAULTKEY" \
  -H 'accept: application/json' | jq

# =========================================================
# STEP 5: CURL request to set CUBE credentials
# =========================================================
curl -X 'POST' \
  "$URL/credentials/CUBE/?vaultKey=$VAULTKEY" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "'$USERNAMECUBE'",
  "password": "'$PASSWORDCUBE'"
}' | jq

# =========================================================
# STEP 6: CURL request to set orthanc credentials
# =========================================================
curl -X 'POST' \
  "$URL/credentials/Orthanc/?vaultKey=$VAULTKEY" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "'$USERNAMEORTHANC'",
  "password": "'$PASSWORDORTHANC'"
}' | jq

# =========================================================
# STEP 7: CURL request to get analysis settings
# =========================================================
curl -X 'GET' \
  "$URL/analysis/?vaultKey=$VAULTKEY" \
  -H 'accept: application/json' | jq
# =========================================================
