from tiler.corea.models import BaseLevel
from django.utils.translation import ugettext, ugettext_lazy as _

class SlideoutLevel(BaseLevel):
    class Meta:
        db_table = 'slideout_level'
        verbose_name = _("Level")
        verbose_name_plural = _("Levels")
