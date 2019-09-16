# Converting Transcriptomics JSON data to BioSamples JSON schema for API submission
# @fuqi 2019-09-13

# When converting transcriptomics data to BSD format, it can be devided into 3 parts
# Part1: attributes exist both in BSD and trans, might under different names
# Part2: Additional trans metadata, all belong to "characteristics" in BSD
# Part3: Essential for BSD, not in trans. e.g. domain

import json
import os
from collections import OrderedDict

# TODO define BSD submission domain

os.chdir("../")

with open("schemas/biosamples_sample.json", "r") as BSD_schema_f:
    BSD_schema = json.load(BSD_schema_f)

# Properties and attributes requested in BSD schema.
BSD_properties = BSD_schema["properties"]
BSD_definitions = BSD_schema["definitions"]

# Load transcriptomics metadata
with open("RESOLUTE_transcriptomics_metadata.json","r") as trans_data_f:
    trans_data = json.load(trans_data_f)

################## Part 1 ##################
# Extract Shared attributes between BSD and trans_data/BSD required data
# e.g. BSD -> Trans
# 1. contact -> contacts
# 2. publications -> publication
# Attributes that is required by BSD is also included

# TODO Find matching attributes automatically
# TODO avoid changing every time
# TODO also map "firstname, lastname" and other attributes.(case-insensitive, plurals

#BSD_names = ["contact","publications","release"]
#trans_names = ["contacts","publication","date"]

# TODO to be updated    
BSD_names = ["contact","release"]
trans_names = ["contacts","date"]
    
## Take the shared attributes out.
def shared_attributes(BSD,trans):
    trans_to_BSD = {}
    value = trans_data[trans]
    trans_to_BSD[BSD] = value
    return trans_to_BSD

if len(BSD_names) == len(trans_names):
    trans_to_BSD_data = {}
    for i in range(0,len(BSD_names)):
        v = shared_attributes(BSD_names[i],trans_names[i])
        trans_to_BSD_data = {**trans_to_BSD_data,**v}

# TODO: remove empty publication
# TODO: change date format and automize
trans_to_BSD_data["release"]="2019-07-16T09:47:20.003Z"

################## Part 2 ##################
# Add specific metadata that's only in BSD
# all attributes that are not in the BSD_names are considered as "characteristics" in BSD schema

# 2.1 Remove data exist in BSD
for i in trans_names:
    del trans_data[i]
    
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

trans_flatten = flatten_json(trans_data)

# Remove all empty attributes "NA" in the original file
trans_clean = {k:v for k, v in trans_flatten.items() if v != 'NA'}

# Remove all duplicated words in attribute names
attributes = list(trans_clean.keys())

def delete_duplicate(l):
    new_l = []
    for i in l:
        if i not in new_l:
            new_l.append(i)
    return new_l

def clean_names(l):
    out= []
    for i in l:
        temp = i.split('_')
        a = delete_duplicate(temp)
        i = " ".join(a)
        out.append(i)
    return out

attributes_clean = clean_names(attributes)

# Replace attribute names with more conside expression
new_dict = {}
if len(attributes_clean) == len(trans_clean):
   for i in range(0,len(attributes_clean)):
       new_dict[attributes_clean[i]]= list(trans_clean.values())[i]

# Convert to BSD "characteristics" format
# BSD json characteristics format: e.g.
# "characteristics":{
#    "A":[{"text":"a"}],
#    "B":[{"text":"b"}]
#  }

trans_to_BSD_data["characteristics"] = {}
with open("temp","a") as t:
    for k,v in new_dict.items():
        d,l,temp = {},[],{}
        temp["text"] = v
        l.append(temp)
        d[k] = l
        trans_to_BSD_data["characteristics"] = {**trans_to_BSD_data["characteristics"],**d}

################## Part 3 ##################
# Add BSD specific attributes
# e.g BSD submissin names, BSD domain


# Equavlent to which() in R. 
# Finding the index of values in a list, which equals to the input.
# TODO whatif there is more than one attribute with the same name.
# TODO will it happen or not. if happens, how to solve
def which_equal(l,target):
    for i in range(0,len(l)):
        if l[i] == target:
            return i

name_index = which_equal(list(trans_clean.keys()),"sample_sample_name")
name = list(trans_clean.values())[name_index]
trans_to_BSD_data["name"] = name

with open("trans_BSD_data.json","w") as out:
    json.dump(trans_to_BSD_data,out)



    
    
