#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python Version: 3.11.4
Creator: 孙一凡-莫无煜
Create Date: 2023/8/1

"""
import sys

__all__ = [
    'import_print_error',
    'import_install_all',
]


def import_print_error():
    MoVoidImport.print_all()


def import_install_all():
    MoVoidImport.install_all()


class MoVoidImport:
    all_package = {}

    @classmethod
    def error(cls, error: ModuleNotFoundError, version=None):
        package = error.name
        error_type = getattr(error, 'type', None)
        if error_type is None:
            if package not in cls.all_package:
                if version:
                    version_text = str(version)
                else:
                    version_text = ''
                cls.all_package[package] = {
                    'bool': True,
                    'print': 'you may lack of package: {0} .'.format(package),
                    'cmd': 'pip install {0}{1}'.format(package, version_text)
                }

    @classmethod
    def version(cls, package, version=None):
        if version is not None and not package.__version__.startswith(version):
            MoVoidImport.all_package[package.__name__] = {
                'bool': True,
                'print': 'your package {0} is version {1} but we need version {2}'.format(package.__name__, package.__version__, version),
                'cmd': 'pip install --upgrade {0}=={1}'.format(package.__name__, version)
            }
        else:
            if package.__name__ not in MoVoidImport.all_package:
                MoVoidImport.all_package[package.__name__] = {
                    'bool': False
                }

    @classmethod
    def print_all(cls):
        tell = False
        for i, v in cls.all_package.items():
            if v['bool']:
                print(v['print'], file=sys.stderr)
                tell = True
        if tell:
            print('you can run "import_install_all()" in python to install all wrong package.', file=sys.stderr)

    @classmethod
    def install_all(cls):
        import subprocess
        for i, v in cls.all_package.items():
            if v['bool']:
                print('now installing {}...'.format(i))
                subprocess.run(v['cmd'])
                print('{} install finished.'.format(i))


if __name__ == '__main__':
    pass
