import json, logging, pprint

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
        except Exception as e:
            err = repr(e)
            log.exception( 'problem loading db data' )
        log.debug( f'data_dct, ``{pprint.pformat(data_dct)}``' )
        log.debug( f'err, ``{err}``' )
        return( data_dct, err )

    def prepare_hold_url( self, data_dct ):
        ( hold_url, err ) = ( '', None )
        return ( hold_url, err )

    # def prep_item_data( self, shortlink ):
    #     """ Preps item-data -- and some patron-data -- from item_request.
    #         Called by views.processor() """
    #     self.item_request = ItemRequest.objects.get( short_url_segment=shortlink )
    #     self.item_dct = item_dct = json.loads( self.item_request.full_url_params )
    #     log.debug( 'item_dct, ```%s```' % pprint.pformat(item_dct) )
    #     patron_dct = json.loads( self.item_request.patron_info )
    #     log.debug( 'patron_dct, ```%s```' % pprint.pformat(patron_dct) )
    #     self.item_bib = item_dct['item_bib']
    #     self.item_barcode = item_dct['item_barcode']
    #     self.item_title = item_dct['item_title']
    #     self.patron_barcode = patron_dct['patron_barcode']
    #     # self.patron_login_name = patron_dct['firstname']
    #     self.patron_sierra_id = patron_dct['sierra_patron_id']
    #     self.get_item_id()
    #     log.debug( 'bib, `%s`; item_barcode, `%s`; patron_barcode, `%s`' % (self.item_bib, self.item_barcode, self.patron_barcode) )
    #     log.debug( 'SierraHelper instance-info, ```%s```' % pprint.pformat(self.__dict__) )
    #     return
