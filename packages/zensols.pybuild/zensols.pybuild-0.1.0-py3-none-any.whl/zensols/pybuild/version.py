"""A helper class for version formatting.

"""
__author__ = 'Paul Landes'

import re


class Version(object):
    """A container class for a tag version.  All tags have an implicit format by
    sorting in decimal format (i.e. ``<major>.<minor>.<version>``).  This class
    contains methods that make it sortable.

    """
    def __init__(self, major=0, minor=0, debug=1):
        self.major = major
        self.minor = minor
        self.debug = debug

    @classmethod
    def from_string(clz, s):
        """Create a version instance from a string formatted version.

        :return: a new instance of ``Version``

        """
        m = re.search(r'^v?(\d+)\.(\d+)\.(\d+)$', s)
        if m is not None:
            return Version(int(m.group(1)), int(m.group(2)), int(m.group(3)))

    def format(self, prefix='v') -> str:
        """Return a formatted string version of the instance.

        """
        return prefix + '{major}.{minor}.{debug}'.format(**self.__dict__)

    def increment(self, decimal='debug', inc=1):
        """Increment the version in the instance.  By default the debug portion of the
        instance is incremented.

        """
        if decimal == 'major':
            self.major += inc
        elif decimal == 'minor':
            self.minor += inc
        elif decimal == 'debug':
            self.debug += inc
        else:
            raise ValueError('uknown decimal type: {}'.format(decimal))

    def __lt__(self, o):
        if self.major < o.major:
            return True
        if self.major > o.major:
            return False

        if self.minor < o.minor:
            return True
        if self.minor > o.minor:
            return False

        if self.debug < o.debug:
            return True
        if self.debug > o.debug:
            return False

        # equal
        return False

    def __le__(self, o):
        if self.major <= o.major:
            return True
        if self.major >= o.major:
            return False

        if self.minor <= o.minor:
            return True
        if self.minor >= o.minor:
            return False

        if self.debug <= o.debug:
            return True
        if self.debug >= o.debug:
            return False

        # equal
        return False

    def __eq__(self, o):
        return self.__dict__ == o.__dict__

    def __str__(self):
        return self.format()

    def __repr__(self):
        return self.__str__()
