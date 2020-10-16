from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import Audit, AuditResults, Check
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
    context = dict()
    template = 'panel/my_audits.html'
    if request.user.is_authenticated:
        audits = Audit.objects.filter(owner_id=request.user.id)
        context['audits'] = audits
        return render(request, template, context)
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


def audit_results(request, audit_id):
    template = 'panel/audit_results.html'
    checks = Check.objects.all()
    checks_group_name = Check.get_group_name()
    audit_obj = Audit.objects.get(pk=audit_id)
    context = {'checks': checks, 'checks_group_name': checks_group_name, 'audit_obj': audit_obj}
    if request.user.is_authenticated:
        if request.user.id == audit_obj.owner_id_id:
            urls_by_checks = dict()
            audit_results = AuditResults.objects.filter(audit_id=audit_id)
            for check in checks:
                results = list()
                for url_result in audit_results:
                    if check.code_error == url_result.code_error:
                        results.append(url_result)
                urls_by_checks[check.code_error] = results
            context.update({'audit_results': urls_by_checks})
            return render(request, template, context)
        else:
            return redirect('my_audits')
    else:
        return redirect('login_page')




