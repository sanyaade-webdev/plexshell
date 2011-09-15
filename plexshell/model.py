from utils import Colors, colorize

class Node(object):
    def __init__(self, name, path):
        self.name = name
        self.path = path


class Track(Node):
    def __str__(self):
        return self.name


class Artist(Node):
    def __str__(self):
        return self.name


class Directory(Node):
    def __init__(self, name = "/", path = "", parent = None,
                 display_name = None):
        super(Directory, self).__init__(name, path)
        self.parent = parent
        self._display_name = display_name

    def __str__(self):
        return colorize(self.display_name, Colors.Blue)

    def is_root(self):
        return self.name == "/"

    def is_parent_dir(self):
        return self.display_name == ".."

    @property
    def display_name(self):
        return self._display_name or self.name


class Plugin(object):
    def __init__(self, identifier):
        self.identifier = identifier

    def __str__(self):
        return self.identifier


class Setting(object):
    def __init__(self, identifier, label, value):
        self.identifier = identifier
        self.label = label
        self.value = value

    def __str__(self):
        return "<setting id: '%s', label: '%s', value: '%s'>" % (
            self.identifier, self.label, self.value)
