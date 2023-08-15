import argparse
import os
import re
import subprocess
import sys
from datetime import datetime

from ul_py_tool.commands.cmd import Cmd
from ul_py_tool.utils.arg_str2bool import arg_str2bool
from ul_py_tool.utils.write_stdout import write_stdout

from ul_api_utils.conf import APPLICATION_GUNICORN_WORKERS
from ul_api_utils.const import THIS_LIB_CWD

ENV_LOCAL = 'local'
PY_FILE_SUF = '.py'


class CmdStart(Cmd):
    app_dir: str
    app_file_name: str = 'main.py'
    app_name: str = 'flask_app'
    env: str
    port: int
    debug: bool

    @property
    def app_rel_dir(self) -> str:
        return os.path.relpath(self.app_dir, os.getcwd())

    @property
    def app_file_path(self) -> str:
        return os.path.join(self.app_dir, self.app_file_name)

    @property
    def app_module(self) -> str:
        file_rel_path = os.path.relpath(self.app_file_path, os.getcwd())
        if file_rel_path.endswith(PY_FILE_SUF):
            file_rel_path = file_rel_path[:-len(PY_FILE_SUF)]
        return re.sub(r'/+', '.', file_rel_path.replace('\\', '/')).strip('.')

    @staticmethod
    def add_parser_args(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--app-dir', dest='app_dir', type=str, required=True, help="dir to import ")
        parser.add_argument('--env', dest='env', type=str, required=True)
        parser.add_argument('--port', dest='port', type=int, required=False, default=30000)
        parser.add_argument('--debug', dest='debug', type=arg_str2bool, default=False, required=False)

    def run(self) -> None:
        env = os.environ.copy()
        name = re.sub(r'[^0-9a-z]+', '-', f'gncrn-{os.path.relpath(self.app_dir, os.getcwd()).lower().strip("/").strip()}')
        env['PYTHONUNBUFFERED'] = os.environ.get('PYTHONUNBUFFERED', '0')
        env['PYTHONPATH'] = os.getcwd()
        env['APPLICATION_START_DT'] = datetime.now().isoformat()
        env['APPLICATION_ENV'] = self.env
        env['APPLICATION_DIR'] = self.app_dir
        env['APPLICATION_DEBUG'] = '1' if self.debug else '0'
        env['FLASK_APP'] = self.app_file_path

        # clr = self.debug and self.env == APPLICATION_ENV__LOCAL

        # log_format = f'<GUNICORN> %(t)s %(h)+15s %({{x-forwarded-for}}i)+15s {FG_YELLOW if clr else ""}%(s)-3s{NC if clr else ""} %(L)-6ss %(B)+9sb %(m)-7s %(U)s'
        #
        # if self.debug and self.env == APPLICATION_ENV__LOCAL:
        #     log_format = f'{FG_GRAY}<GUNICORN> %(t)s{NC} {FG_GREEN}%(m)s{NC} %(U)s {FG_YELLOW}%(s)-3s{NC} {FG_GRAY}%(B)sb{NC} %(L)ss'
        assert len(APPLICATION_GUNICORN_WORKERS) > 0
        # application_options = {
        #     'name': name,
        #     'workers': APPLICATION_GUNICORN_WORKERS,
        #     'bind': f'0.0.0.0:{self.port}',
        #     'config': os.path.join(THIS_LIB_CWD, 'commands', 'start', 'gunicorn.conf.py'),
        #     'loglevel': 'INFO',
        #     'access_log_format': log_format,
        #     'max_requests': 1000,
        #     'timeout': 60,
        #     'preload_app': True
        # }

        # UnicLabWSGIApplication(f'{self.app_module}:{self.app_name}', application_options).run()
        # for i in os.environ['PATH'].split(':'):
        #     bin_file = os.path.join(i, 'gunicorn')
        #     if os.path.exists(bin_file):
        #         break

        conf = os.path.abspath(os.path.normpath(os.path.join(THIS_LIB_CWD, "commands", "start", "gunicorn.conf.py")))
        debug = (self.debug and self.env == ENV_LOCAL)

        # print(name)
        args = [
            f'-n={name}',
            f'-w={APPLICATION_GUNICORN_WORKERS}',
            f'-b=0.0.0.0:{self.port}',
            f'--config={conf}',
            '--log-level=INFO',
            # f'--access-logformat=\'{log_format}\'',
            '--max-requests=1000',
            '--timeout=60',
            # '--worker-class=gthread',
            # '--threads=3',
            # '--worker-class=sync',
            # '--threads=1',
            '--access-logfile=-',
            '--error-logfile=-',
            '--disable-redirect-access-to-syslog',
            *(['--reload'] if debug else ['--preload']),
            f'{self.app_module}:{self.app_name}',
        ]
        write_stdout(f'name={name}')
        write_stdout(f'args={args}')
        subprocess.run(['gunicorn', '--check-config', '--print-config', *args], cwd=os.getcwd(), stdout=sys.stdout, stderr=sys.stderr, text=True, env=env)
        os.execvpe('gunicorn', args, env)
