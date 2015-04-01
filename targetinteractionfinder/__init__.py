import argparse
from target_interaction_finder import TargetInteractionFinder

def main():
    source_xgmml = '../miRNA-protein-mappings/'

    node_id_list_column_index = 0

    output_dir = '../tests/test4/output-actual/';    

    parser = argparse.ArgumentParser(description='Extract data from miRNA to protein files.')
    #parser.add_argument('-i', '--input', help='input file path to miRNA list')
    parser.add_argument('-c', '--column', default=1, type=int, help='column number from input file that contains sourceIds (default = 1)')
    parser.add_argument('-t', '--type', default='rna', help='type of sourceIds (rna or protein; default = rna)')
    #parser.add_argument('-o', '--output', default='./', help='output dir path (default = current working directory)')
    args = parser.parse_args()

    node_id_list_file_path = '../tests/test4/input/node-list.txt'
    '''
    if 'input' in args:
        node_id_list_file_path = args.input
    else:
        raise ValueError('Input missing.')
    '''
       
    if 'column' in args:
        node_id_list_column_index = args.column - 1
    if 'type' in args:
        source_type = args.type
    if 'output' in args:
        output_dir = args.output

    print 'node_id_list_file_path'
    print node_id_list_file_path

    return TargetInteractionFinder(source_xgmml=source_xgmml, node_id_list_file_path=node_id_list_file_path, node_id_list_column_index=node_id_list_column_index, output_dir=output_dir)

if __name__ == '__main__':
    main()
