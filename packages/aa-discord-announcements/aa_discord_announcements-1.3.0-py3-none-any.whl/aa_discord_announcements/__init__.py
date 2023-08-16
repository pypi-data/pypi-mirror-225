"""
A couple of variables to use throughout the app
"""

# Standard Library
from importlib import metadata

# Django
from django.utils.translation import gettext_lazy as _

__version__ = metadata.version("aa-discord-announcements")
__title__ = _("Discord Announcements")

del metadata
