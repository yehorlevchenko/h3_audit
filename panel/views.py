from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import Audit, AuditResults, Check
from .forms import LoginForm, RegisterForm, NewAuditForm

import rabbitpy

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


def new_audit(request):
    template = 'panel/new_audit.html'
    context = {'form': NewAuditForm}

    if not request.user.is_authenticated:
        return redirect('login_page')

    if request.method == "POST":
        form = NewAuditForm(request.POST)
        if not form.is_valid():
            return redirect('new_audit')
        new_audit = Audit(main_url=request.POST['main_url'],
                          owner_id=request.user)
        new_audit.save()
        _post_new_audit({"audit_id": new_audit.id,
                         "main_url": new_audit.main_url,
                         "limit": 50})
        return redirect('my_audits')
    else:
        return render(request, template, context=context)


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

def _post_new_audit(result_data):
    # audit_results = {"audit_id": 1,
    #                  "main_url": "http://python.org",
    #                  "page_data": [%dict with page results%]
    #                  }
    with rabbitpy.Connection('amqp://localhost:5672') as connection:
        with connection.channel() as channel:
            final_message = rabbitpy.Message(
                channel=channel,
                body_value=result_data
            )
            final_message.publish(exchange="audit", routing_key="audit_start")


curl -u guest:guest -H "content-type:application/json" -X POST -d'{"properties":{"delivery_mode":2},"routing_key":"audit_start","payload":"TEST","payload_encoding":"string"}' http://localhost:15672/api/exchanges/%2f/amq.default/publish
