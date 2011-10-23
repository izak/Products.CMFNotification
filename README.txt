CMFNotification is a Plone product that allows users to be notified
when various events occur in the portal: item creation or
modification, workflow actions, etc.

The version hosted here (at git@github.com:izak/Products.CMFNotification.git)
is a fork of the version that is in the collective at
https://svn.plone.org/svn/collective/Products.CMFNotification/trunk. I forked
it here with the permission of Pilot Systems.

This version is different to the one in the collective. The actual notification
process, namely sending an email to interested users, has been split into a
named utility. You can register your own notification methods in the same way,
and CMFNotification will be able to use them.

The primary use for this functionality: We wanted CMFNotification to tell
users about changes by using slc.stickystatusmessages. Other uses might
be that you want to send a Short Message to their cellular phone, or a tweat
on twitter. The possibilities are endless.
