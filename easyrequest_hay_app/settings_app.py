# -*- coding: utf-8 -*-

import json, os


README_URL = os.environ[ 'EZRQST_HAY__README_URL' ]

TEST_SHIB_JSON = os.environ.get( 'EZRQST_HAY__TEST_SHIB_JSON', '{}' )

SHIB_IDP_LOGOUT_URL = os.environ['EZRQST_HAY__SHIB_LOGOUT_URL_ROOT']
SHIB_SP_LOGIN_URL = os.environ['EZRQST_HAY__SHIB_LOGIN_URL_ROOT']
SHIB_ERESOURCE_PERMISSION = os.environ['EZRQST_HAY__SHIB_ERESOURCE_PERMISSION']

PATRON_API_URL = os.environ['EZRQST_HAY__PAPI_URL']
PATRON_API_BASIC_AUTH_USERNAME = os.environ['EZRQST_HAY__PAPI_BASIC_AUTH_USERNAME']
PATRON_API_BASIC_AUTH_PASSWORD = os.environ['EZRQST_HAY__PAPI_BASIC_AUTH_PASSWORD']
PATRON_API_LEGIT_PTYPES = json.loads( os.environ['EZRQST_HAY__PAPI_LEGIT_PTYPES_JSON'] )

AVAILABILITY_API_URL_ROOT = os.environ['EZRQST_HAY__AVAILABILITY_API_URL_ROOT']
USER_AGENT = os.environ['EZRQST_HAY__AVAILABILITY_API_USER_AGENT']

HAY_LOCATION_CODE = 'h0001'

DEMOGRAPHIC_CATEGORIES = json.loads( os.environ['EZRQST_HAY__SHIB_DEMOGRAPHIC_CATEGORIES_JSON'] )
EXPIRY_DAYS = int( os.environ['EZRQST_HAY__EXPIRY_DAYS'] )  # for cron-script that removes P.I.I.

STAFF_EMAIL_FROM = os.environ['EZRQST_HAY__STAFFEMAIL_FROM']
STAFF_EMAIL_REPLYTO = os.environ['EZRQST_HAY__STAFFEMAIL_REPLYTO']
STAFF_EMAIL_TO = json.loads( os.environ['EZRQST_HAY__STAFFEMAIL_TO'] )  # list

SIERRA_API_ROOT_URL = os.environ['EZRQST_HAY__SIERRA_API_ROOT_URL']
SIERRA_API_KEY = os.environ['EZRQST_HAY__SIERRA_API_KEY']
SIERRA_API_SECRET = os.environ['EZRQST_HAY__SIERRA_API_SECRET']

HELP_EMAIL = os.environ['EZRQST_HAY__EMAIL_GENERAL_HELP']

ALMA_IS_LIVE = json.loads( os.environ['EZRQST_HAY__ALMA_IS_LIVE_JSON'] )  # False before go-live; True afterwards

ALMA_API_KEY = os.environ['EZRQST_HAY__ALMA_API_KEY']
ALMA_API_BARCODE_URL = os.environ['EZRQST_HAY__ALMA_API_BARCODE_URL_TEMPLATE']

