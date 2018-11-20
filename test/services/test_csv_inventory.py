__author__ = 'duff'
# Copyright 2016 Duff Gold

import services.import_csv as inventory_reader
from services import consts
import os
import pandas as pd

import unittest

class TestReadInventory(unittest.TestCase):


    def read_schema_file(self, filename='resources/schema.txt'):
        '''
        Read the given schema preparation to reading the inventory
        :param filename:
        :return: the inventory object
        '''
        schema = os.path.abspath(filename)
        assert (os.path.exists(schema))
        inv = inventory_reader.csv_inventory()
        result = inv.read_schema_def(schema)
        assert (result[0])
        assert (result[1] == consts.success)
        assert (inv.schema_file == schema)
        assert (inv.inventory_columns == ['name', 'type', 'sell_in', 'quality'])
        return inv


    def test_read_schema(self):
        self.read_schema_file()

    def test_read_missing_schema(self):
        schema = os.path.abspath('resources/no_schema.txt')
        assert(not os.path.exists(schema))
        inv = inventory_reader.csv_inventory()
        result = inv.read_schema_def(schema)
        assert(not result[0])
        expected_result = 'No such file ({schema})'.format(schema=schema)
        self.assertEquals(result[1], expected_result, "Got {rslt} expected {erslt}".format(rslt=result[1], erslt=expected_result))

    def test_read_inventory(self):
        inv = self.read_schema_file()
        inventory_file = os.path.abspath('resources/inventory.txt')
        inv.read_inventory_file(inventory_file)
        self.assertTrue(inv.get_inventory_dict(), 'Empty inventory')

    def test_prepare_inventory(self):

        schema = os.path.abspath(os.path.join('resources','schema.txt'))
        assert (os.path.exists(schema))
        data = os.path.abspath(os.path.join('resources','inventory.txt'))
        inv = inventory_reader.csv_inventory()



