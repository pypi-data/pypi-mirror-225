import collections
import json
import logging.config
import re
from collections import Counter
from datetime import datetime, timedelta
from enum import Enum
from typing import Pattern, List, Match, Optional, Tuple, TextIO

from log_parser2.__version__ import __version__

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s | %(name)s:%(process)d:%(lineno)d | %(levelname)s | %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'handlers': {
        'verbose': {
            'formatter': 'simple',
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        __name__: {
            'level': 'ERROR',
            'handlers': [
                'verbose',
            ],
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)


class LoggerMeta(type):
    _logger: logging.Logger = logging.getLogger(__name__)

    def __getattr__(cls, name):
        return getattr(cls._logger, name)


# noinspection PyPep8Naming
class logger(metaclass=LoggerMeta):
    @classmethod
    def setLevel(cls, level: int) -> None:
        if level == 1:
            cls._logger.setLevel(logging.WARNING)
            cls._logger.handlers[0].setLevel(logging.WARNING)
        elif level == 2:
            cls._logger.setLevel(logging.INFO)
            cls._logger.handlers[0].setLevel(logging.INFO)
        elif level == 3:
            cls._logger.setLevel(logging.DEBUG)
            cls._logger.handlers[0].setLevel(logging.DEBUG)
        elif level == 4:
            cls._logger.setLevel(5)
            cls._logger.handlers[0].setLevel(5)

    @classmethod
    def trace(cls, *args, **kwargs):
        cls._logger.log(5, *args, **kwargs)


class Functions(Enum):
    # noinspection PyPep8Naming
    class __Helper__:
        __func_def__ = r'(?P<FUNC>{func_name})\('
        __argument__ = r'\ *(?P<ARG{id}>{argument})\ *'

        __interval_types__ = {
            'S': 'second',
            'M': 'minute',
            'H': 'hour',
            'Y': 'year'
        }

        __interval_arguments__ = {
            'S': '{{"second{s}": {val}}}',
            'M': '{{"minute{s}": {val}, "second{s}": 0}}',
            'H': '{{"hour{s}": {val}, "minute{s}": 0, "second{s}": 0}}',
            'Y': '{{"year{s}": {val}, "hour{s}": 0, "minute{s}": 0, "second{s}": 0}}'
        }

        @classmethod
        def get_func_def(cls, name: str):
            return cls.__func_def__.format(func_name=name)

        @classmethod
        def get_argument(cls,
                         number: int,
                         is_digit: bool = False,
                         eager: bool = False,
                         optional: bool = False,
                         last: bool = False,
                         expression: str = None):

            argument = r'\d' if is_digit else r'.'
            argument = rf'{argument}*{r"?" if eager else ""}\ *' if optional and not expression \
                else rf'{argument}+{r"?" if eager else ""}\ *'
            argument = expression if expression else argument

            return cls.__argument__.format(id=number,
                                           argument=argument) + (r'\)' if last else r',')

        @staticmethod
        def __prepare_aggregator__(is_sum: bool = False, **kwargs) -> Counter:
            # noinspection PyBroadException
            try:
                arg = kwargs['ARG1']
                arg = arg if type(arg) is dict else {arg: int(arg) if is_sum and arg.isdigit() else 1}

                return Counter(arg)
            except Exception as _:
                return Counter()

        @classmethod
        def sum(cls, **kwargs) -> Counter:
            return cls.__prepare_aggregator__(is_sum=True, **kwargs)

        @classmethod
        def count(cls, **kwargs) -> Counter:
            return cls.__prepare_aggregator__(is_sum=False, **kwargs)

        @classmethod
        def max(cls, **kwargs):
            return kwargs['ARG1']

        @classmethod
        def min(cls, **kwargs):
            return kwargs['ARG1']

        @classmethod
        def interval(cls, **kwargs) -> str:
            date = datetime.strptime(kwargs['ARG1'], kwargs['ARG2'])

            interval_name = cls.__interval_types__[kwargs['ARG4']]

            round_part = getattr(date, interval_name)
            round_value = round_part - (round_part % int(kwargs['ARG3']))

            to_start = json.loads(cls.__interval_arguments__[kwargs['ARG4']]
                                  .format(s='', val=round_part))
            date = date.replace(**to_start)

            delta_args = json.loads(cls.__interval_arguments__[kwargs['ARG4']]
                                    .format(s='s', val=round_part - round_value))

            return str(date - timedelta(**delta_args))

        @staticmethod
        def re(**kwargs) -> str:
            try:
                return re.compile(kwargs['ARG1']).search(kwargs['ARG2']).group()
            except (re.error, AttributeError) as _:
                return ''

        @staticmethod
        def split(**kwargs) -> List:
            return kwargs['ARG1'].split(kwargs['ARG2'])

        @staticmethod
        def __aggregation__(data: List) -> List:
            dct = collections.defaultdict(Counter)
            for k, v in data:
                dct[k] += v

            return list(dct.items())

        @classmethod
        def count_aggregation(cls, data: List, **_) -> List:
            return cls.__aggregation__(data)

        @classmethod
        def sum_aggregation(cls, data: List, **_) -> List:
            return cls.__aggregation__(data)

        @staticmethod
        def __sorting__(data: List, reverse_order: bool = False, **kwargs) -> List:
            arg1 = kwargs.get('ARG1', None)
            arg1 = arg1 if arg1 and type(arg1) is list else data

            arg2 = kwargs.get('ARG2', None)
            arg2 = int(arg2) if arg2 and arg2.strip().isdigit() else None

            return sorted(arg1,
                          key=lambda x: list(x[1].items())[0][1] if type(x[1]) is Counter
                          else int(x[1]) if x[1].strip().isdigit() else x[1],

                          reverse=reverse_order
                          )[:arg2]

        @classmethod
        def max_aggregation(cls, data: List, **kwargs) -> List:
            return cls.__sorting__(data, reverse_order=True, **kwargs)

        @classmethod
        def min_aggregation(cls, data: List, **kwargs) -> List:
            return cls.__sorting__(data, reverse_order=False, **kwargs)

    MIN = \
        rf'{__Helper__.get_func_def("MIN")}' \
        rf'{__Helper__.get_argument(1)}' \
        rf'{__Helper__.get_argument(2, optional=True, is_digit=True, last=True)}'

    MAX = \
        rf'{__Helper__.get_func_def("MAX")}' \
        rf'{__Helper__.get_argument(1)}' \
        rf'{__Helper__.get_argument(2, optional=True, is_digit=True, last=True)}'

    SPLIT = \
        rf'{__Helper__.get_func_def("SPLIT")}' \
        rf'{__Helper__.get_argument(1, eager=True)}' \
        rf'{__Helper__.get_argument(2, last=True)}'

    SUB = \
        rf'{__Helper__.get_func_def("SUB")}' \
        rf'{__Helper__.get_argument(1)}' \
        rf'{__Helper__.get_argument(2)}' \
        rf'{__Helper__.get_argument(3, last=True)}'

    INTERVAL = \
        rf'{__Helper__.get_func_def("INTERVAL")}' \
        rf'{__Helper__.get_argument(1)}' \
        rf'{__Helper__.get_argument(2)}' \
        rf'{__Helper__.get_argument(3, is_digit=True)}' \
        rf'{__Helper__.get_argument(4, last=True, expression=r"S|M|H|D")}'

    SUM = \
        rf'{__Helper__.get_func_def("SUM")}' \
        rf'{__Helper__.get_argument(1, last=True)}'

    COUNT = \
        rf'{__Helper__.get_func_def("COUNT")}' \
        rf'{__Helper__.get_argument(1, last=True)}'

    RE = \
        rf'{__Helper__.get_func_def("RE")}' \
        rf'{__Helper__.get_argument(1)}' \
        rf'{__Helper__.get_argument(2, last=True)}'

    @classmethod
    def evaluate(cls, expression: str, matcher: Match[str]) -> Optional[str]:
        search_result = None
        for f in cls:
            # noinspection RegExpRedundantEscape
            search_result = re.compile(r'^\ *' + f.value, flags=re.I).search(expression)

            if search_result:
                break

        if not search_result:
            try:
                sanitized_template = re.compile(r'\\(?=[^g])').sub(
                    lambda match: r'\\',
                    expression
                )
                return matcher.expand(sanitized_template)
            except re.error as _:
                return expression

        arguments = {key: cls.evaluate(val, matcher)
                     for key, val in search_result.groupdict().items()
                     if re.compile(r'ARG\d+').search(key)}

        return getattr(cls.__Helper__, search_result['FUNC'].lower())(**arguments)

    @classmethod
    def evaluate_expression(cls, expression: str, matcher: Match[str]) -> str:
        for f in [fnc for fnc in cls if fnc not in [cls.MIN, cls.MAX, cls.SUM, cls.COUNT]]:
            # if f == cls.SPLIT:
            #     # noinspection RegExpRedundantEscape
            #     spl_list = re.compile(r'(?<![^\\]\()\ *' + f.value, flags=re.I).findall(expression)
            #     expressions = [cls.evaluate(spl, matcher) for spl in spl_list]
            #
            #     for ind in range(0, len(expressions)):
            #         # noinspection RegExpRedundantEscape
            #         expressions[ind] = re.compile(r'(?<![^\\]\()\ *' + f.value, flags=re.I).sub(
            #             lambda match: cls.evaluate(match.group(), matcher),
            #             expression)

            # noinspection RegExpRedundantEscape
            expression = re.compile(r'(?<![^\\]\()\ *' + f.value, flags=re.I).sub(
                lambda match: cls.evaluate(match.group(), matcher),
                expression)

        return cls.evaluate(expression, matcher)

    @classmethod
    def aggregate(cls, expression: str, data: List):
        for f in [cls.MIN, cls.MAX, cls.COUNT, cls.SUM]:
            # noinspection RegExpRedundantEscape
            search_result = re.compile(r'^\ *' + f.value, flags=re.I).search(expression)

            if search_result:
                break

        if search_result:
            arguments = {key: cls.aggregate(val, data)
                         for key, val in search_result.groupdict().items()
                         if re.compile(r'ARG\d+').search(key)}

            return getattr(cls.__Helper__, f'{search_result["FUNC"].lower()}_aggregation')(data, **arguments)

        return expression


class LogHandler:
    def __init__(self,
                 log: TextIO,
                 extractor: Pattern[str],
                 selection: str,
                 aggregation: str = '',
                 filter_str: str = '',
                 rows: List[str] = None):

        self.rows = self.__parse_row_list__(rows if rows else [])
        self.output: List[Tuple] = []

        self._parse_log_(log,
                         extractor,
                         selection if selection else '',
                         aggregation if aggregation else '',
                         filter_str if filter_str else r'.*')

    @staticmethod
    def __parse_row_list__(rows: List[str]) -> List[Tuple]:
        return \
            [(
                int(lst[0]) if lst[0] else 1,
                (int(lst[1]) if lst[1] else 'MAX') if len(lst) > 1 else None,
            )
             for el in rows for lst in [el.split('-')]]

    def __in_rows__(self, index: int) -> bool:
        return \
            any([row_tuple for row_tuple in self.rows
                 if (index == row_tuple[0] and not row_tuple[1]) or (index >= row_tuple[0] and row_tuple[1] and
                                                                     (row_tuple[1] == 'MAX' or index <= row_tuple[1]))
                 ])

    def _parse_log_(self, log: TextIO,
                    extractor: Pattern[str],
                    selection: str,
                    aggregation: str = None,
                    filter_str: str = ''):

        error_lines_num = 0
        proceeded_lines = 0
        log_lines_count = 0
        filtered_out_count = 0
        omitted_count = 0
        no_selection_count = 0

        logger.info(f"""Let\'s start log parsing.""")
        logger.debug("""Parameters:
        Extractor: """ + extractor.pattern + f"""
        Selection: {selection}
        Aggregation: {aggregation}
        Filter: {filter_str}
        Rows: {self.rows}
        """)

        for row_num, row in enumerate(log):
            log_lines_count = row_num + 1

            if self.rows and not self.__in_rows__(row_num + 1):
                logger.debug(f'The line #{row_num + 1} has been omitted due to row limitation {self.rows}: {row}')
                omitted_count += 1
                continue

            parsed_result = extractor.search(row)

            if not parsed_result:
                logger.debug(f'Can\'t parse line #{row_num + 1}: {row}')
                error_lines_num += 1
                continue

            if not Functions.evaluate(filter_str, parsed_result):
                logger.debug(f'The line #{row_num + 1} has been filtered out: {row}')
                filtered_out_count += 1
                continue

            if not (select := Functions.evaluate_expression(selection, parsed_result)).strip():
                logger.debug(f'Empty selection in line #{row_num + 1}: {row}')
                no_selection_count += 1
                continue

            self.output += [(select,
                             Functions.evaluate(aggregation, parsed_result))]

            proceeded_lines += 1
            logger.trace(f'The row #{row_num + 1} has been parsed: {row}'
                         + '\n'.join([f'{key}: {val}' for key, val in parsed_result.groupdict().items()]))
            logger.debug(f'Parsed data (#{row_num + 1}): {parsed_result.group()}')

        self.output = out if (out := Functions.aggregate(aggregation, self.output)) else self.output

        logger.info(f'{proceeded_lines} lines have been parsed.')
        logger.info(f'{error_lines_num} lines haven\'t been parsed.')
        logger.info(f'{no_selection_count} lines with empty selection.')
        logger.info(f'{filtered_out_count} lines have been filtered out.')
        logger.info(f'{omitted_count} lines have been omitted due to row limitation.')
        logger.info(f'Total lines count: {log_lines_count}')

        logger.debug(f"""The output:""" + '\n' + '\n'.join([str(el) for el in self.output]))

        self.output = [(el[0],
                        list(el[1].values())[0] if type(el[1]) is Counter else el[1],
                        )
                       for el in self.output]

        logger.debug(f"""The output:""" + '\n' + '\n'.join([str(el) for el in self.output]))


def packet_version() -> str:
    return __version__
