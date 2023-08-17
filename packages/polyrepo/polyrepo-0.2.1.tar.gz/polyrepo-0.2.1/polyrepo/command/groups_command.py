from dataclasses import dataclass
from argparse import ArgumentParser
import os

from polyrepo.command import PolyRepoCommand
from polyrepo.gitlab import GitLab


@dataclass
class GroupsCommand(PolyRepoCommand):

    """Simplifying assumptions:

    - pwd maps to the GitLab host root
    - argument is the path to a directory that exists and maps to a GitLab
      group or subgroup"""

    path: str = ''
    traverse: bool = False
    name = 'groups'

    @classmethod
    def add_args(self, parser):
        parser.add_argument('path', nargs='?')
        parser.add_argument('--traverse', '-t', action='store_true')

    @PolyRepoCommand.wrap
    def execute(self):
        from pathlib import Path
        host = self.config_get('gitlab-host')
        token = self.config_get('gitlab-token')
        if host and token:
            subgroups = GitLab(host, token).group_subgroups(
                self.path, traverse=self.traverse)
            self.status = f"Listed {len(subgroups)} subgroups"
            return "\n".join(subgroups)
        else:
            raise RuntimeError("Missing host or token for GitLab API call")
