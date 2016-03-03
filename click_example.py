# -*- python -*-
# author: krozin@gmail.com
# cliff_example: created 2016/02/08.
# copyright

import sys
import click

@click.group()
def cli():
    print("{} {}".format(sys._getframe().f_code.co_name, locals()))

@cli.command('commit')
@click.option('-m', 'message', nargs=1, type=unicode, required=True)
def do_commit(message):
    print(message)

@cli.command('tag')
@click.option('-m', 'message', nargs=1, type=unicode, required=True)
@click.option('-a', 'tag', nargs=1, type=unicode, required=True)
#@click.option('-a', 'tag', nargs=1, type=unicode, required=False)
def do_tag(message, tag):
    print(tag, message)

@cli.command('list')
def do_list():
    mylist = {'commit': do_commit, 'tag': do_tag, 'list': do_list}
    print [(k,v) for k,v in mylist.items()]

if __name__ == '__main__':
    cli()
