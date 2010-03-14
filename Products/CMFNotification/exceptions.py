"""Define CMFNotification specific exceptions.

$Id$
"""


class MailHostNotFound(Exception):
    """Could not send notification: no mailhost found"""


class DisabledFeature(Exception):
    """Cannot use this feature: it is disabled"""


class InvalidEmailAddress(Exception):
    """The given email address is not valid"""
