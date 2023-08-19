from unittest import TestCase, main
import time
from ciscoaplookup import *


class TestCiscoAPLookup(TestCase):
    def test_positive_models(self):
        cases = [
            ('CW9162I', 'Japan', '-Q'),
            ('C9115AXE', 'Belgium', '-E'),
            ('C9130AXI', 'Gibraltar', '-E'),
            ('AIR-AP1542I', 'Mexico', '-A-K9'),
            ('AIR-AP1562E', 'New Zealand', '-Z-K9'),
            ('IW3702-2E-X-K9', 'Barbados', '-N'),
            ('C9124AXI', 'Denmark', '-E'),
            ('C9136I', 'Denmark', '-E'),
            ('C9120AXI', 'Denmark', '-E'),
            ('C9120AXI', 'South Africa', '-E')

        ]
        for c in cases:
            t1 = time.time()
            res = CiscoAPLookup.models_for(c[0], c[1])
            exp = [c[0]+c[2]]
            self.assertEqual(exp, res, '{} doesn\'t match {} for {} / {}'.format(res, exp, c[0], c[1]))
            print(f"Tested {c[0]} in {c[1]}: {time.time()-t1:.2f}")

    def test_9120(self):
        models = []
        cfgs = []
        model_id = 223
        x = CiscoAPLookup.country_models('C9120AXE')
        for m in x:
            if m[-1:] in [ 'T', 'E']:
                continue
            models.append(f"({model_id}, '{m}', 'ap')")
            cfgs.append(f"('{m}', {model_id}, 1000, 'ap', '', '0,1,2,3,4,5,6', 1)")
            model_id += 1
        print(f"insert into tbl_model(`id`, `name`, `kind`) VALUES {', '.join(models)};")

        print(f"insert into tbl_device_configuration(`name`, `model_id`, `mbps`, `roles_csv`, `licenses_csv`, "
              f"`categories_csv`, `active`) VALUES {', '.join(cfgs)};")


    def test_fail_models(self):
        self.assertRaises(ValueError, CiscoAPLookup.models_for, 'gnyf', 'Denmark')  # invalid model
        self.assertRaises(ValueError, CiscoAPLookup.models_for, 'AIR-CAP1532I', 'Neverland')  # invalid country
        self.assertRaises(ValueError, CiscoAPLookup.models_for, 'AIR-CAP1552H', 'Vietnam')  # not possible

    def test_hest(self):
        self.assertTrue(len(CiscoAPLookup.models()) > 20)

    def test_countries(self):
        import pycountry
        lawless_countries = []

        for c in pycountry.countries:
            try:
                klaf = CiscoAPLookup.models_for('AIR-AP2802I', c.name)
            except ValueError as ve:
                print(f"{ve}: {c.name}")


if __name__ == '__main__':
    main()
