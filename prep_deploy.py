from tempfile import mkstemp
from shutil import move
from os import remove, close
import subprocess
import sys
import re
import datetime
from optparse import OptionParser

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def main():
	start_time = datetime.datetime.now()
	parser = OptionParser()
	parser.add_option('-a','--appid',dest='appid', default='wf-maxpete', help="The appspot id that you will be deploying to. Set in app.yaml")
	parser.add_option('-v','--version',dest='version', default='1', help="The instance version you want to deploy to. Set in app.yaml")
	parser.add_option('-f','--full', dest='full', action='store_true', default=False, help="This tiggers a full build instead of a no-flex build")
	(options, args) = parser.parse_args()
	print "\n"
	print bcolors.OKBLUE + "\tBegin build for deploy" + bcolors.ENDC
        print bcolors.OKBLUE + "\tAppID:    " + bcolors.ENDC + options.appid
        print bcolors.OKBLUE + "\tVersion:  " + bcolors.ENDC + options.version
        print "\n"
	replace('settingslocal.py','MEDIA_COMPRESSED = False', 'MEDIA_COMPRESSED = True')
	print "\tMedia will now be compressed"
	replace('settingslocal.py','MEDIA_MERGED = False', 'MEDIA_MERGED = True')
	print "\tMedia will now be merged"
	replace('settingslocal.py','ENABLE_APPSTATS = False', 'ENABLE_APPSTATS = True')
	print "\tAppStats is now enabled"
	replace('settingslocal.py','DEBUG = True', 'DEBUG = False')
	print "\tDebug is now disabled"
	replace('settingslocal.py','TEMPLATE_DEBUG = "DEBUG"', 'TEMPLATE_DEBUG = False')
	print "\tTemplate Debug is now disabled"
	replace('settingslocal.py','CACHE_TEMPLATES = False', 'CACHE_TEMPLATES = True')
	print "\tTemplates will now be cached"
	
	print "\n"
	print "\tStarting build script..."
	if options.full:
		process = subprocess.Popen("ant set_cachebuster full", shell=True, stdout=subprocess.PIPE)
	else:
		process = subprocess.Popen("ant set_cachebuster clean-no-flex stage-no-flex generate-media", shell=True, stdout=subprocess.PIPE)
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

	#Edit app.yaml
	replace('app.yaml', 'application: (.*)', 'application: %s' % options.appid)
	replace('app.yaml', '^version: (.*)', 'version: %s' % options.version)
	net_time = datetime.datetime.now() - start_time
	print bcolors.OKGREEN + "\tDeploy build completed" + bcolors.ENDC
	#subprocess.Popen('say "Build for deploy completed."', shell=True)

        try:	
	    subprocess.Popen('terminal-notifier -message "Preping for deploy build has completed successfully after %s seconds." -title "Prep for Deploy Completed"' % net_time.seconds, shell=True, stdout=subprocess.PIPE)
	except Exception:
            print "There was a problem executing terminal-notifier\n"

        print "\n"
	sys.exit()

def replace(file, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    new_file = open(abs_path,'w')
    old_file = open(file)
    for line in old_file:
        new_file.write(re.sub(pattern, subst, line))
    #close temp file
    new_file.close()
    close(fh)
    old_file.close()
    #Remove original file
    remove(file)
    #Move new file
    move(abs_path, file)

if __name__ == '__main__':
	main()
