from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, Context, loader
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from inout_manager.models import *

def index(request):
    return render_to_response('starter-template.html',{}, context_instance=RequestContext(request))

def view(request):
    return HttpResponse("ok");

def bootstrap_test(request):
    return render_to_response('inout_manager/index.html',{}, context_instance=RequestContext(request))

def response(request):
    #latest_player = Player.objects.order_by('name')[:5]
    #template = loader.get_template('inout_manager/index.html')
    #context = Context({'latest_poll_list': latest_player,})
    #return HttpResponse(template.render(context))
    #context = {'latest_poll_list': latest_player,}
    return render(request, 'inout_manager/index.html', context)

class MigHistory:
    def __init__(self, prev_event, recent_event):
        """ recent event must not be none """
        self.name = recent_event.name
        if prev_event is None:
            self.prev_exped_name = '-'
            self.prev_time = '-' 
        else:
            if prev_event.exped is None:
                self.prev_exped_name = '-'
            else:
                self.prev_exped_name = prev_event.exped.name
            self.prev_time = prev_event.inserted_time
        self.recent_exped_name = recent_event.exped.name if recent_event.exped is not None else '-'
        self.recent_time = recent_event.inserted_time 

    def __repr__(self):
        return ('%s, %s, %s, %s, %s' %(self.name, self.prev_exped_name, self.recent_exped_name, self.prev_time, self.recent_time)).encode('utf8')

def recent_event(request):
    if 'player_name' in request.GET:
        player_name=request.GET['player_name']
        return HttpResponseRedirect(reverse('player_event'), player_name=request.GET['player_name'])

    recent_event_list = Player.objects.all().order_by('-inserted_time')[:50]  
    mig_history_list = []
    for r_event in recent_event_list:
        prev_event = None
        player_event_list = Player.objects.filter(name=r_event.name).order_by('-inserted_time')
        for p_event in player_event_list:
            #print r_event.name, p_event.inserted_time, r_event.inserted_time
            if p_event.inserted_time < r_event.inserted_time:
                #print 'pass'
                prev_event = p_event
                break;
        mig_history_list.append(MigHistory(prev_event, r_event))

    context = {'mig_history_list':mig_history_list}
    return render_to_response('inout_manager/player_history.dj.html', context, context_instance=RequestContext(request))

def player_event(request, player_name):
    player_event_list = Player.objects.filter(name=player_name).order_by('inserted_time')

    mig_history_list = [] 
    prev_event = None
    for event in player_event_list:
        mig_history_list.append(MigHistory(prev_event, event))
        prev_event = event

    context = {'mig_history_list':mig_history_list}
    return render_to_response('inout_manager/player_history.dj.html', context, context_instance=RequestContext(request))

