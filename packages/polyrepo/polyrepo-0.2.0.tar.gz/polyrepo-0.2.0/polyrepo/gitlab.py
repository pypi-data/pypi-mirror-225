from dataclasses import dataclass
from urllib.parse import quote
from json import dumps
from json import loads

from requests import post
from requests import codes


QUERY = """
query {{
  group(fullPath: "{path}") {{
    descendantGroups(after: "{endCursor}") {{
        nodes {{
            fullPath
        }}
        pageInfo {{
            endCursor
            hasNextPage
        }}
    }}
  }}
}}
"""


@dataclass
class GitLab:

    host: str = None
    token: str = None

    @property
    def headers(self):
        return {
            'Private-Token': self.token,
            'Content-Type': 'application/json'
        }

    def group_subgroups(self, path: str, traverse: bool = True):
        if not path:
            return
        url = f"https://{self.host}/api/graphql"
        paths = [path]
        hasNextPage = True
        endCursor = ""
        while hasNextPage:
            query = QUERY.format(**locals())
            response = post(url, headers=self.headers, json={'query': query})
            if response.status_code == codes.ok:
                groups = response.json()['data']['group']['descendantGroups']
                paths += [n['fullPath'] for n in groups['nodes']]
                hasNextPage = groups['pageInfo']['hasNextPage']
                if hasNextPage:
                    endCursor = groups['pageInfo']['endCursor']
            else:
                # Can we let requests take care of this?
                try:
                    message = response.json()['message']
                except Exception:
                    message = f"Error {response.status_code} from {url}"
                raise Exception(message)
        return sorted(paths)
