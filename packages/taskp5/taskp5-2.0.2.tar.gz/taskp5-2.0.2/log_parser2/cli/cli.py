import argparse
import re
import sys
from abc import abstractmethod
from pathlib import Path
from typing import Optional, List

from log_parser2.cli.patterns import SearchPatterns
from log_parser2.log_parser2 import packet_version, logger, LogHandler, Functions


class Argument:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class Group:
    def __init__(self, title, description: str = None,
                 required: bool = False,
                 arguments: List[Argument] = None):
        self.title = title
        self.description = description
        self.required = required
        self.arguments = arguments


class Command:
    def __init__(self, prog_name: str = None,
                 help_epilog: str = None,
                 help_formatter=argparse.RawDescriptionHelpFormatter,
                 base_arg: List[Argument] = None,
                 groups: List[Group] = None,
                 mutually_groups: List[Group] = None,
                 argv: Optional[str] = None) -> None:
        self.argv = argv or sys.argv[:]
        self.prog_name = prog_name if prog_name else Path(self.argv[0]).name

        base_arg = base_arg if base_arg else []
        groups = groups if groups else []
        mutually_groups = mutually_groups if mutually_groups else []

        self.arguments = self.__parse_args(epilog=help_epilog,
                                           formatter=help_formatter,
                                           base_arg=base_arg,
                                           groups=groups,
                                           mutually_groups=mutually_groups)

    def __parse_args(self, epilog, formatter,
                     base_arg: List[Argument],
                     groups: List[Group],
                     mutually_groups: List[Group]) -> argparse.Namespace:
        parser = argparse.ArgumentParser(
            prog=self.prog_name,
            description=f"{self.prog_name} version {packet_version()}",
            epilog=epilog,
            formatter_class=formatter
        )

        [parser.add_argument(*val.args, **val.kwargs) for val in base_arg]

        for grp in groups:
            group = parser.add_argument_group(grp.title, grp.description)
            [group.add_argument(*val.args, **val.kwargs) for val in grp.arguments]

        for mut_grp in mutually_groups:
            group = parser.add_mutually_exclusive_group(required=mut_grp.required)
            [group.add_argument(*val.args, **val.kwargs) for val in mut_grp.arguments]

        return parser.parse_args(self.argv[1:])

    @abstractmethod
    def execute(self) -> None:
        """
        Perform code based on argument values.
        """
        pass


class CommandCLI(Command):
    @property
    def _iterator(self):
        self.__iterator__ += 1
        return self.__iterator__

    @_iterator.setter
    def _iterator(self, value):
        self.__iterator__ = value

    def __check_arguments__(self) -> bool:
        if self.arguments.file_name.name.find('stdin') != -1 and sys.stdin.isatty():
            logger.warning('File has not been passed and stdin is empty. Let\'s finish.')
            return False

        if len(lst := SearchPatterns.group_declarations().findall(self.arguments.extractor)) != len(set(lst)):
            logger.warning('Group name in the extractor must be unique. Let\'s finish.')
            return False

        return True

    def __add_index_to_group__(self, extractor: str) -> str:
        if len(found := SearchPatterns.group_declarations().findall(extractor)) != len(set(found)):
            raise Exception(f'Group name must be unique in {extractor}')

        for group_name in found:
            current_index = self._iterator + 1

            extractor = \
                SearchPatterns.groups(group_name).sub(
                    lambda match: f'{match.group()}_{current_index}',
                    extractor)

            if self.arguments.selection:
                self.arguments.selection = \
                    SearchPatterns.template_groups(group_name).sub(
                        lambda match: f'{match.group()}_{current_index}',
                        self.arguments.selection)

            if self.arguments.aggregation:
                self.arguments.aggregation = \
                    SearchPatterns.template_groups(group_name).sub(
                        lambda match: f'{match.group()}_{current_index}',
                        self.arguments.aggregation)

            if self.arguments.filter:
                self.arguments.filter = \
                    SearchPatterns.template_groups(group_name).sub(
                        lambda match: f'{match.group()}_{current_index}',
                        self.arguments.filter)

        return extractor

    def __sanitize__(self):
        self._iterator = 0

        self.arguments.extractor = self.__add_index_to_group__(self.arguments.extractor)

        find_enum = re.compile("|".join([rf'\b{en.name}\b' for en in SearchPatterns]))

        self.arguments.extractor = \
            find_enum.sub(
                lambda enum_match: self.__add_index_to_group__(
                    fr"""
                    (?P<{enum_match.group()}>
                        {SearchPatterns[enum_match.group()].value}
                    )
                    """
                ),
                self.arguments.extractor)

        logger.debug(f"""1. Enum names has been replaced with enum value
                     2. An occurrence index have been added to regex group definitions
                     (like: ?P<NAME> to ?P<NAME_IDX>) to avoid group definition repeating.
                     3. An occurrence index have been added to regex group usage
                     (like: ?P=NAME to ?P=NAME_IDX) to avoid group definition repeating.
                     
                     Extractor:
                     {self.arguments.extractor}
                     
                     Selection template:
                     {self.arguments.selection}
                     
                     Aggregation template:
                     {self.arguments.aggregation}
                     
                     Filter:
                     {self.arguments.filter}
                     """)

    @staticmethod
    def print_output(output) -> None:

        if not output:
            return

        selection_max_len = len(
            max(output, key=lambda x: len(x[0]))[0]
        )
        selection_max_len = len('Selected') if selection_max_len < len('Selected') else selection_max_len
        selection_max_len = 100 if selection_max_len > 100 else selection_max_len

        aggregation_max_len = len(
            str(
                max(output, key=lambda x: len(str(x[1])))[1]
            )
        )
        aggregation_max_len = len('Aggregated') if aggregation_max_len < len('Aggregated') else aggregation_max_len
        aggregation_max_len = 50 if aggregation_max_len > 50 else aggregation_max_len

        print(f'|-----|-{"-" * selection_max_len}-|-{"-" * aggregation_max_len}-|')

        # noinspection PyUnresolvedReferences, PyStringFormat
        print(f'| {{:^3}} | {f"{{:^{selection_max_len}}}"} | {f"{{:^{aggregation_max_len}}}"} |'
              .format('#', 'Selected', 'Aggregated'))

        print(f'|-----|-{"-" * selection_max_len}-|-{"-" * aggregation_max_len}-|')

        # noinspection PyUnresolvedReferences, PyStringFormat
        [
            print(f'| {{:^3}} | {f"{{:<{selection_max_len}}}"} | {f"{{:>{aggregation_max_len}}}"} |'
                  .format(index + 1, row[0], row[1]))

            for index, row in enumerate(output)
        ]

        print(f'|_____|_{"_" * selection_max_len}_|_{"_" * aggregation_max_len}_|')

    def execute(self) -> None:
        logger.setLevel(self.arguments.v)

        logger.info(f'The log parsing CLI has been launched.')

        logger.debug('Argument values:')
        [logger.debug(f'{arg_name}: {getattr(self.arguments, arg_name)}') for arg_name in vars(self.arguments)]

        if not self.__check_arguments__():
            exit()

        self.__sanitize__()

        handler = LogHandler(log=self.arguments.file_name,
                             extractor=re.compile(self.arguments.extractor, flags=re.I | re.X),
                             selection=self.arguments.selection,
                             aggregation=self.arguments.aggregation,
                             filter_str=self.arguments.filter,
                             rows=self.arguments.rows)

        self.print_output(handler.output)

        self.arguments.file_name.close()


