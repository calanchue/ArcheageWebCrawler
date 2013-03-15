from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

def index(request):
  return render_to_response('starter-template.html',{}, context_instance=RequestContext(request))

def view(request):
    return HttpResponse("ok");

def detail(request, poll_id):
  return HttpResponse("You're looking at poll %s." % poll_id)

def results(request, poll_id):
  return HttpResponse("You're looking at the results of poll %s." % poll_id)

def vote(request, poll_id):
  return HttpResponse("You're voting on poll %s." % poll_id)
