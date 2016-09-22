from __future__ import print_function
from setuptools import setup, find_packages, Command
from setuptools.command.sdist import sdist
from setuptools.command.build_py import build_py
from setuptools.command.egg_info import egg_info
from subprocess import check_call
import os
import sys


here = os.path.dirname(os.path.abspath(__file__))
node_root = os.path.join(here, '.')
is_repo = os.path.exists(os.path.join(here, '.git'))

npm_path = os.pathsep.join([
    os.path.join(node_root, 'node_modules', '.bin'),
                os.environ.get('PATH', os.defpath),
])

static_files = []
static_dir = os.path.join('{{ cookiecutter.python_package_name }}', 'static')
for (dirpath, dirnames, filenames) in os.walk(static_dir):
    static_files.extend(filenames)
    break

from distutils import log
log.set_verbosity(log.DEBUG)
log.info('setup.py entered')
log.info('$PATH=%s' % os.environ['PATH'])

LONG_DESCRIPTION = '{{ cookiecutter.project_short_description }}'

def js_prerelease(command, strict=False):
    """decorator for building minified js/css prior to another command"""
    class DecoratedCommand(command):
        def run(self):
            jsdeps = self.distribution.get_command_obj('jsdeps')
            if not is_repo and all(os.path.exists(t) for t in jsdeps.targets):
                # sdist, nothing to do
                command.run(self)
                return

            try:
                self.distribution.run_command('jsdeps')
            except Exception as e:
                missing = [t for t in jsdeps.targets if not os.path.exists(t)]
                if strict or missing:
                    log.warn('rebuilding js and css failed')
                    if missing:
                        log.error('missing files: %s' % missing)
                    raise e
                else:
                    log.warn('rebuilding js and css failed (not a problem)')
                    log.warn(str(e))
            command.run(self)
            update_package_data(self.distribution)
    return DecoratedCommand

def update_package_data(distribution):
    """update package_data to catch changes during setup"""
    build_py = distribution.get_command_obj('build_py')
    # distribution.package_data = find_package_data()
    # re-init build_py options which load package_data
    build_py.finalize_options()


class NPM(Command):
    description = 'install package.json dependencies using npm'

    user_options = []

    node_modules = os.path.join(node_root, 'node_modules')

    targets = [f for f in static_files if f.endswith('.js')]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def has_npm(self):
        try:
            check_call(['npm', '--version'])
            return True
        except:
            return False

    def should_run_npm_install(self):
        package_json = os.path.join(node_root, 'package.json')
        node_modules_exists = os.path.exists(self.node_modules)
        return self.has_npm()

    def run(self):
        has_npm = self.has_npm()
        if not has_npm:
            log.error("`npm` unavailable.  If you're running this command using sudo, make sure `npm` is available to sudo")

        env = os.environ.copy()
        env['PATH'] = npm_path

        if self.should_run_npm_install():
            log.info("Installing build dependencies with npm.  This may take a while...")
            check_call(['npm', 'install'], cwd=node_root, stdout=sys.stdout, stderr=sys.stderr)
            os.utime(self.node_modules, None)

        for t in self.targets:
            if not os.path.exists(t):
                msg = 'Missing file: %s' % t
                if not has_npm:
                    msg += ('\nnpm is required to build a development version '
                            '{{ cookiecutter.python_package_name }}')
                raise ValueError(msg)

        # update package data in case this created new files
        update_package_data(self.distribution)

setup_args = {
    'name': '{{ cookiecutter.python_package_name  }}',
    'description': '{{ cookiecutter.project_short_description }}',
    'long_description': LONG_DESCRIPTION,
    'include_package_data': True,
    'data_files': [
        ('share/jupyter/labextensions/{{ cookiecutter.npm_package_name }}',
         static_files),
    ],
    'packages': find_packages(),
    'zip_safe': False,
    'cmdclass': {
        'build_py': js_prerelease(build_py),
        'egg_info': js_prerelease(egg_info),
        'sdist': js_prerelease(sdist, strict=True),
        'jsdeps': NPM,
    },

    'author': '{{ cookiecutter.author_name }}',
    'author_email': '{{ cookiecutter.author_email }}',
    'url': 'https://github.com/{{ cookiecutter.github_organization_name }}/{{ cookiecutter.github_project_name }}',
    'keywords': [
        'jupyterlab',
        'jupyter',
    ],
}

# Look for a versioneer-style _version.py, not included in this cookiecutter.
version_ns = {}
version_file = os.path.join(here, '{{ cookiecutter.python_package_name  }}', '_version.py')
if os.path.isfile(version_file):
    with open() as f:
        exec(f.read(), {}, version_ns)
    setup_args['version'] = version_ns['__version__'],

setup(**setup_args)
