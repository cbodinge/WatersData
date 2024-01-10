import numpy as np

from waters_xml import read
from models import Run
from numpy import array
from calibration import regress
from plot_axp import Figure as F
from PySVG import Document


def read_xml():
    path = 'C:\\PinPoint\\MassHunter\\Data\\KAN\\[C18] TOX-2001A\\Bias & Precision - 1\\quandata.xml'
    with open(path, 'r') as file:
        return Run(read(file))


def main():
    run = read_xml()
    drugs = list(run.drugs)
    istds = list(run.istds)
    doc = Document(w=3000, h=500 * len(drugs))

    cal = run.cals
    qcs = run.qcs

    for row, drug in enumerate(drugs):
        d_res = list(cal.get_drug_results(drug))
        exp = array([i.exp_conc for i in d_res])

        y = [0] * len(istds)

        for index, istd in enumerate(istds):
            i_res = list(cal.get_istd_results(istd))

            rr = array([d.area / i.area if i.area != 0 else 0 for d, i in zip(d_res, i_res)])
            curve = regress(exp, rr)
            conc = curve.conc(rr) / exp

            bias = conc - 1
            bias = bias.mean()

            cv = conc.std(ddof=1) / conc.mean()

            y[index] = (bias ** 2 + cv ** 2) ** 0.5
            if y[index] == np.nan:
                y[index] = 1

        figure = F(istds, array(y), 2500, 500, drug)

        figure.x = 0
        figure.y = row * 500

        doc.addChild(figure.root)
        figure.set_sizes()

    with open('test.svg', 'w') as file:
        file.write(doc.construct())

        pass


main()
