#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import csv
import json
import networkx as nx
import networkxgmml

def Parse_XGMML(xgmml_file_path):
    parser = argparse.ArgumentParser(description="Read network from mirtarbase-sample")
    parser.add_argument('XGMML', default=file(xgmml_file_path), help='XGMML file exported from Cytoscape  default: %(default)s', nargs='?', type=argparse.FileType('r'))
    parser.add_argument('edgelist', default='../tests/test1/output-actual/mirtarbase-sample-edgelist.txt', nargs='?', help='edge list output path  [default: %(default)s]')
    parser.add_argument('nodelist', default='../tests/test1/output-actual/mirtarbase-sample-nodelist.txt', nargs='?', help='node list output path  [default: %(default)s]')
    options = parser.parse_args()

    g = networkxgmml.XGMMLReader(options.XGMML)

    return g
