__author__ = 'duff'
# Copyright 2016 Duff Gold

import unittest

from services.inventory import Inventory

class TestInventory(unittest.TestCase):

    def initialize_table(self):
        table_content = \
            [
                {'name': 'Hand of Ragnaros', 'type': 'Sulfuras', 'sell_in': 80, 'quality': 80, 'depreciation': None},
                {'name': 'Sword', 'type': 'Weapon', 'sell_in': 30, 'quality': 50, 'depreciation': None},
                {'name': 'I am Murloc', 'type': 'Backstage Passes', 'sell_in': 20, 'quality': 10, 'depreciation': None},
                {'name': 'Aged Brie', 'type': 'Food', 'sell_in': 50, 'quality': 10, 'depreciation': None}
            ]
        inv = Inventory()
        inv.drop_data()
        rslt = [inv.add_item(row) for row in table_content]
        return inv, table_content

    def test_initialization(self):
        inv, table_content = self.initialize_table()

        for row in table_content:
            inv_row = inv.get('name', row['name'])[0]

            [self.assertEquals(inv_row[key], row[key]) for key in inv_row.keys()]


    def test_age(self):
        inv, table_content = self.initialize_table()

        inv.age()  # age it a day

        item = inv.get('name', 'Hand of Ragnaros')[0]
        self.assertEquals(item['quality'], 80)

        item = inv.get('name', 'Sword')[0]
        self.assertEquals(item['quality'], 49)

        item = inv.get('name', 'I am Murloc')[0]
        self.assertEquals(item['quality'], 11)

        item = inv.get('name', 'Aged Brie')[0]
        self.assertEquals(item['quality'], 11)
