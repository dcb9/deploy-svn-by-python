# @since 2014-09-22 14:35
# @author bob <bob@jjwxc.com>
# @version $Id$
#coding=utf-8

import sys 
reload(sys) 
sys.setdefaultencoding('utf-8')

import os, subprocess, re
from config import *
from tools import implode, get_svn_changes, svnpath_2_realpath


def fetch_svn():
    changes_str = ''
    # changes from global variable
    for i in changes:
        changes_str = changes_str + ' ' + os.path.join(LOCAL_ROOT, i[1])

    command = '%s update %s --username %s --password %s --no-auth-cache' % (SVN, changes_str, SVN_USERNAME, SVN_PASSWORD)
    exec_commands(['export LANG="zh_CN.UTF-8"', command])
			
def depoly_to_online():
    # changes came from global variables
    for (status, svnpath) in changes:
        repos_path = os.path.join(LOCAL_ROOT, svnpath)

        fn = svnpath.rstrip('/')
        if fn in LAMBDA.keys():
            exec_commands(LAMBDA[fn](fn), False)
            continue

        real_path = svnpath_2_realpath(svnpath)
        master_path = os.path.join(MASTER_ROOT, real_path)
        test_path = os.path.join(TEST_ROOT, real_path)

        if status == STATUS_D:
            if svnpath.rstrip('/') in EXCLUDE[STATUS_D]: continue

            trash_name = svnpath.replace('/', '.') + '_' + get_time_format('%Y%m%d%H%M%S')
            trash_name = os.path.join(TRASH_DIR, trash_name)
            command = "mv '%s' '%s'" % (master_path, trash_name);
        else:
            command = "cp -af %s %s" % (repos_path, master_path)

        exec_commands(command)



if __name__ == "__main__":
    REV=int(sys.argv[1])
    REPOS=sys.argv[2]
    changes = get_svn_changes(
                            "-r %d %s" % (REV, REPOS)
                            )
    if changes:
        fetch_svn()
        depoly_to_online()
