"""Product initialization.

$Id$
"""
from Products.CMFCore import utils as CMFCoreUtils

## Apply monkey patches and set permissions
import Products.CMFNotification.patches
import Products.CMFNotification.permissions

def initialize(context):
    from Products.CMFNotification import NotificationTool
    tools = (NotificationTool.NotificationTool, )
    CMFCoreUtils.ToolInit(NotificationTool.META_TYPE,
                          tools=tools,
                          icon='tool.gif').initialize(context)
