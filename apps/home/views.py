# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import json
import os
import shutil
from base64 import b64encode

import pandas as pd
from django import template
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
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
        load_template = ''
        if os.name == 'posix':
            temp = request.path.split('?')[0]
            load_template = temp.split('/')[-1]
        else:
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
        if load_template == 'explore.html':
            return explore(request, context, load_template)
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
    if request.method == 'POST':
        print("POST request made")
        upload_file = request.FILES['inpFile']
        temp_path = request.POST['path'].replace('\\\\', '/')
        if os.path.isfile(temp_path + '/' + upload_file.name):
            os.remove(temp_path + '/' + upload_file.name)
        fs = FileSystemStorage(location=temp_path)
        fs.save(upload_file.name, upload_file)

    # download request
    if request.GET.get('download'):
        dir = os.path.normpath(request.GET.get('download'))
        # redirect to not found page in case user make an invalid request
        path = '\\' if os.name != 'posix' else '/'
        if dir.split(path)[1] != str(request.user):
            html_template = loader.get_template('home/page-404.html')
            return HttpResponse(html_template.render(context, request))

        # response for download
        response = HttpResponse(open(dir, 'rb').read(), content_type="application/file")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(dir)
        return response

    elif request.GET.get('dir') is None:
        dir = os.path.normpath(f'onenine_priv/{request.user}')

    else:
        dir = request.GET.get('dir')
        path = '\\' if os.name != 'posix' else '/'
        if dir.split(path)[1] != str(request.user):
            html_template = loader.get_template('home/page-404.html')
            return HttpResponse(html_template.render(context, request))

    # File preview

    if os.path.isfile(dir) and dir.split('.')[-1] != "zip":
        context['is_file'] = True

        file_type = os.path.splitext(dir)[1].lower()
        context['file_type'] = file_type

        if file_type == '.csv':
            # reading csv data file
            csv_data = pd.read_csv(dir, nrows=999)
            # setting context to dictionary item of dataframe
            context['csv_header'] = csv_data.columns.values.tolist()
            context['csv_data'] = csv_data.to_dict('records')
        if file_type == '.txt':
            txt_file = open(dir, "r+", encoding='UTF-8')
            txt_content = txt_file.read()
            context['txt_data'] = txt_content
        if file_type == '.jpg' or file_type == '.jpeg' or file_type == '.png':
            img = ''
            with open(dir, "rb") as image:
                img = b64encode(image.read()).decode('utf-8')
            context['img_data'] = img

    else:
        context['is_file'] = False

    directory = filetree.FileTree(dir)
    file_path = directory.get_contents()
    file_size = directory.get_size()
    file_type = directory.get_type()

    context['user_dir'] = os.path.normpath(f'onenine_priv/{request.user}')

    context['files'] = zip(file_path, file_size, file_type)
    context['curr_path'] = directory.get_current_path()
    if os.name == "posix":
        context['curr_dir'] = directory.get_current_path()
    else:
        context['curr_dir'] = directory.get_current_path().replace('\\\\', '\\')

    context['path'] = '/' if os.name == 'posix' else '\\'
    html_template = loader.get_template('home/' + load_template)
    return HttpResponse(html_template.render(context, request))


def explore(request, context, load_template):
    if not os.path.exists('onenine_priv'):
        os.mkdir('onenine_priv')
    if not os.path.exists(f'onenine_priv/{request.user}'):
        os.mkdir(f'onenine_priv/{request.user}')

    if request.GET.get('dir') is None:
        dir = os.path.normpath(f'onenine_priv/{request.user}')

    else:
        dir = request.GET.get('dir')
        path = '\\' if os.name != 'posix' else '/'
        if dir.split(path)[1] != str(request.user):
            html_template = loader.get_template('home/page-404.html')
            return HttpResponse(html_template.render(context, request))

    # File preview

    if os.path.isfile(dir) and dir.split('.')[-1] != "zip":

        # Here file path is the uploaded file
        # It can be used to read / update the file
        # In this case we are using it to read the file for preview

        context['is_file'] = True

        file_type = os.path.splitext(dir)[1].lower()
        context['file_type'] = file_type

        if file_type == '.csv':
            # reading csv data file
            csv_data = pd.read_csv(dir, nrows=999)
            # setting context to dictionary item of dataframe
            context['csv_header'] = csv_data.columns.values.tolist()
            context['csv_data'] = csv_data.to_dict('records')
        if file_type == '.txt':
            txt_file = open(dir, "r+", encoding='UTF-8')
            txt_content = txt_file.read()
            context['txt_data'] = txt_content
        if file_type == '.jpg' or file_type == '.jpeg' or file_type == '.png':
            img = ''
            with open(dir, "rb") as image:
                img = b64encode(image.read()).decode('utf-8')
            context['img_data'] = img

    else:
        context['is_file'] = False

    directory = filetree.FileTree(dir)
    file_path = directory.get_contents()
    file_size = directory.get_size()
    file_type = directory.get_type()

    context['user_dir'] = os.path.normpath(f'onenine_priv/{request.user}')

    context['files'] = zip(file_path, file_size, file_type)
    context['curr_path'] = directory.get_current_path()
    if os.name == "posix":
        context['curr_dir'] = directory.get_current_path()
    else:
        context['curr_dir'] = directory.get_current_path().replace('\\\\', '\\')

    context['path'] = '/' if os.name == 'posix' else '\\'
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
