# target-interaction-finder
Find interactions between nodes and extract subgraphs in an XGMML network, with forgiving resolution of node ids, whether specified as a name, an identifier or an IRI.

A component for the Genboree workbench.

## To install

```
git clone git@github.com:ariutta/target-interaction-finder.git
cd target-interaction-finder
pip install -e .
easy_install -U setuptools # Only if your setuptools is outdated
pip install https://github.com/ariutta/networkxxgmml/zipball/master
```

This library by default expects the source XGMML network file(s) to be located in the ```source_xgmml``` directory. For example, to run the tests, you will need to download the three miRNA-protein mapping files used at Genboree into the ```source_xgmml``` directory: https://github.com/ariutta/target-interaction-finder/tree/master/source_xgmml

## To run

Note: in the future, the command line argument functionality should allow for just calling ```targetinteractionfinder```, but for now we're using the kludge of ```python targetinteractionfinder/__init__.py```. This kludge might not work in a future version.

Check command line argument defaults:

```
python targetinteractionfinder/__init__.py -h
```

If the defaults are OK, you can then find target interactions for one specific node_id (e.g., an miRNA name):

```
python targetinteractionfinder/__init__.py hsa-miR-370-3p
```

or for multiple node_ids, by providing a file path to a CSV file that has a column of node_ids:

```
python targetinteractionfinder/__init__.py 'tests/test4/input/node-list.txt'
```

If the defaults are not OK, you can override them, e.g., to override the default output directory path:

```
python targetinteractionfinder/__init__.py 'tests/test4/input/node-list.txt' -o 'tests/test4/output-actual/'
```

## Todo
* [x] Get command line arguments working
* [x] Test
* [ ] Automated unit tests
* [ ] Publish to the Python Package Index
