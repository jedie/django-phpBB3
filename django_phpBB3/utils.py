# coding: utf-8

"""
    django-phpBB3 utils
    ~~~~~~~~~~~~~~~~~~~
    
    Deentity stuff borrowed from python-creole.

    :copyleft: 2012 by the django-phpBB3 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

import re
import htmlentitydefs as entities

EMAIL_RE = (
    re.compile(r' ?<!-- e --><a href="([^"]*)">(.*?)</a><!-- e --> ?', re.S),
    r' [url=\1]\2[/url] '
)
EMOTICON_RE = (
    re.compile(r' ?<!-- s.*?alt="([^"]*)".*? s\1 --> ?', re.S),
     r' \1 '
)
URL_RE = (
    re.compile(r' ?<!-- [m|w] --><a class="postlink" href="([^"]*)">(.*?)</a><!-- [m|w] --> ?', re.S),
    r' [url=\1]\2[/url] '
)
BBCODE_REPLACES = (EMAIL_RE, EMOTICON_RE, URL_RE)


ENTITIES_REGEX = re.compile(
    '|'.join([
        r"(&\#(?P<number>\d+);)",
        r"(&\#x(?P<hex>[a-fA-F0-9]+);)",
        r"(&(?P<named>[a-zA-Z]+);)",
    ]),
    re.VERBOSE | re.UNICODE | re.MULTILINE
)


class Deentity(object):
    """
    replace html entity

    >>> d = Deentity()
    >>> d.replace_all(u"-=[&nbsp;&gt;&#62;&#x3E;nice&lt;&#60;&#x3C;&nbsp;]=-")
    u'-=[ >>>nice<<< ]=-'
        
    >>> d.replace_all(u"-=[M&uuml;hlheim]=-") # uuml - latin small letter u with diaeresis
    u'-=[M\\xfchlheim]=-'

    >>> d.replace_number(u"126")
    u'~'
    >>> d.replace_hex(u"7E")
    u'~'
    >>> d.replace_named(u"amp")
    u'&'
    """
    def replace_number(self, text):
        """ unicode number entity """
        unicode_no = int(text)
        return unichr(unicode_no)

    def replace_hex(self, text):
        """ hex entity """
        unicode_no = int(text, 16)
        return unichr(unicode_no)

    def replace_named(self, text):
        """ named entity """
        if text == "nbsp":
            # Non breaking spaces is not in htmlentitydefs
            return " "
        else:
            codepoint = entities.name2codepoint[text]
            return unichr(codepoint)

    def replace_all(self, content):
        """ replace all html entities form the given text. """
        def replace_entity(match):
            groups = match.groupdict()
            for name, text in groups.items():
                if text is not None:
                    replace_method = getattr(self, 'replace_%s' % name)
                    return replace_method(text)

            # Should never happen:
            raise RuntimeError("deentitfy re rules wrong!")

        return ENTITIES_REGEX.sub(replace_entity, content)

deentity = Deentity()


def phpbb_html2bbcode(text):
    """
    >>> phpbb_html2bbcode('DjangoBB <!-- m --><a class="postlink" href="http://djangobb.org/">trac</a><!-- m --> page.')
    'DjangoBB [url=http://djangobb.org/]trac[/url] page.'
    """
    for regex, replace_by in BBCODE_REPLACES:
        text = regex.sub(replace_by, text)
    return text


def clean_bbcode(text, bbcode_uid=None):
    """
    >>> clean_bbcode('DjangoBB <!-- m --><a class="postlink" href="http://djangobb.org/">trac</a><!-- m --> page.')
    'DjangoBB [url=http://djangobb.org/]trac[/url] page.'
    
    >>> clean_bbcode(
    ...     u'Look at [url=https&#58;//github&#46;com/jedie/PyLucid/views&#46;py:1234abcd]/views.py[/url:1234abcd]',
    ...     bbcode_uid=u"1234abcd"
    ... )
    u'Look at [url=https://github.com/jedie/PyLucid/views.py]/views.py[/url]'
    """
    if bbcode_uid is not None:
        text = text.replace(":%s" % bbcode_uid, "")

    text = deentity.replace_all(text)

    return phpbb_html2bbcode(text)


if __name__ == "__main__":
    import doctest
    print doctest.testmod()
