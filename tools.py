from config import WEB_USER_NAME, SVNLOOK, PATH_REPLACE, DEPOLY_PATH

def implode(glue , pieces):
    return glue.join([str(i) for i in pieces])

def exec_commands( commands = [], sudo=True):
    if commands:
        if not isinstance(commands, list): commands = [commands]
        commands_str = implode(';', commands)

        if (sudo): commands_str = 'sudo -u %s sh -c "%s"' % (WEB_USER_NAME, commands_str)

        p = subprocess.Popen(commands_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        command_log(commands_str)
        error_log(p.stderr.readlines())
        return p.stdout.readlines()

def get_svn_changes(arguments):
    command = '%s changed %s' % (SVNLOOK, arguments)

    changes = []
    for line in exec_commands(command):
        row = line.strip('\n').split()
        # if needs depoly
        if row[1].split('/')[0] in DEPOLY_PATH:
            changes.append(row)
    return changes

def get_time_format(format_str):
    from datetime import datetime
    return datetime.now().strftime(format_str)
	
def command_log(command):
    print get_time_format('%Y-%m-%d %H:%M:%S') + ' ' + command

def error_log(message):
    if message:
        for i in message:
            sys.stderr.write(get_time_format('%Y-%m-%d %H:%M:%S') + ' ' + i)

def svnpath_2_realpath(svnpath):
    # PATH_REPLACE is in config.py
    real_path = svnpath
    for (svn_prefix, real_prefix) in PATH_REPLACE.items():
        if (svn_prefix == svnpath[0:len(svn_prefix)]):
            real_path = svnpath.replace(svn_prefix, real_prefix, 1)

    return real_path
