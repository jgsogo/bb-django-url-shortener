from django.dispatch.dispatcher import Signal

link_followed = Signal(providing_args=['request'])
