#!/usr/bin/env python

import sys
import optparse
import logging
import os
import requests
import pickle
import datetime
import json
import pprint

from redis import StrictRedis as Redis
import httplib

from dateutil import parser as date_parser

GITHUB_API_KEY = os.environ.get("GITHUB_API_KEY")
GITHUB_ORGANIZATION = os.environ.get("GITHUB_ORGANIZATION")
GITHUB_REPO = os.environ.get("GITHUB_REPO")

logger = logging.getLogger(__name__)

GITHUB_API_ENDPOINT = "https://api.github.com"

github_url = lambda *components: "{}/{}".format(GITHUB_API_ENDPOINT, "/".join(components))
HEADERS = {
    'Authorization': "token {}".format(GITHUB_API_KEY),
    'Content-Type': "application/json",
    'Accept': "application/json"
}

milestone_url = github_url("repos", GITHUB_ORGANIZATION, GITHUB_REPO, "milestones")

def delete_all_milestones_with_no_issues():
    response = requests.get(milestone_url, headers=HEADERS)
    for milestone in response.json():
        if milestone['open_issues'] == 0 and milestone['closed_issues'] == 0 and "week" in milestone['title'].lower():
            response = requests.delete(milestone['url'], headers=HEADERS)
            if response.status_code == 204:
                print "Deleting", milestone['title']
            else:
                print "Error"
        else:
            print "Skipping", milestone['title']

# delete_all_milestones_with_no_issues()
# sys.exit(1)

def create_milestone(title, due_date=None):
    milestone_data = {
        'title': title,
    }

    if due_date is not None:
        milestone_data['due_on'] = due_date.isoformat()

    response = requests.post(milestone_url, data=json.dumps(milestone_data), headers=HEADERS)
    if response.status_code == 201:
        print "Created", title
    else:
        print "Error creating", title

day = datetime.date(2015, 1, 1)
groupings = []
group_start = day
group_end = None
previous_week_number = -1
for i in range(365):
    week_number = day.isocalendar()[1]
    if week_number != previous_week_number:
        if group_start and group_end and datetime.date.today() < group_end:
            title = "Week {0}: {1.month}/{1.day}-{2.month}/{2.day}".format(previous_week_number, group_start, group_end)
            create_milestone(title, group_end + datetime.timedelta(days=1))

        previous_week_number = week_number
        group_start = day
    else:
        group_end = day

    day += datetime.timedelta(days=1)

title = "Week {0}: {1.month}/{1.day}-{2.month}/{2.day}".format(previous_week_number, group_start, group_end)
create_milestone(title, group_end + datetime.timedelta(days=1))

create_milestone("Backlog")

