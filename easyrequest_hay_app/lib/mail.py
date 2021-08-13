""""
Contains code for checking whether a 'problem' email needs to be sent to staff, and if so, sends the email.
Triggered initially by views.processor()
"""

import json, logging

from django.core.mail import EmailMessage
from easyrequest_hay_app import settings_app
from easyrequest_hay_app.models import ItemRequest


log = logging.getLogger(__name__)


class Emailer:

    def __init__( self ):
        self.email_subject = 'easyrequest_hay auto-annex-request unsuccessful'

    def email_staff( self, patron_json, item_json ):
        """ Emails staff problem alert.
            Called by run_send_check() """
        err = None
        try:
            body = self.build_email_body( patron_json, item_json )
            # log.debug( f'body, ```{body}```' )
            ffrom = settings_app.STAFF_EMAIL_FROM  # `from` reserved
            to = settings_app.STAFF_EMAIL_TO  # list
            extra_headers = { 'Reply-To': settings_app.STAFF_EMAIL_REPLYTO }
            email = EmailMessage( self.email_subject, body, ffrom, to, headers=extra_headers )
            email.send()
            log.debug( 'mail sent' )
        except Exception as e:
            err = repr(e)
            log.exception( 'problem sending staff-email' )
        log.debug( f'err, ``{err}``' )
        return err

    def build_email_body( self, patron_json, item_json ):
        """ Prepares and returns email body.
            Called by email_staff().
            TODO: use render_to_string & template. """
        body = f'''Greetings Hay Staff,

This is an automated email from the easyRequest_Hay web-app.

This was sent because a patron requested an AnnexHay item, but the item could not be auto-requested (behind-the-scenes) from Sierra.

The patron landed at the Aeon request form (where a staff note about Sierra was auto-inserted).

(Note that the patron may or may not have actually submitted the Aeon request.)

FYI, the patron info...

{patron_json}

...and the item info...

{item_json}

::: END :::
'''
        return body

        ## end def build_email_body()

    ## end class Emailer
