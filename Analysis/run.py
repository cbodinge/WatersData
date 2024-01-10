from waters_xml import read
from models import Run
from numpy import array
from calibration import regress
from plot_residuals import Figure as PR
from PySVG import Document

indices = [[0, 1, 2, 3, 4, 5, 6, 7],
           [1, 2, 3, 4, 5, 6, 7],
           [2, 3, 4, 5, 6, 7],
           [3, 4, 5, 6, 7],
           [0, 1, 2, 3, 4, 5, 6],
           [1, 2, 3, 4, 5, 6],
           [2, 3, 4, 5, 6]]


def main():
    path = 'C:\\PinPoint\\MassHunter\\Data\\KAN\\[C18] TOX-2001A\\Bias & Precision - 1\\quandata.xml'
    with open(path, 'r') as file:
        run = Run(read(file))

    doc = Document(w=7 * 500, h=500 * len(run.drugs))
    for ind, drug in enumerate(run.drugs):
        smpls = run.iter(drug_pred=lambda x: x == f'{drug}',
                         sample_pred=lambda x: x.sample_type == 'Standard')
        res = [r for _, _, r in smpls]

        for j, t in enumerate(indices):
            exp = array([i.exp_conc for i in res])[t]
            rr = array([i.rr for i in res])[t]

            curve = regress(exp, rr)

            pr = PR(x=exp, y=(curve.conc(rr) - exp) / exp, title=drug)

            pr.x = j * 500
            pr.y = ind * 500

            doc.addChild(pr.root)
            pr.set_sizes()

    with open('test.svg', 'w') as file:
        file.write(doc.construct())

        pass


main()
