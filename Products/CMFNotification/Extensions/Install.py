"""Install method.

$Id$
"""

from zope.component import getUtility
from zope.component import getMultiAdapter

from Products.CMFCore.utils import getToolByName

from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping

from Products.CMFNotification.config import PORTLET_NAME
from Products.CMFNotification.config import PROJECT_NAME
from Products.CMFNotification.exportimport import addPermissions


def install(context):
    """Install CMFNotification.

    Most of the job is done by a Generic Setup profile.
    """
    ## I do not know how (and if it is possible) to define that an
    ## import step is a dependency of the 'rolemap' step.
    addPermissions(context)

    ## Import GenericSetup default profile
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-Products.CMFNotification:default')

    return 'Successfully installed %s.' % PROJECT_NAME


def uninstall(context):
    """Uninstall CMFNotification."""
    portal = getToolByName(context, 'portal_url').getPortalObject()
    ps = getToolByName(portal, "portal_setup")
    irs = ps.getImportStepRegistry()

    ## Import GenericSetup uninstallation profile
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-Products.CMFNotification:uninstall')

    ## Remove portlet
    rightColumn = getUtility(IPortletManager,
                             name=u'plone.rightcolumn',
                             context=portal)
    right = getMultiAdapter((portal, rightColumn),
                            IPortletAssignmentMapping,
                            context=portal)
    if PORTLET_NAME in right:
        del right[PORTLET_NAME]

    ## Remove the import and export steps from portal_setup
    ## Since 'remove=True' doesn't seem to work for import/export
    ## steps, here we manually remove import/export steps (Kurt)
    if 'export_cmfnotification' in ps.listExportSteps():
        ps.manage_deleteExportSteps(['export_cmfnotification',])
    if 'import_cmfnotification' in irs.listSteps():
        ps.manage_deleteImportSteps(['import_cmfnotification',])

    ## Remove installation step for the subscription portlet
    if u'' in irs.listSteps():
        ## The 2.2-dev step didn't specify an ID. So, check for a step
        ## called '' (Kurt)
        irs.unregisterStep('')
    if 'import_cmfnotification_portlet' in irs.listSteps():
        irs.unregisterStep('import_cmfnotification_portlet')

    ## Remove configlet
    panel = getToolByName(portal, 'portal_controlpanel')
    if panel is not None:
        panel.unregisterConfiglet('cmfnotification_configuration')

    return '%s has been successfully uninstalled.' % PROJECT_NAME
