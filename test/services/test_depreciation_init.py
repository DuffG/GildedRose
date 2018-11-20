__author__ = 'duff'
# Copyright 2016 Duff Gold

import unittest

from services.depreciation_rules import DepreciationRules

class TestDepreciationInitRules(unittest.TestCase):

    def test_default_depreciation_init(self):
        row_normal = {'name':'Sword', 'type':'Weapon', 'sell_in':30, 'quality':50, 'depreciation':None}
        rules_engine = DepreciationRules()
        rules_engine.initialize_row_depreciation(row_normal)
        self.assertEquals(row_normal['depreciation'], 1)

    def test_brie_depreciation_init(self):
        row_normal = {'name':'Aged Brie', 'type':'Food', 'sell_in':50, 'quality':10, 'depreciation':None}
        rules_engine = DepreciationRules()
        rules_engine.initialize_row_depreciation(row_normal)
        self.assertEquals(row_normal['depreciation'], -1)

    def test_sulfuras_depreciation_init(self):
        row_normal = {'name':'Hand of Ragnaros', 'type':'Sulfuras', 'sell_in':80, 'quality':80, 'depreciation':None}
        rules_engine = DepreciationRules()
        rules_engine.initialize_row_depreciation(row_normal)
        self.assertEquals(row_normal['depreciation'], 0)

    def test_backstage_depreciation_init(self):
        #I am Murloc,Backstage Passes,20,10
        row_normal = {'name':'I am Murloc', 'type':'Backstage Passes', 'sell_in':20, 'quality':10, 'depreciation':None}
        rules_engine = DepreciationRules()
        rules_engine.initialize_row_depreciation(row_normal)
        self.assertEquals(row_normal['depreciation'], -1)

