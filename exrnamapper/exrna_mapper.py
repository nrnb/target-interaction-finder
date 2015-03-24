#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import csv
import json
import networkx as nx
import networkxgmml
from parse_rna_list import Parse_RNA_List
from parse_xgmml import Parse_XGMML
from parse_bridgedb_datasources import Parse_BridgeDb_Datasources
import regexes

def _main():
    miriam_ns_list = Parse_BridgeDb_Datasources()
    print 'miriam_ns_list'
    print miriam_ns_list
    test_name = 'test3'

    rna_list_file_path = '../tests/' + test_name + '/input/rna-list-' + test_name + '.txt'
    rna_list_column_index = 0

    results_file_path = '../tests/' + test_name + '/output-actual/' + test_name + '-results.csv';
    results_file = open(results_file_path, 'w')
    results_file.write('queryID,targetId,score,pvalue,pmid,datasource\n')
    results_file.close()

    logfile_path = '../tests/' + test_name + '/output-actual/' + test_name + '.log';
    open(logfile_path, 'w').close()

    log_result = dict()
    log_result['total_result_count'] = 0
    log_result['skipped_count'] = 0
    log_result['results_by_source'] = {}

    mirna_protein_mapping_file_paths = [
        '../miRNA-protein-mappings/microcosm-hsa-2012-12-05.xgmml',
        '../miRNA-protein-mappings/mirtarbase-hsa-4.4.xgmml',
        '../miRNA-protein-mappings/targetscan-hsa-2012-12-05.xgmml'
    ]

    versions = []

    rna_list = Parse_RNA_List(rna_list_file_path, rna_list_column_index)
    log_result['query_count'] = len(rna_list)

    for mirna_protein_mapping_file_path in mirna_protein_mapping_file_paths:
        mirna_protein_mapping_file_path_components = mirna_protein_mapping_file_path.split('/')
        version = mirna_protein_mapping_file_path_components[len(mirna_protein_mapping_file_path_components) - 1].replace('.xgmml', '')
        versions.append(version)

        current_mapping_graph = Parse_XGMML(mirna_protein_mapping_file_path)
        log_result[version + '_result_count'] = 0

        datasource_subgraph_node_ids = []

        name_to_identifier_mappings={}

        for result in rna_list:
            identifier = None
            fuzzy_id = None
            if ('identifier' in result):
                identifier = fuzzy_id = result['identifier']
            else:
                if ('name' in result):
                    fuzzy_id = result['name']
                    print 'Warning: It is safest to provide a Miriam/identifiers.org identifier.'
                    print ''
                else:
                    raise ValueError('No name (hsa-miR-542-3p) or identifier (MIMAT0003389) provided.')

            if not (current_mapping_graph.has_node(fuzzy_id)):
                matching_node_graphid = None
                print 'Warning: Provided mapping XGMML file does not identify nodes using Miriam/identifiers.org identifiers.'
                print ''
                current_graph_id = ''
                for onenode in current_mapping_graph.nodes():
                    current_node = current_mapping_graph.node[onenode]
                    if ((('identifiers' in current_node) and (fuzzy_id in current_node['identifiers'])) or (('@label' in current_node) and (fuzzy_id == current_node['@label'])) or (('label' in current_node) and (fuzzy_id == current_node['label'])) or (('mimat id' in current_node) and (fuzzy_id == current_node['mimat id']))):
                        if (('mimat id' in current_node) and (fuzzy_id == current_node['mimat id'])):
                            matching_node_graphid = onenode
                            break
                        elif (('identifiers' in current_node) and (fuzzy_id in current_node['identifiers'])):
                            matching_node_graphid = onenode
                        elif not matching_node_graphid:
                            matching_node_graphid = onenode

                print 'matching_node_graphid'
                print matching_node_graphid
                if not matching_node_graphid:
                    #raise ValueError('No matching identifier found.')
                    print 'Warning: No matching identifier found for "' + fuzzy_id + '"'
                    print ''
                    fuzzy_id = None
                else:
                    fuzzy_id = matching_node_graphid

            if fuzzy_id:
                if regexes.mirbase_identifier.match(fuzzy_id):
                    identifier = fuzzy_id
                else:
                    matching_node = current_mapping_graph.node[fuzzy_id]
                    if (('mimat id' in matching_node) and (fuzzy_id == matching_node['mimat id'])):
                        identifier = matching_node['mimat id']
                    else:
                        if ('identifiers' in current_node):
                            identifiers = current_node['identifiers']
                            for current_identifier in identifiers:
                                if regexes.mirbase_identifier.match(current_identifier):
                                    identifier = current_identifier
                                    break

                        if not identifier:
                            print 'Could not convert provided name/id to Miriam/identifiers.org identifier.'
                            print ''
                            identifier = fuzzy_id
                            #raise ValueError('Could not convert provided name/id.')

                if not identifier:
                    log_result['skipped_count'] += 1
                    print 'Skipped due to no valid identifier found for: '
                    print fuzzy_id
                    print ''
                else:
                    # TODO handle other namespaces.
                    if (fuzzy_id != identifier):
                        print 'adding to mappings'
                        print 'fuzzy_id'
                        print fuzzy_id
                        name_to_identifier_mappings[fuzzy_id] = identifier

                    print ''
                    '''
                    print 'node for selected fuzzy_id'
                    print current_mapping_graph.node[fuzzy_id]
                    '''

                    neighbor_fuzzy_ids = current_mapping_graph.neighbors(fuzzy_id)
                    '''
                    print ''
                    print 'neighbor_fuzzy_ids for selected fuzzy_id'
                    print neighbor_fuzzy_ids
                    '''

                    '''
                    # Normalize target(s) to use Ensembl
                    # TODO it's thinking both ensembl and entrez match -- not working
                    for neighbor_fuzzy_id in neighbor_fuzzy_ids:
                        current_neighbor_identifier = None
                        current_neighbor_node = current_mapping_graph.node[neighbor_fuzzy_id]
                        if regexes.ensembl_identifier.match(neighbor_fuzzy_id) and (not regexes.ncbigene_identifier.match(neighbor_fuzzy_id)):
                            current_neighbor_identifier = neighbor_fuzzy_id
                        else:
                            if 'identifiers' in current_neighbor_node:
                                for current_neighbor_identifier in current_neighbor_node['identifiers']:
                                    if regexes.ensembl_identifier.match(current_neighbor_identifier) and (not regexes.ncbigene_identifier.match(current_neighbor_identifier)):
                                        current_neighbor_identifier = current_neighbor_identifier
                                        break
                        if current_neighbor_identifier:
                            name_to_identifier_mappings[neighbor_fuzzy_id] = current_neighbor_identifier
                    '''

                    if not identifier in log_result['results_by_source']:
                        log_result['results_by_source'][identifier] = {}
                    log_result['results_by_source'][identifier][version] = len(neighbor_fuzzy_ids)

                    log_result['total_result_count'] += len(neighbor_fuzzy_ids)

                    log_result[version + '_result_count'] += len(neighbor_fuzzy_ids)

                    item_subgraph_node_ids = neighbor_fuzzy_ids
                    item_subgraph_node_ids.append(fuzzy_id)
                    print 'item_subgraph_node_ids'
                    print item_subgraph_node_ids
                    datasource_subgraph_node_ids += item_subgraph_node_ids

        print 'datasource_subgraph_node_ids'
        print datasource_subgraph_node_ids

        if (len(name_to_identifier_mappings) > 0):
            print 'name_to_identifier_mappings'
            print name_to_identifier_mappings
            tmp_subgraph = current_mapping_graph.subgraph(datasource_subgraph_node_ids)
            datasource_subgraph = nx.relabel_nodes(tmp_subgraph, name_to_identifier_mappings, copy=False)
            print 'relabeled'
        else:
            datasource_subgraph = current_mapping_graph.subgraph(datasource_subgraph_node_ids)

        '''
        print 'datasource_subgraph nodes'
        print datasource_subgraph.nodes()
        '''
        print 'datasource_subgraph edges'
        print datasource_subgraph.edges()

        #output_xgmml_file_path = '../tests/' + test_name + '/output-actual/' + identifier + '.xgmml';
        output_xgmml_file_path = '../tests/' + test_name + '/output-actual/' + version + '-results.xgmml';
        output_xgmml = open(output_xgmml_file_path, 'w')
        networkxgmml.XGMMLWriter(output_xgmml, datasource_subgraph, version + 'subgraph')
                
        ''' The resulting CSV file should look like this:
        queryID	targetId	score	pvalue	pmid	datasource
        hsa-miR-542-3p	332			20728447	miRTarBase_hsa_r4.4
        '''

        with open(results_file_path, 'a') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for oneedge in datasource_subgraph.edges(data=True):
                print 'oneedge'
                print oneedge
                edge_attributes = oneedge[2]
                print 'edge_attributes'
                print edge_attributes
                #row_value = [identifier, edge_attributes['Target Gene (Entrez ID)']]
                row_value = [oneedge[0], oneedge[1]]

                if 'score' in edge_attributes:
                    row_value.append(edge_attributes['score'])
                else:
                    row_value.append('')

                if 'pValue' in edge_attributes:
                    row_value.append(edge_attributes['pValue'])
                else:
                    row_value.append('')

                if 'References (PMID)' in edge_attributes:
                    row_value.append(edge_attributes['References (PMID)'])
                else:
                    row_value.append('')

                '''
                matching_miriam_ns = False
                for miriam_ns in miriam_ns_list:
                    if miriam_ns in edge_attributes:
                        matching_miriam_ns = miriam_ns

                if matching_miriam_ns:
                    row_value.append(matching_miriam_ns)
                else:
                    row_value.append('')
                '''

                if 'datasource' in edge_attributes:
                    row_value.append(edge_attributes['datasource'])
                else:
                    row_value.append('')

                #row_value.append(version)

                print 'row_value'
                print row_value
                csvwriter.writerow(row_value)

    print 'log_result'
    print log_result
    with file(logfile_path, 'w') as f:
        print >>f, '# Queried {} miRNA identifiers.'.format(log_result['query_count'])
        print >>f, '# Skipped {} identifiers.'.format(log_result['skipped_count'])
        print >>f, '# Found {} results.'.format(log_result['total_result_count'])
        header = ['queryID'] + versions
        print 'header'
        print header
        print >>f, '\t'.join(header)
        for oneidentifier in log_result['results_by_source']:
            row = [oneidentifier]
            #for oneversion in log_result['results_by_source'][oneidentifier]:
            for oneversion in versions:
                if oneversion in log_result['results_by_source'][oneidentifier]:
                    row.append(str(log_result['results_by_source'][oneidentifier][oneversion]))
                else:
                    row.append(str(0))
            print 'row'
            print row
            print >>f, '\t'.join(row)

if __name__ == '__main__':
    _main()
