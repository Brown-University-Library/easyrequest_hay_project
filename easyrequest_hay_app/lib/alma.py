import datetime, json, logging, pprint

import requests
from django.core.mail import mail_admins
from easyrequest_hay_app import settings_app
from easyrequest_hay_app.models import ItemRequest


log = logging.getLogger(__name__)


class AlmaHelper():

    def __init__( self ):
        pass

    def load_db_data( self, shortlink ):
        ( data_dct, err ) = ( {}, None )
        try:
            assert type(shortlink) == str
            item_obj = ItemRequest.objects.get( short_url_segment=shortlink )
            item_dct = item_dct = json.loads( item_obj.full_url_params )
            patron_dct = json.loads( item_obj.patron_info )
            data_dct = { 'item_dct': item_dct, 'patron_dct': patron_dct }
            assert len( data_dct['item_dct']['item_barcode'] ) > 10  # usually 14
            assert len( data_dct['patron_dct']['patron_barcode'] ) > 10  # usually 14
        except Exception as e:
            err = repr(e)
            log.exception( 'problem loading db data' )
        log.debug( f'data_dct, ``{pprint.pformat(data_dct)}``' )
        log.debug( f'err, ``{err}``' )
        return( data_dct, err )

    def prepare_hold_url( self, item_barcode, patron_barcode ):
        ( hold_url, err ) = ( '', None )
        try:
            barcode_url = settings_app.ALMA_API_BARCODE_URL.replace( '{ITEM_BARCODE}', item_barcode ).replace( '{API_KEY}', settings_app.ALMA_API_KEY )
            header_data = { 'accept': 'application/json' }
            r = requests.get( barcode_url, headers=header_data )
            resp_dct = r.json()
            log.debug( f'resp_dct, ``{pprint.pformat(resp_dct)}``' )
            mms_id = resp_dct['bib_data']['mms_id']
            holding_id = resp_dct['holding_data']['holding_id']
            item_pid = resp_dct['item_data']['pid']
            log.debug( f'mms_id, ``{mms_id}``; holding_id, ``{holding_id}``; item_id, ``{item_pid}``' )
            # export EZRQST_HAY__ALMA_API_HOLD_URL_TEMPLATE="https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs/{MMS_ID}/holdings/{HOLDING_ID}/items/{ITEM_PID}/requests?user_id={USER_ID}&user_id_type=all_unique&allow_same_request=false&apikey={API_KEY}"
            hold_url = settings_app.ALMA_API_HOLD_URL.replace(
                '{MMS_ID}', mms_id ).replace(
                '{HOLDING_ID}', holding_id ). replace(
                '{ITEM_PID}', item_pid ).replace(
                '{USER_ID}', patron_barcode ).replace(
                '{API_KEY}', settings_app.ALMA_API_KEY )
        except Exception as e:
            err = repr(e)
            log.exception( 'problem preparing hold-url' )
            self.email_admins( 'for admin -- easyRequest-Hay problem', f'error: ``{err}``; staff will be emailed; user will land at aeon, as usual' )
        log.debug( f'hold_url, ``{hold_url}``' )
        log.debug( f'err, ``{err}``' )
        return ( hold_url, err )

    def prep_email_patron_json( self, patron_dct ):
        """ Prepares subset of full patron info for hay-staff email.
            Called by views.alma_processor() """
        ( email_patron_json, err ) = ( '', None )
        email_patron_dct = {}
        try:
            target_key_segments = [ 'browntype', 'department', 'email', 'eppn', 'firstname', 'lastname', 'patron_barcode', 'sierra_patron_id' ]
            for key in patron_dct.keys():
                for segment in target_key_segments:
                    if segment in key.lower():
                        email_patron_dct[key] = patron_dct[key]
            email_patron_json = json.dumps( email_patron_dct, sort_keys=True, indent=2 )
        except Exception as e:
            err = repr(e)
            log.exception( 'problem preparing patron-json for email' )
            self.email_admins( 'for admin -- easyRequest-Hay problem', f'error: ``{err}``; staff could not be emailed; user will land at aeon, as usual' )
        log.debug( f'email_patron_json, ``email_patron_json``' )
        log.debug( f'err, ``{err}``' )
        return ( email_patron_json, err )


    def manage_place_hold( self, hold_url ):
        """ Tries to place hold in Alma on behalf of the patron.
            Called by views.alma_processor() """
        ( request_id, err ) = ( '', None )
        try:
            header_data = {
                'accept': 'application/json',
            }
            payload_data = {
              'pickup_location_library': 'HAY',  # ROCK/HAY
              'pickup_location_type': 'LIBRARY',
              'request_type': 'HOLD',
              'comment': 'auto-requested via easyRequest-Hay webapp'
            }
            r = requests.post( hold_url, headers=header_data, json=payload_data )
            log.debug( f'r.content, ``{r.content}``' )
            dct = r.json()
            assert type(dct) == dict
            log.debug( f'response-dct, ``{pprint.pformat(dct)}``' )
            # request_id = dct['request_id']
            request_id = dct.get( 'request_id', '' )
        except Exception as e:
            err = repr(e)
            log.exception( 'problem placing hold' )
            # self.email_admins( 'for admin -- easyRequest-Hay problem', f'error: ``{err}``; staff could not be emailed; user will land at aeon, as usual' )
        log.debug( f'request_id, ``request_id``' )
        log.debug( f'err, ``{err}``' )
        return ( request_id, err )


    def email_admins( self, subject, message ):
        """ Wraps django.mail_admins in try/except. """
        try:
            mail_admins( subject, message )
        except:
            log.exception( 'Unable to send admin email; traceback follows; processing continues' )

    def send_email_check( self, item_title, item_barcode, patron_barcode ):
        """ Evaluates whether an email -- TO HAY STAFF -- needs to be sent.
            Called by views.alma_processor() """
        log.debug( 'starting send_email_check()' )
        return_check = False
        log.debug( f'checking for duplicate against item_barcode, ```{item_barcode}``` and patron_barcode, ```{patron_barcode}```' )
        now_time = datetime.datetime.now()
        half_hour_ago = now_time - datetime.timedelta( minutes=30 )
        log.debug( f'half_hour_ago, ``{half_hour_ago}``' )
        ## query all requests for past half-hour where past-request.item-id == current-item.item-id
        possible_duplicates = ItemRequest.objects.filter( item_title=item_title, create_datetime__gte=half_hour_ago )  # add `, patron_info__isnull=False`? I don't think so, because this path assumes shib, so there should always be patron info
        log.debug( f'possible_duplicates, ``{possible_duplicates}``' )
        ## loop through them
        recent_email_sent = False
        for poss_dup in possible_duplicates:
            poss_dup_item_dct = json.loads( poss_dup.full_url_params )

            poss_dup_patron_dct = None
            try:
                poss_dup_patron_dct = json.loads( poss_dup.patron_info )
            except:
                log.exception( 'problem getting expected patron-dct; processing continues' )

            if poss_dup_patron_dct:

                if poss_dup_item_dct.get('item_barcode', None) == item_barcode:
                    if poss_dup_patron_dct.get('patron_barcode', None) == patron_barcode:
                        ## ok poss_dup _is_ a duplicate
                        log.debug( 'duplicate found' )
                        if poss_dup.admin_notes:
                            if 'email_sent' in poss_dup.admin_notes.lower():
                                recent_email_sent = True
                                # updated_notes = 'Not sending staff-email re unable-to-request-via-alma; already sent.' + '\n\n' + current_notes
                                # self.item_request.admin_notes = updated_notes.strip()
                                # self.item_request.save()
                                log.info( 'not sending staff-email re unable-to-request-via-alma; already sent.' )
                                break
        log.debug( f'recent_email_sent, ```{recent_email_sent}```' )
        if recent_email_sent is False:
            return_check = True
            log.info( 'will send staff-email re unable-to-request-via-alma.' )
        log.debug( f'return_check, `{return_check}`' )
        return return_check

    def add_note( self, shortlink, note ):
        """ Adds note to item. """
        item_obj = ItemRequest.objects.get( short_url_segment=shortlink )
        item_obj.admin_notes = note
        item_obj.save()
        return


    # def send_email_check( self, item_title, item_barcode, patron_barcode ):
    #     """ Evaluates whether an email -- TO HAY STAFF -- needs to be sent.
    #         Called by views.alma_processor() """
    #     log.debug( 'starting send_email_check()' )
    #     return_check = False
    #     log.debug( f'checking for duplicate against item_barcode, ```{item_barcode}``` and patron_barcode, ```{patron_barcode}```' )
    #     now_time = datetime.datetime.now()
    #     half_hour_ago = now_time - datetime.timedelta( minutes=30 )
    #     log.debug( f'half_hour_ago, ``{half_hour_ago}``' )
    #     ## query all requests for past half-hour where past-request.item-id == current-item.item-id
    #     possible_duplicates = ItemRequest.objects.filter( item_title=item_title, create_datetime__gte=half_hour_ago )  # add `, patron_info__isnull=False`? I don't think so, because this path assumes shib, so there should always be patron info
    #     log.debug( f'possible_duplicates, ``{possible_duplicates}``' )
    #     ## loop through them
    #     recent_email_sent = False
    #     for poss_dup in possible_duplicates:
    #         poss_dup_item_dct = json.loads( poss_dup.full_url_params )

    #         poss_dup_patron_dct = None
    #         try:
    #             poss_dup_patron_dct = json.loads( poss_dup.patron_info )
    #         except:
    #             log.exception( 'problem getting expected patron-dct; processing continues' )

    #         if poss_dup_patron_dct:

    #             if poss_dup_item_dct.get('item_barcode', None) == item_barcode:
    #                 if poss_dup_patron_dct.get('patron_barcode', None) == patron_barcode:
    #                     ## ok poss_dup _is_ a duplicate
    #                     recent_email_sent = True
    #                     log.info( 'not sending staff-email re unable-to-request-via-alma; already sent.' )
    #                     break
    #     log.debug( f'recent_email_sent, ```{recent_email_sent}```' )
    #     if recent_email_sent is False:
    #         return_check = True
    #         log.info( 'will send staff-email re unable-to-request-via-alma.' )
    #     log.debug( f'return_check, `{return_check}`' )
    #     return return_check
