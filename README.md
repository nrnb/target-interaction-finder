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
python __init__.py
```

## Todo
* [ ] Get command line arguments working
* [ ] Test
* [ ] Publish
