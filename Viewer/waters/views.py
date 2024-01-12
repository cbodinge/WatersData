from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

from .models import runs, drug_methods, istd_methods, samples, drugs
from .importer import read, import_method as im_method
from .analysis.run2 import main
from django.db.models import Q

from .exporter.export_method import main as ex_method

# Create your views here.

url = 'http://127.0.0.1:8000/'


def home(request: HttpRequest):
    data = {}
    query = runs.objects.filter(active=True)

    data['runs'] = [{'name': i.run_name,
                     'link': f'{url}show/{i.id}'} for i in query]

    data['url'] = url

    return render(request, 'home.html', data)


def new_run(request: HttpRequest):
    data = {'post': f'{url}post_run',
            'title': 'New Run'}

    return render(request, 'new_run.html', data)


def post_run(request: HttpRequest):
    info = request.POST
    file = request.FILES['xml']
    read(str(info['Name']), file)

    return redirect(f'{url}')


########################################################################################################################
# Front End
########################################################################################################################


def show(request: HttpRequest, run_id: int):
    run = runs.objects.filter(id=run_id).get()
    drgs = drug_methods.objects.filter(run=run).order_by('drug_name')
    istd = istd_methods.objects.filter(run=run).order_by('istd_name')
    smpls = samples.objects.filter(run=run, sample_type='CAL')

    return render(request, 'results.html', {'run': run, 'drugs': drgs, 'istds': istd,
                                            'samples': smpls, 'url': f'{url}show/{run_id}/refresh'})


def refresh(request: HttpRequest):
    data = request.POST
    if data['drugs'] == '':
        return HttpResponse('')
    drug = drug_methods.objects.get(id=data['drugs'])

    cals = drugs.objects \
        .filter(method=drug, sample__sample_type='CAL', include=True) \
        .values_list('exp_conc', flat=True)

    drug.min = min(cals)
    drug.max = max(cals)
    drug.save()

    return HttpResponse(main(drug))


def add_checkbox(request: HttpRequest):
    data = request.POST
    if data['drugs'] == '':
        return HttpResponse('')
    drug = drug_methods.objects.get(id=data['drugs'])

    x = drugs.objects.filter(method=drug, sample__sample_type='CAL')
    d = {True: 'checked', False: 'unchecked'}
    html_str = [f'''
    <label for="s_{i.sample_id}">{i.exp_conc}</label>
    <input hx-get="/save_check" hx-include="#drugs,#s_{i.sample_id}" hx-swap="none"
    class="ranges refresh" type="checkbox" id="s_{i.sample_id}" name="sample - {i.sample_id}" {d[i.include]}>
    <input type="hidden" id="s_{i.sample_id}" name="sample" value="{i.sample_id}"/>
    ''' for i in x]

    return HttpResponse('\n'.join(html_str))


def add_istd_box(request: HttpRequest):
    data = request.POST
    if data['drugs'] == '':
        return HttpResponse('')
    drug = drug_methods.objects.get(id=data['drugs'])

    if drug.assigned_istd is None:
        istd = istd_methods.objects.filter(run_id=drug.run_id).order_by('istd_name')
        istd = istd.values_list('id', 'istd_name')
        assigned = ''
        ass_id = ''
    else:
        istd = istd_methods.objects.filter(Q(run_id=drug.run_id) & ~Q(id=drug.assigned_istd_id)).order_by('istd_name')
        istd = istd.values_list('id', 'istd_name')
        assigned = drug.assigned_istd.istd_name
        ass_id = drug.assigned_istd_id

    options = '\n'.join([f'<option value="{i}">{j}</option>' for i, j in istd])
    html_str = f'''
    <label for="istds">Choose an Internal Standard:</label>
    <select hx-get="/save_istd" hx-include="#istds,#drugs" hx-swap="none" 
    name="istds" id="istds" class="refresh">
        <option value="{ass_id}" selected="selected">{assigned}</option>
        {options}
    </select>
    '''

    return HttpResponse(html_str)


def save_istd(request: HttpRequest):
    data = request.GET
    if not data:
        data = request.POST
    if data['drugs'] == '':
        return render(request, '')
    drug = drug_methods.objects.get(id=data['drugs'])

    if data['istds'] != '':
        istd = istd_methods.objects.get(id=data['istds'])
        drug.assigned_istd = istd
        drug.save()

    return HttpResponse('')


def save_check(request: HttpRequest):
    data = request.GET
    if data['drugs'] == '':
        return render(request, '')
    drug = drug_methods.objects.get(id=data['drugs'])

    included = len(data) == 3
    drug = drugs.objects.filter(sample_id=data['sample'], method=drug).get()
    drug.include = included
    drug.save()

    return HttpResponse('')


# Data I/O ############################################################################################################

def export_method(request: HttpRequest, run_id: int):
    ex_method(run_id)

    return redirect(f'{url}')


def import_method(request: HttpRequest, run_id: int):
    im_method(run_id)

    return redirect(f'{url}show/{run_id}')
