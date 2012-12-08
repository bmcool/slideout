from tiler.corea.models import *

def get_member_by_user_id(user_id):
    try:
        return Member.objects.get(user_id=user_id)
    except:
        return None

def get_levels_by_member_with_check(level_class, current_member, user):
    levels = level_class.objects.filter(owner=current_member)
    if current_member.user != user:
        levels = level_class.objects.filter(owner=current_member).filter(published=True)
    
    return levels
