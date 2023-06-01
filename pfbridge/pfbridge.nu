# Hello nushell!
#
# This script provides some functions for interacting with the `pfbridge` API
# using nushell.
#
#   $ source $PWD/pfbridge.nu
#
# MAKE SURE ANY ENV VARIABLES SET BY THIS ARE WHAT YOU WANT!
#
#     * May-2023
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
let-env pfbridge    = http://localhost:33333
let-env prefix      = 'api/v1'
# To access the API swagger documentation, point a browser at:
let-env swaggerURL  = ":33333/docs"
let-env VERBOSITY   = 0 | into int

###############################################################################
#_____________________________________________________________________________#
# H E L P                                                                     #
#_____________________________________________________________________________#
# Use pflink_help to get some in-line alias help.                             #
###############################################################################
def pfbridge_help [] {
  $"
                 (ansi purple)WELCOME TO THE PFBRIDGE VIA NUSHELL PAGE!(ansi reset)

  By sourcing the file 'pfbridge.nu' several convenience functions for
  accessing 'pfbridge' are now available in your namespace:

  (ansi cyan)vaultKey_set (ansi green)[key](ansi reset)
  Set the vaultKey to <key>.

  (ansi cyan)vault_check(ansi reset)
  Check the status of the vault.

  (ansi cyan)credentials_get (ansi green)[service key](ansi reset)
  The <service> can be one of 'CUBE' or 'Orthanc', and the <key> is the
  vaultKey value. The command gets the credentials, i.e username and password,
  for the <service>.

  (ansi cyan)credentials_set (ansi green)[service key user string](ansi reset)
  As above, but set the username and password for the <service>. A correct
  <key> must be supplied.

  (ansi cyan)pflinkURLs_get(ansi reset)
  Simply get the 'pflink' URLs with which 'pfbridge' communicates. These are
  a testURL for returning test responses from 'pflink' and a prodURL
  that does production runs.

  (ansi cyan)testURL_set (ansi green)[url](ansi reset)
  Set the 'test' URL of 'pflink'.

  (ansi cyan)prodURL_set (ansi green)[url](ansi reset)
  Set the 'production' URL of 'pflink'

  (ansi cyan)serviceURLs_get(ansi reset)
  Get the 'service URLs', i.e. the URLs of CUBE and Orthanc as set/tracked
  by 'pfbridge'.

  (ansi cyan)CUBEURL_set (ansi green)[url](ansi reset)
  Set the URL of the CUBE instance on which the analysis will be performed.
  Only required in some cases and is largely analysis dependent.

  (ansi cyan)OrthancURL_set (ansi green)[url](ansi reset)
  Set the URL of the orthanc instance which might be relevant to a given
  analysis. As implied, this is highly analysis dependent and only used
  in some cases.

  (ansi cyan)analysis_get (ansi green)[key](ansi reset)
  Get the details of an analysis, i.e. plugin name, username, etc, to be
  passed to 'pflink'. If the correct vaultKey is supplied, then all
  template strings in the plugin command are decoded.

  (ansi cyan)analysis_set (ansi green)[param val](ansi reset)
  Set the analysis record's <param> to <val>

  (ansi cyan)relay (ansi green)[StudyInstanceUID SeriesInstanceUID type=test](ansi reset)
  Call 'pflink' to start an analysis on the image specified with the
  <StudyInstanceUID> and <SeriesInstanceUID>. If the optional type is
  passed an is 'test', then relay to the 'pflink' testing URL, otherwise
  use the production URL.

  (ansi yellow)NB:

  * Set the 'pfbridge' environment variable if needed:

    let-env pfbridge = http://localhost:33333

  * Also, note that on startup, the 'pflink' production and test
    URLs can be specified in environment variables, e.g:

    let-env PRODURL = http://localhost:8050/workflow/
    let-env TESTURL = http://localhost:8050/testing/

    These are 'pflink' URLS!

"
}


