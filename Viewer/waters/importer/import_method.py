from ..models import drug_methods, istd_methods
from csv import reader


def main(run_id: int):
    with open('method.csv', 'r') as file:
        r = reader(file)
        data = list(r)

    data = {row[0]: row[1:] for row in data}

    drug_qs = drug_methods.objects \
        .filter(run_id=run_id)

    for drug in drug_qs:
        from_csv = data.get(drug.drug_name, '')
        if from_csv != '':
            drug.assigned_istd = istd_methods.objects.filter(istd_name=from_csv[0], run_id=run_id).get()
            drug.min = from_csv[1]
            drug.max = from_csv[2]
