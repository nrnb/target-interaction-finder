#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import json
from os import listdir
from os.path import isfile, join
import networkx as nx
import networkxgmml
from parse_rna_list import Parse_RNA_List
from parse_xgmml import Parse_XGMML
from parse_bridgedb_datasources import Parse_BridgeDb_Datasources
import regexes


def has_file_extension(filename, file_extension):
    expected_index = len(filename) - len(file_extension)
    return filename.find(file_extension, expected_index, len(filename)) == expected_index

def ExRNAMapper(mirna_protein_mapping_files_dir, rna_list_file_path=None, rna_list_column_index=0, output_dir='./'):
    results_file_path = output_dir + 'exrna-mapper-results.csv'
    results_file = open(results_file_path, 'w')
    results_file.write('queryID,targetId,score,pvalue,pmid,datasource\n')
    results_file.close()

    logfile_path = output_dir + 'exrna-mapper-logs.log'
    open(logfile_path, 'w').close()

    log_result = dict()
    log_result['total_result_count'] = 0
    log_result['skipped_count'] = 0
    log_result['results_by_source'] = {}

    file_extension = '.xgmml'
    mirna_protein_mapping_file_paths = [ mirna_protein_mapping_files_dir + f for f in listdir(mirna_protein_mapping_files_dir) if isfile(join(mirna_protein_mapping_files_dir,f)) and has_file_extension(f, file_extension) ]
    print 'mirna_protein_mapping_file_paths'
    print mirna_protein_mapping_file_paths

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

        id_mappings={}

        for result in rna_list:
            fuzzy_id = None
            verified_node_id = None

            if ('identifier' in result):
                fuzzy_id = result['identifier']
            else:
                if ('name' in result):
                    fuzzy_id = result['name']
                    print 'Warning: It is safest to provide a Miriam/identifiers.org identifier.'
                    print ''
                else:
                    print 'Warning: No name (e.g., hsa-miR-542-3p) or identifier (e.g., MIMAT0003389) provided.'
                    log_result['skipped_count'] += 1

            # name or identifier. potentially the verified_node_id, if it exists in the graph.
            if fuzzy_id:
                if current_mapping_graph.has_node(fuzzy_id):
                    verified_node_id = fuzzy_id
                else:
                    for onenode in current_mapping_graph.nodes():
                        current_node = current_mapping_graph.node[onenode]
                        if ((('identifiers' in current_node) and (fuzzy_id in current_node['identifiers'])) or (('@label' in current_node) and (fuzzy_id == current_node['@label'])) or (('label' in current_node) and (fuzzy_id == current_node['label'])) or (('mimat id' in current_node) and (fuzzy_id == current_node['mimat id']))):
                            if (('mimat id' in current_node) and (fuzzy_id == current_node['mimat id'])):
                                verified_node_id = onenode
                                break
                            elif (('identifiers' in current_node) and (fuzzy_id in current_node['identifiers'])):
                                verified_node_id = onenode
                            elif not verified_node_id:
                                verified_node_id = onenode

                    if not verified_node_id:
                        #raise ValueError('No matching identifier found.')
                        print 'Warning: No node found with id "' + fuzzy_id + '"'
                        print ''

            # verified to exist
            if verified_node_id:
                    if (verified_node_id != fuzzy_id):
                        print 'adding to mappings'
                        print 'verified_node_id'
                        print verified_node_id
                        id_mappings[verified_node_id] = fuzzy_id

                    print ''
                    '''
                    print 'node for selected verified_node_id'
                    print current_mapping_graph.node[verified_node_id]
                    '''

                    neighbor_verified_node_ids = current_mapping_graph.neighbors(verified_node_id)
                    '''
                    print ''
                    print 'neighbor_verified_node_ids for selected verified_node_id'
                    print neighbor_verified_node_ids
                    '''

                    if not verified_node_id in log_result['results_by_source']:
                        log_result['results_by_source'][verified_node_id] = {}
                    log_result['results_by_source'][verified_node_id][version] = len(neighbor_verified_node_ids)

                    log_result['total_result_count'] += len(neighbor_verified_node_ids)

                    log_result[version + '_result_count'] += len(neighbor_verified_node_ids)

                    item_subgraph_node_ids = neighbor_verified_node_ids
                    item_subgraph_node_ids.append(verified_node_id)
                    print 'item_subgraph_node_ids'
                    print item_subgraph_node_ids
                    datasource_subgraph_node_ids += item_subgraph_node_ids

        print 'datasource_subgraph_node_ids'
        print datasource_subgraph_node_ids

        if (len(id_mappings) > 0):
            print 'id_mappings'
            print id_mappings
            tmp_subgraph = current_mapping_graph.subgraph(datasource_subgraph_node_ids)
            datasource_subgraph = nx.relabel_nodes(tmp_subgraph, id_mappings, copy=False)
            print 'relabeled'
        else:
            datasource_subgraph = current_mapping_graph.subgraph(datasource_subgraph_node_ids)

        '''
        print 'datasource_subgraph nodes'
        print datasource_subgraph.nodes()
        '''
        print 'datasource_subgraph edges'
        print datasource_subgraph.edges()

        output_xgmml_file_path = output_dir + version + '-results.xgmml';
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
        for one_fuzzy_id in log_result['results_by_source']:
            row = [one_fuzzy_id]
            #for oneversion in log_result['results_by_source'][one_fuzzy_id]:
            for oneversion in versions:
                if oneversion in log_result['results_by_source'][one_fuzzy_id]:
                    row.append(str(log_result['results_by_source'][one_fuzzy_id][oneversion]))
                else:
                    row.append('0')
            print 'row'
            print row
            print >>f, '\t'.join(row)

    return log_result
