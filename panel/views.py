from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    """
    Main panel page
    :param request:
    :return:
    """
    return HttpResponse("Hello, audit.")
