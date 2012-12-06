#-*- encoding: utf-8 -*-

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as django_login
from django.contrib.auth.views import logout as django_logout

from main.models import *

def login(request):
    if request.user.is_authenticated():
        return redirect('/')
    else:
        return django_login(request, "index.html")

def logout(request):
    django_logout(request)
    return redirect('/')

def home(request):
    members = Member.objects.all()
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))

def _get_member_by_username(username):
    try:
        return Member.objects.get(user__username=username)
    except:
        return None

def game_member(request, username):
    current_member = _get_member_by_username(username)
    if not current_member:
        return redirect('/')
    
    levels = current_member.level_set.filter(published=True).order_by("order")
    
    return render_to_response('member.html', locals(), context_instance=RequestContext(request))

def game_level(request, username, level_id):    
    current_member = _get_member_by_username(username)
    if not current_member:
        return redirect('/')
    
    levels = current_member.level_set.filter(published=True)
    if levels.count() == 0:
        return redirect('/game/' + current_member.user.username + '/')
    levels = levels.order_by("order")
    
    try:
        level = levels.get(id=level_id)
    except Exception as e:
        return redirect('/game/' + current_member.user.username + '/')
    
    return render_to_response('game.html', locals(), context_instance=RequestContext(request))
