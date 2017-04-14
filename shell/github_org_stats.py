#!/usr/bin/env python

from __future__ import print_function
import json

from github import Github


def get_org_stats():
    """
    Get stats on each contributor in an organization on github.
    """
    username = raw_input('GH Username: ')
    password = raw_input('GH Password: ')
    org = raw_input('GH Org: ')
    g = Github(username, password)
    contributors = dict()

    for repo in g.get_organization(org).get_repos():
        if repo.fork:
            continue
        repo_contributors = repo.get_stats_contributors()
        if not repo_contributors:
            continue

        for contributor in repo_contributors:
            login = contributor.author.login
            cont_data = contributors.get(login, dict())
            for stat in ('total_commits', 'additions', 'deletions'):
                cont_data[stat] = cont_data.get(stat, 0)
            cont_data['total_commits'] += contributor.total

            for week in contributor.weeks:
                for key, ghkey in (('additions', 'a'), ('deletions', 'd')):
                    cont_data[key] += getattr(week, ghkey)
            contributors[login] = cont_data
    print(json.dumps(contributors, indent=2))
    with open('data.json', 'w') as outfile:
        json.dump(contributors, outfile, indent=2)


if __name__ == '__main__':
    get_org_stats()
