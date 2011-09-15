from lxml import etree
from pmshell.commands import PlexCmd
from pmshell.model import Directory, Track, Artist
from pmshell.utils import get


class DirectoryCmd(PlexCmd):
    ''' Plex directory related commands '''

    @classmethod
    def parse_directory_response(cls, response, directory):
        result = list()
        path = directory.path if directory else ""
        if not directory.is_root():
            parent = Directory(directory.name, path, directory.parent, "..")
            result.append(parent)
        listing = etree.fromstring(response)
        for dir_node in listing.findall(".//Directory"):
            name = (dir_node.get("name", None)
                    or dir_node.get('title')).encode("utf8")
            key = dir_node.get('key').encode("utf8")
            dir_path = key if key.startswith("/") else "%s/%s" % (path, key)
            result.append(Directory(name, dir_path, directory))
        for track_node in listing.findall(".//Track"):
            name = track_node.get("title", None)
            track_path = track_node.find(".//Media/Part").get("key")
            result.append(Track(name, track_path))
        for artist_node in listing.findall(".//Artist"):
            name = artist_node.get("artist", None).encode("utf8")
            artist_path = "%s/%s" % (path, artist_node.get("key"))
            result.append(Artist(name, artist_path))
        return result

    def __init__(self, *args, **kwargs):
        super(DirectoryCmd, self).__init__(*args, **kwargs)
        self.set_cwd(Directory())

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

    def get_cwd(self):
        return getattr(self, "_cwd")

    def set_cwd(self, cwd):
        setattr(self, "_cwd", cwd)
        self.prompt_context = cwd
        self.update_prompt()

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
            self.set_cwd(Directory())
            return
        for name in name.split("/"):
            if not name:
                continue
            directory = self.get_directory(name)
            if directory:
                if not self.list_directory(directory):
                    print "Directory not found"
                else:
                    self.set_cwd(directory)
            else:
                print "Invalid directory"

    def do_ls(self, name):
        directory = self.get_directory(name) if name else self.cwd
        listing = self.list_directory(directory, "Couldn't list directory")
        for subdir in listing or []:
            print subdir

    do_l = do_ls
    cwd = property(get_cwd, set_cwd)
