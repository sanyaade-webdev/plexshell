from .directory import DirectoryCmd
from plexshell.model import Search
from plexshell.utils import PlexError
from urllib import quote


class SearchCmd(DirectoryCmd):
    def __init__(self, *args, **kwargs):
        super(SearchCmd, self).__init__(*args, **kwargs)
        if self.is_interactive():
            self.prompt = "Enter search term: "

    def do_search(self, term):
        path = self.cwd.path + "&query=%s" % quote(term)
        response = self.get_resource(path, "Search failed")
        search_type = self.cwd.name
        self.cwd = self.cwd.parent # if parsing fails jump back to the parent
        self.cwd = Search(
            self.parse_response(response), self.cwd, term, search_type, path)

    def onecmd(self, line):
        try:
            self.do_search(line)
        except PlexError, e:
            print e
        return True
