import requests
import sys
from requests import exceptions
from github import Github, GithubException
from Miner.Activity_performance import RequestVerificationClass
from Miner.Issues_Persistence.PersistencePattern import PersistencePattern

class MinersClass():
    def __init__(self, issue, authentication, time_to_wait, set_num_requests):
        self.issue = issue
        self.authentication = authentication
        self.time_to_wait = time_to_wait
        self.num_requests = set_num_requests

    def event_mining(self, issue):
        issue_events_list = []
        RequestVerificationClass(self.authentication, self.time_to_wait, self.num_requests)

        try:

            for event in self.issue.get_events():
                RequestVerificationClass(self.authentication, self.time_to_wait, self.num_requests)
                e = ''
                pattern = PersistencePattern()

                if(event.actor is None):
                    if (event.label is None):
                        event_formatted = pattern.eventPattern([issue.number, '-', event.created_at, event.event, '-'])
                    else:
                        event_formatted = pattern.eventPattern([issue.number, '-', event.created_at, event.event, event.label.name])

                else:
                    if(event.label is None):
                        event_formatted = pattern.eventPattern([issue.number, event.actor.login, event.created_at, event.event, '-'])
                    else:
                        event_formatted = pattern.eventPattern([issue.number, event.actor.login, event.created_at, event.event, event.label.name])
                issue_events_list.append(event_formatted)
        except requests.exceptions.ReadTimeout as aes:
            raise SystemError('ReadTimeout error in event mining')
        except requests.exceptions.ConnectionError as aes:
            raise SystemError('Connection error in event mining')
        except GithubException as d:
            if (d.status == 403):
                raise SystemError('Request limit achieved in event mining ')

        return issue_events_list

    def comments_mining(self, issue):
        issue_comments_list = []
        RequestVerificationClass(self.authentication, self.time_to_wait, self.num_requests)

        try:
            for comment in issue.get_comments():
                RequestVerificationClass(self.authentication, self.time_to_wait, self.num_requests)
                pattern = PersistencePattern()

                ## Adding method
                reactions = ''
                if(comment.user is None):
                    comment_formatted = pattern.CommentsPattern(['-', comment.created_at, comment.body, reactions])
                else:
                    comment_formatted = pattern.CommentsPattern([comment.user.login, comment.created_at, comment.body, reactions])

                issue_comments_list(comment_formatted)


        except requests.exceptions.ReadTimeout as aes:
            raise SystemError('ReadTimeout error in event mining')
        except requests.exceptions.ConnectionError as aes:
            raise SystemError('Connection error in event mining')
        except GithubException as d:
            if (d.status == 403):
                raise SystemError('Request limit achieved in event mining ')