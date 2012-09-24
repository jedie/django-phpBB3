# coding: utf-8

"""
    password hashers
    ~~~~~~~~~~~~~~~~
    
    https://docs.djangoproject.com/en/1.4/topics/auth/#how-django-stores-passwords
    
    some code borrowed from:
        https://github.com/japsu/phpbb-python/blob/master/phpbb/functions.py
    phpbb-python © Copyright 2010 Santtu Pajukanta - http://pajukanta.fi
    phpBB3 © Copyright 2000, 2002, 2005, 2007 phpBB Group - http://www.phpbb.com

    :copyleft: 2012 by the django-phpBB3 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from hashlib import md5

if __name__ == "__main__":
    import os
    os.environ["DJANGO_SETTINGS_MODULE"] = "django_phpBB3.test_settings"

from django.contrib.auth.hashers import BasePasswordHasher, mask_hash
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext_noop as _

ITOA64 = './0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

def raw_md5(*args):
    m = md5()
    for i in args:
        m.update(i)
    return m.digest()

def hex_md5(*args):
    m = md5()
    for i in args:
        m.update(i)
    return m.hexdigest()


def hash_encode64(raw_hash, count, itoa64=ITOA64):
    output = ''
    i = 0
    while True:
        value = ord(raw_hash[i])
        i += 1
        output += itoa64[value & 0x3f]
        if i < count:
            value |= ord(raw_hash[i]) << 8
        output += itoa64[(value >> 6) & 0x3f]
        i += 1
        if i >= count:
            break
        if i < count:
            value |= ord(raw_hash[i]) << 16
        output += itoa64[(value >> 12) & 0x3f]
        i += 1
        if i >= count:
            break
        output += itoa64[(value >> 18) & 0x3f]
        if not i < count:
            break
    return output


def hash_crypt_private(password, setting, itoa64=ITOA64):
    output = '*'
    if setting[0:0 + 3] != '$H$':
        return output
    count_log2 = itoa64.find(setting[3])
    if count_log2 < 7 or count_log2 > 30:
        return output
    count = 1 << count_log2
    salt = setting[4:4 + 8]
    if len(salt) != 8:
        return output
    raw_hash = raw_md5(salt, password)
    for i in xrange(count):
        raw_hash = raw_md5(raw_hash, password)
    output = setting[0:0 + 12]
    output += hash_encode64(raw_hash, 16, itoa64)
    return output


class PhpBB3PasswordHasher(BasePasswordHasher):
    """    
    >>> p = PhpBB3PasswordHasher()
    >>> p.verify("123456", "phpBB3_md5$H$9XB6lIDmryamBri4ovyxkvY8I8gjIL/")
    True
    >>> p.verify("12345678", "phpBB3_md5$H$9dwN9omKahSh5YzR1R.I7/Q/pGJn5E0")
    True
    >>> p.verify("wrong", "phpBB3_md5$H$9XB6lIDmryamBri4ovyxkvY8I8gjIL/")
    False
    >>> p.safe_summary("phpBB3_md5$H$9XB6lIDmryamBri4ovyxkvY8I8gjIL/")
    {'algorithm': 'phpBB3_md5', 'hash': 'phpBB3_md5$H$9XB****************************'}
       
    >>> from django.contrib.auth.hashers import check_password
    >>> check_password("12345678", "phpBB3_md5$H$9dwN9omKahSh5YzR1R.I7/Q/pGJn5E0")
    True
    """
    algorithm = "phpBB3_md5"

    def encode(self, password, salt):
        raise NotImplementedError("PhpBB3PasswordHasher().encode() not imlemented!")

    def verify(self, password, encoded):
        """
        Checks if the given phpBB password is correct
        """
        assert encoded.startswith("%s$H$" % self.algorithm)
        encoded = encoded[10:]
        return hash_crypt_private(password, encoded) == encoded

    def safe_summary(self, encoded):
        """
        Returns a summary of safe values

        The result is a dictionary and will be used where the password field
        must be displayed to construct a safe representation of the password.
        """
        return SortedDict([
            (_('algorithm'), self.algorithm),
            (_('hash'), mask_hash(encoded, show=16)),
        ])


if __name__ == "__main__":
    import doctest
    print doctest.testmod()