ARGUMENTS = [
    Argument("--version", action="version", version=f"%(prog)s {packet_version()}"),

    Argument('-e', '--extractor',
             dest='extractor',
             metavar='',
             type=str,
             required=True,
             help=rf"""Specify a regular expression for extracting certain data from each log line. 
             The following expression patterns can be used to make writing an expression easier and reduce its size.
             For instance, 
             "IP4\ \((?P<IP4_LIST>(?:(?:IP4|.*?),\ )*)(?:IP4|.*?)\)\ -\ -\ \[DATE_TIME_SEC\]\ \"(?:REQUEST|-)\""

             {', '.join([e.name for e in SearchPatterns])}"""),

    Argument('-s', '--selection',
             dest='selection',
             metavar='',
             type=str,
             help=rf"""Specify a regular expression template to output selected data.
             To add previously extracted data via regular expression groups use template group naming like 
             \g<group_name>. It is allowed to use various transformation functions for substitution, extracting 
             and even splitting data.
             For instance, 
             "TO_MIN(\g<DATE_TIME>) \g<URL>"
             or 
             "SPLIT(RE('(?<=\().+?(?=\))', \g<IP4>), ',\ ')"

             The list of possible functions:
             {', '.join([e.name for e in Functions])}"""),

    Argument('-a', '--aggregation',
             dest='aggregation',
             metavar='',
             type=str,
             help=f"""The aggregate to be calculated during log parsing. It is used for sorting or summation.
             For instance, "MAX(\\g<STATUS>,5)" or .....

             The list of possible functions:
             {', '.join([e.name for e in Functions])}"""),

    Argument('-f', '--filter',
             dest='filter',
             metavar='',
             type=str,
             help=f"""Specify a regular expression for filtering each line. It is supposed to 
             used RE functions and group naming like \\g<group_name>. If the result of using regular expression
             return None the line will be omitted. 
             For instance, "RE('50\\d', \\g<STATUS>)"
             """),

    Argument('-r', '--rows',
             dest='rows',
             nargs='*',
             metavar='INDEXES',
             type=str,
             help="""The row range from the log file to be parsed. 
             You can pass values in the following formats:
             particular indexes: index1 index2 ... indexN
             range of indexes: index1-index2
             from the beginning up to index: -index
             from index to the end: index-"""),

    Argument('-v',
             action='count',
             default=0,
             help='Increase verbosity level (add more v)'),

    Argument('file_name',
             nargs='?',
             type=argparse.FileType('r'),
             default='-',
             help='An input filename'),
]


def parse_cli(argv: Optional[str] = None) -> None:
    # sys.stdout.reconfigure(encoding="utf-8")

    if sys.stdout.encoding is None:
        print(
            "please set python env PYTHONIOENCODING=UTF-8, example: "
            "export PYTHONIOENCODING=UTF-8, when writing to stdout",
            file=sys.stderr,
        )
        exit(1)

    command = CommandCLI('log_parser',
                         base_arg=ARGUMENTS,
                         argv=argv)
    command.execute()


if __name__ == '__main__':
    parse_cli()
