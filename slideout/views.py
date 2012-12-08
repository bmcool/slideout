#-*- encoding: utf-8 -*-

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from slideout.models import *

from tiler.utils.models import *

def game_member(request, user_id):
    current_member = get_member_by_user_id(user_id)
    if not current_member:
        return redirect('/')
    
    levels = get_levels_by_member_with_check(SlideoutLevel, current_member, request.user).order_by("order")
    
    return render_to_response('member.html', locals(), context_instance=RequestContext(request))

def game_level(request, user_id, level_id):    
    current_member = get_member_by_user_id(user_id)
    if not current_member:
        return redirect('/')
    
    levels = get_levels_by_member_with_check(SlideoutLevel, current_member, request.user)
    
    if levels.count() == 0:
        return redirect('/game/' + current_member.user.user_id + '/')
    levels = levels.order_by("order")
    
    try:
        current_level = levels.get(id=level_id)
    except Exception as e:
        return redirect('/game/' + current_member.user.user_id + '/')
    
    return render_to_response('game.html', locals(), context_instance=RequestContext(request))
