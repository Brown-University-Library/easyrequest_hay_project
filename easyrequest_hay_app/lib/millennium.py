# -*- coding: utf-8 -*-

import json, logging, os, pprint
import requests
from easyrequest_hay_app import settings_app
from easyrequest_hay_app.lib.iii_account import IIIAccount
from easyrequest_hay_app.models import ItemRequest


log = logging.getLogger(__name__)


class Millennium( object ):
    """ Gets item_id and places hold. """

    def __init__( self ):
        self.AVAILABILITY_API_URL_ROOT = settings_app.AVAILABILITY_API_URL_ROOT
        self.LOCATION_CODE = settings_app.HAY_LOCATION_CODE
        self.item_bib = ''
        self.item_barcode = ''
        self.item_id = ''
        self.patron_barcode = ''
        self.patron_login_name = ''


    def prep_item_data( self, shortlink ):
        """ Preps item-data from item_request.
            Called by views.processor() """
        item_request = ItemRequest.objects.get( short_url_segment=shortlink )
        item_dct = json.loads( item_request.full_url_params )
        patron_dct = json.loads( item_request.patron_info )
        self.item_bib = item_dct['item_bib']
        self.item_barcode = item_dct['item_barcode']
        self.patron_barcode = patron_dct['patron_barcode']
        self.patron_login_name = patron_dct['firstname']
        self.get_item_id()
        log.debug( 'bib, `%s`; item_barcode, `%s`; patron_barcode, `%s`' % (self.item_bib, self.item_barcode, self.patron_barcode) )
        return

    def get_item_id( self ):
        """ Calls availability-api to get the item-id.
            Called by views.processor() """
        avail_dct = self.hit_availability_api( self.item_bib )
        self.item_id = self.extract_item_id( avail_dct, self.item_barcode )
        log.debug( 'item_id, `%s`' % self.item_id )
        return

    # def get_item_id( self, shortlink ):
    #     """ Calls availability-api to get the item-id.
    #         Called by views.processor() """
    #     self.prep_item_data( shortlink )
    #     avail_dct = self.hit_availability_api( self.item_bib )
    #     item_id = self.extract_item_id( avail_dct, self.item_barcode )
    #     log.debug( 'item_id, `%s`' % item_id )
    #     return item_id

    def hit_availability_api( self, bibnum ):
        """ Returns availability-api dct.
            Called by get_item_id() """
        avail_dct = {}
        availability_api_url = '%s/bib/%s' % ( self.AVAILABILITY_API_URL_ROOT, bibnum )
        log.debug( 'availability_api_url, ```%s```' % availability_api_url )
        try:
            r = requests.get( availability_api_url )
            avail_dct = r.json()
            log.debug( 'partial availability-api-response, `%s`' % pprint.pformat(avail_dct)[0:200] )
        except Exception as e:
            log.error( 'exception, %s' % str(e) )
        log.debug( 'avail_dct, ```%s```' % avail_dct )
        return avail_dct

    def extract_item_id( self, avail_dct, item_barcode ):
        """ Uses barcode to get item_id.
            Called by get_item_id() """
        results = avail_dct['response']['backend_response']
        for result in results:
            items = result['items_data']
            for item in items:
                if item_barcode == item['barcode']:
                    # callnumber = item['callnumber_interpreted'].replace( ' None', '' )
                    item_id = item['item_id'][:-1]  # removes trailing check-digit
        log.debug( 'item_id, `%s`' % item_id )
        return item_id

    def place_hold( self ):
        """ Calls lib to place hold.
            Called by views.processor()
            Elements needed for hold: user_name, user_barcode, item_bib, item_id, pickup_location """
        status = 'init'
        try:
            jos_sess = IIIAccount( name=self.patron_login_name, barcode=self.patron_barcode )
            jos_sess.login()
            log.debug( 'jos_sess, ```%s```' % jos_sess )
            hold = jos_sess.place_hold( bib=self.item_bib, item=item_id, pickup_location=self.LOCATION_CODE )
            jos_sess.logout()
            log.debug( 'hold, `%s`' % hold )
            status = 'request_placed'
            return status
        except Exception as e:
            log.error( 'exception, ```%s```' % str(e) )
            try:
                jos_sess.logout()
                log.debug( 'jos_sess.logout() succeeded on exception catch' )
            except Exception as f:
                log.error( 'exception, ```%s```' % str(f) )
        return status

    ## end class Millennium()

