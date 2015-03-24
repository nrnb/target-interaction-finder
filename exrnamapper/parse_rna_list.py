#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import regexes

def Parse_RNA_List(file_path, column_index):
    rna_list = list()

    with open(file_path, 'rb') as csvfile:
        rna_list_reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for row in rna_list_reader:
            result = dict()
            first_cell = row[column_index]
            if regexes.mirna_name.match(first_cell):
                result['name'] = first_cell
            elif regexes.mirbase_identifier.match(first_cell):
                result['identifier'] = first_cell

            rna_list.append(result)

    return rna_list
