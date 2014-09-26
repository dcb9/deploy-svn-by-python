#coding=utf-8

import sys 
reload(sys) 
sys.setdefaultencoding('utf-8')

LOCAL_ROOT='/depoly-svn/'

MASTER_ROOT = '/var/www/master/'

TRASH_DIR = '/trash/'

LOG = '/var/log/depoly-svn/depoly-svn.log'
WEB_USER_NAME = 'apache'

SVN_USERNAME='svnusername'
SVN_PASSWORD='svnpassword'

SVNLOOK='/usr/bin/svnlook'
SVN='/usr/bin/svn'

STATUS_A="A"
STATUS_D="D"

PHP_MUST_HAS_KEYWORDS = ['@version']

# svn path and real path not matchs
PATH_REPLACE = {
    "www": "aaa.net/www.aaa",
}

# don't end of / 
EXCLUDE = {
    STATUS_D: ["www/impotantdir1", "www/impotantdir"]
}

LAMBDA = {
    # "depoly-svn/pre-commit": lambda x: "cp -af %s %s; cp -af %s %s; chmod 755 %s ; chown -R apache.apache %s" % (LOCAL_ROOT+'/'+x, MASTER_ROOT+'/'+x, LOCAL_ROOT+'/'+x, '/var/svn/repos/codes/hooks/pre-commit', '/var/svn/repos/codes/hooks/pre-commit', '/var/svn/repos/codes/hooks/pre-commit'),
}

DEPOLY_PATH = ['www']
