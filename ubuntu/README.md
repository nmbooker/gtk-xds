Building Ubuntu Packages
========================

This 'ubuntu' directory is for building Ubuntu (and possibly Debian)
packages for your platform.

The scripts in this directory, unless otherwise noted, should be run in
the gtk2 or gtk3 subdirectories, e.g.:

```
cd gtk2
../clean
../get_source
```

The `build.ini` files in the gtk2 and gtk3 subdirectories specify what
source packages to download among other things.

The build actually happens in the `build` directory.

## Script: ../clean

Running the `clean` script will delete the `build` directory and all of the
files held within.  Run this before building a new version.

## Script: ../get\_source

Running the `get\_source` script will make a new `build` directory and get
the source latest source code release using `apt-get source`.
