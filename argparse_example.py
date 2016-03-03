# -*- python -*-
# author: krozin@gmail.com
# cliff_example: created 2016/02/08.
# copyright

import argparse
import sys

class GitCli(object):
    def __init__(self, args):
        self.commands = {'commit': self.do_commit, 'tag': self.do_tag, 'list': self.do_list}
        self.args = args
        self.params = self.get_params()
        self.commands.get(self.params.command)()

    def get_params(self):
        commit = argparse.ArgumentParser(add_help=False)
        commit.add_argument('-m', dest='message', required=True)
        tag = argparse.ArgumentParser(add_help=False)
        tag.add_argument('-a', dest='tag', required=True)
        parser = argparse.ArgumentParser(description="desc")
        subparsers = parser.add_subparsers(title="commands", help='list commands', dest='command')
        subparsers.add_parser('commit', parents=[commit], help="commit", description="make commit")
        subparsers.add_parser('tag', parents=[commit, tag], help="commit", description="make commit")
        subparsers.add_parser('list', help="list", description="see list of commands")
        #print parser.parse_args(self.args)
        return parser.parse_args(self.args)

    def do_commit(self):
        print self.params.message

    def do_tag(self):
        print (self.params.tag, self.params.message)

    def do_list(self):
        print self.commands

def main(args=None):
    #print "args={}".format(args)
 if args is None:
        args = sys.argv[1:]
    f = GitCli(args)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))