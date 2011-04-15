import os
from argparse import ArgumentParser

from pin import command
from pin.config import config
from pin.event import eventhook
from pin.hook import PinHook, register
from pin.util import get_settings_path, get_project_root

class PinPipRequiresCommand(command.PinCommand):
    '''
    print project's requirements.txt file.
    '''
    command = 'pip-requires'

    def execute(self):
        self.script = ''
        requirements_file = os.path.join(self.root, 'requirements.txt')
        if os.path.isfile(requirements_file):
            self.script = "cat %s;" % requirements_file
            return True
        
    def write_script(self, file):
        file.write(self.script)
command.register(PinPipRequiresCommand)

class PinPipMeetCommand(command.PinCommand):
    '''
    process project's requirements.txt file. (VirtualEnv aware)
    '''
    command = 'pip-meet'

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

class PinPipCommand(command.PinPluginCommandDelegator):
    '''
    Commands for managing dependencies with pip.
    '''
    command = 'pip'
    subcommands = ['pip-requires', 'pip-meet'] 
command.register(PinPipCommand)

class PipPinHook(PinHook):
    '''
    Processes a requirements.txt file with pip
    '''
    name = "pip"

    def __init__(self):
        self.options = None

    def isactive(self):
        if self.options: # have we parsed options?
            # were both required options present?
            return self.options.pip
        return False

    @eventhook('init-post-args')
    # parse --pip flag
    def postargs(self, args):
        parser = ArgumentParser()
        parser.add_argument('--venv', action='store_true')
        parser.add_argument('--pip', action='store_true')
        self.options, extargs = parser.parse_known_args(args)

    @eventhook('init-post-exec')
    # save project root
    def getroot(self, cwd, root):
        self.options.root = cwd

    @eventhook('venv-post-create')
    def venvpath(self, path):
        # only install if options were present
        if self.active and self.options.venv: 
            self.options.venv = path

    @eventhook('init-post-script')
    # install the requirements file
    def install_reqs(self, file):
        if self.active:
            venvopt = ''
            if self.options.venv:
                venvopt = "-E %s" % self.options.venv
            file.write("pip install %s -r %s;" % (venvopt, 
                                          os.path.join(self.options.root,
                                                       'requirements.txt')))

register(PipPinHook)
