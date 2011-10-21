import logging
from ZODB.POSException import ConflictError
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from Products.CMFNotification.utils import encodeMailHeaders
from Products.CMFNotification.NotificationTool import EMAIL_REGEXP
from Products.CMFNotification.exceptions import MailHostNotFound
from Products.CMFNotification.interfaces import INotificationDelivery

LOG = logging.getLogger('CMFNotification.mail')
MAIL_HOST_META_TYPES = ('Mail Host', 'Secure Mail Host', 'Maildrop Host',
    'Secure Maildrop Host')

class MailNotificationDelivery(object):
    implements(INotificationDelivery)

    def notify(self, obj, user, what, label,
                       get_users_extra_bindings,
                       mail_template_extra_bindings,
                       mail_template_options):
        mtool = getToolByName(obj, 'portal_membership')
        member = mtool.getMemberById(str(user))
        if member is None:
            return 0
        email = member.getProperty('email', '')
        if email is None:
            return 0
        if not EMAIL_REGEXP.match(email):
            return 0

        pn = getToolByName(obj, 'portal_notification')
        template = pn.getTemplate(obj, what, mail_template_extra_bindings)
        if template is None:
            LOG.warning("No mail template for label '%s' for "\
                        "'%s' notification of '%s'",
                        label, what, obj.absolute_url(1))
            return 0

        try:
            message = template(**mail_template_options)
        except ConflictError:
            raise
        except:
            LOG.error("Cannot evaluate mail template '%s' on '%s' "\
                      "for '%s' for label '%s'",
                      template.absolute_url(1),
                      obj.absolute_url(1), what, label,
                      exc_info=True)
            return 0
        return self.sendNotification(obj, email, message)

    def sendNotification(self, obj, address, message):
        """Send ``message`` to ``address``."""
        portal = obj.restrictedTraverse('@@plone_portal_state').portal()
        mailhosts = portal.superValues(MAIL_HOST_META_TYPES)
        if not mailhosts:
            raise MailHostNotFound
        mailhost = mailhosts[0]

        ptool = getToolByName(obj, 'portal_properties').site_properties
        encoding = ptool.getProperty('default_charset', 'utf-8')
        message = encodeMailHeaders(message, encoding)

        this_message = ('To: %s\n' % address) + message
        this_message = this_message.encode(encoding)
        try:
            mailhost.send(this_message)
        except ConflictError:
            raise
        except:
            LOG.error('Error while sending '\
                      'notification: \n%s' % this_message,
                      exc_info=True)
            return 0
        return 1
