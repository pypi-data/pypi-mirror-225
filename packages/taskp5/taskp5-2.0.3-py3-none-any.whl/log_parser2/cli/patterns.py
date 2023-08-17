import re
from enum import Enum
from typing import List, Pattern


class SearchPatterns(Enum):

    IP4_OCTET = \
        r'25[0-5]|2[0-4]\d|[01]?\d\d?'

    MASK_OCTET = \
        r'0{1,3}|128|192|224|24[08]|25[245]'

    IP4 = \
        fr"""
        (?= 
            (?P<IP4_PRIVATE> 10|010|192.168|172.16|172.016)
            | (?P<IP4_PUBLIC>
                (?:{IP4_OCTET})\.
                (?:{IP4_OCTET})\.
                (?:{IP4_OCTET})\.
                (?:{IP4_OCTET})
              )
            | (?P<IP4_MASK>
                (?: (?:{MASK_OCTET})\.){{3}}
                (?:{MASK_OCTET})
              )
        )
        (?P<IP4_OCTET_1>{IP4_OCTET})\.
        (?P<IP4_OCTET_2>{IP4_OCTET})\.
        (?P<IP4_OCTET_3>{IP4_OCTET})\.
        (?P<IP4_OCTET_4>{IP4_OCTET})
        """

    IP4_CIDR = \
        fr"""
        (P<IP4>{IP4})
        /(?P<IP4_MASK> \d|[12]\d|3[0-2])
        """

    MASK = \
        fr"""
        (?: (?:{MASK_OCTET})\.){{3}}
        (?:{MASK_OCTET})
        """

    IP6 = \
        r"""
        (?=
            (?<IP6_PRIVATE> F[CD])
            | (?P<IP6_PUBLIC>
                (?:[A-F\d]{1,4}:){7}[A-F\d]{1,4}
                | (?:[\dA-F]{1,4}:){1,6}(?::[\dA-F]{1,4}){1,6}
                | (?:[A-F\d]{1,4}:){1,7}:
                | :(?::[A-F\d]{1,4}){1,7}              
              )
        )
        (?P<IP6_CANONICAL> (?:[A-F\d]{1,4}:){7}[A-F\d]{1,4} )
        | (?P<IP6_OMITTED_MIDDLE> (?:[\dA-F]{1,4}:){1,6}(?::[\dA-F]{1,4}){1,6} )
        | (?P<IP6_OMITTED_END> (?:[A-F\d]{1,4}:){1,7}: )
        | (?P<IP6_OMITTED_START> :(?::[A-F\d]{1,4}){1,7} )
        """

    IP6_CIDR = \
        fr"""
        (P<IP6>{IP6})
        /(?P<IP6_MASK> 12[0-8]|1[0-1]\d|\d\d|\d)
        """

    MAC_PART = \
        r'[A-Z\d]{2}'

    MAC = \
        fr"""
        {MAC_PART}
        (?<MAC_DELIMITER> 
            (?P<MAC_LINUX_DELIMITER>-)
            | (?P<MAC_WINDOWS_DELIMITER>:)
            | (?P<MAC_CISCO_DELIMITER>.)
        )
        (?: {MAC_PART}(?P=MAC_DELIMITER) ){{4}}
        {MAC_PART}
        """

    VERSION = \
        r'\d+(?:\.\d+)*(?![.\d])'

    AGENT_AGENT = \
        rf'Mozilla/(?P<AGENT_VER>{VERSION})'

    AGENT_OS = \
        rf"""
        (?P<AGENT_OS_WIN> Windows[\ ]\w+[\ ](?P<AGENT_WIN_VER>{VERSION}))
        | (?P<AGENT_OS_LINUX> Linux(?:[\ ](?:i686|x86_64))?)
        | (?P<AGENT_OS_MAC> Macintosh)
        | (?P<AGENT_OS_IOS> (?:CPU[\ ])?iPhone[\ ]OS|CPU[\ ]OS.*?like[\ ]Mac[\ ]OS[\ ]X)
        """

    AGENT_DEVICE = \
        rf"""
        (?P<AGENT_DEVICE_IOS> iPhone|iPad)
        | (?P<AGENT_DEVICE_FIREFOX> Mobile)
        | (?P<AGENT_DEVICE_ANDROID> Android(?:[\ ](P<AGENT_ANDROID_VER>{VERSION}))?)
        """

    AGENT_BROWSER = \
        rf"""
        (?:
            (?P<AGENT_BROWSER_IE> MSIE)
            | (?P<AGENT_BROWSER_SAFARI> (?:Mobile[\ ])?Safari)
            | (?P<AGENT_BROWSER_CHROME> Chrome)
            | (?P<AGENT_BROWSER_CHROMIUM> \b\w+\b[\ ]Chromium)
            | (?P<AGENT_BROWSER_FIREFOX> Firefox)
            | (?P<AGENT_BROWSER_VERSION> Version)
            | (?P<AGENT_BROWSER_MOBILE> Mobile)
            | (?P<AGENT_BROWSER_GSA> GSA)
            | (?P<AGENT_BROWSER_QUICKLOOK> QuickLook)
            | (?P<AGENT_BROWSER_OPERA> OPR)
        )
        [\ /]
        (?: [A-Z\d]+\b(?!\.) | (?P<AGENT_BROWSER_VER>{VERSION}) )
        """

    USER_AGENT = \
        rf"""
        (?: 
            .*?(?P<AGENT>{AGENT_AGENT})
        )
        (?: 
            .*?(?P<AGENT_OS>{AGENT_OS})
        )
        (?: 
            .*?(?P<AGENT_DEVICE>{AGENT_DEVICE})
        )?
        (?: 
            .*?(?P<AGENT_BROWSER>{AGENT_BROWSER})
        )?
        """
    # .*?(?P<BROWSER>{AGENT_BROWSER}(?:[\ ]{AGENT_BROWSER})* )

    DOMAIN = \
        r'(?P<TLD> \*?\.[a-z\d-]+)+'

    EMAIL_NAME_CHARSET = \
        r'[\w!#$%&''*+/=?`{|}~^-]+'

    EMAIL = \
        fr"""
        (?P<EMAIL_NAME>
            {EMAIL_NAME_CHARSET}
            (?: \.{EMAIL_NAME_CHARSET})*\
        )
        @
        (?P<EMAIL_DOMAIN> (?: [A-Z\d-]+\.)+[A-Z]{{2,6}} )
        """

    URI = \
        r"""
        (?P<URI_SCHEME> ([a-z][a-z\d+\-.]*:)+ )
        /{0,3}
        (?P<URI_USER> [a-z\d\-._~%!$&\'()*+,:;=]+ @ )?
        (?P<URI_ADDRESS> 
            (
                (?P<URI_IPV6_HOST>\[[a-f\d:.]+])
                | [a-z\d-]+
                  (?P<URI_TLD>\.[a-z\d-]+)+
                  (?P<URI_PORT>:\d+)?
            )
            | (?P<URI_DIGIT_ADDRESS> [\d\-+]+ )
        )
        (?P<URI_PATH> (?: /[a-z\d\-._~%!$&\'()*+,;=:@}{]+ )*/? )
        (?P<URI_QUESTION_QUERY> \?[a-z\d\-._~%!$&\'()*+,;=:@/?]* )?
        (?P<URI_HASH_QUERY> \#[a-z\d\-._~%!$&\'()*+,;=:@/?]* )?
        """

    URL = \
        r"""
        (?P<URL_PROTOCOL> https? | ftp | file )
        :/{2,3}
        (?P<URL_USER> [a-z\d\-._~%!$&\'()*+,:;=]+ @ )?
        (?P<URL_SITE>
            (?P<URL_WWW_FTP> www|ftp )?
            \.?
            [a-z\d-]+
            (?P<URL_TLD> \.[a-z0-9-]+ )+
        )
        (?P<URL_PORT> :\d+ )?
        (?P<URL_PATH> (?: /[a-z\d\-._~%!$&\'()*+,;=:@}{]+ )*/? )
        (?P<URL_QUESTION_QUERY> \?[a-z\d\-._~%!$&\'()*+,;=:@/?]* )?
        (?P<URL_HASH_QUERY> \#[a-z\d\-._~%!$&\'()*+,;=:@/?]* )?
        """

    REQUEST_TYPES = \
        r'GET | POST | HEAD | PUT | DELETE | CONNECT | OPTIONS | TRACE | PATCH'

    REQUEST = \
        fr"""
        (?P<REQUEST_TYPE> {REQUEST_TYPES})
        [\ ]
        (?P<REQUEST_PATH> (?: /+[a-z\d\-._~%!$&\'()*+,;=:@{'}{'}]+ )* /? )
        (?P<REQUEST_QUESTION_QUERY> \?[a-z\d\-._~%!$&\'()*+,;=:@/?]* )?
        (?P<REQUEST_HASH_QUERY> \#[a-z\d\-._~%!$&\'()*+,;=:@/?]* )?
        [\ ]
        (?P<REQUEST_PROTOCOL> HTTPS?/(?P<REQUEST_VER>{VERSION}) )
        """

    DATE_TIME_SEC = \
        r"""
        (?P<DATE> 
            \d{4}-\d{2}-\d{2} 
            | \d{2}[:/-](?:\d{2}|\w+)[:/-]\d{4} 
        )
        [:T\ ]
        (?P<TIME>
            \d{2}:\d{2}:\d{2}(?:\.\d+)?
        )
        [\ ]? [+-]?
        (?P<SECONDS> 
            Z 
            | \d{2}[:\ ]?\d{2}
        )?
        """

    UUID = \
        r"""
        [A-F\d]{8}
        -
        (?: [A-F\d]{4}-){3}
        -
        [A-F\d]{12}
        """

    __group_declarations__ = r'(?<=[^\\]\?P<){group_name}(?=>)'

    __group_usage__ = r'(?<=[^\\]\?P=){group_name}(?=\ *\))'

    __template_group__ = r'(?<=\\g<){group_name}(?=>)'

    @classmethod
    def get_pattern_groups(cls) -> List[str]:
        return [el for expr in cls
                for el in cls.group_declarations().findall(expr.value)]

    @classmethod
    def group_declarations(cls, group_name: str = None) -> Pattern[str]:
        # noinspection PyUnresolvedReferences
        return re.compile(cls.__group_declarations__.format(group_name=group_name if group_name else r'.+?'))

    @classmethod
    def group_usage(cls, group_name: str = None) -> Pattern[str]:
        # noinspection PyUnresolvedReferences
        return re.compile(cls.__group_usage__.format(group_name=group_name if group_name else r'.+?'))

    @classmethod
    def groups(cls, group_name: str = None) -> Pattern[str]:
        # noinspection PyUnresolvedReferences
        return re.compile((cls.__group_declarations__ + '|' + cls.__group_usage__)
                          .format(group_name=group_name if group_name else r'.+?'))

    @classmethod
    def template_groups(cls, group_name: str = None) -> Pattern[str]:
        # noinspection PyUnresolvedReferences
        return re.compile(cls.__template_group__.format(group_name=group_name if group_name else r'.+?'))
