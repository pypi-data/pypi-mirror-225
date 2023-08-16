"""
Initialize the app
"""

# Standard Library
from importlib import metadata

# Django
from django.utils.translation import gettext_lazy as _

__version__ = metadata.version("aa-fleetfinder")
__title__ = _("Fleet Finder")
__verbose_name__ = "Fleet Finder for Alliance Auth"

del metadata
