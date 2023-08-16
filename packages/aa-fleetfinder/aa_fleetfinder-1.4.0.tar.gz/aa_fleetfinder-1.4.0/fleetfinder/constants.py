"""
Constants used in this app
"""

# Django
from django.utils.text import slugify

# AA Fleet Finder
from fleetfinder import __verbose_name__, __version__

verbose_name_slugified: str = slugify(__verbose_name__, allow_unicode=True)
github_url: str = "https://github.com/ppfeufer/aa-fleetfinder"

USER_AGENT = f"{verbose_name_slugified} v{__version__} {github_url}"
