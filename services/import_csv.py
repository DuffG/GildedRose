__author__ = 'duff'
# Copyright 2016 Duff Gold
import pandas as pd
import os.path
import consts
import csv

class csv_inventory:
    '''
    Read a csv file representing an inventory and hold it as a dict
    Requires a schema definition file
    empty schema file causes a fault
    empty inventory is OK, returns an empty dict
    Missing files cause fault
    '''
    def __init__(self):
        # string to hold schema definition file name
        self.schema_file = None
        # string to hold inventory file name
        self.inventory_file = None
        # List of columns from inventory schema. List.
        self.inventory_columns = None
        # Datraframe tp hold inventory. Was originally going to use dataframes to manage the inventory,
        # but the Db interface made that awkward.
        self.inventory_df = None
        pass

    def read_schema_def(self, file_name_with_path):
        '''
        Get the schema of the inventory file, save as a list of column names
        :param file_name_with_path: the path and name of the schema def file
        :return: tuple (state, message) where state is boolean (True for success) and the message is indicative of any issues
        '''
        self.schema_file = file_name_with_path
        if not os.path.exists(self.schema_file):
            return False,'No such file ({schema})'.format(schema=self.schema_file)
        try:
            self.inventory_columns = pd.read_csv(file_name_with_path, skipinitialspace=True).columns.values.tolist()
        except Exception as e:
            print(e)
            return False, 'Unable to read schema file ({schema}) as csv'.format(schema=self.schema_file)

        return True,consts.success

    def read_inventory_file(self, file_name_with_path):
        '''
        Read the inventory file and create the final inventory dataframe
        :param file_name_with_path:
        :return: tuple (state, message) where state is boolean (True for success) and the message is indicative of any issues
        '''
        self.inventory_file = file_name_with_path
        if not os.path.exists(self.inventory_file):
            return False,'No such file({inv})'.format(schema=self.inventory_file)
        try:
            self.inventory_df = pd.read_csv(file_name_with_path, header=None)
            self.inventory_df.columns=self.inventory_columns
        except Exception as e:
            return False, 'Unable to read inventory file ({inv}) as csv'.format(inv=self.inventory_file)
        return True, consts.success

    def get_inventory_dict(self):
        '''
        Return the internal data as a list of dicts, each dict representing one row as defined by the schema def file.
        :return:
        '''
        return self.inventory_df.to_dict('records')

    def prepare_inventory(self, inventory_file_with_path, schema_file_with_path):
        self.read_schema_def(schema_file_with_path)
        self.read_inventory_file(inventory_file_with_path)

