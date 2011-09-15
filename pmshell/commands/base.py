from cmd import Cmd
from httplib import HTTPConnection
from pmshell.utils import Colors, colorize
import sys


class PlexCmd(Cmd, object):
    ''' Base class for plex commands '''

    def __init__(self, *args, **kwargs):
        if kwargs.get('stdin', None) and kwargs['stdin'] != sys.stdin:
            setattr(self, "interactive", False)
            self.use_rawinput = False
        super(PlexCmd, self).__init__(*args, **kwargs)
        self.conn = None

    def help_help(self):
        print 'Print command specific help'

    def help_exit(self):
        print "Exit the interpreter."
        print "You can also use the Ctrl-D shortcut."

    def help_shell(self):
        print "Execute shell commands"

    def help_clear(self):
        print "Clear the screen"

    def do_exit(self, s):
        return True

    def do_shell(self, s):
        os.system(s)

    def do_clear(self, s):
        os.system("clear")

    def do_EOF(self, line):
        return True

    def set_host(self, host, port):
        self.conn = HTTPConnection(host, port)
        self.update_prompt()

    def update_prompt(self):
        context = getattr(self, "prompt_context", None)
        interactive = getattr(self, "interactive", True)
        if not interactive:
            prompt = ''
        elif not self.conn:
            prompt = "disconnected >"
        elif context:
            prompt = "%s:%s %s > " % (self.conn.host, self.conn.port, context)
        else:
            prompt = "%s:%s > " % (self.conn.host, self.conn.port)
        self.prompt = colorize(prompt, Colors.Green)

    def cmdloop(self, intro=None):
        while True:
            try:
                return super(PlexCmd, self).cmdloop(intro)
            except KeyboardInterrupt:
                print "Goodbye!"
                exit(1)

    do_EOF = do_exit
    help_EOF = help_exit