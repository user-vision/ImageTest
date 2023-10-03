"""
Exports issues from a list of repositories to individual csv files.
Uses basic authentication (Github username + password) to retrieve issues
from a repository that username has access to. Supports Github API v3.
Forked from: unbracketed/export_repo_issues_to_csv.py
"""
import argparse
import csv
import re
from getpass import getpass
from collections import Counter
import json
from addict import Dict
from getpass import getpass
import requests
import os

auth = None
state = 'open'

failedLabels = []

# ratingtemplate = open(os.getcwd() + "/utils/wcag-rating.txt", "r")
# print(ratingtemplate.read())

wcagpath = os.getcwd() + "/utils/wcag21.json"
wcagpath2 = os.getcwd() + "/utils/wcagprinciples.json"
wcagdict = {}
wcagprinciples = {}
with open(wcagpath, "r") as config_file:
    wcagdict = json.load(config_file)

with open(wcagpath2, "r") as config_file:
    wcagprinciples = json.load(config_file)

   

def locate_issues(r):
    """Parses JSON response and writes to CSV."""
    if r.status_code != 200:
        raise Exception(r.status_code)
    for issue in r.json():
        if 'pull_request' not in issue:
            if 'closed' not in issue['state']:

                if any(args.project in s['name'] for s in issue['labels']):
                    
                    wcag = []
                    severity = []
                    platform = []
                    location = []


                    for label in issue['labels']:
                        if re.match(r'[0-9.]', label['name']) is not None: 
                            failedLabels.append(label['name'])


def get_ratings(name, state):
    """Requests issues from GitHub API and writes to CSV file."""

    ratings = ["H", "M", "L"]
    csvfilename = '02.2-wcag-overview.Rmd'
    with open(csvfilename, 'w') as csvfile:
        csvout = csvfile
        # csvout.writelines(["WCAG\n" ])
        for rating in ratings:

            url = 'https://api.github.com/repos/{}/issues?state={}&labels={}'.format(name, state, rating)
            # print(url)
            r = requests.get(url, auth=auth)
            locate_issues(r)

            # Multiple requests are required if response is paged
            if 'link' in r.headers:
                pages = {rel[6:-1]: url[url.index('<')+1:-1] for url, rel in
                        (link.split(';') for link in
                        r.headers['link'].split(','))}
                while 'last' in pages and 'next' in pages:
                    pages = {rel[6:-1]: url[url.index('<')+1:-1] for url, rel in
                            (link.split(';') for link in
                            r.headers['link'].split(','))}
                    r = requests.get(pages['next'], auth=auth)
                    locate_issues(r)
                    if pages['next'] == pages['last']:
                        break
        wcaglabels = failedLabels.sort()
        wcaglist = '\n'.join([l for l in failedLabels])
        mylist = []
        principlelist = []

        for l in failedLabels:
            mylist.append(l)
            principlelist.append(l)
        # print(Counter(principlelist).keys())
        # print(Counter(mylist).values())

        criteria = []
        csvout.writelines("### WCAG 2.1 Compliance {-}\n\n| **Principle**|**Description**| **Result**|\n|:------------:|--------------:|:---------:|")


        for principle in wcagprinciples:
            if principle in principlelist[:3]:
                    line = "|" + principle + "|" + wcagprinciples[principle]['Principle'] + "| Fail|" + "\n"
            else:
                line = "|" + principle + "|" + wcagprinciples[principle]['Principle'] + "| **Pass** |" + "\n"
            csvout.writelines(line)


        mylist = list(dict.fromkeys(mylist))
        wcaglabels = ', '.join([l for l in mylist])
        # print(wcaglabels)







parser = argparse.ArgumentParser(description="Write GitHub repository issues "
                                             "to CSV file.")
parser.add_argument('repositories', nargs='+', help="Repository names, "
                    "formatted as 'username/repo'")
parser.add_argument('project', help="Project")
parser.add_argument('username', help="Username")
parser.add_argument('token', help="GitHub Token")
parser.add_argument('--all', action='store_true', help="Returns both open "
                    "and closed issues.")
args = parser.parse_args()

if args.all:
    state = 'all'
    
username = args.username
password = args.token
project = args.project

auth = (username, password)
for repository in args.repositories:
    get_ratings(repository, state)
