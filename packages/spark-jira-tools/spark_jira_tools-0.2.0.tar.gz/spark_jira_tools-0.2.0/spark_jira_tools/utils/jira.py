import requests
import json


class Jira(object):

    def __init__(self, username=None, token=None, proxy=False):
        self._session = requests.Session()
        self.base_url = "https://jira.globaldevtools.bbva.com"
        self.base_path = "/rest/auth/1/session"
        self.proxies = proxy
        url = f"{self.base_url}{self.base_path}"
        if username is None and token is None:
            payload = json.dumps({
                "username": "jonathan.quiza",
                "password": "MTc1MzM5NzEyMTA0OqK/nSm+o45gAPayE0q6nkd25xIE"
            })
        else:
            payload = json.dumps({
                "username": username,
                "password": token
            })

        self.current_proxies = {
            'https': 'http://118.180.54.170:8080',
            'http': 'http://118.180.54.170:8080'
        }

        self.headers = {
            'Content-Type': 'application/json'
        }
        if not self.proxies:
            self.r = self._session.post(url, headers=self.headers, data=payload)
        else:
            self.r = self._session.post(url, headers=self.headers, data=payload, proxies=self.current_proxies)
        self.cookies = requests.utils.dict_from_cookiejar(self.r.cookies)

    def get_key_issue(self, issue):
        self.base_path = f"/rest/api/2/issue/{issue}"
        url = f"{self.base_url}{self.base_path}"
        r = self._session.get(url, cookies=self.cookies)
        response = r.json()
        response = dict(
            id=response.get("id"),
            key=response.get("id"),
            self=response.get("self"),
        )
        return response

    def generated_issue(self, summary=None, description=None, assignee=None,
                        labels=None, feature_pad=None, acceptance_criteria=None,
                        code_team_backlog=None):
        issue_dict = {
            "fields": {"project": {"key": "PAD3"},
                       "summary": f"{summary}",
                       "description": f"{description}",
                       "issuetype": {"name": "Historia"},
                       'assignee': {'name': f'{assignee}'},
                       'priority': {'name': 'Medium'},
                       'labels': labels,
                       'customfield_10004': f"{feature_pad}",
                       'customfield_10260': f"{acceptance_criteria}",
                       'customfield_10270': {'id': '20247'},
                       'customfield_13300': [f"{code_team_backlog}"],
                       'customfield_18001': {'id': '91610'},
                       }

        }
        payload = json.dumps(issue_dict)
        self.base_path = f"/rest/api/2/issue"
        url = f"{self.base_url}{self.base_path}"
        if not self.proxies:
            r = self._session.post(url, cookies=self.cookies, headers=self.headers, data=payload)
        else:
            r = self._session.post(url, cookies=self.cookies, headers=self.headers, data=payload, proxies=self.current_proxies)
        response = r.json()
        return response
