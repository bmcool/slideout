from django.contrib import admin
from tiler.corea.admin import BaseLevelAdmin

from slideout.models import *

admin.site.register(SlideoutLevel, BaseLevelAdmin)
