import sys
from datetime import datetime
import asyncore
from smtpd import SMTPServer
import subprocess

MAILDIR = False

def run_addtomaildir(filename, maildir):
    # The reason from running this as a subprocess is to be able to run
    # it as user peterbe otherwise the email will by put into the maildir
    # owned by user root who needs to be the user running the sink since
    # it opens a port :25
    cmd = 'su peterbe -c "./addtomaildir.py %s %s"' % (filename, maildir)
    subprocess.call(cmd, shell=True)

class EmlServer(SMTPServer):
    no = 0
    verbose = False
    def process_message(self, peer, mailfrom, rcpttos, data):
        filename = '%s-%d.eml' % (datetime.now().strftime('%Y%m%d%H%M%S'),
                self.no)
        f = open(filename, 'w')
        f.write(data)
        f.close
        print '%s saved.' % filename
        if self.verbose:
            print data.encode('ascii','replace')
        
        self.no += 1
        
        if MAILDIR:
            run_addtomaildir(filename, MAILDIR)


def run(verbose=False):
    foo = EmlServer(('localhost', 25), None)
    foo.verbose = verbose
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        return 0


if __name__ == '__main__':
    args = sys.argv[1:]
    verbose = False
    if '-v' in args or '--verbose' in args:
        verbose = True
    sys.exit(run(verbose=verbose))
