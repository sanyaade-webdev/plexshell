from plexshell.commands import DirectoryCmd, PluginCmd, UpdateCmd


class PlexShell(DirectoryCmd, UpdateCmd, PluginCmd):
    ''' The command line interpretter '''

    def __init__(self, host, port, stdin = None):
        super(PlexShell, self).__init__(stdin = stdin)
        self.set_host(host, port)
