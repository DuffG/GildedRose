__author__ = 'duff'
# Copyright 2016 Duff Gold

import unittest

from services.depreciation_rules import DepreciationRules

class TestSulfurasDepreciationRules(unittest.TestCase):

    def test_sulfuras_aging_1_day(self):
        row_normal = {'name':'Hand of Ragnaros', 'type':'Sulfuras', 'sell_in':80, 'quality':80, 'depreciation':None}
        rules_engine = DepreciationRules()
        rules_engine.initialize_row_depreciation(row_normal)
        rules_engine.age_entry(row_normal)
        self.assertEquals(row_normal['depreciation'], 0)
        self.assertEquals(row_normal['quality'], 80)

    def test_sulfuras_aging_past_sell_in(self):
        row_normal = {'name':'Hand of Ragnaros', 'type':'Sulfuras', 'sell_in':80, 'quality':80, 'depreciation':None}
        rules_engine = DepreciationRules()
        rules_engine.initialize_row_depreciation(row_normal)
        for day in range(row_normal['sell_in'], 0, -1):
            rules_engine.age_entry(row_normal)
        self.assertEquals(row_normal['depreciation'], 0)
        self.assertEquals(row_normal['quality'], 80)
        rules_engine.age_entry(row_normal)
        self.assertEquals(row_normal['depreciation'], 0)
        self.assertEquals(row_normal['quality'], 80)

