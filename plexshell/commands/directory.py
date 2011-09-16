from lxml import etree
from plexshell.commands import PlexCmd
from plexshell.model import Node, Directory, Track, Artist
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
        if directory.backlink:
            result.append(directory.backlink)
        for child in listing.iterchildren():
            result.append(Node.create(child, directory))
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
        return self.parse_directory_response(
            response, directory) if response and parse else response

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
            if not self.cd_to_sibling(name):
                return

    def cd_to_sibling(self, name):
        if not name:
            return True
        directory = self.get_directory(name)
        if not directory:
            print "Invalid directory"
        elif directory.is_search_dir():
            print "NOT IMPLEMENTED: search command"
        elif not self.list_directory(directory):
            print "Directory not found: %s" % directory
        else:
            self.cwd = directory
        return self.cwd.name == name

    def do_ls(self, name):
        directory = self.get_directory(name) if name else self.cwd
        listing = self.list_directory(directory, "Couldn't list directory")
        for subdir in listing or []:
            print colorize(subdir.display_name, subdir.color)

    do_l = do_ls
