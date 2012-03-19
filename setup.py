try:
    import setuptools
except:
    print '''
setuptools not found.

On linux, the package is often called python-setuptools'''
    exit(1)
from distutils.core import setup

execfile('imcol/imcol_version.py')

ext_modules = []

packages = setuptools.find_packages()
if 'tests' in packages: packages.remove('tests')


setup(name = 'imcol',
      version = __version__,
      description = 'Image Collection',
      author = 'Luis Pedro Coelho',
      author_email = 'luis@luispedro.org',
      packages = packages,
      ext_modules = ext_modules,
      test_suite = 'nose.collector',
      )


