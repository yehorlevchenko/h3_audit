from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User

from .models import Audit


def index(request):
    """
    Main panel page
    :param request:
    :return:
    """
    return HttpResponse("Hello, audit.")


def my_audits(request):
    audits = Audit.objects.filter(owner_id=2)
    audits = "\n".join([f"{a.id} - {a.main_url}"
                       for a in audits])
    return HttpResponse(f"Your audits: \n{audits}")
