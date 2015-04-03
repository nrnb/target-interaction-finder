#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from target_interaction_finder import TargetInteractionFinder

def main():

    parser = argparse.ArgumentParser(description='Extract subgraph(s) from XGMML network(s).')
    parser.add_argument('ids', type=str, help='identifier or file path to identifier list')
    parser.add_argument('-c', '--column', default=1, type=int, help='column number for node identifiers in node_ids file (default = 1)')
    parser.add_argument('-s', '--source', default='./source_xgmml/', help='source file or directory path(s) to database XGMML(default = directory named "source_xgmml" in current working directory)')
    parser.add_argument('-t', '--type', default='rna', help='node type (rna or protein; default = rna)')
    parser.add_argument('-o', '--output', default='.', help='output directory path (default = current working directory)')
    parser.add_argument('-d', '--debug', default=False, type=bool, help='Show debug messages')
    args = parser.parse_args()

    node_ids = args.ids
    source_xgmml = args.source
    node_id_list_column_index = args.column - 1
    source_type = args.type
    output_dir = args.output
    debug = args.debug

    return TargetInteractionFinder(source_xgmml=source_xgmml, node_ids=node_ids, node_id_list_column_index=node_id_list_column_index, output_dir=output_dir, debug=debug)

if __name__ == '__main__':
    main()
