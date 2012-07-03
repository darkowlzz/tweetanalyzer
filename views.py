#from django.template.loader import get_template
#from django.template import Context
#from django.http import HttpResponse
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
import datetime

def custom_proc(request):
    return  {
                'user': request.user,
                'ip_address': request.META['REMOTE_ADDR']
            }

@login_required
def home(request):
    return render_to_response('home.html',context_instance=RequestContext(request, processors=[custom_proc]))

def current_datetime(request):
    current_date = datetime.datetime.now()
    return render_to_response('current_datetime.html', locals())

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/home/")
    else:
        form = UserCreationForm()
    return render_to_response("registration/register.html", {'form': form, }, context_instance=RequestContext(request, processors=[custom_proc]))
