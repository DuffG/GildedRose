__author__ = 'duff'
# Copyright 2016 Duff Gold

import pandas as pd
from tinydb import TinyDB, Query
import os.path as ospath
from services import depreciation_rules

class Inventory:
    def __init__(self):
        self.db = None
        self.inventory_table = None
        self.depreciation_rules_eng = depreciation_rules.DepreciationRules()
        self.db = TinyDB(ospath.join('db', 'inventory.dat'))
        self.inventory_table = self.db.table('inventory')

    def drop_data(self):
        self.inventory_table.purge()

    def read(self):
        '''
        Get the inventory data from the DB.
        Set internal dataframe
        :return:
        '''
        pass

    def save(self):
        '''
        save inventory data to disk
        :return:
        '''
        pass

    def age_entry(self, row):
        '''
        Look up the aging function based on the type, and apply it to this row.
        :param row: row in table
        :return: None
        '''
        self.depreciation_rules_eng.age_entry(row)

    def age_row(self, database, record_id):
        self.age_entry(database.get(record_id))

    def age(self):
        '''
        Age the inventory by 1 day, applying the depreciation rules
        :return:
        '''
        # aged = self.depreciation_rules_eng.age(self.inventory_table)
        self.inventory_table.process_elements(self.age_row)

    def add_item(self, row):
        '''
        Add an item to the inventory. depreciation is calculated here
        :param kwargs:
        :return:
        '''
        self.depreciation_rules_eng.initialize_row_depreciation(row)
        doc_id = self.inventory_table.insert(row)
        return self.inventory_table.get(doc_id=doc_id)

    def remove_item(self, **kwargs):
        '''
        Delete an item from the inventory, by name
        :param kwargs:
        :return:
        '''
        self.inventory_table.remove(kwargs['item'].doc_id)

    def get(self, field, value):
        '''
        Get a specific doc from the database

        :param field: fieldname for query
        :param value: value of field to make true
        :return: the found row(s) or None
        '''
        item = Query()

        return self.inventory_table.search(item[field] == value)