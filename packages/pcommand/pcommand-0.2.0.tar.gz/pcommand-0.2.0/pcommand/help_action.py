# noinspection PyUnresolvedReferences,PyProtectedMember
from argparse import _HelpAction


class HelpAction(_HelpAction):
    # To print only the usage when "-h"
    def __call__(self, parser, namespace, values, option_string=None):
        if option_string == "-h":
            parser.print_usage()
        else:
            parser.print_help()

        parser.exit()
