import subprocess
import sys
import signal
import os
import settingslocal

manage_py_process = "python manage.py runserver"

if hasattr(settingslocal, 'RUNSERVER_PROCESS'):
    manage_py_process = getattr(settingslocal, 'RUNSERVER_PROCESS')

class color:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

class custom_color:
    WARNING = color.YELLOW
    DEBUG = color.BLUE
    INFO = color.GREEN
    ERROR = color.RED

def main():
    process = subprocess.Popen("%s %s" % (manage_py_process, (' '.join(sys.argv[1:]))), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = process.stderr

    def signal_handler(input_signal, frame):
        os.kill(process.pid, signal.SIGTERM)
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    blank_lines = 0
    while output:
        line = output.readline().strip('\n')
        if line:
            blank_lines = 0
            split_location = str.find(line, ']') + 1
            first_part = line[:split_location]
            second_part = line[split_location:]
    	
            if line.startswith('WARNING'):
                print custom_color.WARNING + first_part + color.ENDC + second_part 
            elif line.startswith('DEBUG'):
                print custom_color.DEBUG + first_part + color.ENDC + second_part 
            elif line.startswith('INFO'):
                print custom_color.INFO + first_part + color.ENDC + second_part
            elif line.startswith('ERROR'):
                print custom_color.ERROR + first_part + color.ENDC + second_part 
            else:
                print line
        else:
            print line
            blank_lines += 1
            if blank_lines > 4:
                sys.exit(0)

if __name__ == '__main__':
    main()
