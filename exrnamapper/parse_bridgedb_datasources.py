#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import re

def Parse_BridgeDb_Datasources():
    file_path = './bridgedb-datasources.tsv'
    column_index = 8

    dataset_name_list = list()

    miriam_pattern = re.compile('^urn:miriam')

    with open(file_path, 'rb') as csvfile:
        dataset_list_reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for row in dataset_list_reader:
            miriam_ns = row[column_index]
            if miriam_pattern.match(miriam_ns):
                dataset_name = miriam_ns.replace('urn:miriam:', '')
                dataset_name_list.append(dataset_name)

    return dataset_name_list
