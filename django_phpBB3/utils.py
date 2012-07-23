# coding: utf-8

"""
    django-phpBB3 utils
    ~~~~~~~~~~~~~~~~~~~

    :copyleft: 2012 by the django-phpBB3 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

import re

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
    ...     'Look at [url=https&#58;//github&#46;com/jedie/PyLucid/views&#46;py:1234abcd]/views.py[/url:1234abcd]',
    ...     bbcode_uid="1234abcd"
    ... )
    'Look at [url=https://github.com/jedie/PyLucid/views.py]/views.py[/url]'
    """
    replace_list = [('&#58;', ':'), ('&#46;', '.'), ('&quot;', ''), ]

    if bbcode_uid is not None:
        replace_list += [(':' + bbcode_uid, ''), ] #('quote=&quot;', 'quote='), ('&quot;:' + self.bbcode_uid, ''),
    for word, replace_by in replace_list:
        text = text.replace(word, replace_by)
    return phpbb_html2bbcode(text)


if __name__ == "__main__":
    import doctest
    print doctest.testmod()
