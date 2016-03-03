# cli_cliff_click_argparse
cliff vs click vs argparse

I dont have indend to describe cliff or click functionality here. That is not a target of this page.
I would like to show how to use it and what is a reason to use cliff insted of argparse.
 
-----------------------   DEVELOPER HISTORY  -------------------------------------------
Actually we are using argparse everywhere and it is enought in common cases. Let's take a look at several cases where we still using argparse but
we have to add wrappers above. For example we know "git" commands. Actually git is supporting many commands and arguments for them.
examples: git clone <hreff>  git add, git commit, git checkout ..... and those commands have their own list arguments. 
How argparse can be used for such cases?  Code is below

commit= argparse.ArgumentParser(add_help=False)
commit.add_argument('-m', dest='message', required=True)
tag = argparse.ArgumentParser(add_help=False)
tag.add_argument('-a', dest='tag', required=True)
 
Another things that mentioned attributes can be applicable for several commands:
git tag -a v1.0 -m 'version 1.0'  or git commit -m 'message'
In this case we have to create couple subparsers
parser = argparse.ArgumentParser(description="desc", "use with -h/--help option")
subparsers = parser.add_subparsers(title="commands", help='list commands', dest='command')
subparsers.add_parser('commit', parents=[commit], help="commit", description="make commit")
subparsers.add_parser('tag', parents=[commit, tag], help="commit", description="make commit")
 
finally it look like: https://github.com/Betrezen/cli_cliff_click_argparse/blob/master/argparse_example.py

Hm, argparse is just smart parser and nothing else. If we need to control command line attributes in scope of one entity we have to implement a wrapper and wrapper depends on implementation and engineer experience and knowledge base. Another things that we have to extend our wrapper in order to support of different output. For example we would like to see the same data in table or json views. Another case: if we would like to do logging we have to extend our wrapper. IF we have a lot of commands which shall be supported then own CLI will grown and we have to divide it on several files. Take into account that we have only one class which control all arguments. Hm,,,, seems we have to split it. Common, we have to do refactoring because our wrapper is not flexible enough.
Seems we trying to develop CLI and don't take into account that many CLI libs already are presented on python. 
We are going to do own CLI or to use existing one? We just waste time if will develop own CLI lib.
 
Another history......
As developer I would like to control list of commands, control list of arguments per each command and keep command handler under one object (function or class). Argparse don't provide such things and it is focused on transformation command line string to python objects (very similar to ORM) How to implement it? 
So, we can develop CLI framework or to use existing one. Cliff especially was developed for CLI functionality.
Cliff using argparse and it was done in OOP (object oriented programming) style. We have a common APP class which focused on general things like logging, getting management and pass it to inside. Let me show: https://github.com/Betrezen/cli_cliff_click_argparse/blob/master/cliff_example.py
 
By any way we still follow to OOP style and if I would like to follow to functional programming style?
Click is good enough here. Let's take a look. https://github.com/Betrezen/cli_cliff_click_argparse/blob/master/click_example.py


-----------------------   USER HISTORY  -------------------------------------------
cliff/click/argparse - doesnt matter for end user because he is interesting what he/she can do in CLI
OK. I'm end user and I woiuld like to have ability to get data in different formats. I like csv, json, yaml and table view.
So, such output can be utilized in reports and It can be utilized by other tool directly and I dont need to do it manually.
Hm,.. looks like argparse don't support output format and developer shall do it himself. I have to wait then such functionality will be 
implemented by development team. 
 
Let';s take a look at command mentioned above: 1.py (cliff)  2.py (own wrapper wuth argparse)
C:\Users\krozi\PycharmProjects\untitled>1.py tag -a v1 -m hi
('v1', 'hi')
C:\Users\krozi\PycharmProjects\untitled>2.py tag -a v1 -m hi
('v1', 'hi')
Do you see difference? NO!
 
