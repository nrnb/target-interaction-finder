#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import re

def Parse_RNA_List(file_path, column_index):
    rna_list = list()

    # only works for human miRNA names
    name_pattern = re.compile('^hsa-.*-.*')
    # based on the regex from http://identifiers.org/mirbase.mature/
    identifier_pattern = re.compile('^(MIMAT\d{7})|(MI\d{7})$')

    with open(file_path, 'rb') as csvfile:
        rna_list_reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for row in rna_list_reader:
            result = dict()
            first_cell = row[column_index]
            if name_pattern.match(first_cell):
                result['name'] = first_cell
            elif identifier_pattern.match(first_cell):
                result['identifier'] = first_cell

            rna_list.append(result)

    return rna_list
