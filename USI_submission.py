#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
USI submission pipeline

Features:
- Creating a new submission
- Adding samples, projects, studies to submission
- check validation status

PreRequest:
    The user MUST get an AAP account at https://explore.aai.ebi.ac.uk/home

Example:
    python3 USI_submission -flags arguments

Note:
    This script doesn't support validation right now. The provided input data
    need to be

Options:
    * Compulsory
    -u Username *
    -s SampleFile
    -p projectFile
    -r sequencingRunFile
    -d study

    TODO -h help
"""

import sys
import os
import json
import subprocess
import requests
import time
import getpass
import argparse

#username = sys.argv[1]
my_parser = argparse.ArgumentParser(description='Easier USI submission')


"""
Command line interface
"""
def cli():

    parser = argparse.ArgumentParser(prog=f'Data submission Portal API tool. TODO add delete,update actions')

    #subparsers = parser.add_subparsers(help='execution modes', dest='exec_mode')
    # ----- Mode 'create' -----
    #sub = subparsers.add_parser('create', help='create a team/submission/sample/proj   ect,etc')
    parser.add_argument('-u','--username', metavar='<Username>', type=str, nargs='+',
                        help='AAP username, case-sensitive')
    parser.add_argument('-t', '--team', metavar='<Teamname>', type=str, nargs='+',
                        help='create a unique teamname')
    parser.add_argument('-n', '--new-submission',nargs='+',
                        help='Create a new submission. Requested for every data submission step')
    parser.add_argument('-p', '--project', nargs='+',
                        help='submit a new project')
    parser.add_argument('-sp', '--sample', nargs='+',
                        help='Submit a new sample')
    parser.add_argument('-seq', '--seqRun', nargs='+',
                        help='Submit a new sequence run')
    parser.add_argument('-a', '--assay', nargs='+',
                        help='Submit a new assay')
    parser.add_argument('-ad', '--assay_data', nargs='+',
                        help='Submit a new assay data')


    args = parser.parse_args()
    # ------- Mode 'delete' ----
    #sub = subparsers.add_parser('delete', help='delete a submission TODO')
    # ----- Mode 'update' -----
    #sub = subparsers.add_parser('update', help=' TODO')
    parser.print_help()
    return args

args = cli()


username = args.username
team_name = args.team

input("Press Enter to continue...")
try:
    password = getpass.getpass(prompt="AAP Password:",stream=None)
except Exception as error:
    print('ERROR', error)


print("Username(case sensitive: )"+username)

sample_filename = "RESOLUTE/transcriptomics/data/data_for_USI/samples.json"

def authenticate():
    """
    Get token for API submission

    PreRequest: the user must get a valid username from https://explore.api.aai.ebi.ac.uk/auth

    Note:
        1. username is case-sensitive
        2. The token is only valid for one hour
        3. Every time creating a new submission, the token has to be refreshed.

    Output: if credientials correct, return token.
    """
    r = requests.get('https://explore.api.aai.ebi.ac.uk/auth', auth=(username, password))
    if r.status_code == requests.codes.ok:
        return r.text
    else:
        raise r.raise_for_status()

def creat_team(team_name,team_description):
    #TODO new team or check if teamname exist or not

    header = {"Content-Type": "application/json",
              "Authorization": "Bearer " + token,
              "Accept": "application/hal+json"
              }

    team_info = {
        "description":team_description,
        "centreName":team_name
                }
    response = requests.post("https://submission-dev.ebi.ac.uk/api/user/teams",
                             headers = header,json = team_info)
    if response.status_code == requests.codes.created:
        response_json = response.json()
        team = response_json["name"]
        link_submissions_create = response_json['_links']["submissions:create"]['href']
        return team,link_submissions_create
    else:
        raise response.raise_for_status()

def create_submission(link,token):
    header = {"Content-Type": "application/json;charset=UTF-8",
              "Authorization": "Bearer " + token,
              "Accept": "application/hal+json"
              }
    data = {}
    response = requests.post(link,headers = header, json = data)
    if response.status_code == requests.codes.created:
        response_json = response.json()
        return response_json
    else:
        raise response.raise_for_status()

def load_data(filename):
    with open(filename) as f:
        data = json.load(f)
    return data

def update_sample(token, link, data):
    url = link
    header = {
        "Content-Type": "application/json;charset=UTF-8",
        "Accept": "application/hal+json",
        "Authorization": "Bearer " + token
    }
    response = requests.post(url, headers=header, json=data)
    if response.status_code == requests.codes.created:
        pass
    else:
        raise response.raise_for_status()

# Collect links in the content for next submission
def get_content(link,token):
    header = {"Content-Type": "application/json;charset=UTF-8",
              "Authorization": "Bearer " + token,
              "Accept": "application/hal+json"
              }
    data = {}
    response = requests.post(eval("link_contents"),headers = header, json = data)
    # test
    a = response.json()
    return a
    '''
    if response.status_code == requests.codes.created:
        print(response.json())
        response_json = response.json()
        return response_json
    else:
        raise response.raise_for_status()
    '''

def create_domainData(domain,data):
    """
    Create a data in one USI submission. the domains are e.g. samples,sequencingRuns,etc

    :param domain:eg samples, projects,sequencingRuns
    :param data: data in json format, should follow corresponding domain-specific schema requirement
    :return:Data submission response
    """
    header = {"Content-Type": "application/json;charset=UTF-8",
              "Authorization": "Bearer " + token,
              "Accept": "application/hal+json"
              }
    response = requests.post(eval("link_"+domain), headers=header, json=data)
    if response.status_code == requests.codes.created:
        response_json = response.json()
        print(domain)
        print(response.status_code)
        return response_json
    else:
        raise response.raise_for_status()

def submission_status(link,token):

    header = {
        "Accept": "application/hal+json",
        "Authorization": "Bearer " + token
    }

    response = requests.get(link, headers=header)

    if response.status_code == requests.codes.ok:
        print("submission status")
        print(response.status_code)
        #print(response.json())
    else:
        raise response.raise_for_status()

def validation_status(link,token):
    header = {
        "Accept": "application/hal+json",
        "Authorization": "Bearer " + token
    }

    response = requests.get(link, headers=header)

    if response.status_code == requests.codes.ok:
        print("validation results")
        print(response.status_code)
        responses = response.json()
        print(responses['_embedded']['validationResults'][0]['overallValidationOutcomeByAuthor'])
        return responses
    else:
        raise response.raise_for_status()

# get original token
token = authenticate()
# creating new team
teams,link_submission = creat_team(team_name,team_description)
# Refresh token after created a new team
token = authenticate()

new_submission = create_submission(link_submission,token)

# Create link variable with the links in the submission
for i in list(new_submission['_links'].keys()):
    # If link name includes ":", replace with "_"
    if (":" in i):
        new = i.replace(":","_")
        vars()["link_"+new]= new_submission['_links'][i]['href']
    else:
        vars()["link_"+i]= new_submission['_links'][i]['href']



contents = get_content(eval("link_contents"),token)
# Create variable for link to different types of metadata
for i in list(contents['_links'].keys()):
    # If link name includes ":", replace with "_"
    if (":" in i):
        new = i.replace(":","_")
        vars()["link_"+new]= contents['_links'][i]['href']
    else:
        vars()["link_"+i]= contents['_links'][i]['href']
"""
# list all variables
for i in vars().keys():
    if i.startswith("link_"):
        print(i)
"""

sample = load_data(sample_filename)

create_domainData("samples",sample)
submission_status(link_submissionStatus,token)
validation_status(link_validationResults,token)


