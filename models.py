class samples:
    ID = ''
    run = None
    sample_name = ''
    sample_type = ''
    inj_time = None
    matrix = ''

    drugs = None
    istds = None

    def __str__(self):
        return self.sample_name


class drug:
    name = ''
    exp_conc = 0
    area = 0
    area2 = 0

    @property
    def ir(self):
        return self.area2 / self.area if self.area != 0 else 0


class istd:
    name = ''
    area = 0

    # @property
    # def bias(self):
    #     if self.exp_conc != 0:
    #         bias = (self.conc - self.exp_conc) / self.exp_conc
    #     else:
    #         bias = 0
    #
    #     return bias


class Run(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def cals(self):
        return Run([smpl for smpl in self if smpl.sample_type == 'Standard'])

    @property
    def qcs(self):
        return Run([smpl for smpl in self if smpl.sample_type == 'QC'])

    @property
    def drugs(self):
        if self:
            smpl = self[0]
            return list(smpl.drugs.keys())

        return []

    @property
    def istds(self):
        if self:
            smpl = self[0]
            return list(smpl.istds.keys())

        return []

    def get_drug_results(self, name: str, sample_type: str = ''):
        for sample in self:
            test = True
            if sample_type != '':
                test = sample.sample_type == sample_type

            if test:
                for d in sample.drugs.values():
                    if d.name == name:
                        yield d

    def get_istd_results(self, name: str, sample_type: str = ''):
        for sample in self:
            test = True
            if sample_type != '':
                test = sample.sample_type == sample_type

            if test:
                for i in sample.istds.values():
                    if i.name == name:
                        yield i
