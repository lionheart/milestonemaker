# Copyright 2015-2017 Lionheart Software LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import logging
import requests
import datetime
import json

from dateutil import parser as date_parser

logger = logging.getLogger(__name__)
GITHUB_API_ENDPOINT = "https://api.github.com"
github_url = lambda *components: "{}/{}".format(GITHUB_API_ENDPOINT, "/".join(components))

class MilestoneMaker(object):
    def __init__(self, api_key, organization, repository, start_date=None):
        self.api_key = api_key
        self.organization = organization
        self.repository = repository
        if start_date is not None:
            self.start_date = date_parser.parse(start_date).date()
        else:
            self.start_date = datetime.date.today()

    @property
    def HEADERS(self):
        return {
            'Authorization': "token {}".format(self.api_key),
            'Content-Type': "application/json",
            'Accept': "application/json"
        }

    @property
    def milestone_url(self):
        return github_url("repos", self.organization, self.repository, "milestones")

    def delete(self):
        response = requests.get(self.milestone_url, headers=self.HEADERS)
        for milestone in response.json():
            if milestone['open_issues'] == 0 and milestone['closed_issues'] == 0 and "week" in milestone['title'].lower():
                response = requests.delete(milestone['url'], headers=self.HEADERS)
                if response.status_code == 204:
                    print("Deleting", milestone['title'])
                else:
                    print("Error")
            else:
                print("Skipping", milestone['title'])

    def create(self):
        def create_milestone(title, due_date=None):
            milestone_data = {
                'title': title,
            }

            if due_date is not None:
                milestone_data['due_on'] = datetime.datetime.fromordinal(due_date.toordinal()).isoformat() + "Z"

            response = requests.post(self.milestone_url, data=json.dumps(milestone_data), headers=self.HEADERS)
            if response.status_code == 201:
                print("Created", title)
            else:
                print("Error creating", title)

        day = datetime.date(self.start_date.year, 1, 1)
        groupings = []
        group_start = day
        group_end = None
        previous_week_number = -1
        while True:
            week_number = day.isocalendar()[1]
            if week_number != previous_week_number:
                if group_start and group_end and self.start_date < group_end:
                    title = "Week {0}: {1.month}/{1.day}-{2.month}/{2.day}".format(previous_week_number, group_start, group_end)
                    create_milestone(title, group_end + datetime.timedelta(days=1))

                previous_week_number = week_number
                group_start = day
            else:
                group_end = day

            day += datetime.timedelta(days=1)

            if day.year != self.start_date.year:
                break

        title = "Week {0}: {1.month}/{1.day}-{2.month}/{2.day}".format(previous_week_number, group_start, group_end)
        create_milestone(title, group_end + datetime.timedelta(days=1))

        create_milestone("Backlog")


