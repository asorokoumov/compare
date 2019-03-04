# coding=utf-8

import logging
from django.shortcuts import render

logger = logging.getLogger('compare')



def error404(request):
    return render(request, 'technical/404.html', status=404)


def error500(request):
    return render(request, 'technical/500.html', status=500)

