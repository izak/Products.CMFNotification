from zope.interface import Interface

class IUnsubscribeMenuConfiglet(Interface):
    """Configlet to allow admins to unsubscribe users
    """

    def getUsersList():
        """Get a list of users and the path for each of their subscriptions
        """

    def unsubscribe():
        """init
        """

