# coding: utf-8

"""
    version info
    ~~~~~~~~~~~~

    :copyleft: 2012 by the django-phpBB3 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


import os
import subprocess
import time
import warnings


__version__ = (0, 1, 0)


VERSION_STRING = '.'.join(str(part) for part in __version__)


# Display get_git_hash() errors as warnings?
#VERBOSE = True
VERBOSE = False

def _error(msg):
    if VERBOSE:
        warnings.warn(msg)
    return ""

def get_commit_timestamp(path=None):
    if path is None:
        path = os.path.abspath(os.path.dirname(__file__))

    try:
        process = subprocess.Popen(
            # %ct: committer date, UNIX timestamp  
            ["/usr/bin/git", "log", "--pretty=format:%ct", "-1", "HEAD"],
            shell=False, cwd=path,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
    except Exception, err:
        return _error("Can't get git hash: %s" % err)

    process.wait()
    returncode = process.returncode
    if returncode != 0:
        return _error(
            "Can't get git hash, returncode was: %r"
            " - git stdout: %r"
            " - git stderr: %r"
            % (returncode, process.stdout.readline(), process.stderr.readline())
        )

    output = process.stdout.readline().strip()
    try:
        timestamp = int(output)
    except Exception, err:
        return _error("git log output is not a number, output was: %r" % output)

    try:
        return time.strftime(".%m%d", time.gmtime(timestamp))
    except Exception, err:
        return _error("can't convert %r to time string: %s" % (timestamp, err))


VERSION_STRING += get_commit_timestamp()


if __name__ == "__main__":
    print VERSION_STRING
