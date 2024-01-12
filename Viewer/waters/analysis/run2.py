from ..models import drug_methods
from django.db import connection
from .calibration import regress
from .plot_residuals import Figure
from numpy import array
from PySVG import Document


def main(drug: drug_methods):
    doc = Document(w=1100, h=500)

    data = query(drug)

    doc.addChild(residual_figure(data))

    f2 = ir_figure(data)
    f2.x = 600
    doc.addChild(f2)
    return doc.construct()


def residual_figure(data):
    def split(select):
        d = [(i.exp_conc, i.rr) for i in data if i.sample_type == select]
        d.sort()
        exp_conc, rr = zip(*d)
        return array(exp_conc), array(rr)

    exp_cal, rr_cal = split('CAL')
    exp_qcs, rr_qcs = split('QC')

    curve = regress(exp_cal, rr_cal)

    bias = (curve.conc(rr_cal) - exp_cal) / exp_cal
    cal = list(zip(exp_cal, bias))

    bias = (curve.conc(rr_qcs) - exp_qcs) / exp_qcs
    qcs = list(zip(exp_qcs, bias))

    f = Figure(cal, qcs)
    f.set_sizes()

    return f.root


def ir_figure(data):
    def split(select):
        d = [(i.exp_conc, i.ir) for i in data if i.sample_type == select]
        d.sort()
        exp_conc, rr = zip(*d)
        return array(exp_conc), array(rr)

    exp_cal, ir_cal = split('CAL')
    exp_qcs, ir_qcs = split('QC')

    mir = ir_cal.mean()

    bias = (ir_cal - mir) / mir
    cal = list(zip(exp_cal, bias))

    bias = (ir_qcs - mir) / mir
    qcs = list(zip(exp_qcs, bias))

    f = Figure(cal, qcs)
    f.set_sizes()

    return f.root


def query(drug: drug_methods):
    cur = connection.cursor()

    if drug.assigned_istd is not None:
        cur.execute("SELECT ws.sample_name, ws.sample_type, ws.inj_time, wd.exp_conc, wd.area, wd.area2, wi.area "
                    "FROM waters_drugs AS wd "
                    "INNER JOIN waters_istds AS wi ON wd.sample_id = wi.sample_id "
                    "INNER JOIN waters_samples ws on ws.id = wd.sample_id "
                    "WHERE wd.method_id=%s and wi.method_id=%s and "
                    "(ws.sample_type='CAL' or ws.sample_type='QC') and wd.include=True;",
                    (drug.id, drug.assigned_istd.id))
    else:
        cur.execute("SELECT ws.sample_name, ws.sample_type, ws.inj_time, wd.exp_conc, wd.area, wd.area2 "
                    "FROM waters_drugs AS wd "
                    "INNER JOIN waters_samples ws on ws.id = wd.sample_id "
                    "WHERE wd.method_id=%s and "
                    "(ws.sample_type='CAL' or ws.sample_type='QC') and wd.include=True;",
                    (drug.id,))

    data = [Row(i) for i in cur.fetchall()]

    return data


class Row:
    def __init__(self, row: tuple):
        self.sample_name = row[0]
        self.sample_type = row[1]
        self.inj_time = row[2]
        self.exp_conc = self._to_float(row[3])
        self.drug_area = self._to_float(row[4])
        self.qual_area = self._to_float(row[5])

        if len(row) == 7:
            self.istd_area = row[6]
        else:
            self.istd_area = 0

    def _to_float(self, val):
        try:
            return float(val)
        except TypeError:
            return 0

    @property
    def rr(self):
        if self.istd_area is not None and self.istd_area > 0:
            return self.drug_area / self.istd_area
        elif self.drug_area is not None:
            return self.drug_area
        else:
            return 0

    @property
    def ir(self):
        if self.drug_area > 0 and self.drug_area is not None:
            return self.qual_area / self.drug_area
        else:
            return 0
