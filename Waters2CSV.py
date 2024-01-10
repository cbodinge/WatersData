from pathlib import Path


def main():
    path = Path.cwd()
    path = path / 'Input'
    for file in path.iterdir():
        one_run(file)


def open_file(path: Path):
    with open(path, 'r') as file:
        data = file.read()
        dlist = data.split('\n')

    return [row.split('\t') for row in dlist]


def one_run(path: Path):
    data = open_file(path)
    csv = []

    for index, row in enumerate(data):
        drug = row[0]
        n = drug.find(':') + 3
        if drug.find('Compound') != -1 and n != 2:
            drug = drug[n:]
            q = fetch_drug(data, drug, index)
            csv = csv + q

    publish_csv(csv, path.stem)


def drug_dict():
    dd = {'Sample Name': 1,
          'Acq. Time': 12,
          'Exp. Conc.': 4,
          'Calc. Conc.': 10,
          'RT': 5,
          'S:N1': 10,
          'S:N2': 11,
          'Ion Ratio': 6,
          'ISTD Area': 9,
          'Target Area': 8}

    return dd


def fetch_drug(data, drug, index):
    index = index + 3
    drug_data = []
    while len(data[index]) > 1 and data[index] != 17 * ['']:
        dd = drug_dict()
        row = data[index]
        new_row = {key: row[dd[key]] for key in dd.keys()}
        new_row['Drug'] = drug
        drug_data.append(new_row)
        index += 1

    return drug_data


def publish_csv(data, name):
    big_str = ''
    for row in data:
        row_reorganized = [row['Sample Name'], '', row['Drug'], row['Acq. Time'], '', row['RT'], row['Calc. Conc.'],
                           row['S:N1'], row['S:N2'], row['Ion Ratio'], row['Target Area'], row['ISTD Area']]
        big_str = big_str + ','.join(row_reorganized) + '\n'

    with open(f'Output\\{name}.csv', 'w') as file:
        file.write(big_str)


main()
