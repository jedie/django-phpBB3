# coding: utf-8

"""
    django-phpBB3 utils
    ~~~~~~~~~~~~~~~~~~~

    Deentity stuff borrowed from python-creole.

    :copyleft: 2012 by the django-phpBB3 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

import htmlentitydefs as entities
import re
import time

from django.utils.encoding import force_unicode


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
        if text == u"nbsp":
            # Non breaking spaces is not in htmlentitydefs
            return u" "
        else:
            try:
                codepoint = entities.name2codepoint[text]
            except KeyError:
                return text
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
    >>> phpbb_html2bbcode(u'DjangoBB <!-- m --><a class="postlink" href="http://djangobb.org/">trac</a><!-- m --> page.')
    u'DjangoBB [url=http://djangobb.org/]trac[/url] page.'
    """
    for regex, replace_by in BBCODE_REPLACES:
        text = regex.sub(replace_by, text)
    return text


def clean_bbcode(text, bbcode_uid=None):
    """
    >>> clean_bbcode('DjangoBB <!-- m --><a class="postlink" href="http://djangobb.org/">trac</a><!-- m --> page.')
    u'DjangoBB [url=http://djangobb.org/]trac[/url] page.'

    >>> clean_bbcode(
    ...     u'Look at [url=https&#58;//github&#46;com/jedie/PyLucid/views&#46;py:1234abcd]/views.py[/url:1234abcd]',
    ...     bbcode_uid=u"1234abcd"
    ... )
    u'Look at [url=https://github.com/jedie/PyLucid/views.py]/views.py[/url]'
    
    >>> clean_bbcode(
    ...     u"[code:1234abcd]What's &broken; hey?[/code:1234abcd]",
    ...     bbcode_uid=u"1234abcd"
    ... )
    u"[code]What's broken hey?[/code]"
    """
    text = force_unicode(text)

    if bbcode_uid is not None:
        text = text.replace(u":%s" % bbcode_uid, u"")

    text = deentity.replace_all(text)

    return phpbb_html2bbcode(text)


def human_duration(t):
    """
    Converts a time duration into a friendly text representation.

    >>> human_duration("type error")
    Traceback (most recent call last):
        ...
    TypeError: human_duration() argument must be integer or float

    >>> human_duration(0.01)
    u'10.0 ms'
    >>> human_duration(0.9)
    u'900.0 ms'
    >>> human_duration(65.5)
    u'1.1 min'
    >>> human_duration((60 * 60)-1)
    u'59.0 min'
    >>> human_duration(60*60)
    u'1.0 hours'
    >>> human_duration(1.05*60*60)
    u'1.1 hours'
    >>> human_duration(2.54 * 60 * 60 * 24 * 365)
    u'2.5 years'
    """
    if not isinstance(t, (int, float)):
        raise TypeError("human_duration() argument must be integer or float")

    chunks = (
      (60 * 60 * 24 * 365, u'years'),
      (60 * 60 * 24 * 30, u'months'),
      (60 * 60 * 24 * 7, u'weeks'),
      (60 * 60 * 24, u'days'),
      (60 * 60, u'hours'),
    )

    if t < 1:
        return u"%.1f ms" % round(t * 1000, 1)
    if t < 60:
        return u"%.1f sec" % round(t, 1)
    if t < 60 * 60:
        return u"%.1f min" % round(t / 60, 1)

    for seconds, name in chunks:
        count = t / seconds
        if count >= 1:
            count = round(count, 1)
            break
    return u"%(number).1f %(type)s" % {'number': count, 'type': name}


class ProcessInfo(object):
    """
    >>> p = ProcessInfo(100)
    >>> p.update(1)[0]
    99
    >>> p = ProcessInfo(100)
    >>> p.update(0)
    (100, u'-', 0.0)
    """
    def __init__(self, total, use_last_rates=4):
        self.total = total
        self.use_last_rates = use_last_rates
        self.last_count = 0
        self.last_update = self.start_time = time.time()
        self.rate_info = []

    def update(self, count):
        current_duration = time.time() - self.last_update
        current_rate = float(count) / current_duration
        self.rate_info.append(current_rate)
        self.rate_info = self.rate_info[-self.use_last_rates:]
        smoothed_rate = sum(self.rate_info) / len(self.rate_info)
        rest = self.total - count
        try:
            eta = rest / smoothed_rate
        except ZeroDivisionError:
            # e.g. called before a "count+=1"
            return self.total, u"-", 0.0
        human_eta = human_duration(eta)
        return rest, human_eta, smoothed_rate


if __name__ == "__main__":
    import doctest
    print doctest.testmod()
