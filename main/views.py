#-*- encoding: utf-8 -*-

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as django_login
from django.contrib.auth.views import logout as django_logout

def login(request):
    if request.user.is_authenticated():
        return redirect('/')
    else:
        return django_login(request, "index.html")

def logout(request):
    django_logout(request)
    return redirect('/')

def home(request):
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))
