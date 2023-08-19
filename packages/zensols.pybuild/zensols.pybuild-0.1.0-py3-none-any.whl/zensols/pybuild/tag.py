"""A utility class that represents a Git tag.

"""
__author__ = 'Paul Landes'

from typing import Dict, List, Union
import logging
import sys
from io import TextIOWrapper
import json
from pathlib import Path
from datetime import datetime
from git import Repo, TagReference
from zensols.pybuild import Version

logger = logging.getLogger(__name__)


class Tag(object):
    """Represents a Git tag.  It's main use is determining the last tag in a sorted
    (by version) used to increment to the next version.  However, it also
    creates tags and provides additional information about existing tags.

    All tags have an implicit format by sorting in decimal format
    (i.e. ``<major>.<minor>.<version>``).

    """
    def __init__(self, repo_dir: Path = Path('.'), message: str = 'none',
                 dry_run: bool = False):
        """Initialize.

        :param repo_dir: the root Git repo directory
        :param message: the message to use when creating new tags
        :param dry_run: if ``True`` do not create new tags
        """
        logger.debug('creating tag witih repo dir: {}'.format(repo_dir))
        if isinstance(repo_dir, Path):
            repo_dir = str(repo_dir.resolve())
        self.repo = Repo(repo_dir)
        assert not self.repo.bare
        self.message = message
        self.dry_run = dry_run

    def get_entries(self) -> List[Dict[str, str]]:
        """Return a list of dicts, each with information about the tag.

        Keys::
            - name: the name of the tag
            - ver: the version of the tag (in format ``v<major>.<minor>.<debug>``)
            - date: date the tag was created
            - tag: the tag without the prefix (i.e. sans ``v``)
            - message: the comment given at tag creation
        """
        tags = self.repo.tags
        logger.debug('tags: {}'.format(tags))
        tag_entries = []
        for tag in tags:
            logger.debug('{} ({})'.format(tag, type(tag)))
            name = str(tag)
            ver = Version.from_string(name)
            date = None
            if hasattr(tag.object, 'tagged_date'):
                date = tag.object.tagged_date
            if ver is not None:
                tag_entries.append({'name': name,
                                    'ver': ver,
                                    'date': date,
                                    'tag': tag,
                                    'message': tag.object.message})
        tag_entries = sorted(tag_entries, key=lambda t: t['ver'])
        return tag_entries

    @property
    def last_tag_entry(self) -> Dict[str, str]:
        """Return the last entry given by ``get_entries``.

        :py:meth:`Tag.get_entries`
        """
        entries = self.get_entries()
        logger.debug('entires: {}'.format(entries))
        if (len(entries) > 0):
            return entries[-1]

    @property
    def last_tag(self) -> str:
        """Return the last tag.

        """
        entry = self.last_tag_entry
        if entry:
            return entry['ver'].format(prefix='')

    @property
    def last_commit(self):
        """Return rhe last commit ID (sha1).

        """
        commits = list(self.repo.iter_commits('HEAD'))
        if len(commits) > 0:
            return commits[0]

    @property
    def build_info(self) -> Dict[str, Union[str, dict]]:
        """Return information about the last commit and a build time with the current
        time.

        """
        inf = {'build_date': datetime.now().isoformat()}
        last_entry = self.last_tag_entry
        if last_entry:
            tag = last_entry['tag']
            message = None
            if hasattr(tag.object, 'message'):
                message = tag.object.message
            inf.update({'tag': last_entry['ver'].format(prefix=''),
                        'name': last_entry['name'],
                        'message': message})
        c = self.last_commit
        if c:
            inf['commit'] = {'author': str(c.author),
                             'date': c.committed_datetime.isoformat(),
                             'sha': str(c),
                             'summary': c.summary}
        return inf

    def to_json(self, indent: int = 4, writer: TextIOWrapper = sys.stdout) -> str:
        """Return build information in JSON format.

        """
        json.dump(self.build_info, writer, indent=4)

    def delete_last_tag(self):
        """Delete the last commit tag.

        """
        entry = self.last_tag_entry
        tag = entry['tag']
        name = entry['name']
        logger.info('deleting: {}'.format(name))
        if not self.dry_run:
            TagReference.delete(self.repo, tag)

    def recreate_last_tag(self):
        """Delete the last tag and create a new one on the latest commit.

        """
        entry = self.last_tag_entry
        tag = entry['tag']
        name = entry['name']
        msg = entry['message']
        logger.info('deleting: {}'.format(name))
        if not self.dry_run:
            TagReference.delete(self.repo, tag)
        logger.info('creating {} with commit <{}>'.format(name, msg))
        if not self.dry_run:
            TagReference.create(self.repo, name, message=msg)

    def create(self):
        """Create a new tag on the latest commit.

        """
        entry = self.last_tag_entry
        if entry is None:
            ver = Version.from_string('v0.0.0')
        else:
            ver = entry['ver']
        ver.increment('debug')
        new_tag_name = str(ver)
        logger.info('creating {} with commit <{}>'.format(
            new_tag_name, self.message))
        if not self.dry_run:
            TagReference.create(self.repo, new_tag_name, message=self.message)
