from os import getcwd, path
from yaml import full_load as yaml_load


class Paths:

    def __init__(self):
        self.configs = ''
        self.results = ''
        self.set_paths()

    def set_paths(self):
        """Определить путь к файлу"""
        for f in self.__dict__.keys():
            if f == 'results':
                setattr(self, f, path.join(getcwd(), f))
            else:
                setattr(self, f, path.join(path.dirname(__file__), f))


class FileNames:

    selenoid = 'selenoid.yml'
    env = 'env.yml'
    users = 'users.yml'
    pages = 'pages.yml'


class Option:

    def __init__(self, name, action='store', default='', info=''):
        self.name = name
        self.action = action
        self.default = default
        self.info = info
        self.value = ''


class Options:

    def __init__(self):
        """
        Имена опций должны соответствовать преобразованию:
        --option-name = option_name
        То есть два первых дефиса будут убраны, а последующие будут преобразованы в нижнее подчеркивание.
        Именно так делает преобразование имен опций PyTest
        """
        self.selenoid = Option(
            '--selenoid', default='local',
            info='Name of selenoid host from config file'
                 '(local, server)')
        self.br_name = Option(
            '--br-name', default='chrome',
            info='Browser name for UI testing')
        self.br_size = Option(
            '--br-size', default='1920x1080',
            info='Window size of browser for UI testing')
        self.env = Option(
            '--env', default='test', info='Environment name')


class PyTestManager:

    paths = Paths()
    file_names = FileNames()
    options = Options()
    test_name = ''
    test_start = ''

    def __init__(self):
        self.selenoid = {}
        self.env = {}
        self.users = {}
        self.pages = {}

    def __parse_yml(self, filename):
        """Парсит yml файл"""
        if filename:
            return yaml_load(open(path.join(self.paths.configs, filename)))
        return dict()

    def set_configs(self):
        """Записывает информацию из yml файла"""
        self.selenoid = self.__parse_yml(self.file_names.selenoid).get(self.options.selenoid.value)
        self.env = self.__parse_yml(self.file_names.env).get(self.options.env.value)
        self.users = self.__parse_yml(self.file_names.users)
        self.pages = self.__parse_yml(self.file_names.pages)


manager = PyTestManager()
