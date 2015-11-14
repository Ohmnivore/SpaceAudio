import sys

class Logger(object):
    def __init__(self, name):
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        self.log = open(name, "a")
        self.log.truncate()

    def write(self, message):
        self.stdout.write(message)
        self.stderr.write(message)
        self.log.write(message)

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass
