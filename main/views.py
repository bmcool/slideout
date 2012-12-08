#-*- encoding: utf-8 -*-

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from django.contrib.auth.views import login as django_login
from django.contrib.auth.views import logout as django_logout
from django.contrib.auth.views import password_change as django_password_change

from django.contrib.auth.models import Group

from tiler.corea.models import *

def login(request):
    if request.user.is_authenticated():
        return redirect('/')
    else:
        return django_login(request, "index.html")

def logout(request):
    django_logout(request)
    return redirect('/')

def password_change(request, template_name='password_change_form.html'):
    if not request.user.is_authenticated():
        return redirect('/login/')
    
    if request.user.is_staff:
        return redirect('/admin/password_change/')
    else:
        return django_password_change(request, template_name=template_name, post_change_redirect='/logout/')

def home(request):
    if request.user.is_active and not request.user.is_staff:
        game_maker_group = Group.objects.get(name='GameMaker')
        request.user.groups.add(game_maker_group)
        request.user.is_staff = True
        request.user.save()
    
    members = Member.objects.all()
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))
