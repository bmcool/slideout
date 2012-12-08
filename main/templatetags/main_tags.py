from tiler.corea.models import *

from mezzanine import template
register = template.Library()

@register.as_tag
def get_all_members_for():
    return Member.objects.all()
