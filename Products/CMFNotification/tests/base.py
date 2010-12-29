"""Define a base class and prepare ZopeTestCase and PloneTestCase to
be used in CMFNotification tests.

$Id$
"""

## Installation voodoo
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from Testing import ZopeTestCase as ztc

@onsetup
def setup_product():
    """Yeah, you probably have seen this code a few times already..."""
    fiveconfigure.debug_mode = True
    import Products.CMFNotification
    zcml.load_config('configure.zcml', Products.CMFNotification)
    fiveconfigure.debug_mode = False
    ztc.installPackage('Five')
    ztc.installPackage('Products.CMFNotification')

setup_product()
ptc.setupPloneSite(products=['Products.CMFNotification'])


## Import statements for our own code below
from OFS.SimpleItem import SimpleItem
from Products.CMFCore.utils import getToolByName

## Monkey-patch logger so that we can test log messages (and not
## display them when tests are run).
from Products.CMFNotification.tests import fakelogger
fakelogger.patchLogging()
import logging
from Products.CMFNotification import NotificationTool
NotificationTool.LOG = logging.getLogger()


## A fake mail host which does not send emails but keep them in a
## list.
NotificationTool.MAIL_HOST_META_TYPES = ('FakeMailHost', )

class FakeMailHost(SimpleItem):
    meta_type = 'FakeMailHost'

    def __init__(self, *args, **kwargs):
        SimpleItem.__init__(self, *args, **kwargs)
        self.sent = []

    def send(self, message):
        self.sent.append(message)

    def getSentList(self):
        return self.sent

    def clearSentList(self):
        self.sent = []


class CMFNotificationBaseTestCase:
    """Base mixin for CMFNotification tests."""

    def createTestUsersAndContent(self):
        """Create some test users and content

        Three users are created:
        - a manager: 'manager'
        - two members: 'member1' and 'member2'

        The following items are created:
        + folder
        |--+-- document1
        |--+-- subfolder
        |-----+-- document2
        """
        ## Create users
        mtool = getToolByName(self.portal, 'portal_membership')
        users = ({'id': 'member1', 'roles': ('Member', )},
                 {'id': 'member2', 'roles': ('Member', )},
                 {'id': 'manager', 'roles': ('Manager', 'Member')})
        for user in users:
            email = user['id'] + '@example.com'
            mtool.addMember(user['id'], user['id'], user['roles'], [],
                            properties={'email': email})

        ## Create content
        self.login('manager')
        self.portal.invokeFactory('Folder', 'folder')
        folder = self.portal.folder
        folder.unmarkCreationFlag()
        folder.invokeFactory('Document', 'document1')
        folder.document1.unmarkCreationFlag()
        folder.invokeFactory('Folder', 'subfolder')
        subfolder = folder.subfolder
        subfolder.unmarkCreationFlag()
        subfolder.invokeFactory('Document', 'document2')
        subfolder.document2.unmarkCreationFlag()


class CMFNotificationTestCase(CMFNotificationBaseTestCase,
                              ptc.PloneTestCase):
    pass ## Nothing special to do


class CMFNotificationBrowserTestCase(CMFNotificationBaseTestCase,
                                     ptc.FunctionalTestCase):
    """A special base class for browser tests."""
    pass ## Nothing special to do.
