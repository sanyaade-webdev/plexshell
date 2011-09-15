from utils import Colors, colorize

class Node(object):
    def __init__(self, node = None, parent = None, display_name = None):
        self._node = node
        self._parent = parent
        self._display_name = display_name

    def __str__(self):
        return self.display_name

    @property
    def node(self):
        return self._node

    @property
    def parent(self):
        return self._parent

    @property
    def display_name(self):
        return self._display_name or self.name

    @property
    def color(self):
        return Colors.EndC


class Track(Node):
    @property
    def name(self):
        name = node.get("title", None)

    @property
    def path(self):
        return self.node.find(".//Media/Part").get("key")


class Artist(Node):
    def __str__(self):
        return self.name

    @property
    def name(self):
        return self.node.get("artist", None).encode("utf8")

    @property
    def path(self):
        parent_path = self.parent.path if self.parent else ""
        return "%s/%s" % (parent_path, self.node.get("key"))


class Directory(Node):
    def is_root(self):
        return self.name == "/"

    def is_parent_dir(self):
        return self.display_name == ".."

    def is_search_dir(self):
        return False

    @property
    def path(self):
        path = ""
        if self.node is not None:
            key = self.node.get('key').encode("utf8")
            path = key if key.startswith("/") else "%s/%s" % (
                self.parent.path, key)
        return path

    @property
    def name(self):
        name = "/"
        if self.node is not None:
            key = self.node.get('key').encode("utf8")
            name = (self.node.get("name", None) or
                    self.node.get('title')).encode("utf8")
        return name

    @property
    def display_path(self):
        if not self.parent:
            return "/"
        parent = self.parent.display_path
        return "%s/%s" % (parent if parent != "/" else "", self.name)

    @property
    def color(self):
        return Colors.Blue


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
