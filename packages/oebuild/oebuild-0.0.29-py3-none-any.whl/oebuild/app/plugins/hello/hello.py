import argparse
import textwrap
import logging

from oebuild.command import OebuildCommand
from oebuild.util import *
from oebuild.configure import Configure

logger = logging.getLogger()

class Hello(OebuildCommand):

    def __init__(self):
        self.configure = Configure()
        super().__init__(
            'hello',
            'this is your hello mesasge',
            textwrap.dedent('''\
            this is hello description
'''
        ))

    def do_add_parser(self, parser_adder) -> argparse.ArgumentParser:
        parser = self._parser(
            parser_adder,
            usage='''

  %(prog)s [-x xxx]

''')

        return parser

    def do_run(self, args: argparse.Namespace, unknown = None):
        args = args.parse_args(unknown)

        # this is your function code
        print("hello world")
