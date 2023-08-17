import os
import platform
import subprocess
import sys
import time
from typing import Dict, List, Optional, Union

import questionary
import select
from questionary import prompt, Choice

from log_parser2 import logger
from log_parser2.cli import Command, Argument
from log_parser2.log_parser2 import packet_version

if sys.platform.startswith('win32'):
    import msvcrt


class CommandShowcase(Command):
    __intro__ = '''
    ███    ███  ██████  ██████  ██    ██ ██      ███████     ██████         
    ████  ████ ██    ██ ██   ██ ██    ██ ██      ██               ██ ██     
    ██ ████ ██ ██    ██ ██   ██ ██    ██ ██      █████        █████         
    ██  ██  ██ ██    ██ ██   ██ ██    ██ ██      ██          ██      ██     
    ██      ██  ██████  ██████   ██████  ███████ ███████     ███████        
                                                                            
                                                                            
        ██████  ██    ██ ████████ ██   ██  ██████  ███    ██                
        ██   ██  ██  ██     ██    ██   ██ ██    ██ ████   ██                
        ██████    ████      ██    ███████ ██    ██ ██ ██  ██                
        ██         ██       ██    ██   ██ ██    ██ ██  ██ ██                
        ██         ██       ██    ██   ██  ██████  ██   ████                
                                                                            
                                                                            
            ████████  █████  ███████ ██   ██     ██   ██                            
               ██    ██   ██ ██      ██  ██      ██   ██                            
               ██    ███████ ███████ █████       ███████                            
               ██    ██   ██      ██ ██  ██           ██                            
               ██    ██   ██ ███████ ██   ██          ██       
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__command_key_name__ = 'module_command' if self.arguments.as_module else 'command'

    @staticmethod
    def __wait_for_input__(timeout):
        start_time = time.time()
        input_str = ""

        try:
            if sys.platform.startswith('win'):
                while True:
                    if msvcrt.kbhit():
                        char = msvcrt.getwch()
                        if char == '\r':  # Check for Enter key
                            input_str += 'Enter'
                        else:
                            input_str += char
                        break
                    elif time.time() - start_time >= timeout:
                        break
                    time.sleep(0.1)  # Adjust the sleep duration as needed

            else:  # Unix-based systems (Linux, macOS)
                while True:
                    # Check if there is input available to read
                    if sys.stdin in select.select([sys.stdin], [], [], timeout)[0]:
                        char = sys.stdin.read(1)
                        if char == '\n':  # Check for Enter key
                            input_str += 'Enter'
                        else:
                            input_str += char
                        break
                    elif time.time() - start_time >= timeout:
                        break
                    time.sleep(0.1)  # Adjust the sleep duration as needed
        except KeyboardInterrupt:
            exit()

        return input_str.strip()

    # noinspection DuplicatedCode
    def packet_output(self) -> None:
        command_packet = [
            *[
                (val.get('descr', ''),
                 val.get(self.__command_key_name__, '').format(
                     *[
                         arg.get('default', '') if 'filter' not in arg
                         else arg.get('filter', lambda x: '')(arg.get('default', ''))
                         for arg in val['arguments']
                     ]),
                 )
                if 'arguments' in val else val.get(self.__command_key_name__, '')
                for key, val in OPTIONS.items() if val.get(self.__command_key_name__, None)
            ],
            *[
                (o_val.get('descr', ''),
                 o_val.get(self.__command_key_name__, '').format(
                     *[
                         arg.get('default', '') if 'filter' not in arg
                         else arg.get('filter', lambda x: '')(arg.get('default', ''))
                         for arg in o_val['arguments']
                     ]),
                 )
                if 'arguments' in o_val else o_val.get(self.__command_key_name__, '')
                for key, val in OPTIONS.items() if 'options' in val
                for o_key, o_val in val['options'].items() if o_val.get(self.__command_key_name__, None)
            ]
        ]

        [self.__print_output__(el[1], el[0]) for el in command_packet]

    @staticmethod
    def __print_output__(command: str,
                         main_message='According to your choice, the command to be invoked will be:') -> None:

        if not command:
            return

        print(f'\n{main_message}')
        questionary.print(f'{command}', style='#009b06')

        result = subprocess.run(command, capture_output=True, text=True, shell=True)

        if result.stdout and result.stdout.strip():
            print('\nThe output is:')
            questionary.print(f'{result.stdout.strip()}', style='#009b06')

        if result.stderr:
            print('\nThe log messages are:')
            questionary.print(f'{result.stderr}', style='#009b06')

    def execute(self) -> None:
        logger.setLevel(self.arguments.v)

        logger.info(f'The parse_xsv library showcase.')

        logger.debug('Argument values:')
        [logger.debug(f'{arg_name}: {getattr(self.arguments, arg_name)}') for arg_name in vars(self.arguments)]

        if self.arguments.all:
            self.packet_output()
            exit()

        delay = 0.3
        for line in self.__intro__.splitlines():
            print(line)

            if delay and self.__wait_for_input__(delay):
                delay = 0

        time.sleep(3.3 * delay)

        answers = prompt(questions)
        command = ''.join(
            [
                *[
                    o_val.get(self.__command_key_name__, '').format(*[a_val for _, a_val in list(answers.items())[2:]])
                    for key, val in OPTIONS.items() if key == answers.get('category', None) and 'options' in val
                    for o_key, o_val in val['options'].items() if o_key == answers.get(key, None)
                ],
                *[
                    val.get(self.__command_key_name__, '').format(*[a_val for _, a_val in list(answers.items())[1:]])
                    for key, val in OPTIONS.items()
                    if key == answers.get('category', None) and 'arguments' in val and self.__command_key_name__ in val
                ],
            ]
        )

        self.__print_output__(command)


# Determine the platform
current_platform = platform.system()

# Set the Python command based on the platform
if current_platform == 'Windows':
    python_command = 'python -m'
    quoting = r'""'
else:
    python_command = 'python3 -m'
    quoting = r'\"'

select_style = questionary.Style([
    #     ('default', "bg:#ffffff fg:#000000"),
    # ('selected', 'bg:#336699 fg:#ffffff'),
    ('highlighted', '#008888'),
    ('pointer', '#008888'),
    # ('question', 'fg:#009b06'),
    ('qmark', 'fg:#009b06'),
    ('instruction', "#008888"),
    ('answer', "#009b06"),
])

extractor = fr'IP4\ \((?P<IP4_LIST>(?:(?:IP4|.*?),\ )*(?:IP4|.*?))\)' \
            fr'\ -\ -\ \[DATE_TIME_SEC\]\ {quoting}(?:REQUEST|-){quoting}\ (?P<STATUS>\d{{3}})' \
            fr'\ (?P<BYTES>\d+|-)\ (?P<MINUTES>\d+|-)\ (?P<SECONDS>\d+|-)\ {quoting}(?:URL|-|.*?){quoting}' \
            fr'\ {quoting}(?:USER_AGENT|-|.*?){quoting}\ {quoting}(?:URI|-){quoting}'

OPTIONS_ARGUMENTS = {
    'r': {
        'descr': 'r',
        'type': 'text',
        'message': 'Provide row range (row1 row2 ... rowN) (row1-rowN) (from the beginning: -row) (to the end: row-)',
        'default': '1-',
    },
    'e': {
        'descr': 'c',
        'type': 'text',
        'message': 'Specify a regular expression for extracting certain data from a log file',
        'default': f'"{extractor}"',
    },
    's_ip': {
        'descr': 's_intervals',
        'type': 'text',
        'message': 'Please, specify a regular expression template to output selected data',
        'default': r'"\g<IP4_LIST>"',
    },
    'a_ip': {
        'descr': 'a_ip',
        'type': 'text',
        'message': 'Please, specify an aggregation template for sorting or summation',
        'default': r'"MAX(COUNT(\g<IP4_LIST>),20)"',
    },
    's_intervals': {
        'descr': 's_intervals',
        'type': 'text',
        'message': 'Please, specify a regular expression template to output selected data',
        'default': r'"INTERVAL(\g<DATE_TIME_SEC>,%d/%b/%Y:%H:%M:%S %z,5,M)"',
    },
    'a_intervals': {
        'descr': 'a_intervals',
        'type': 'text',
        'message': 'Please, specify an aggregation template for sorting or summation',
        'default': r'"COUNT(INTERVAL(\g<DATE_TIME_SEC>,%d/%b/%Y:%H:%M:%S %z,5,M))"',
    },
    's_agent': {
        'descr': 's_agent',
        'type': 'text',
        'message': 'Please, specify a regular expression template to output selected data',
        'default': r'"\g<AGENT> \g<AGENT_BROWSER>"',
    },
    'a_agent': {
        'descr': 'a_agent',
        'type': 'text',
        'message': 'Please, specify an aggregation template for sorting or summation',
        'default': r'"MAX(COUNT(\g<AGENT> \g<AGENT_BROWSER>),20)"',
    },
    's_500': {
        'descr': 's_500',
        'type': 'text',
        'message': 'Please, specify a regular expression template to output selected data',
        'default': r'"INTERVAL(\g<DATE_TIME_SEC>,%d/%b/%Y:%H:%M:%S %z,5,M) | \g<STATUS>"',
    },
    'a_500': {
        'descr': 'a_500',
        'type': 'text',
        'message': 'Please, specify an aggregation template for sorting or summation',
        'default': r'"COUNT(INTERVAL(\g<DATE_TIME_SEC>,%d/%b/%Y:%H:%M:%S %z,5,M))"',
    },
    'f_500': {
        'descr': 'f_500',
        'type': 'text',
        'message': 'Please, specify a regular expression for filtering each line',
        'default': r'"RE(50\d, \g<STATUS>)"',
    },
    's_seconds': {
        'descr': 's_seconds',
        'type': 'text',
        'message': 'Please, specify a regular expression template to output selected data',
        'default': r'"\g<DATE_TIME_SEC> | \g<REQUEST> | \g<URL> |  \g<SECONDS>"',
    },
    'a_seconds': {
        'descr': 'a_seconds',
        'type': 'text',
        'message': 'Please, specify an aggregation template for sorting or summation',
        'default': r'"MAX(\g<SECONDS>,20)"',
    },
    's_path': {
        'descr': 's_path',
        'type': 'text',
        'message': 'Please, specify a regular expression template to output selected data',
        'default': r'"\g<REQUEST_PATH>"',
    },
    'a_path': {
        'descr': 'a_path',
        'type': 'text',
        'message': 'Please, specify an aggregation template for sorting or summation',
        'default': r'"MAX(COUNT(\g<REQUEST_PATH>),20)"',
    },
    'f_path': {
        'descr': 'f_path',
        'type': 'text',
        'message': 'Please, specify a regular expression for filtering each line',
        'default': r'"RE((?:/+[a-z\d\-._~%&\'()*+,;=:@{\'}{\'}]+){2}, \g<REQUEST_PATH>)"',
    },
    's_workers': {
        'descr': 's_workers',
        'type': 'text',
        'message': 'Please, specify a regular expression template to output selected data',
        'default': r'"\g<URI>"',
    },
    'a_workers': {
        'descr': 'a_workers',
        'type': 'text',
        'message': 'Please, specify an aggregation template for sorting or summation',
        'default': r'"MIN(COUNT(\g<URI>),)"',
    },
    's_url': {
        'descr': 's_url',
        'type': 'text',
        'message': 'Please, specify a regular expression template to output selected data',
        'default': r'"\g<URL_SITE>"',
    },
    'a_url': {
        'descr': 'a_url',
        'type': 'text',
        'message': 'Please, specify an aggregation template for sorting or summation',
        'default': r'"MAX(COUNT(\g<URL_SITE>),20)"',
    },
    's_workers_interval': {
        'descr': 's_workers_interval',
        'type': 'text',
        'message': 'Please, specify a regular expression template to output selected data',
        'default': r'"INTERVAL(\g<DATE_TIME_SEC>,%d/%b/%Y:%H:%M:%S %z,5,M) | \g<URI>"',
    },
    'a_workers_interval': {
        'descr': 'a_workers_interval',
        'type': 'text',
        'message': 'Please, specify an aggregation template for sorting or summation',
        'default': r'"COUNT(INTERVAL(\g<DATE_TIME_SEC>,%d/%b/%Y:%H:%M:%S %z,5,M))"',
    },
    'file': {
        'descr': 'file',
        'type': 'path',
        'message': 'Which log file would you like to parse?',
        'validation': lambda val: True if val else 'Please, provide a path to a file',
        'default': f'{os.path.dirname(os.path.abspath(__file__))}/access.log',
        'filter': lambda val: f'"{val}"' if val else val,
    },
    'v': {
        'descr': 'v',
        'type': 'text',
        'message': 'What logging level would you like to set?',
        'default': '2',
        'validation': lambda val: True if val.isdigit() else 'Please, provide a number',
        'filter': lambda val: f'{"-" if int(val) > 0 else ""}{"v" * (int(val) if int(val) <= 4 else 4)}',
    },
}

# OPTIONS: Dict[str, Dict[str, str | List[Dict] | Dict[str, Dict[str, str | List[Dict]]]]] = {
OPTIONS: Dict[str, Dict[str, Union[str, List[Dict], Dict[str, Dict[str, Union[str, List[Dict]]]]]]] = {
    'ip': {
        'descr': 'ip request statistic',
        'command': f'log_parser -e {{}} -s {{}} -a {{}} -r {{}} {{}} -- {{}}',
        'module_command': f'{python_command} log_parser -e {{}} -s {{}} -a {{}} -r {{}} {{}} -- {{}}',
        'arguments': [OPTIONS_ARGUMENTS['e'], OPTIONS_ARGUMENTS['s_ip'],
                      OPTIONS_ARGUMENTS['a_ip'], OPTIONS_ARGUMENTS['r'],
                      OPTIONS_ARGUMENTS['v'], OPTIONS_ARGUMENTS['file'], ],
    },
    'time_intervals': {
        'descr': 'frequency of requests in time intervals',
        'command': f'log_parser -e {{}} -s {{}} -a {{}} -r {{}} {{}} -- {{}}',
        'module_command': f'{python_command} log_parser -e {{}} -s {{}} -a {{}} -r {{}} {{}} -- {{}}',
        'arguments': [OPTIONS_ARGUMENTS['e'], OPTIONS_ARGUMENTS['s_intervals'],
                      OPTIONS_ARGUMENTS['a_intervals'], OPTIONS_ARGUMENTS['r'],
                      OPTIONS_ARGUMENTS['v'], OPTIONS_ARGUMENTS['file'], ],
    },
    'user_agent': {
        'descr': 'user agent request statistic',
        'command': f'log_parser -e {{}} -s {{}} -a {{}} -r {{}} {{}} -- {{}}',
        'module_command': f'{python_command} log_parser -e {{}} -s {{}} -a {{}} -r {{}} {{}} -- {{}}',
        'arguments': [OPTIONS_ARGUMENTS['e'], OPTIONS_ARGUMENTS['s_agent'],
                      OPTIONS_ARGUMENTS['a_agent'], OPTIONS_ARGUMENTS['r'],
                      OPTIONS_ARGUMENTS['v'], OPTIONS_ARGUMENTS['file'], ],
    },
    'error_500': {
        'descr': 'error code 500 frequency in time intervals',
        'command': f'log_parser -e {{}} -s {{}} -a {{}} -f {{}} -r {{}} {{}} -- {{}}',
        'module_command': f'{python_command} log_parser -e {{}} -s {{}} -a {{}} -f {{}} -r {{}} {{}} -- {{}}',
        'arguments': [OPTIONS_ARGUMENTS['e'], OPTIONS_ARGUMENTS['s_500'],
                      OPTIONS_ARGUMENTS['a_500'], OPTIONS_ARGUMENTS['f_500'],
                      OPTIONS_ARGUMENTS['r'], OPTIONS_ARGUMENTS['v'],
                      OPTIONS_ARGUMENTS['file'], ],
    },
    'request_time': {
        'descr': 'request execution time statistic',
        'command': f'log_parser -e {{}} -s {{}} -a {{}} -r {{}} {{}} -- {{}}',
        'module_command': f'{python_command} log_parser -e {{}} -s {{}} -a {{}} -r {{}} {{}} -- {{}}',
        'arguments': [OPTIONS_ARGUMENTS['e'], OPTIONS_ARGUMENTS['s_seconds'],
                      OPTIONS_ARGUMENTS['a_seconds'], OPTIONS_ARGUMENTS['r'],
                      OPTIONS_ARGUMENTS['v'], OPTIONS_ARGUMENTS['file'], ],
    },
    'request_path': {
        'descr': 'request path statistic',
        'command': f'log_parser -e {{}} -s {{}} -a {{}} -f {{}} -r {{}} {{}} -- {{}}',
        'module_command': f'{python_command} log_parser -e {{}} -s {{}} -a {{}} -f {{}} -r {{}} {{}} -- {{}}',
        'arguments': [OPTIONS_ARGUMENTS['e'], OPTIONS_ARGUMENTS['s_path'],
                      OPTIONS_ARGUMENTS['a_path'], OPTIONS_ARGUMENTS['f_path'],
                      OPTIONS_ARGUMENTS['r'], OPTIONS_ARGUMENTS['v'],
                      OPTIONS_ARGUMENTS['file'], ],
    },
    'workers': {
        'descr': 'worker request statistic',
        'command': f'log_parser -e {{}} -s {{}} -a {{}} -r {{}} {{}} -- {{}}',
        'module_command': f'{python_command} log_parser -e {{}} -s {{}} -a {{}} -r {{}} {{}} -- {{}}',
        'arguments': [OPTIONS_ARGUMENTS['e'], OPTIONS_ARGUMENTS['s_workers'],
                      OPTIONS_ARGUMENTS['a_workers'], OPTIONS_ARGUMENTS['r'],
                      OPTIONS_ARGUMENTS['v'], OPTIONS_ARGUMENTS['file'], ],
    },
    'url_site': {
        'descr': 'url site request statistic',
        'command': f'log_parser -e {{}} -s {{}} -a {{}} -r {{}} {{}} -- {{}}',
        'module_command': f'{python_command} log_parser -e {{}} -s {{}} -a {{}} -r {{}} {{}} -- {{}}',
        'arguments': [OPTIONS_ARGUMENTS['e'], OPTIONS_ARGUMENTS['s_url'],
                      OPTIONS_ARGUMENTS['a_url'], OPTIONS_ARGUMENTS['r'],
                      OPTIONS_ARGUMENTS['v'], OPTIONS_ARGUMENTS['file'], ],
    },
    'workers_interval': {
        'descr': 'worker request time statistic',
        'command': f'log_parser -e {{}} -s {{}} -a {{}} -r {{}} {{}} -- {{}}',
        'module_command': f'{python_command} log_parser -e {{}} -s {{}} -a {{}} -r {{}} {{}} -- {{}}',
        'arguments': [OPTIONS_ARGUMENTS['e'], OPTIONS_ARGUMENTS['s_workers_interval'],
                      OPTIONS_ARGUMENTS['a_workers_interval'], OPTIONS_ARGUMENTS['r'],
                      OPTIONS_ARGUMENTS['v'], OPTIONS_ARGUMENTS['file'], ],
    },
    'time_intervals_sorting': {
        'descr': 'the most/less frequency of requests in time intervals',
        'command': f'log_parser -e {{}} -s {{}} -a {{}} -r {{}} {{}} -- {{}}',
        'module_command': f'{python_command} log_parser -e {{}} -s {{}} -a {{}} -r {{}} {{}} -- {{}}',
        'arguments': [OPTIONS_ARGUMENTS['e'], OPTIONS_ARGUMENTS['s_intervals'],
                      OPTIONS_ARGUMENTS['a_intervals'], OPTIONS_ARGUMENTS['r'],
                      OPTIONS_ARGUMENTS['v'], OPTIONS_ARGUMENTS['file'], ],
    },
}

questions = [
    {
        'type': 'select',
        'name': 'category',
        'message': 'Which log parser category would you like to choose?',
        'choices': [Choice(title=val['descr'], value=key) for key, val in OPTIONS.items()],
        'instruction': '(Use arrow keys to navigate through the menu)',
        'pointer': '>',
        'use_shortcuts': True,
        'style': select_style,
    },
    *[
        {
            'type': 'select',
            'name': key,
            'message': 'Which log parser example would you like to choose?',
            'choices': [Choice(title=o_val['descr'], value=o_key) for o_key, o_val in val['options'].items()],
            'when': lambda x, key=key: x['category'] == key,
            'instruction': '(Use arrow keys to navigate through the menu)',
            'pointer': '>',
            'use_shortcuts': True,
            'style': select_style,
        } for key, val in OPTIONS.items() if 'options' in val
    ],
    *[
        {
            'type': a_val.get('type', 'text'),
            'name': f'{key}_{a_val.get("descr", "")}',
            'message': a_val.get('message', ''),
            'when': lambda x, key=key: x['category'] == key,
            'style': select_style,
            **({'choices': a_val['choices']} if 'choices' in a_val else {}),
            **({'filter': a_val['filter']} if 'filter' in a_val else {}),
            **({'validate': a_val['validation']} if 'validation' in a_val else {}),
            **({'default': a_val['default']} if 'default' in a_val else {}),
        }
        for key, val in OPTIONS.items() if 'options' not in val and 'arguments' in val
        for a_val in val['arguments']
    ],
    *[
        {
            'type': a_val.get('type', 'text'),
            'name': f'{o_key}_{a_val.get("descr", "")}',
            'message': a_val.get('message', ''),
            'when': lambda x, key=key, o_key=o_key: x.get(key, None) == o_key,
            'style': select_style,
            **({'choices': a_val['choices']} if 'choices' in a_val else {}),
            **({'filter': a_val['filter']} if 'filter' in a_val else {}),
            **({'validate': a_val['validation']} if 'validation' in a_val else {}),
            **({'default': a_val['default']} if 'default' in a_val else {}),
        }
        for key, val in OPTIONS.items() if 'options' in val
        for o_key, o_val in val['options'].items() if 'arguments' in o_val
        for a_val in o_val['arguments']
    ],
]

ARGUMENTS = [
    Argument("--version", action="version", version=f"%(prog)s {packet_version()}"),

    Argument('-m', '--module',
             dest='as_module',
             action='store_true',
             help='Invoke log_parser using python -m approach'),

    Argument('--all',
             dest='all',
             action='store_true',
             help='Show all use cases at once without any interaction'),

    Argument('-v',
             action='count',
             default=0,
             help='Increase verbosity level (add more v)'),
]


def parse_showcase(argv: Optional[str] = None):
    # sys.stdout.reconfigure(encoding="utf-8")

    if sys.stdout.encoding is None:
        print(
            "please set python env PYTHONIOENCODING=UTF-8, example: "
            "export PYTHONIOENCODING=UTF-8, when writing to stdout",
            file=sys.stderr,
        )
        exit(1)

    command = CommandShowcase('log_parser showcase',
                              base_arg=ARGUMENTS,
                              argv=argv)
    command.execute()


if __name__ == '__main__':
    parse_showcase()
