__author__ = 'duff'
# Copyright 2016 Duff Gold

import unittest

from services.depreciation_rules import DepreciationRules

class TestTableDepreciationRules(unittest.TestCase):

    def test_table_init(self):
        table_content = \
        [
            {'name':'Hand of Ragnaros', 'type':'Sulfuras', 'sell_in':80, 'quality':80, 'depreciation':None},
            {'name':'Sword', 'type':'Weapon', 'sell_in':30, 'quality':50, 'depreciation':None},
            {'name':'I am Murloc', 'type':'Backstage Passes', 'sell_in':20, 'quality':10, 'depreciation':None},
            {'name':'Aged Brie', 'type':'Food', 'sell_in':50, 'quality':10, 'depreciation':None}
        ]

        rules_engine = DepreciationRules()
        rules_engine.initialize_depreciation(table_content)
        sulfuras = table_content[0]
        normal = table_content[1]
        backstage = table_content[2]
        aged_brie = table_content[3]
        self.assertEquals(sulfuras['depreciation'], 0)
        self.assertEquals(normal['depreciation'], 1)
        self.assertEquals(backstage['depreciation'], -1)
        self.assertEquals(aged_brie['depreciation'], -1)

    def test_table_age_1(self):
        table_content = \
        [
            {'name':'Hand of Ragnaros', 'type':'Sulfuras', 'sell_in':80, 'quality':80, 'depreciation':None},
            {'name':'Sword', 'type':'Weapon', 'sell_in':30, 'quality':50, 'depreciation':None},
            {'name':'I am Murloc', 'type':'Backstage Passes', 'sell_in':20, 'quality':10, 'depreciation':None},
            {'name':'Aged Brie', 'type':'Food', 'sell_in':50, 'quality':10, 'depreciation':None}
        ]

        rules_engine = DepreciationRules()
        rules_engine.initialize_depreciation(table_content)
        table_content = rules_engine.age(table_content)
        sulfuras = table_content[0]
        normal = table_content[1]
        backstage = table_content[2]
        aged_brie = table_content[3]
        self.assertEquals(sulfuras['quality'], 80)
        self.assertEquals(normal['quality'], 49)
        self.assertEquals(backstage['quality'], 11)
        self.assertEquals(aged_brie['quality'], 11)