One more attempt
C:\Users\krozi\PycharmProjects\untitled>1.py list
+----------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| commands | classes |
+----------+--------------------------------------------------------------------------------+
| commit | do_commit(<class '__main__.do_commit'>, <class 'cliff.command.Command'>, <type 'object'>) |
| tag | do_tag(<class '__main__.do_tag'>, <class 'cliff.command.Command'>, <type 'object'>) |
| list | do_list(<class '__main__.do_list'>, <class 'cliff.lister.Lister'>, <class 'cliff.display.DisplayCommandBase'>, <class 'cliff.command.Command'>, <type 'object'>) |
+----------+--------------------------------------------------------------------------------+
C:\Users\krozi\PycharmProjects\untitled>1.py list -f yaml
- classes: do_commit(<class '__main__.do_commit'>, <class 'cliff.command.Command'>,
<type 'object'>)
commands: commit
- classes: do_tag(<class '__main__.do_tag'>, <class 'cliff.command.Command'>, <type
'object'>)
commands: tag
- classes: do_list(<class '__main__.do_list'>, <class 'cliff.lister.Lister'>, <class
'cliff.display.DisplayCommandBase'>, <class 'cliff.command.Command'>, <type 'object'>)
commands: list
 
C:\Users\krozi\PycharmProjects\untitled>2.py list
{'commit': <bound method GitCli.do_commit of <__main__.GitCli object at 0x02733870>>, 'tag': <bound method GitCli.do_tag of <__main__.GitCli object at 0x02733870>>, 'list': <bound method GitCli.do_list of <__main__.GitCli object at 0x02733870>>}
C:\Users\krozi\PycharmProjects\untitled>2.py list -f yaml
usage: 2.py [-h] {commit,tag,list} ...
2.py: error: unrecognized arguments: -f yaml

<red>Oh.... I see a difference....</red>
 
>>> Cliff provides different output by default and we have to implement similar for our wrapper if we would like to support such functionality. 
 
 I'm end user and I woiuld like to have ability to have interactive mode.
C:\Users\krozi\PycharmProjects\untitled>2.py
usage: 2.py [-h] {commit,tag,list} ...
2.py: error: too few arguments

<pre>
C:\Users\krozi\PycharmProjects\untitled>1.py
(1) commit -m aaa
aaa
(1)
</pre>
>>> WOW. Cliff provides interactive mode by default.
 
 I'm end user and I would like to have ability to generate bash script based on python CLI
C:\Users\krozi\PycharmProjects\untitled>2.py complete
usage: 2.py [-h] {commit,tag,list} ...
2.py: error: argument command: invalid choice: 'complete' (choose from 'commit', 'tag', 'list')
 
C:\Users\krozi\PycharmProjects\untitled>1.py complete
_1()
{
local cur prev words
COMPREPLY=()
_get_comp_words_by_ref -n : cur prev words
# Command data:
cmds='commit complete help list tag'
cmds_commit='-h --help --message -m'
cmds_complete='-h --help --name --shell'
cmds_help='-h --help'
cmds_list='-h --help -f --format -c --column --max-width --noindent --quote'
cmds_tag='-h --help --tag -a --message -m'
cmd=""
words[0]=""
completed="${cmds}"
for var in "${words[@]:1}"
do
if [[ ${var} == -* ]] ; then
break
fi
if [ -z "${cmd}" ] ; then
proposed="${var}"
else
proposed="${cmd}_${var}"
fi
local i="cmds_${proposed}"
local comp="${!i}"
if [ -z "${comp}" ] ; then
break
fi
if [[ ${comp} == -* ]] ; then
if [[ ${cur} != -* ]] ; then
completed=""
break
fi
fi
cmd="${proposed}"
completed="${comp}"
done
if [ -z "${completed}" ] ; then
COMPREPLY=( $( compgen -f -- "$cur" ) $( compgen -d -- "$cur" ) )
else
COMPREPLY=( $(compgen -W "${completed}" -- ${cur}) )
fi
return 0
}
complete -F _1 1
 
>>> WOW. amazingly! Cliff provides ability to generate bash script.

What are you choise?
