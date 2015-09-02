#!/usr/bin/env python

import os
import uuid
import json
from datetime import time, date, datetime, timedelta
from random import randint
from random import choice

import click
import git

hello_world_c = """#include <iostream>
int main()
{
  std::cout << "Hello World!" << std::endl;
  return 0;
}
"""

default_file_name = 'main.cpp'


class RockStar:

    def __init__(self, days=400, days_off=[], file_name=default_file_name,
                 code=hello_world_c):
        self.days = days
        self.file_name = file_name
        self.file_path = os.path.join(os.getcwd(), file_name)
        self.code = code
        self.repo_path = os.getcwd()
        self.messages_file_name = 'commit-messages.json'
        self.messages_file_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), self.messages_file_name)
        self.days_off = list(map(str.capitalize, days_off))

        self._load_commit_messages()

    def _make_face():
        sunday = _get_last_sunday
        catSet = set([
            (21,0), (21,1), (21,2), (21,3), (21,4), (21,5), (22,1), 
            (22,5), (23,1), (23,5), (24,1), (24,5), (25,1), (25,5), 
            (26,0), (26,1), (26,5), (27,2), (27,3), (27,4), (27,5)
        ])
        return catSet;

    def _make_body():
        catSet = set([
            (9,0),  (9,1),  (9,2),  (10,0), (10,2), (11,1), (11,3), 
            (11,5), (11,6), (12,2), (12,3), (12,4), (12,5), (12,6), 
            (13,0), (13,1), (13,2), (13,3), (13,4), (13,5), (14,0),
            (14,5), (14,6), (15,0), (15,5), (15,6), (16,0), (16,5),
            (17,0), (17,5), (18,0), (18,5), (19,0), (19,5), (20,0),
            (20,5), (20,6), (21,6), (22,0), (24,6), (13,5), (14,0)
        ])
        return catSet

    def _make_tail():
        catSet = set([
            (0,0),  (0,2),  (0,4),  (1,0),  (1,2),  (1,4),  (2,0), 
            (2,2),  (2,4),  (3,1),  (3,3),  (3,5),  (4,1),  (4,3), 
            (4,5),  (5,1),  (5,3),  (5,5),  (6,0),  (6,2),  (6,4),
            (7,0),  (7,2),  (7,4),  (8,0),  (8,2),  (8,4),  (9,3),
            (9,5),  (10,1), (10,3), (10,5), (11,2), (12,0), (14,1),
            (14,1), (14,2), (14,3), (14,4), (15,1), (15,2), (15,3), 
            (15,4), (16,1), (16,2), (16,3), (16,4), (17,1), (17,2), 
            (17,3), (17,4), (18,1), (18,2), (18,3), (18,4), (19,1), 
            (19,2), (19,3), (19,4), (20,1), (20,2), (20,3), (20,4)
        ])
        return catSet

    def _make_tail_alt():
        catSet = set([
            (0,1),  (0,3),  (0,5),  (1,1),  (1,3),  (1,5),  (2,1), 
            (2,3),  (2,5),  (3,2),  (3,4),  (3,6),  (4,2),  (4,4), 
            (4,6),  (5,2),  (5,4),  (5,6),  (6,1),  (6,3),  (6,5),
            (7,1),  (7,3),  (7,5),  (8,1),  (8,3),  (8,5),  (9,4),
            (9,6),  (10,4), (10,6), (11,4), (12,1)
        ])
        return catSet

    def _get_last_sunday():
        d = date.today().toordinal()
        last = d - 6
        sunday = last - (last % 7)
        return date.fromordinal(sunday)

    def _translate_set_to_date(cat_coordinate):
        starting_date = _get_last_sunday().toordinal()
        difference = 189 - (cat_coordinate[0] * 7) - cat_coordinate[1]
        last = starting_date - difference
        return date.fromordinal(last)

    def _load_commit_messages(self):
        with open(self.messages_file_path) as f:
            messages_file_contents = json.load(f)
        names = messages_file_contents['names']
        messages = messages_file_contents['messages']
        self.commit_messages = [m.format(name=choice(names)) for m in messages]

    def _get_random_commit_message(self):
        return choice(self.commit_messages)

    def _make_last_commit(self):
        with open(self.file_path, 'w') as f:
            f.write(self.code)

        os.environ['GIT_AUTHOR_DATE'] = ''
        os.environ['GIT_COMMITTER_DATE'] = ''
        self.repo.index.add([self.file_path])
        self.repo.index.commit('Final commit :sunglasses:')

    def _edit_and_commit(self, message, commit_date):
        with open(self.file_path, 'w') as f:
            f.write(message)
        self.repo.index.add([self.file_path])
        date_in_iso = commit_date.strftime("%Y-%m-%d %H:%M:%S")
        os.environ['GIT_AUTHOR_DATE'] = date_in_iso
        os.environ['GIT_COMMITTER_DATE'] = date_in_iso
        self.repo.index.commit(self._get_random_commit_message())

    def _get_random_time(self):
        return time(hour=randint(0, 23), minute=randint(0, 59),
                    second=randint(0, 59), microsecond=randint(0, 999999))

    def _get_dates_list():
        return [datetime.combine(d, _get_random_time()) 
            for d in dates(_make_face(), 6) + dates(_make_body(), 5) + dates(_make_tail(), 2) + dates(_make_tail_alt(), 1)]


    def make_me_a_rockstar(self):
        self.repo = git.Repo.init(self.repo_path)
        label = 'Making you a Rockstar Programmer'
        with click.progressbar(self._get_dates_list(), label=label) as bar:
            for commit_date in bar:
                self._edit_and_commit(str(uuid.uuid1()), commit_date)
        self._make_last_commit()
        print('\nYou are now a Rockstar Programmer!')


@click.command()
@click.option('--days', type=int, default=400)
def cli(days):
    magic = RockStar(days=days)
    magic.make_me_a_rockstar()
