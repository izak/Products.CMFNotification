"""Tests for CMFNotification subscription.

$Id: testSubscription.py 229875 2011-01-06 10:42:55Z dbaty $
"""

from Products.CMFCore.utils import getToolByName

from Products.CMFNotification.NotificationTool import ID as NTOOL_ID

from Products.CMFNotification.tests.base import CMFNotificationTestCase


class TestUnsubscribeMenuConfiglet(CMFNotificationTestCase):
    """Make sure that the Unsubscribe Menu configlet is working
    as expected"""

    def afterSetUp(self):
        """Called before each tests.

        This method:
        - Creates users and content;
        - Enables extra subscriptions
        - Subscribes the users to some objects
        """
        self.createTestUsersAndContent()

        self.login('manager')
        portal = self.portal
        ntool = getToolByName(portal, NTOOL_ID)
        ntool.manage_changeProperties(extra_subscriptions_enabled=True)

        folder = portal.folder
        document = folder.document1

        ## Subscribe 'member1'
        self.login('member1')
        ntool.subscribeTo(document)

        ## Subscribe 'manager'
        self.login('manager')
        ntool.subscribeTo(document)
        ntool.subscribeTo(folder)

    def testGetUsersList(self):
        """Test that we get the proper list of users subscribed"""
        unsubscribemenu_configlet = self.portal.unrestrictedTraverse(
            "@@unsubscribemenu_configlet"
        )
        users_list = unsubscribemenu_configlet.getUsersList()
        expected_users_list = {
            'manager': ['/folder/', '/folder/document1'],
            'member1': ['/folder/document1']
        }
        for user in users_list.keys():
            paths = users_list[user]
            self.assertTrue(user in expected_users_list.keys())
            self.failUnless(paths == expected_users_list[user])

    def testUnsubscribe(self):
        """Test unsubscribing manager and member1 from the document1"""
        unsubscribemenu_configlet = self.portal.unrestrictedTraverse(
            "@@unsubscribemenu_configlet"
        )
        # make fake request
        unsubscribemenu_configlet.request.form = {
            'manager': ["/folder/document1"],
            "member1": ["/folder/document1"]
        }
        unsubscribemenu_configlet.unsubscribe()
        users_list = unsubscribemenu_configlet.getUsersList()
        expected_users_list = {
            'manager': ['/folder/'],
        }
        for user in users_list.keys():
            paths = users_list[user]
            self.assertTrue(user in expected_users_list.keys())
            self.failUnless(paths == expected_users_list[user])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestUnsubscribeMenuConfiglet))
    return suite

