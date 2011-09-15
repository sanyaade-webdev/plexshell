from lxml import etree
from plexshell.commands import PlexCmd
from plexshell.model import Directory, Track, Artist
from plexshell.utils import get, colorize


class DirectoryCmd(PlexCmd):
    ''' Plex directory related commands '''

    def __init__(self, *args, **kwargs):
        super(DirectoryCmd, self).__init__(*args, **kwargs)
        self.cwd = Directory()

    @classmethod
    def parse_directory_response(cls, response, directory):
        result = list()
        listing = etree.fromstring(response)
        if not directory.is_root():
            result.append(Directory(directory.node, directory.parent, ".."))
        for node in listing.findall(".//Directory"):
            result.append(Directory(node, directory))
        for node in listing.findall(".//Track"):
            result.append(Track(node, directory))
        for node in listing.findall(".//Artist"):
            result.append(Artist(node, directory))
        return result

    @property
    def cwd(self):
        return self._cwd

    @cwd.setter
    def cwd(self, cwd):
        self._cwd = cwd
        self.prompt_context = colorize(cwd.display_path, cwd.color)
        self.update_prompt()

    def list_directory(self, directory, error_msg = None, parse = True):
        response = get(self.conn, directory.path, error_msg)
        if not response:
            return None
        return self.parse_directory_response(
            response, directory) if parse else response

    def get_node(self, directory, klass, matcher):
        directory = directory if directory else self.cwd
        for node in self.list_directory(directory):
            if not isinstance(node, klass):
                continue
            if matcher(node):
                return node

    def get_track(self, name, cwd = None):
        matcher = lambda n: n.name == name
        return self.get_node(cwd, Track, matcher)

    def get_directory(self, name, cwd = None):
        matcher = lambda n: (n.display_name or n.name) == name
        subdir = self.get_node(cwd, Directory, matcher)
        if subdir:
            if subdir.is_parent_dir():
                return subdir.parent
            return subdir

    def help_cd(self):
        print 'Change to a given directory'

    def help_ls(self):
        print 'List directory contents (defaults to current dir)'

    def help_pwd(self):
        print 'Print the path to the current directory'

    def complete_cd(self, text, line, begidx, endidx):
        components = line[3:].split("/")
        cwd = self.cwd
        for index, name in enumerate(components) or (0, ".."):
            if index == len(components) - 1:
                subdirs = self.list_directory(cwd)
                return [s.display_name for s in subdirs
                        if s.display_name.startswith(text)
                        and isinstance(s, (Directory))]
            cwd = self.get_directory(name, cwd)
            if not cwd:
                return []

    def do_pwd(self, s):
        print self.cwd.path or "/"

    def do_cd(self, name):
        if not len(name) or name == "/":
            self.cwd = Directory()
            return
        for name in name.split("/"):
            if not name:
                continue
            directory = self.get_directory(name)
            if directory:
                if not self.list_directory(directory):
                    print "Directory not found: %s" % directory
                else:
                    self.cwd = directory
            else:
                print "Invalid directory"

    def do_ls(self, name):
        directory = self.get_directory(name) if name else self.cwd
        listing = self.list_directory(directory, "Couldn't list directory")
        for subdir in listing or []:
            print colorize(subdir.display_name, subdir.color)

    do_l = do_ls
