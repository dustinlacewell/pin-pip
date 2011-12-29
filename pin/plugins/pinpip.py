import os

from pin import command, hook
from pin.event import eventhook
from pin.util import get_settings_path, get_project_root

class PinPipRequiresCommand(command.PinSubCommand):
    '''Print project's requirements.txt file'''

    command = 'pip-requires'

    def setup_parser(self, parser):
        parser.usage = "pin pip requires"

    def execute(self):
        self.script = ''
        requirements_file = os.path.join(self.root, 'requirements.txt')
        if os.path.isfile(requirements_file):
            self.script = "cat %s;" % requirements_file
            return True
        
    def write_script(self, file):
        file.write(self.script)

command.register(PinPipRequiresCommand)

class PinPipMeetCommand(command.PinSubCommand):
    '''Process project's requirements.txt file. (VirtualEnv aware)'''
    command = 'pip-meet'

    def setup_parser(self, parser):
        parser.usage = "pin pip meet"

    def execute(self):
        self.script = ''
        requirements_file = os.path.join(self.root, 'requirements.txt')
        if os.path.isfile(requirements_file):
            envpath = os.path.join(self.root, 'env')
            venvopt = ''
            if os.path.isdir(envpath):
                venvopt = "-E %s " % envpath
            self.script = "pip install %s -r %s;" % (venvopt, requirements_file)
            return True
        
    def write_script(self, file):
        file.write(self.script)

command.register(PinPipMeetCommand)

class PinPipCommand(command.PinDelegateCommand):
    '''
    Commands for managing dependencies with pip.
    '''
    command = 'pip'
    subcommands = [PinPipMeetCommand, PinPipRequiresCommand]

    def is_relevant(self):
        return self.root and \
            os.path.isfile(os.path.join(self.root, 'requirements.txt'))

    def setup_parser(self, parser):
        parser.usage = "pin pip [subcommand]"
    
command.register(PinPipCommand)

class PipPinHook(hook.PinHook):
    '''Adds pip argument to core init command'''

    name = "pip"

    def __init__(self):
        self.options = None

    @eventhook('init-post-parser')
    def init_post_parser(self, parser):
        '''Add argument to core init command'''
        parser.add_argument('--pip', action='store_true', help='Process your requirements.txt (requires, --mkenv or --lnenv)')

    @eventhook('init-post-args')
    def init_post_args(self, args, options):
        '''Save init parsed options for later'''
        self.options = options

    @eventhook('init-post-exec')
    def init_post_exec(self, cwd, root):
        '''Save path of new project'''
        self.options.root = root

    @eventhook('venv-post-create')
    def venv_post_create(self, path):
        '''Save path of new virtualenv'''
        # only install if options were present
        if self.options.pip and (self.options.mkenv or self.options.lnenv): 
            self.options.venvpath = path
        else:
            self.options.venvpath = None

    @eventhook('init-post-script')
    def init_post_script(self, file):
        '''Write shell script to process requirements file using new virtualenv'''
        if self.options.pip and getattr(self.options, 'venvpath', None):
            venvopt = "-E %s" % self.options.venvpath
            file.write("pip install %s -r %s;" % (venvopt, 
                                          os.path.join(self.options.root,
                                                       'requirements.txt')))

hook.register(PipPinHook)
