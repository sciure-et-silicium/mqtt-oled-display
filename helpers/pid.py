import os

pid_file = '/tmp/mqtt-oled-display.pid'

def create_pid_file():
    with open(pid_file, 'w') as f:
        f.write(str(os.getpid()))

def cleanup_pid_file():
    if os.path.exists(pid_file):
        os.remove(pid_file)

def read_pid_file():
    try:
        with open(pid_file, 'r') as f:
            return int(f.read().strip())
    except:
        return None