from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest

from .models import runs
from .importer import read

# Create your views here.

url = 'http://127.0.0.1:8000/'


def home(request: HttpRequest):
    data = {}
    query = runs.objects.filter(active=True)

    data['runs'] = [{'name': i.run_name,
                     'link': f'{url}run/{i.id}'} for i in query]

    data['url'] = url

    return render(request, 'home.html', data)


def new_run(request: HttpRequest):
    data = {'post': f'{url}post_run',
            'title': 'New Run'}

    return render(request, 'new_run.html', data)


def post_run(request: HttpRequest):
    info = request.POST

    try:
        file = request.FILES['xml']
        data = read(info['Name'], file)
    except:
        pass

    return redirect(f'{url}')

########################################################################################################################
# Front End
########################################################################################################################

