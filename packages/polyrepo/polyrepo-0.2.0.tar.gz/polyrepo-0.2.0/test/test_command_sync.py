from unittest import TestCase
import os

from wizlib.command_handler import CommandHandler
from polyrepo.command import PolyRepoCommand
from polyrepo.command.sync_command import SyncCommand


class TestCommandSync(TestCase):

    def test_from_handler(self):
        r, s = CommandHandler(PolyRepoCommand).handle(['sync'])
        self.assertEqual(r, 'Sync!')

    def test_default(self):
        r, s = CommandHandler(PolyRepoCommand).handle()
        self.assertEqual(r, 'Sync!')

    def test_argument(self):
        r, s = CommandHandler(PolyRepoCommand).handle(['sync', 'foo'])
        self.assertEqual(s, 'Synced foo.')

    def test_config(self):
        h = CommandHandler(PolyRepoCommand)
        c = h.get_command(
            ['--config', 'test/files/.polyrepo.yml', 'sync', 'foo'])
        self.assertEqual(c.config_get('gitlab-host'), 'gitlab.com')

    def test_dir_list(self):
        c = SyncCommand()
        c.gitlab_host = 'gitlab.local'
        self.assertEqual(c.config_get('gitlab-host'), 'gitlab.local')
