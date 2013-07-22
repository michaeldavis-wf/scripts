from tempfile import mkstemp
from shutil import move
from os import remove, close
import subprocess
import sys
import re
import datetime


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def main():
    start_time = datetime.datetime.now()
    print "\n"
    print bcolors.WARNING + "\tBegin build for development" + bcolors.ENDC
    print "\n"
    replace('settingslocal.py','MEDIA_COMPRESSED = True', 'MEDIA_COMPRESSED = False')
    print "\tMedia will no longer be compressed"
    replace('settingslocal.py','MEDIA_MERGED = True', 'MEDIA_MERGED = False')
    print "\tMedia will no longer be merged"
    replace('settingslocal.py','ENABLE_APPSTATS = True', 'ENABLE_APPSTATS = False')
    print "\tAppStats is now disabled"
    replace('settingslocal.py','DEBUG = False', 'DEBUG = True')
    print "\tDebug is now enabled"
    replace('settingslocal.py','TEMPLATE_DEBUG = False', 'TEMPLATE_DEBUG = "DEBUG"')
    print "\tTemplate Debug is now enabled"
    replace('settingslocal.py','CACHE_TEMPLATES = True', 'CACHE_TEMPLATES = False')
    print "\tTemplates will now no longer be cached"

    print "\n"
    print "\tStarting build script..."
    process = subprocess.Popen("ant set_cachebuster clean-no-flex stage-no-flex", shell=True,
                               stdout=subprocess.PIPE)
    stdout = process.communicate()[0]
    swf_num = 1
    web_num = 1

    if stdout:
        stdout = stdout.split('\n')
        for line in stdout:
            if 'max.svn.swf.revision=' in line:
                swf_num = line.split('=')[1]
            elif 'max.svn.web.revision=' in line:
                web_num = line.split('=')[1]
    print "\tSetting SWF_REVISION = '%s'" % swf_num
    print "\tSetting WEB_REVISION = '%s'" % web_num
    replace('settingslocal.py',"SWF_REVISION = '(.*)'","SWF_REVISION = '%s'" % swf_num)
    replace('settingslocal.py',"WEB_REVISION = '(.*)'","WEB_REVISION = '%s'" % web_num)

    # Edit app.yaml
    replace('app.yaml',"application: (.*)", "application: big-sky")
    replace('app.yaml','(version: )(?!.*\").*', "version: 1", 10)

    print bcolors.OKGREEN + "\tDev build completed." + bcolors.ENDC
    # subprocess.Popen('say "Dev build completed."', shell=True)
    net_time = datetime.datetime.now() - start_time

    try:
        subprocess.Popen('terminal-notifier -message "The dev build has completed successfully after %s seconds." -title "Dev Build Completed"' % net_time.seconds, shell=True, stdout=subprocess.PIPE)
    except Exception:
        print "There was a problem executing terminal-notifier\n"

    print "\n"
    sys.exit()


def replace(file, pattern, subst, limit=None):
    # Create temp file
    fh, abs_path = mkstemp()
    new_file = open(abs_path,'w')
    old_file = open(file)
    counter = 0
    for line in old_file:
        counter += 1
        if not limit or counter < limit:
            new_file.write(re.sub(pattern, subst, line))
        else:
            new_file.write(line)
    # Close temp file
    new_file.close()
    close(fh)
    old_file.close()
    # Remove original file
    remove(file)
    # Move new file
    move(abs_path, file)


if __name__ == '__main__':
    main()
