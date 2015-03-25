# exrna-mapper
Map ExRNA to proteins and interactions

A component for the Genboree workbench.

## To install

```
git clone git@github.com:ariutta/exrna-mapper.git
cd exrna-mapper
pip install -e .
easy_install -U setuptools # Only if your setuptools is outdated
pip install https://github.com/ariutta/networkxxgmml/zipball/master
```

You will also need to download the miRNA-protein mapping files into the "miRNA-protein-mappings" directory: https://github.com/ariutta/exrna-mapper/tree/master/miRNA-protein-mappings

## To run

```
cd exrnamapper
python __init__.py
```

## Todo
* [ ] Get command line arguments working
* [ ] Test
* [ ] Publish
