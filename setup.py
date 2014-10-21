from pip.req import parse_requirements as parse

import versioneer

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(name='schemator',
      version=versioneer.get_version(),
      description='Python Schemator',
      author='Alexander Plesovskikh',
      author_email='me@hgen.ru',
      license='LICENSE',
      package_dir={'schemator': 'schemator'},
      install_requires=list(str(r.req) for r in parse('requirements.txt')),
      tests_require=list(str(r.req) for r in parse('requirements-dev.txt')),
      cmdclass=versioneer.get_cmdclass(),
      classifiers=(
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python :: 3.4'))
