from website.models.guest import init as admin_init_guest
from website.models.mail.subscription_group import init as admin_init_email_subscription_group
from website.models.mail.template import init as admin_init_email_template
from website.models.reservation import init as admin_init_reservation

admin_init_reservation()
admin_init_guest()
admin_init_email_template()
admin_init_email_subscription_group()
