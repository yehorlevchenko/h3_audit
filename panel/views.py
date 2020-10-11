from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import Audit
from .forms import LoginForm, RegisterForm


def index(request):
    """
    Main panel page
    :param request:
    :return:
    """
    template = 'panel/index.html'
    return render(request, template)


def my_audits(request):
    if request.user.is_authenticated:
        audits = Audit.objects.filter(owner_id=2)
        audits = "\n".join([f"{a.id} - {a.main_url}"
                           for a in audits])
        return HttpResponse(f"Your audits: \n{audits}")
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

def register(request):
    context = {}
    template = 'panel/register.html'
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user:
                login(request, user)
                return redirect('index')
        else:
            context['register_form'] = form
            return render(request, template, context)
    else:
        if request.user.is_authenticated:
            return redirect('index')
        else:
            form = RegisterForm()
            context['register_form'] = form
            return render(request, template, context)



