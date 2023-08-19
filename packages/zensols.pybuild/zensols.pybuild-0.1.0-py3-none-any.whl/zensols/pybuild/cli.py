"""Client entry point for the command line program.

"""
__author__ = 'Paul Landes'

from pathlib import Path
from zensols.cli import OneConfPerActionOptionsCli
from zensols.pybuild import Tag, SetupUtil


# The version of the applicatin
# *Important*: must also be updated in src/python/setup.py
VERSION = '0.1.0'


class Cli(object):
    def __init__(self, setup_path: str = None, output_format: str = None):
        self.setup_path = Path(setup_path)
        self.output_format = output_format

    def write(self):
        sutil = SetupUtil.source(start_path=self.setup_path)
        if self.output_format == 'json':
            sutil.to_json()
        else:
            sutil.write()


# recommended app command line
class ConfAppCommandLine(OneConfPerActionOptionsCli):
    def __init__(self):
        repo_dir_op = ['-r', '--repodir', True,
                       {'dest': 'repo_dir',
                        'metavar': 'DIRECTORY',
                        'default': '.',
                        'help': 'path of the repository'}]
        msg_op = ['-m', '--message', True,
                  {'dest': 'message',
                   'default': 'none',
                   'metavar': 'STRING',
                   'help': 'documentation for the new tag'}]
        cnf = {'executors':
               [{'name': 'tag',
                 'executor': lambda params: Tag(**params),
                 'actions': [{'name': 'last',
                              'meth': 'print_last_tag',
                              'doc': 'Print the last tag',
                              'opts': [repo_dir_op]},
                             {'name': 'info',
                              'meth': 'to_json',
                              'doc': 'give repo version information in JSON',
                              'opts': [repo_dir_op]},
                             {'name': 'create',
                              'doc': 'Create a new tag',
                              'opts': [repo_dir_op, msg_op]},
                             {'name': 'del',
                              'meth': 'delete_last_tag',
                              'doc': 'Delete the tag',
                              'opts': [repo_dir_op]},
                             {'name': 'recreate',
                              'meth': 'recreate_last_tag',
                              'opts': [repo_dir_op]}],
                 'doc': 'Recreate the tag (delete then add)'},
                {'name': 'setup',
                 'executor': lambda params: Cli(**params),
                 'actions': [{'name': 'write',
                              'meth': 'write',
                              'doc': 'print the setup used for setuptools',
                              'opts': [['-s', '--setupapth', True,
                                        {'metavar': 'DIRECTORY',
                                         'dest': 'setup_path',
                                         'default': '.',
                                         'help': 'the path to the setup directory (setup.py)'}],
                                       ['-f', '--format', True,
                                        {'metavar': 'flat|json',
                                         'dest': 'output_format',
                                         'default': 'flat',
                                         'help': 'format used to write the data'}]
                              ]}]}],
               'whine': 1}
        super(ConfAppCommandLine, self).__init__(cnf, version=VERSION)


def main():
    cl = ConfAppCommandLine()
    cl.invoke()
