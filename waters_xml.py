from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element
from models import samples as s, drug as d, istd
from datetime import datetime


def read(data):
    tree = ET.parse(data)
    root = tree.getroot().find("./GROUPDATA/GROUP/SAMPLELISTDATA")

    drugs = get_drugs(root)
    istds = get_istds(root)

    return get_samples(root, drugs, istds)


def get_samples(root: Element, drugs: list[str], istds: list[str]):
    smpls = [init_samples(i, drugs, istds) for i in {i for i in root.findall("./SAMPLE")}]
    smpls = [i for i in smpls if i is not None]
    smpls.sort(key=lambda x: x.inj_time)
    return smpls


def get_drugs(root: Element):
    drugs = list({i.attrib['name'] for i in root.findall("./SAMPLE/COMPOUND") if i.attrib['type'] != 'ISTD'})
    drugs.sort(key=lambda x: x.lower())
    return drugs


def get_istds(root: Element):
    istds = list({i.attrib['name'] for i in root.findall("./SAMPLE/COMPOUND") if i.attrib['type'] == 'ISTD'})
    istds.sort(key=lambda x: x.lower())
    return istds


def init_samples(smpl: Element, drugs: list[str], istds: list[str]):
    si = s()
    si.ID = smpl.attrib['id']
    si.sample_name = smpl.attrib['name']
    si.sample_type = smpl.attrib['type']

    d = smpl.attrib['createdate']
    t = smpl.attrib['createtime']

    pattern = '%d-%b-%y %H:%M:%S'

    try:
        si.inj_time = datetime.strptime(f'{d} {t}', pattern)
        si.drugs = {i: init_drugs(smpl.findall(f"./COMPOUND/[@name='{i}']")[0]) for i in drugs}
        si.istds = {i: init_istds(smpl.findall(f"./COMPOUND/[@name='{i}']")[0]) for i in istds}
        return si
    except:
        return None


def to_float(val):
    try:
        return float(val)
    except:
        return 0


def init_drugs(analyte: Element):
    di = d()
    di.name = analyte.attrib['name']
    di.exp_conc = to_float(analyte.attrib['stdconc'])

    peak = analyte.find('./PEAK')
    if peak is not None:
        di.area = to_float(peak.attrib['area'])

        qual = peak.find('./CONFIRMATIONIONPEAK1')
        if qual is not None:
            di.area2 = to_float(qual.attrib['area'])

    return di


def init_istds(analyte: Element):
    istd_i = istd()

    istd_i.name = analyte.attrib['name']

    peak = analyte.find('./PEAK')
    if peak is not None:
        istd_i.area = to_float(peak.attrib['area'])

    return istd_i
