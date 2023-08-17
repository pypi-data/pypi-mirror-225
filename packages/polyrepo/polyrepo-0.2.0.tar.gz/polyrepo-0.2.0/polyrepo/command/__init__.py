from dataclasses import dataclass

from wizlib.command_handler import Command
from wizlib.config_machine import ConfigMachine


@dataclass
class PolyRepoCommand(ConfigMachine, Command):

    appname = 'polyrepo'
    default = 'sync'
