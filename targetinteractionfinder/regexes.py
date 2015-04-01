#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

# based on the regexes from http://identifiers.org/mirbase.mature/
# and http://identifiers.org/mirbase/
identifiers_org = re.compile('^http:\/\/identifiers.org\/.*\/')

# based on the regexes from http://identifiers.org/mirbase.mature/
# and http://identifiers.org/mirbase/
mirbase_identifier = re.compile('^(MIMAT\d{7})|(MI\d{7})$')

# from http://www.ebi.ac.uk/miriam/main/collections/MIR:00000003
ensembl_identifier = re.compile('^((ENS[A-Z]*[FPTG]\d{11}(\.\d+)?)|(FB\w{2}\d{7})|(Y[A-Z]{2}\d{3}[a-zA-Z](\-[A-Z])?)|([A-Z_a-z0-9]+(\.)?(t)?(\d+)?([a-z])?))$')

# from http://www.ebi.ac.uk/miriam/main/collections/MIR:00000069
ncbigene_identifier = re.compile('^\d+$')

# only works for human miRNA names
mirna_name = re.compile('^hsa-.*-.*')
