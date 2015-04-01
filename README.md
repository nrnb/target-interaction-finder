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

To run the tests, you will need to download the miRNA-protein mapping files into the "miRNA-protein-mappings" directory: https://github.com/ariutta/target-interaction-finder/tree/master/miRNA-protein-mappings

## To run

```
cd targetinteractionfinder
python __init__.py -h #to view options
```

if the defaults are OK, you can then run:

```
python __init__.py hsa-miR-370-3p
```

or

```
python __init__.py '../tests/test4/input/node-list.txt'
```

Or you can override the defaults, as is required to run the tests:

```
python __init__.py '../tests/test4/input/node-list.txt' -i '../miRNA-protein-mappings/' -o '../tests/test4/output-actual/'
```

## Todo
* [x] Get command line arguments working
* [ ] Test
* [ ] Publish
