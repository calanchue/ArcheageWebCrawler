from bs4 import BeautifulSoup
import urllib

from django.utils import timezone
from inout_manager.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max
from datetime import datetime


def getSoup(url) :
    f= urllib.urlopen(url)
    s = f.read()
    f.close()
    return BeautifulSoup(s)
    
def isErrorPage(soup):
    error_section = soup.find("section", {"class","errorpage"}) 
    return error_section is not None

def getExpedInfo(expedId) : 
    soup = getSoup("http://play.archeage.com/expeditions/HIRAMAKAND/"+str(expedId))
    expedInfoDiv = soup.find("div", {"class","exped_info"}) 
    if(expedInfoDiv is None):
        print("cannot find info div")
    #else:
        #print type(expedInfoDiv).__name__
        #print(expedInfoDiv)
    count = expedInfoDiv.find("em", {"class", "count"})
    print(count.text)

class MemberInfo : 
    def __init__(self, name, classType, level,id) : 
        self.name = name
        self.classType = classType
        self.level = level
        self.id = id
        
    def __repr(self) :
        return "name=%s, classType=%s, level=%d" % (self.name, self.classType, self.level)

class ExpedInfo : 
    def __init__(self, name, id) : 
        self.name = name
        self.id = id

    def __repr__(self) : 
        return "{name=%s, id=%d}" % (self.name.encode('utf8'), self.id)


def getAllExpedList() :
    """ return list of instances of ExpedInfo """
    allExpedInfo = []
    currPageNum = 1
    while True :
        listFromPage = getExpedListFromPage(currPageNum)
        if (len(listFromPage) < 1)  :
            break
        #print "page=%d, num=%d" % (currPageNum, len(listFromPage))
        allExpedInfo = allExpedInfo + listFromPage
        currPageNum += 1
    return allExpedInfo
    

def getExpedListFromPage(pageNum) :
    """ return list of instances of EpxedInfo """
    expedList = []
    soup = getSoup("http://play.archeage.com/exps/all?page="+str(pageNum)+"&expeditionType=MANUFACTURE&gameServer=HIRAMAKAND&searchType=EXPEDITION_NAME")
    expedInfoList = soup.find("ul", {"class","lst"}).findAll("div", {"class", "exped_info"})
    #print expedInfoList
    for expedInfo in expedInfoList:
        nameSpan = expedInfo.find("span", {"class","name"})
        link = expedInfo.find("a") 
        expedId = link["href"].split('/')[3]
        expedList.append(ExpedInfo(nameSpan.text, int(expedId)))
        #print expedId
        
        """
        print link["href"]
        print expedId
        print nameSpan.text
        """
    return expedList
    

def getExpedMemberInfo(expedId): 
    """ return MemberInfo List """
    soup = getSoup("http://play.archeage.com/expeditions/HIRAMAKAND/"+str(expedId)+"/members")
    if  isErrorPage(soup):
        exped = Expedition.objects.get(exped_id=expedId)
        exped.update_time=currTime
        exped.hidden = True
        exped.save()
        return []
    expedMemberTable = soup.find("tbody").findAll("tr")
    ret = []
    for memberRow in expedMemberTable :
        memberInfo = memberRow.findAll("td")
        print memberInfo[1].find("a").text.encode('utf8')
        print memberInfo[1].find("a")
        id = memberInfo[1].find("a")['data-uuid']
        ret.append(MemberInfo(memberInfo[1].find("a").text, memberInfo[3].text, memberInfo[2].text,id))
    return ret

def updatePlayerInfo(exped, player):
    """ input : django Expedition model, Player """
    # iterate all player who is in any expedition. 
    try :
        # get one rows from multiple player rows.
        # the most recent date of the player
        playerInDbHistory = PlayerHistory.objects.filter(name=player.name).order_by('-inserted_time')
        if len(playerInDbHistory) == 0:
            ph = PlayerHistory(name=player.name, exped=exped, update_time=currTime, inserted_time=currTime).save()
            Player(name=player.name, player_id=player.id, recent_record=ph).save()
            return

        playerInDb = playerInDbHistory[0]

        if playerInDb.exped is not None and exped.exped_id == playerInDb.exped.exped_id:
            playerInDb.update_time=currTime
            playerInDb.save()
        else :
            print playerInDb.id
            player = PlayerHistory(name=player.name,exped=exped, update_time = currTime, inserted_time=currTime, prev_record=playerInDb ) 
            player.save()
            player_recent = Player.objects.get(name=player.name)
            player_recent.recent_record = player
            player_recent.save()
    except ObjectDoesNotExist:
        player = PlayerHistory(name=player.name,exped=exped, update_time = currTime, inserted_time=currTime ) 
        player.save()
        player_recent = Player.objects.get(name=player.name)
        player_recent.recent_record = player
        player_recent.save()


def startCrawling():
    global currTime 
    currTime = datetime.now()    

    print 'start crawling %s' % currTime
    
    #update exped
    crawledList = getAllExpedList()
    for crawled in crawledList:
        if not Expedition.objects.filter(exped_id=crawled.id).exists():
            Expedition(name=crawled.name, exped_id=crawled.id, update_time=currTime,inserted_time=currTime).save()
    # get all members of the expeditions in the server.
    expedIdList = Expedition.objects.all().values_list('exped_id', flat=True)
    # crawl current all player in exped
    for expedId in expedIdList:
        print '# process exped %d' % expedId
        pList = getExpedMemberInfo(expedId)
        for player in pList:
            print player.name.encode('utf8')
            exped = Expedition.objects.get(exped_id=expedId)
            updatePlayerInfo(exped, player)
    print '-------outed---------' 
    # remained player is someone who is out of exepdtion. update this.
    #playerNameOuted = list(set(PlayerHistory.objects.exclude(update_time=currTime).values_list('name',flat=True)))           

    outed_player_list_id = Player.objects.filter(recent_record__update_time__lt=currTime).values_list('recent_record', flat=True)
    outed_player_list = PlayerHistory.objects.filter(id__in=outed_player_list_id)

    for player in outed_player_list:
        if player.exped is None:
            # alredy outsider
            player.update_time = currTime
            player.save()
            continue
        else :
            # new outsider
            player = PlayerHistory(name=player.name, exped=None, update_time = currTime, inserted_time=currTime, prev_record=player )
            player.save()
            player_recent = Player.objects.get(name=player.name )
            player_recent.recent_record = player
            player_recent.save()
    

def test():
    name_time_list= PlayerHistory.objects.values('name').annotate(recent_time=Max('update_time'))
    for name_time in name_time_list:
        print name_time['name'], name_time['recent_time']

def updateRecentPlayer():
    name_list=list(set(PlayerHistory.objects.values_list('name',flat=True)))
    for name in name_list:
        player = PlayerHistory.objects.filter(name=name).order_by('-inserted_time')[0]
        try:
            player_recent = Player.objects.get(name=name);
            player_recent.recent_record=player
        except DoesNotExist:
            Player(name=name, recent_record = player).save() 
    

def run():
    #getExpedMemberInfo(1005)
    #playerInDb = PlayerHistory.objects.filter(name='test_outed').order_by('-update_time')[0]
    #print 'expedition = %s' % playerInDb.exped.name
    startCrawling()
    #updateRecentPlayer()
    #test()

#getExpedInfo(1005)
#getExpedMemberInfo(1005)
#getExpedList()
#getExpedListFromPage(2)
