#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Combine multiple metadata files (e.g. sample.json, contacts.json) to one BioSamples Json Object for submission

@author: fuqi
@18-09-2019
"""
import os
import sys
import json

os.chdir("/home/fuqi/EBI/FAIRPlus/RESOLUTE/transcriptomics/scripts")

metadata_dir = "../data/RESOLUTE_transcriptomics/"
BSD_out = "../data/RESOLUTE_transcriptomics_metadata_BSD.json"
BSD_schema_file = "../schemas/biosamples_sample.json"

# Select metadata that needs to be submitted to biosamples
BSD_lists = ["cell_line","contact","sample","license"]
meta_files = []
metadata = []
for i in BSD_lists:
    if i+".json" in os.listdir(metadata_dir):
        print(i + ": added to BioSamples metadata")
        with open(metadata_dir+i+".json","r") as f:
            metadata.append(json.load(f))

# Check if metadata included in BSD_schema.
# if so, keep original format. If not, convert to part of "characteristics" attribute
with open(BSD_schema_file,"r") as schema_file:
    BSD_schema = json.load(schema_file)
# Attributes that are already defined in BSD
BSD_defined = list(BSD_schema["properties"].keys()) + list(BSD_schema["definitions"].keys())
# Attributes that are essential for BSD submission
BSD_required = BSD_schema["required"]

defined = []
undefined = []
for i in BSD_lists:
    if i in BSD_defined:
        defined.append(i)
    else:
        undefined.append(i)

# Combine undefined to "characteristics"
# 1. Flatten all undefined structures

def flatten_json(y):
    out = {}
    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


# 2. Remove NA attributes
# 3. merge following 
            

#with open(BSD_out,"w") as out:
#    json.dump(metadata,out)

        



