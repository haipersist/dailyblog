__author__ = 'haibo'

import os
import sys
import signal


class SigHandler(object):

    SIGNALS = [
       "SIGKILL",
       "SIGINT",
       "SIGQUIT",
       "SIGTTIN",
       "SIGTTOU",
       "SIGHUP",
       "SIGUSR1",
       "SIGUSR2",
   ]

    SIG_QUEUE = []

    def init_signals(self):
       for sig in self.SIGNALS:
           sig_value = getattr(signal,sig)
           signal.signal(sig_value,self.put)


    def put(self,sig):
        if len(self.SIG_QUEUE) < 9:
            self.SIG_QUEUE.append(sig)

    def handle_int(self,sig,frame):
        print 'test int signal'
        sys.exit(0)

    def handle_hup(self):
        pass

    def handle_ttin(self):
        pass

    def handle_ttou(self):
        pass

    def handle_kill(self):
        pass

    def handle_usr1(self,sig,frame):
        print 'get signal'

    def run(self):
        import time
        print 'pid:{0}'.format(os.getpid())
        signal.signal(10,self.handle_usr1)
        signal.signal(2,self.handle_int)
        #signal.signal(9,self.handle_kill())
        while 1:
            time.sleep(1)


if __name__ == "__main__":
    si = SigHandler()
    si.run()


