from zope.interface import implements

from Products.Archetypes.utils import addStatusMessage
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFNotification.browser.interfaces import \
        IUnsubscribeMenuConfiglet

class UnsubscribeMenuConfiglet(BrowserView):
    """Configlet to allow admins to unsubscribe users
    """

    implements(IUnsubscribeMenuConfiglet)

    def __init__(self, context, request):
        """
        """
        self.context = context
        self.request = request

    def getUsersList(self):
        """Get a list of users and the path for each of their subscriptions
        """
        pn = getToolByName(self, "portal_notification")
        users_list = {}
        subscriptions = pn._subscriptions
        for path in subscriptions.keys():
            user_ids = subscriptions[path]
            for user_id in user_ids:
                if user_id not in users_list.keys():
                    users_list[user_id] = [path]
                else:
                    users_list[user_id].append(path)
        return users_list

    def deleteUserOnPath(self, subscriptions, userid, path):
        subscribers = subscriptions[path]
        if userid in subscribers.keys():
            del subscribers[userid]
            subscriptions[path] = subscribers

    def unsubscribe(self):
        """init
        """
        pn = getToolByName(self, "portal_notification")
        subscriptions = pn._subscriptions
        sub_keys = subscriptions.keys()
        variables = self.request.form
        for userid in variables.keys():
            paths = variables[userid]
            for path in paths:
                if path == "all":
                    for existing_path in sub_keys:
                        self.deleteUserOnPath(subscriptions,
                                              userid,
                                              existing_path)
                else:
                    if path in sub_keys:
                        self.deleteUserOnPath(subscriptions,
                                              userid,
                                              path)
        addStatusMessage(self.request,
                         "User(s) unsubscribed successfully",
                         type='info')
        url = "%s/notification_controlpanel" % self.context.absolute_url()
        self.request.RESPONSE.redirect(url)
