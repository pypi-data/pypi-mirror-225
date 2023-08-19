"""A utility class to help with ``setuptools``, git and GitHub integration.

"""
__author__ = 'Paul Landes'

from typing import List, Tuple, Dict, Union
import logging
import os
import re
import sys
import json
import inspect
from io import StringIO, TextIOWrapper
from pathlib import Path
import setuptools
from zensols.pybuild import Tag, RemoteSet

logger = logging.getLogger(__name__)


class SetupUtil(object):
    """This class is used in ``setup.py`` in place of the typical call to
    ``setuptools`` and provides a lot of the information contained in the git
    repo as metadata, such as the version from the latest tag.  It also helps
    with finding paths in a the Zensols default Python project configuration.

    The class also provides build information to client APIs (see ``source``).

    """
    FIELDS = """
name packages package_data version description author author_email url
download_url long_description long_description_content_type install_requires
keywords classifiers
"""
    DO_SETUP = True
    DEFAULT_ROOT_CONTAINED_FILE = 'README.md'

    def __init__(self, name: str, user: str, project: str,
                 setup_path: Path = None, package_names: List[str] = None,
                 root_contained_file=None, req_file: str = 'requirements.txt',
                 has_entry_points=True, **kwargs):
        """Initialize.

        :param name: the full name of the package (i.e. ``zensols.zenpybuild``)

        :param user: the user name of the author of the package
                     (i.e. ``plandes``)

        :param project: the project name, usually the last project component
                        (i.e. ``zenpybuild``)

        :param setup_path: the path to the ``setup.py`` file
                           (i.e. ``src/python/setup.py``)

        :param package_names: a list of directories in the root that are to be
                              included in the packge, which is typically the
                              source (``zensols``) and any directories to be
                              included in the wheel/egg distribution file
                              (i.e. ``resources``)

        :param root_contained_file: a file used to help find the project root,
                                    which default to ``README.md``

        :param req_file: the requirements file, which defaults to
                         ``requirements.txt``, which is found in the same
                         directory as the ``setup.py``.

        """
        self.name = name
        self.user = user
        self.project = project
        if setup_path is None:
            setup_path = Path(__file__).parent.absolute()
        else:
            setup_path = setup_path
        self.setup_path = setup_path
        if package_names is None:
            m = re.match(r'^(.+)\..*', name)
            if m:
                package_names = [m.group(1)]
            else:
                package_names = [name]
        self.package_names = package_names
        if root_contained_file is None:
            self.root_contained_file = SetupUtil.DEFAULT_ROOT_CONTAINED_FILE
        else:
            self.root_contained_file = root_contained_file
        self.req_file = req_file
        self.has_entry_points = has_entry_points
        self.__dict__.update(**kwargs)

    @property
    def root_path(self) -> Path:
        """Return root path to the project.

        """
        return self.find_root(self.setup_path.parent, self.root_contained_file)

    @classmethod
    def find_root(cls, start_path: Path,
                  root_contained_file: Path = None) -> Path:
        """Find the root path by iterating to the root looking for the
        ``root_contained_file`` starting from directory ``start_path``.

        """
        if root_contained_file is None:
            root_contained_file = cls.DEFAULT_ROOT_CONTAINED_FILE
        logger.debug(f'using setup path: {start_path}')
        nname, dname = None, start_path
        while nname != dname:
            rm_file = dname.joinpath(root_contained_file)
            logging.debug(f'rm file: {rm_file}')
            if rm_file.is_file():
                logger.debug(f'found file: {rm_file}')
                break
            logger.debug(f'nname={nname}, dname={dname}')
            nname, dname = dname, dname.parent
        logging.debug(f'found root dir: {dname}')
        return dname

    @property
    def packages(self) -> List[str]:
        """Get a list of directories that contain package information to tbe included
        with the distribution files.

        """
        dirs = []
        logger.debug(f'walking on {self.package_names}')
        for dname in self.package_names:
            for root, subdirs, files in os.walk(dname):
                logger.debug(f'root: {root}')
                root = os.path.relpath(root, dname)
                if root != '.':
                    dirs.append(os.path.join(dname, root.replace(os.sep, '.')))
        return dirs

    @property
    def long_description(self) -> str:
        """Return a long human readable description of the package, which is the
        contents of the ``README.md`` file.  This is added so the README shows
        up on the pypi module page.

        """
        path = Path(self.root_path, self.root_contained_file)
        logger.debug(f'reading long desc from {path}')
        with open(path, encoding='utf-8') as f:
            return f.read()

    @property
    def short_description(self) -> str:
        pat = re.compile(r'^\s*#\s*(.+)$', re.MULTILINE)
        desc = self.long_description
        m = pat.match(desc)
        if m:
            return m.group(1)

    @property
    def install_requires(self) -> List[str]:
        """Get a list of pip dependencies from the requirements file.

        """
        path = Path(self.setup_path, self.req_file)
        with open(path, encoding='utf-8') as f:
            return [x.strip() for x in f.readlines()]

    @property
    def url(self) -> str:
        """Return the URL used to access the project on GitHub.

        """
        return f'https://github.com/{self.user}/{self.project}'

    @property
    def download_url(self) -> str:
        """Return the download URL used to obtain the distribution wheel.

        """
        params = {'url': self.url,
                  'name': self.name,
                  'version': self.version,
                  'path': 'releases/download',
                  'wheel': 'py3-none-any.whl'}
        return '{url}/{path}/v{version}/{name}-{version}-{wheel}'.\
            format(**params)

    @property
    def tag(self) -> Tag:
        """Return the tag for the project.

        """
        return Tag(self.root_path)

    @property
    def remote_set(self) -> RemoteSet:
        """Return a remote set for the project.

        """
        return RemoteSet(self.root_path)

    @property
    def author(self) -> str:
        """Return the author of the package.

        """
        commit = self.tag.last_commit
        if commit:
            return commit.author.name

    @property
    def author_email(self) -> str:
        """Return the email address of the project.
        """
        commit = self.tag.last_commit
        if commit:
            return commit.author.email

    @property
    def version(self) -> str:
        """Return the version of the last tag in the git repo.

        """
        return self.tag.last_tag

    @property
    def entry_points(self):
        """Return the entry points (i.e. console application script), if any.

        """
        if hasattr(self, 'console_script'):
            script = self.console_script
        else:
            m = re.match(r'.*\.(.+?)$', self.name)
            if m:
                script = m.group(1)
            else:
                script = self.name
        return {'console_scripts': ['{}={}:main'.format(script, self.name)]}

    def get_properties(self, paths: bool = False) -> \
            Tuple[List[str], Dict[str, str]]:
        """Return the properties used by ``setuptools``.

        """
        fields = self.FIELDS.split()
        if paths:
            fields.extend('setup_path root_path'.split())
        if self.has_entry_points:
            fields.append('entry_points')
        fset = set(fields)
        logger.debug(f'fields: {fset}')
        props = {'long_description_content_type': 'text/markdown'}
        members = inspect.getmembers(self)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f'all members: {members}')
        for mem in filter(lambda x: x[0] in fset, members):
            logger.debug(f'member: {mem}')
            val = mem[1]
            if val is not None:
                props[mem[0]] = mem[1]
        return fields, props

    def write(self, depth: int = 0, writer: TextIOWrapper = sys.stdout):
        sp = ' ' * (depth * 4)
        fields, props = self.get_properties(False)
        if 'long_description' in props:
            props['long_description'] = props['long_description'][0:20] + '...'
        for field in fields:
            if field in props:
                writer.write(f'{sp}{field}={props[field]}\n')

    def get_info(self) -> Dict[str, Union[str, dict]]:
        props = self.get_properties(True)[1]
        for path in 'setup_path root_path'.split():
            props[path] = str(props[path].absolute())
        props['build'] = self.tag.build_info
        short_description = self.short_description
        if short_description:
            props['short_description'] = short_description
        props['user'] = self.user
        props['project'] = self.project
        props['remotes'] = tuple(self.remote_set)
        return props

    def to_json(self, indent: int = 4, writer: TextIOWrapper = sys.stdout) -> str:
        json.dump(self.get_info(), writer, indent=indent)

    def setup(self):
        """Called in the ``setup.py`` to invoke the Python ``setuptools`` package.
        This assembles the information needed and calls ``setuptools.setup``.

        :py:func:`setuptools:setup`

        """
        if self.DO_SETUP:
            _, props = self.get_properties()
            sio = StringIO()
            self.write(writer=sio)
            logger.info('setting up with: ' + sio.getvalue())
            setuptools.setup(**props)
        else:
            return self

    @classmethod
    def source(cls, start_path: Path = Path('.').absolute(),
               rel_setup_path: Path = Path('src/python/setup.py'),
               var: str = 'su'):
        """Source the ``setup.py`` ``setuptools`` file to get an instance of this class
        to be used in other APIs that want to access build information.  This
        is done by using ``exec`` to evaluate the ``setup.py`` file and
        skipping the call to ``setuptools.setup``.

        :param rel_setup_path: the relative path to the ``setup.py`` file,
                               which defaults to ``src/python/setup.py`` per
                               standard Zensols build

        :param start_path: the path to start looking for the ``rel_setup_path``

        :param var: the name of the variable that was was in ``setup.py`` for
                    the instantiation of this class

        """
        logger.debug(f'sourcing: start={start_path}, ' +
                     f'rel_setup_path={rel_setup_path}')
        do_setup = cls.DO_SETUP
        try:
            cls.DO_SETUP = False
            root = cls.find_root(start_path)
            setup_path = root / rel_setup_path
            logger.debug(f'found root: {root}, setup path = {setup_path}')
            setup_path = setup_path.absolute()
            logger.debug(f'loading setup file from {setup_path}')
            with open(setup_path) as f:
                code = f.read()
            locs = {'__file__': str(setup_path)}
            exec(code, locs)
            return locs[var]
        finally:
            cls.DO_SETUP = do_setup
