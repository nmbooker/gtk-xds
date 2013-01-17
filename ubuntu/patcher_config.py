#! /usr/bin/env python

"""Make sure you don't os.chdir() until AFTER you have imported this.
"""

import ConfigParser
import os

IMPORTED_WD = os.getcwd()

def fullpath():
    return os.path.join(IMPORTED_WD, 'build.ini')

class Config(object):
    """Configuration for patch scripts for GTK DnD.
    """
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = fullpath()
        self.config = ConfigParser.RawConfigParser()
        self.config.read(config_path)
        self.config_path = config_path

    def source_package(self):
        return self.config.get('package', 'source_package')

    def patches_subdir(self):
        return self.config.get('package', 'patches_subdir')

    def patches_fullpath(self):
        subdir = self.patches_subdir()
        return os.path.realpath(os.path.join(IMPORTED_WD, subdir))

    def version_suffix(self):
        return self.config.get('meta', 'version_suffix')

    def patch_author(self):
        fullname = self.patch_fullname()
        email = self.patch_email()
        return "%s <%s>" % (fullname, email)

    def patch_origin(self):
        return self.config.get('meta', 'origin')

    def patch_email(self):
        return self.config.get('meta', 'email')

    def patch_fullname(self):
        return self.config.get('meta', 'fullname')
