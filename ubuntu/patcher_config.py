#! /usr/bin/env python

"""Make sure you don't os.chdir() until AFTER you have imported this.
"""

import ConfigParser
import os

IMPORTED_WD = os.getcwd()

class Config(object):
    """Configuration for patch scripts for GTK DnD.
    """
    def __init__(self):
        self.config = ConfigParser.RawConfigParser()
        self.config.read(os.path.join(IMPORTED_WD, 'build.ini'))

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
        return self.config.get('meta', 'author')

    def patch_origin(self):
        return self.config.get('meta', 'origin')
