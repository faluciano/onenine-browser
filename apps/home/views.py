# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import json
import os
import shutil

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
        if load_template == 'addFolder':
            return create_folder(request, context)
        if load_template == 'delete':
            return delete(request, context)
        if load_template == 'download':
            return download(request, context)
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
        if dir.split('\\')[1] != str(request.user):
            dir = os.path.normpath(f'onenine_priv/{request.user}')
            print("Invalid user request")

    directory = filetree.FileTree(dir)
    file_path = directory.get_contents()
    file_size = directory.get_size()
    file_type = directory.get_type()

    context['user_dir'] = os.path.normpath(f'onenine_priv/{request.user}')

    context['files'] = zip(file_path, file_size, file_type)
    context['curr_path'] = directory.get_current_path()
    context['curr_dir'] = directory.get_current_path().replace('\\\\', '\\')

    html_template = loader.get_template('home/' + load_template)
    return HttpResponse(html_template.render(context, request))


def create_folder(request, context):
    post_data = json.loads(request.body.decode("utf-8"))
    prev = post_data['file']['dir']
    name = post_data['file']['dir_name']

    html_template = loader.get_template('home/browser.html')
    os.mkdir(f'{prev}/{name}')
    return HttpResponse(html_template.render(context, request))


def delete(request, context):
    post_data = json.loads(request.body.decode("utf-8"))
    path = os.path.normpath(post_data['file'])
    if os.path.isfile(path):
        os.remove(path)
    else:
        shutil.rmtree(path)
    html_template = loader.get_template('home/browser.html')
    return HttpResponse(html_template.render(context, request))


def download(request, context):
    post_data = json.loads(request.body.decode("utf-8"))
    print(post_data['file'])

    html_template = loader.get_template('home/browser.html')
    return HttpResponse(html_template.render(context, request))
