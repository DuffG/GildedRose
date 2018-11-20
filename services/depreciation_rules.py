__author__ = 'duff'
# Copyright 2016 Duff Gold

import pandas as pd

class DepreciationRules:
    '''
    Manage depreciation rules. Default is to subtract the depreciation column from the quality. In the case of Aged Brie,
    the depreciation is -1, so that ends up increasing the quality.

    Depreciation is initialized to 1, and the the initialize_depreciation function is called.
    initialize_depreciation calls initialize_row, which looks up the init function in the initialization_rules.
    If there isn't a special behavior, no init function is found and nothing ese is done to the row
    Special behavior is found be comparing the _field_'s value with the _key_. The rule_name specifies the function
    to be called: the name is used to look up the entry in the initialization_function_index. If that isn't found, we
    raise an exception, to be handled by the caller.

    '''

    def __init__(self):
        # used to keep default aging form acting on these types
        self.legendary_types = ['Sulfuras']

        # TODO read rules file
        # list of dicts. Each one has field and key, which is used to trigger on the row we're looking at.
        # e.g. if row['name'] == 'Aged Brie', then the 1st rule applies.
        # The rule_name must correspond to a function in this class the function is called by name
        # e.g. self[rule[rule_name]](row, rule)
        # Initially I used a lookup table, but this seems clearer
        self.initialization_rules = \
            [
                {'field': 'name', 'key': 'Aged Brie', 'depr_value': -1, 'rule_name': 'multiply'},
                {'field': 'type', 'key': 'Backstage Passes', 'depr_value': -1, 'rule_name': 'multiply'},
                {'field': 'type', 'key': 'Conjured', 'depr_value': 2, 'rule_name': 'multiply'},
                {'field': 'type', 'key': 'Sulfuras', 'depr_value': 0, 'rule_name': 'replace'}
            ]
        # Lookup for aging. Almost every item is aged by applying quality -= depreciation, except for backstage passes.
        # this gets applied once a day.
        self.aging_functions = \
            {
                'default': self.straight_aging,
                'Backstage Passes': self.backstage_passes_aging
            }

        # lookup for misspellings
        self.backstage_passes = ['Backstage Passes', 'Backstage Passess']

    def multiply(self, row, rule):
        '''
        Used by initialization
        multiply the depreciation field value by deprvaljue if the field contains an exact match to fieldval

        row represents a row in the dataframe. kwargs contains data to be used in the eval
        The field row['depreciation'] is replaced by the evaluation
        :param row: the dataframe row
        :param kwargs:
         fieldname: name of field to be checked in the row
         fieldval: value of the above field to be used to trigger multiplication
         deprvalue: value to be used
        :return:

        Function for the function index in apply_depreciation_rules
        Used by dataframe.apply
        '''
        row['depreciation'] = rule['depr_value'] * row['depreciation']

    def replace(self, row, rule):
        '''
        Used by initialization
        replace the depreciation field value by deprvaljue if the field contains an exact match to fieldval

        row represents a row in the dataframe. kwargs contains data to be used in the eval
        The field row['depreciation'] is replaced by the evaluation
        :param row: the dataframe row
        :param kwargs:
         fieldname: name of field to be checked in the row
         fieldval: value of the above field to be used to trigger multiplication
         deprvalue: value to be used
        :return:

        Function for the function index in apply_depreciation_rules
        Used by dataframe.apply
        '''

        row['depreciation'] = rule['depr_value']


    def initialize_row_depreciation(self, row):
        '''
        Apply the appropriate init rule to this row's depreciation field
        :return: None
        '''
        row['depreciation'] = 1

        for rule in self.initialization_rules:
            if row[rule['field']] == rule['key']:
                # Call the appropriate function by name: get the function by the name stored in rule['rule_name'] and
                # apply it to the row we're working on
                getattr(self, rule['rule_name'])(row, rule=rule)

    def initialize_depreciation(self, table):
        '''
        Initialize the table's rows by setting the depreciation value correctly.
        Expecting this to be called for entries we get from a text file.
        This will not work correctly on a database table, only a list of dict we're going to save in the db.
        :param table: list of dict entries with at least name, type and depreciation fields
        :return: same table, with depreciation column filled in correctly.
        '''
        for row in table:
            self.initialize_row_depreciation(row)

    def age_entry(self, row):
        '''
        Look up the aging function based on the type, and apply it to this row.
        :param row: row in table
        :return: None
        '''
        aging_function = self.aging_functions.get(row['type'], self.aging_functions.get('default'))
        aging_function(row)
        return row

    def age(self, inventory_table):
        '''
        Age the inventory by 1 day, applying the depreciation rules.
        Assumes inventory_table is an array of json dicts
        expecting caller to pass in table.all()
        :return:
        '''
        return [self.age_entry(row) for row in inventory_table]
        # create a dataframe from the table. This won't work for truly huge collections, but for a few thousand we're good
        # df2 = pd.DataFrame.from_dict(inventory_table, orient='columns')
        # # apply our age_entry to each row in the table
        # df2.apply(self.age_entry, axis=1)
        # return df2.to_dict('records')

    def straight_aging(self, row):
        '''
        reduce quality by depreciation until sell_in is 0, then double depreciation. Quality always >= 0 and
        quality always <= 50 unless of Legendary quality
        :param row: dict containing type, quality, sell_in and depreciation entries
        :return: same row with quality reduced by depreciation, sell_in reduced by 1 and depreciation
        double when sell_in is 0
        '''
        if not row['type'] in self.legendary_types:
            row['quality'] = min(50, max(row['quality'] - row['depreciation'], 0))
            row['sell_in'] -= 1
            if row['sell_in'] == 0:
                row['depreciation'] = row['depreciation'] * 2


    def backstage_passes_aging(self, row):
        '''
        "Backstage passes", like aged brie, increases in Quality as it's SellIn value approaches;
            Quality increases
                by 2 when there are 10 days or less and
                by 3 when there are 5 days or less but Quality
                drops to 0 after the concert
        :param row:
        :return:
        '''
        row['sell_in'] -= 1
        sell_in = row['sell_in']
        if sell_in == 10:
            row['depreciation'] = -2
        if sell_in == 5:
            row['depreciation'] = -3
        if sell_in < 0:
            row['quality'] = 0
            row['depreciation'] = 0

        row['quality'] = max(row['quality'] - row['depreciation'], 0)