###############################################################################
#_____________________________________________________________________________#
# B U I L D                                                                   #
#_____________________________________________________________________________#
# Build the container image in a variety of difference contexts/use cases.    #
###############################################################################

def build [] {
  let-env UID = (id -u)
  # Build (for fish shell syntax!)
  (docker build --build-arg UID=$UID -t local/pfbridge .)
}

###############################################################################
#_____________________________________________________________________________#
# G E T / S E T / P O S T  h e l p e r s                                      #
#_____________________________________________________________________________#
###############################################################################
# Simple helper functions that simply calls to the API                        #
###############################################################################

def http_get [url:string] {
  http get $"($env.pfbridge)/($env.prefix)/($url)"
}

def http_put [url:string query:string] {
  # The body in this request is passed since the nushell "http put" seems
  # to require it, but is ignored by the API
  http put -t application/json $"($env.pfbridge)/($env.prefix)/($url)/($query)" {
    "dummy": ($query)
  }
}

def http_post [url:string body:record] {
  let CMD = $'http post -t application/json $"($env.pfbridge)/($env.prefix)/($url)" ($body)'
  if ($env.VERBOSITY | into bool) { print $CMD }
  nu -c $CMD
  #http post -t application/json $"($env.pfbridge)/($env.prefix)/($url)" ($body)
}

###############################################################################
#_____________________________________________________________________________#
# V A U L T / c r e d e n t i a l l i n g                                     #
#_____________________________________________________________________________#
###############################################################################
# vaultKey and credentialling                                                 #
###############################################################################
#

def vaultKey_set [key:string] {
  http_put vaultKey $"?key=($key)"
}

def vault_check [] {
  http_get vaultKey
}

def credentials_get [service:string key:string = ""] {
  http_get credentials/($service)/?vaultKey=($key)
}

def credentials_set [
  service:string
  key:string
  user:string
  password:string
] {
  http_post credentials/($service)/?vaultKey=($key) {
    "username": ($user),
    "password": ($password)
  }
}

################################################################################
##_____________________________________________________________________________#
## G E T / P U T  pflink and service URLs                                                  #
##_____________________________________________________________________________#
################################################################################
## Simply get and set various URLs used by the service                         #
################################################################################
##

def pflinkURLs_get [] {
  http_get pflink/URLs/
}

def serviceURLs_get [] {
  http_get service/URLs/
}

def CUBEURL_set [url:string] {
  http_put /service/URL/CUBE $"?URL=($url)"
}

def OrthancURL_set [url:string] {
  http_put service/URL/Orthanc $"?URL=($url)"
}

def testURL_set [url:string] {
  http_put pflink/testURL $"?URL=($url)"
}

def prodURL_set [url:string] {
  http_put pflink/prodURL $"?URL=($url)"
}

def analysis_get [key:string = ""] {
  mut query = ""
  if ($key | str length) > 0 {
    $query = $"?vaultKey=($key)"
  } else {
    $query = ""
  }
  http_get analysis/($query)
}

def analysis_set [param:string value:string] {
  http_put analysis $"?key=($param)&value=($value)"
}

################################################################################
##_____________________________________________________________________________#
## R E L A Y                                                                   #
##_____________________________________________________________________________#
################################################################################
## Relay payloads to the workflow API endpoint of pflink                       #
################################################################################
##

def relay [StudyInstanceUID:string SeriesInstanceUID:string type:string = "test"] {
  let PACSDIRECTIVE = {
    "StudyInstanceUID": ($StudyInstanceUID),
    "SeriesInstanceUID": ($SeriesInstanceUID)
  }
  let PAYLOAD = {
    "imageMeta" :  $PACSDIRECTIVE,
    "analyzeFunction" : "dylld"
  }
  mut query = ""
  if ($type == 'test') {
    $query = "?test=true"
  } else {
    $query = ""
  }
  http_post analyze/($query) ($PAYLOAD)
}

#
##
## And we're done!
## _-30-_
##
#
