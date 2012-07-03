from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from tweetanalyzer.bmtu.forms import FollowForm
from bmtu.models import Tweets, Usr, Follow
from tweetanalyzer.views import custom_proc
from django.template import RequestContext
from django.http import HttpResponseRedirect

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
def follow(request):
    if request.method == 'POST':
        form = FollowForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            a = Usr(user=request.user, following=cd['handler'])
            b = Follow(handler=cd['handler'])
            
            present=False
            for i in Usr.objects.filter(user=request.user):
                if a.following == i.following:
                    present=True
                    break
            if not present:
                try:
                    a.save()
                    b.save()
                except:
                    pass

            return HttpResponseRedirect('/follow/thanks/')
    else:
        form = FollowForm()
    return render_to_response('follow_form.html', {'form': form}, context_instance=RequestContext(request, processors=[custom_proc]))

@login_required
def thanks(request):
    return render_to_response('thanks.html', context_instance=RequestContext(request, processors=[custom_proc]))
