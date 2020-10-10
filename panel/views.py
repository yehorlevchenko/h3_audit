from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import Audit
from .forms import LoginForm


def index(request):
    """
    Main panel page
    :param request:
    :return:
    """
    template = 'panel/index.html'
    return render(request, template)


def my_audits(request):
    # TODO: add django table library
    if request.user.is_authenticated:
        audits = Audit.objects.filter(owner_id=request.user)
        audits = [{'id': a.id, 'main_url': a.main_url} for a in audits]
        context = {'audits': audits}
        template = 'panel/my_audits.html'

        return render(request, template, context=context)
    else:
        return redirect('login_page')


def login_page(request):
    template = 'panel/login_page.html'
    context = {'form': LoginForm}
    # login attempt
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'panel/index.html')
        else:
            return render(request, template, context=context)
    # login form
    else:
        return render(request, template, context=context)

