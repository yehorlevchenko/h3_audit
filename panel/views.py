from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import Audit
from .forms import LoginForm, RegistrationForm


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


def registration(request):
    template = 'panel/registration.html'
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, template, {'new_user': new_user})
    else:
        user_form = RegistrationForm()
    return render(request, template, {'user_form': user_form})
