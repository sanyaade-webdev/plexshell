from plexshell.commands import PlexCmd
from plexshell.model import Setting
from plexshell.utils import get, Colors, colorize
from lxml import etree
from urllib import quote


class SettingsCmd(PlexCmd):
    ''' Mixin that provides commands to edit user settings '''

    @classmethod
    def parse_settings_response(cls, response):
        result = list()
        listing = etree.fromstring(response)
        for setting_node in listing.findall("./Setting"):
            identifier = setting_node.get("id")
            label = setting_node.get("label")
            value = setting_node.get("value")
            result.append(Setting(identifier, label, value))
        return result

    @classmethod
    def is_settings_resource(cls, response):
        settings = cls.parse_settings_response(response)
        return len(settings)

    def do_save(self, s):
        to_string = lambda s: "%s=%s" % (quote(s.identifier), quote(s.value))
        params = "&".join(map(to_string, self.settings))
        path = self.directory.path + "/set?" + params
        if get(self.conn, path, "Unable to save settings") is not None:
            return self.do_exit()

    def do_set(self, string):
        components = string.split()
        if not len(components) >= 2:
            return self.help_set()
        identifier = components[0]
        value = " ".join(components[1:])
        self.update_setting(identifier, value)

    def help_save(self):
        print 'Save settings back to PMS'

    def help_set(self):
        print 'Usage: set identifier value'
        print 'Change a setting value'

    def do_get(self, identifier):
        if not len(identifier):
            return help_get()
        setting = self.get_setting(identifier)
        if not setting:
            print "Invalid setting: %s" % identifier
            return
        print setting.value

    def help_get(self):
        print 'Usage: get identifier'
        print 'Print a setting value'

    def get_setting(self, identifier):
        for setting in self.settings:
            if setting.identifier == identifier:
                return setting
        return None

    def update_setting(self, identifier, value):
        setting = self.get_setting(identifier)
        if not setting:
            print "Invalid setting: %s" % identifier
            return
        setting.value = value

    def __init__(self, conn, directory, stdin = None):
        super(SettingsCmd, self).__init__(stdin = stdin)
        response = get(conn, directory.path, "Failed to get resource")
        self.conn = conn
        self.directory = directory
        self.settings = self.parse_settings_response(response)
        self.prompt_context = "%s[%s]"  % (
            self.directory, colorize("edit", Colors.Red))
        self.update_prompt()
