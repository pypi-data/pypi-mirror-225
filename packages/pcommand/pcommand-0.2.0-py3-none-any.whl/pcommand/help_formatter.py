import re
from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter

from pcommand import SubParsersAction


# noinspection PyProtectedMember
class HelpFormatter(ArgumentDefaultsHelpFormatter):
    def _format_action_invocation(self, action):
        # Override to hide subparsers group help
        if isinstance(action, SubParsersAction):
            return SUPPRESS
        return super(HelpFormatter, self)._format_action_invocation(action)

    def _join_parts(self, part_strings):
        # Override to format the help
        def sanitize(part):
            if SUPPRESS in part:
                part = re.sub(rf" *{SUPPRESS} *", "", part)
                if not part.strip():
                    part = part.strip()
            # Change the help from "--kwargs [KWARGS ...]" to "--kwargs KWARGS ...
            var_keywords_regex = r"--(\w+) \[(\w+) \.\.\.\]"
            var_keywords = re.search(var_keywords_regex, part)
            if var_keywords:
                option_string, metavar = var_keywords.groups()
                part = re.sub(var_keywords_regex, f"--{option_string} {metavar} ...", part)

            # Remove the "..." from the end of the line
            part = re.sub(r" \.\.\.\n", "", part)
            return part

        part_strings = map(sanitize, part_strings)
        resp = super(HelpFormatter, self)._join_parts(part_strings)
        return resp

    def _metavar_formatter(self, action, default_metavar):
        # Override to hide the "{}" when there is no choices
        result = default_metavar
        if action.metavar is not None:
            result = action.metavar
        elif action.choices is not None:
            choice_strs = [str(choice) for choice in action.choices]
            if choice_strs:
                result = '{%s}' % ','.join(choice_strs)

        # noinspection PyShadowingBuiltins
        def format(tuple_size):
            if isinstance(result, tuple):
                return result
            else:
                return (result,) * tuple_size

        return format
