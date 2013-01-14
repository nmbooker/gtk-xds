
"""Find the source under the current working directory.
"""

import os
import glob

def chdir_source(config):
    """Find and chdir to the source tree.
    """
    source = config.source_package()
    old_wd = os.getcwd()
    os.chdir('build')
    try:
        source_dirs = glob.glob('%s*/' % source)
        source_dir = source_dirs[0]
        os.chdir(source_dir)
    except:
        os.chdir(old_wd)
        raise
    return
