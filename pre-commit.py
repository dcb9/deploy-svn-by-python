# @since 2014-09-24 09:52
# @author bob <bob@jjwxc.com>
# @version $Id$
#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os, subprocess, re

from config import *
from depoly import exec_commands
from tools import implode, get_svn_changes

repos = sys.argv[1]
txn = sys.argv[2] # transaction

TAG_RE = re.compile(r'\@\w+')
PHP_SUFFIX_RE = re.compile(r'.*\.php')

def has_keywords(content):
    keywords = TAG_RE.findall(content)
    intersection =  list(set(PHP_MUST_HAS_KEYWORDS).intersection(set(keywords)))
    return len(intersection) == len(PHP_MUST_HAS_KEYWORDS):

def main():
    changes = get_svn_changes('%s -t %s' % (repos, txn))
    for (status, svnpath)  in changes:
        if status == STATUS_D and svnpath.rstrip('/') in EXCLUDE[STATUS_D]:
            sys.stderr.write(
                "%s can not delete, because it in pre-comment.py EXCLUDE." % svnpath
            )
            return False

        else if PHP_SUFFIX_RE.match(svnpath):
            command = "%s cat -t %s %s %s | head -n 50 "  % (SVNLOOK, txn, repos, svnpath)
            # svnlook cat -t txn  REPOS_PATH FILE_PATH
            content = implode('', exec_commands(command))
            if not has_keywords(content):
                sys.stderr.write(
                    'Can not find keywords %s in %s contents.' % (implode(' ', PHP_MUST_HAS_KEYWORDS), svnpath)
                )
                return False
    
if __name__ == "__main__":
    if main() == False:
        sys.exit(2)
    else:
        sys.exit(0)
