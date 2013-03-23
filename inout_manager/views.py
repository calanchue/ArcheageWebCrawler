from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, Context, loader
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from inout_manager.models import *
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
        self.id = recent_event.id

    def __repr__(self):
        return ('%s, %s, %s, %s, %s' %(self.name, self.prev_exped_name, self.recent_exped_name, self.prev_time, self.recent_time)).encode('utf8')

class PagifiedList(list):
    def __init__(self, page):
        self.page = page
    

row_per_page = 25 

def get_page_num(request):
    if 'page_num' in request.GET:
        page_num = request.GET['page_num'] 
    else :
        page_num = 1
    return page_num

def get_list_from_paginator(paginator, page_num):
    try:
        list = paginator.page(page_num)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        list = paginator.page(paginator.num_pages)
    return list

def pagified_mig_history(player_queryset, page_num):
    paginator = Paginator(player_queryset, row_per_page)
    event_list = get_list_from_paginator(paginator, page_num)
    pagified_history = PagifiedList(event_list)
    for r_event in event_list:
        #mig_history_list.append(MigHistory(r_event.prev_record, r_event))
        pagified_history.append(MigHistory(r_event.prev_record, r_event))
    
    return pagified_history

row_per_page=25
def recent_history_list(page_num):
    all_recent_event_list = Player.objects.all().order_by('-inserted_time')  
    """
    paginator = Paginator(all_recent_event_list, row_per_page)

    recent_event_list = get_list_from_paginator(paginator, page_num) 

    mig_history_list = []
    pagified_history = PagifiedList(paginator)
    for r_event in recent_event_list:
        #mig_history_list.append(MigHistory(r_event.prev_record, r_event))
        pagified_history.append(MigHistory(r_event.prev_record, r_event))
    
    return pagified_history
    #return mig_history_list
    """
    return pagified_mig_history(all_recent_event_list, page_num)

def recent_event(request):
    page_num = get_page_num(request)
    if 'player_name' in request.GET:
        player_name=request.GET['player_name']
        return HttpResponseRedirect(reverse('player_event',args=(request.GET['player_name'],)))

    mig_history_list = recent_history_list(page_num)
 
    context = {'mig_history_list':mig_history_list}
    return render_to_response('inout_manager/base_player_history.dj.html', context, context_instance=RequestContext(request))

def player_event(request, player_name):
    page_num = get_page_num(request)
    player_event_list = Player.objects.filter(name=player_name).order_by('-inserted_time') 
    mig_history_list = pagified_mig_history(player_event_list,page_num) 
    context = {'mig_history_list':mig_history_list}
    return render_to_response('inout_manager/base_player_history.dj.html', context, context_instance=RequestContext(request))

def recent_exped_event(request):
    page_num = get_page_num(request)

    mig_history_list = recent_history_list(page_num)
    context = {'mig_history_list':mig_history_list}
    return render_to_response('inout_manager/base_exped_history.dj.html', context, context_instance=RequestContext(request))

def exped_event(request, exped_name):
    page_num = get_page_num(request)
    exped_history = Player.objects.filter(Q(exped__name=exped_name)|Q(prev_record__exped__name=exped_name)).order_by('-inserted_time')
    mig_history_list = pagified_mig_history(exped_history, page_num) 
    context = {'mig_history_list':mig_history_list}
    return render_to_response('inout_manager/base_exped_history.dj.html', context, context_instance=RequestContext(request))
            
def search_exped_event(request):
    if 'exped_name' in request.GET:
        return HttpResponseRedirect(reverse('exped_event',args=(request.GET['exped_name'],)))
    mig_history = []
    context = {'mig_history_list':mig_history}
    return render_to_response('inout_manager/base_exped_history.dj.html', context, context_instance=RequestContext(request))
