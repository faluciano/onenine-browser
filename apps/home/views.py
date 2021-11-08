# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from apps.home import filetree


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {'user': request.user}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]
        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template
        if load_template == 'browser.html':
            return browser(request, context, load_template)
        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def browser(request, context, load_template):
    if not os.path.exists('onenine_priv'):
        os.mkdir('onenine_priv')
    if not os.path.exists(f'onenine_priv/{request.user}'):
        os.mkdir(f'onenine_priv/{request.user}')

    if request.GET.get('dir') is None:
        dir = os.path.normpath(f'onenine_priv/{request.user}')

    else:
        dir = request.GET.get('dir')

    directory = filetree.FileTree(dir)
    file_path = directory.get_contents()
    file_size = directory.get_size()
    file_type = directory.get_type()

    context['files'] = zip(file_path, file_size, file_type)

    html_template = loader.get_template('home/' + load_template)
    return HttpResponse(html_template.render(context, request))


def create_folder(prev, name):
    os.mkdir(f'{prev}/{name}')
