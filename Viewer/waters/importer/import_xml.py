from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element
from ..models import samples, drugs, runs, istds, istd_methods, drug_methods
from datetime import datetime


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

    smpls = [init_samples(i, run, _drugs, _istds) for i in {i for i in root.findall("./SAMPLE")}]
    smpls = [i for i in smpls if i is not None]
    smpls.sort(key=lambda x: x.inj_time)


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

    try:
        sample = samples(sample_name=smpl.attrib['name'],
                         sample_type=smpl.attrib['type'],
                         inj_time=datetime.strptime(f'{d} {t}', pattern),
                         run=run)
        sample.save()
        _ = {i: init_drugs(smpl.findall(f"./COMPOUND/[@name='{i}']")[0], sample, j) for i, j in drug.items()}
        _ = {i: init_istds(smpl.findall(f"./COMPOUND/[@name='{i}']")[0], sample, j) for i, j in istd.items()}

    except:
        return None


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
