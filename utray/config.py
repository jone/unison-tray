from ConfigParser import RawConfigParser
import os


class Config(object):

    def __init__(self):
        self._load()
        self._read()

    def _load(self):
        path = os.path.join(os.getcwd(), 'syncer.cfg')
        self.config = RawConfigParser()
        self.config.read(path)

    def _read(self):
        self.sync_crons = self._get_multiline(
            'cron', 'sync', [])
        self.unison_executable = self._get(
            'unison', 'executable',
            '/usr/local/bin/unison')

    def _get(self, section, option, default):
        if not self.config.has_option(section, option):
            return default

        value = self.config.get(section, option)
        if value:
            return value
        else:
            return default

    def _get_multiline(self, section, option, default):
        value = self._get(section, option, default)
        if value is not default:
            return value.strip().split('\n')
        else:
            return value


CONFIG = Config()
