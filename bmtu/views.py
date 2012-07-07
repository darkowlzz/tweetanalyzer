from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from tweetanalyzer.bmtu.forms import FollowForm
from bmtu.models import Tweets, Usr, Follow
from tweetanalyzer.views import custom_proc
from django.template import RequestContext
from django.http import HttpResponseRedirect
import requests     # install this module separately if not installed

@login_required
def home(request):
    lst = Usr.objects.filter(user=request.user)
        
    return render_to_response('home.html', {'lst':lst}, context_instance=RequestContext(request, processors=[custom_proc]))

@login_required
def tweet_list(request, handler, page=0):
    tweets = Tweets.objects.filter(handler=handler)
    img = tweets[0].image
    print img

    count = tweets.count()/10
    next = 1
    if int(page) == (count):
        next = 0
   
    lst = []
    for i in range(int(page)*10, (int(page)*10)+10):
        try:
            lst.append(tweets[i])
        except:
            pass

    return render_to_response('tweets.html', locals(), context_instance=RequestContext(request, processors=[custom_proc]))

@login_required
def subscribe(request):

    """ This part receives the twitter id's and maked necessary changes in the database"""
    if request.method == 'POST':
        form = FollowForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data  # make the received data more pythonic
            a = Usr(user=request.user, following=cd['handler']) # creates an instance of Usr according to the received data from POST request
            b = Follow(handler=cd['handler'])   # creates an instance of Follow according to the received data from the POST request
            
            present=False   # presence of a not known
            for i in Usr.objects.filter(user=request.user):
                # check for same entry in table
                if a.following == i.following:  
                    present=True    # a is presnet
                    break

            if not present:     # a not present 
                a.save()
                try:
                    b.save()    #this will fail if a user is already being followed by TweetAnalyzer
                except:
                    # don't save anything if anyone of a and b fails to save
                    pass

            return HttpResponseRedirect('/subscribe/thanks/')
    else:
        """ Collects all the followers using Twitter API and sends to the form"""
        # sending the http request to twitter
        r = requests.get('https://api.twitter.com/1/friends/ids.json?id=' + request.user.username)
        idlst = r.json['ids']    #   store the json id list string to a variable

        # list of users already subscribed
        lst1 = []
        following = Usr.objects.filter(user=request.user)
        for f in following:
            lst1.append(f.following)
        
        print lst1
        # list of all the users followed
        lst2 = []   

        # convert all the twitter user ids to username
        for l in idlst:
            r = requests.get('http://api.twitter.com/1/users/lookup.json?user_id=' + str(l))
            lst2.append(r.json[0]['screen_name']) 
        
        print lst2 
        # difference of lst2 and lst1
        lst = []
        for item in lst2:
            if not item in lst1:
                lst.append(item)
         
        print lst
        #    form = FollowForm()
        return render_to_response('follow_form.html', {'lst': lst}, context_instance=RequestContext(request, processors=[custom_proc]))

@login_required
def thanks(request):
    return render_to_response('thanks.html', context_instance=RequestContext(request, processors=[custom_proc]))
