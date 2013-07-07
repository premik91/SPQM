from django.conf import settings
from django.core.urlresolvers import resolve


def global_vars(request):
    """
    Adds global variables to the context.
    """

    return {
        # Constants
        'SITE_NAME': settings.SITE_NAME,
        'current_url': resolve(request.path_info).url_name,

        # Variables
    }