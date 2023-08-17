from dataclasses import dataclass
from argparse import ArgumentParser

from polyrepo.command import PolyRepoCommand


@dataclass
class SyncCommand(PolyRepoCommand):

    """Simplifying assumptions:

    - pwd maps to the GitLab host root
    - argument is the path to a directory that exists and maps to a GitLab
      group or subgroup"""

    path: str = ''
    name = 'sync'

    @classmethod
    def add_args(self, parser):
        parser.add_argument('path', nargs='?')

    @PolyRepoCommand.wrap
    def execute(self):
        # self.host = self.cmachine.get('gitlab-host')
        self.status = f"Synced {self.path}."
        return "Sync!"
