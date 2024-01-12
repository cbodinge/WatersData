from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element
from ..models import samples, drugs, runs, istds, istd_methods, drug_methods
from datetime import datetime
from django.db import connection


def to_float(val):
    try:
        return float(val)
    except:
        return 0


def read(run_name: str, data):
    tree = ET.parse(data)
    root = tree.getroot().find("./GROUPDATA/GROUP/SAMPLELISTDATA")

    get_samples(root, run_name)


def get_samples(root: Element, run_name: str):
    run = runs.objects.filter(run_name=run_name)
    if len(run) == 0:
        run = runs(run_name=run_name, active=True)
        run.save()
    else:
        run = run.get()

    _drugs = get_drugs(run, root)
    _istds = get_istds(run, root)

    smpls = list({i for i in root.findall("./SAMPLE")})
    smpls.sort(key=lambda x: x.attrib['name'])
    _ = [init_samples(i, run, _drugs, _istds) for i in smpls]

    init_ranges(run.id)


def get_drugs(run: runs, root: Element):
    _drugs = list({i.attrib['name'] for i in root.findall("./SAMPLE/COMPOUND") if i.attrib['type'] != 'ISTD'})
    _drugs.sort(key=lambda x: x.lower())
    d = {}
    for drug in _drugs:
        item = drug_methods.objects.filter(run=run, drug_name=drug)
        if not item:
            item = drug_methods(run=run, drug_name=drug)
            item.save()
        else:
            item = item.get()
        d[drug] = item

    return d


def get_istds(run: runs, root: Element):
    _istds = list({i.attrib['name'] for i in root.findall("./SAMPLE/COMPOUND") if i.attrib['type'] == 'ISTD'})
    _istds.sort(key=lambda x: x.lower())
    d = {}
    for istd in _istds:
        item = istd_methods.objects.filter(run=run, istd_name=istd)
        if not item:
            item = istd_methods(run=run, istd_name=istd)
            item.save()
        else:
            item = item.get()
        d[istd] = item

    return d


def init_samples(smpl: Element, run: runs, drug, istd):
    d = smpl.attrib['createdate']
    t = smpl.attrib['createtime']
    pattern = '%d-%b-%y %H:%M:%S'

    # try:
    stype = {'Standard': 'CAL', 'QC': 'QC'}

    sample = samples(sample_name=smpl.attrib['name'],
                     sample_type=stype.get(smpl.attrib['type'], 'O'),
                     inj_time=datetime.strptime(f'{d} {t}', pattern),
                     run=run)
    sample.save()
    _ = {i: init_drugs(smpl.findall(f"./COMPOUND/[@name='{i}']")[0], sample, j) for i, j in drug.items()}
    _ = {i: init_istds(smpl.findall(f"./COMPOUND/[@name='{i}']")[0], sample, j) for i, j in istd.items()}

    # except:
    #     return None


def init_drugs(analyte: Element, sample: samples, method: drug_methods):
    drug = drugs(method=method,
                 exp_conc=to_float(analyte.attrib['stdconc']),
                 sample=sample)

    peak = analyte.find('./PEAK')
    if peak is not None:
        drug.area = to_float(peak.attrib['area'])

        qual = peak.find('./CONFIRMATIONIONPEAK1')
        if qual is not None:
            drug.area2 = to_float(qual.attrib['area'])

    drug.save()


def init_istds(analyte: Element, sample: samples, method: drug_methods):
    istd = istds(method=method,
                 sample=sample)

    peak = analyte.find('./PEAK')
    if peak is not None:
        istd.area = to_float(peak.attrib['area'])

    istd.save()


def init_ranges(run_id: int):
    cur = connection.cursor()

    cur.execute("""WITH cals AS (SELECT id FROM waters_samples AS ws WHERE sample_type='CAL')
                    UPDATE waters_drug_methods SET
                        min = (SELECT min(wd.exp_conc) FROM waters_drugs AS wd                        
                            WHERE wd.method_id=waters_drug_methods.id and wd.sample_id IN cals and wd.include=TRUE),
                        max = (SELECT max(wd.exp_conc) FROM waters_drugs AS wd 
                            WHERE wd.method_id=waters_drug_methods.id and wd.sample_id IN cals and wd.include=TRUE)
                    WHERE run_id=%s;""", (run_id,))
