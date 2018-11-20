__author__ = 'duff'
# Copyright 2016 Duff Gold

import unittest

from services.depreciation_rules import DepreciationRules

class TestBackstageDepreciationRules(unittest.TestCase):

    def test_backstage_depreciation_age_1_day(self):
        #I am Murloc,Backstage Passes,20,10
        row_normal = {'name':'I am Murloc', 'type':'Backstage Passes', 'sell_in':20, 'quality':10, 'depreciation':None}
        rules_engine = DepreciationRules()
        rules_engine.initialize_row_depreciation(row_normal)
        rules_engine.age_entry(row_normal)
        self.assertEquals(row_normal['depreciation'], -1)
        self.assertEquals(row_normal['quality'], 11)
        self.assertEquals(row_normal['sell_in'], 19)

    def test_backstage_depreciation_age_to_10(self):
        #I am Murloc,Backstage Passes,20,10
        row_normal = {'name':'I am Murloc', 'type':'Backstage Passes', 'sell_in':20, 'quality':10, 'depreciation':None}
        initial_quality = row_normal['quality']
        rules_engine = DepreciationRules()
        rules_engine.initialize_row_depreciation(row_normal)
        days_left = 10
        # days_left is 10, so we calculate 9 days at normal age plus 1 at 2x
        expected_quality = row_normal['quality'] + 9 + 1*2
        days = 0
        while row_normal['sell_in'] > 10:
            rules_engine.age_entry(row_normal)
            days += 1
        self.assertEquals(row_normal['depreciation'], -2)
        self.assertEquals(row_normal['quality'], expected_quality)
        self.assertEquals(row_normal['sell_in'], days_left)

    def test_backstage_depreciation_age_to_5(self):
        #I am Murloc,Backstage Passes,20,10
        row_normal = {'name':'I am Murloc', 'type':'Backstage Passes', 'sell_in':20, 'quality':10, 'depreciation':None}
        initial_quality = row_normal['quality']
        days_left = 5
        # days_left is 10, so we calculate 9 days at normal age plus 5 at 2x plus 1 at 3x
        expected_quality = 9 + 2*5 + 1*3 +10
        rules_engine = DepreciationRules()
        rules_engine.initialize_row_depreciation(row_normal)
        days = 0
        while row_normal['sell_in'] > 5:
            rules_engine.age_entry(row_normal)
            days += 1
        self.assertEquals(row_normal['depreciation'], -3)
        self.assertEquals(row_normal['quality'], expected_quality)
        self.assertEquals(row_normal['sell_in'], 5)

    def test_backstage_depreciation_age_to_sell_in(self):
        #I am Murloc,Backstage Passes,20,10
        row_normal = {'name':'I am Murloc', 'type':'Backstage Passes', 'sell_in':20, 'quality':10, 'depreciation':None}
        initial_quality = row_normal['quality']
        days_left = 5
        # days_left is 10, so we calculate 9 days at normal age plus 5 at 2x plus 6 at 3x (5 days until, then day of)
        expected_quality = 9 + 2*5 + 6*3 + initial_quality
        rules_engine = DepreciationRules()
        rules_engine.initialize_row_depreciation(row_normal)
        days = 0
        while row_normal['sell_in'] > 0:
            rules_engine.age_entry(row_normal)
            days += 1
        self.assertEquals(row_normal['depreciation'], -3)
        self.assertEquals(row_normal['quality'], expected_quality)
        self.assertEquals(row_normal['sell_in'], 0)

    def test_backstage_depreciation_age_past_sell_in(self):
        #I am Murloc,Backstage Passes,20,10
        row_normal = {'name':'I am Murloc', 'type':'Backstage Passes', 'sell_in':20, 'quality':10, 'depreciation':None}
        initial_quality = row_normal['quality']
        # we calculate 9 days at normal age plus 5 at 2x plus 6 at 3x (5 days until, then day of)
        expected_quality = 0
        rules_engine = DepreciationRules()
        rules_engine.initialize_row_depreciation(row_normal)
        days = 0
        while row_normal['sell_in'] > 0:
            rules_engine.age_entry(row_normal)
            days += 1
        rules_engine.age_entry(row_normal)
        self.assertEquals(row_normal['depreciation'], 0)
        self.assertEquals(row_normal['quality'], expected_quality)
        self.assertEquals(row_normal['sell_in'], -1)
