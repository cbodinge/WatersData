from ..models import drug_methods
from csv import writer


def main(run_id: int):
    drug_qs = drug_methods.objects \
        .filter(run_id=run_id) \
        .values_list('drug_name', 'assigned_istd__istd_name', 'min', 'max')

    dlist = list(drug_qs)

    with open('method.csv', 'w', newline='') as file:
        w = writer(file)
        w.writerows(dlist)
