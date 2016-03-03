# -*- python -*-
# author: krozin@gmail.com
# cliff_example: created 2016/02/08.
# copyright

import logging
import sys

from cliff.app import App
from cliff.command import Command
from cliff.commandmanager import CommandManager
from cliff.lister import Lister
from cliff.complete import CompleteCommand

class GitCli(App):
    log = logging.getLogger(__name__)
    def __init__(self):
        command_manager = CommandManager('gitcli.app')
        super(GitCli, self).__init__(
            description='sample app',
            version='0.1',
            command_manager=command_manager,
        )
        commands = {'commit': do_commit, 'tag': do_tag, 'list': do_list}
        for k, v in commands.iteritems():
            command_manager.add_command(k, v)
        self.command_manager.add_command('complete', CompleteCommand)

    def initialize_app(self, argv):
        self.log.debug('initialize_app')
    def prepare_to_run_command(self, cmd):
        self.log.debug('prepare_to_run_command %s', cmd.__class__.__name__)
    def clean_up(self, cmd, result, err):
        self.log.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.log.debug('got an error: %s', err)

class do_commit(Command):
    "commit"
    log = logging.getLogger(__name__)
    def get_parser(self, prog_name):
        parser = super(do_commit, self).get_parser(prog_name)
        parser.add_argument('--message', '-m', help='message', required=True)
        return parser

    def take_action(self, parsed_args):
        print (parsed_args.message)

class do_tag(Command):
    "tag"
    log = logging.getLogger(__name__)
    def get_parser(self, prog_name):
        parser = super(do_tag, self).get_parser(prog_name)
        parser.add_argument('--tag', '-a', help='tag', required=True)
        parser.add_argument('--message', '-m', help='message')
        return parser

    def take_action(self, parsed_args):
        print (parsed_args.tag, parsed_args.message)

class do_list(Lister):
    "list"
    log = logging.getLogger(__name__)
    def get_parser(self, prog_name):
        parser = super(do_list, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        headers = ["commands", "classes"]
        records = []
        mylist = {'commit': do_commit, 'tag': do_tag, 'list': do_list}
        for k,v in mylist.items():
            records.append((k,"{}{}".format(v.__name__, v.__mro__)))
        return (headers, records)

def main(argv=sys.argv[1:]):
    myapp = GitCli()
    return myapp.run(argv)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))