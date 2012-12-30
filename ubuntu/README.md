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

## Script: ../patch\_source

```console
$ cd gtk2-precise     # for example
$ ../patch_source
```

`patch\_source` is a work-in-progress script to apply the patch and
automatically 'commit' it to the local source package, in preparation
for building binaries.

Currently, it gets as far as replacing the short and detailed descriptions
at the top of the patch file, and it knows where to find the line specifying
the version number, but not how to change the version just yet.

Also, because it uses `dpkg-source --commit` to generate an initial patch
file it opens up the unedited version of the patch in the text editor
(vim in my case) before then proceeding to make the changes it can.

It then opens up the editor again, so I can finish the job off manually.

So the first time the editor is loaded, you should exit it without making
any changes.  When it opens again, the file will have been changed by the
script and is ready for edits to be completed manually if necessary.

The plan is to keep shoving more and more of the editing process into
this script rather than having to do it manually each time, and to try to
eliminate the initial invocation of the editor.

## Module: pyed.py
`patch\_source` uses the Python module `pyed`, developed alongside,
to do the editing.  `pyed.py` is a generic line-based text editor,
which I've written alongside this script to simulate the line navigation
and manipulation in vim, so I can quickly translate my actions within vim
into Python code for doing the same edits.
As it's generic, I may extract it into its own project in the near future.

Examples are, I can jump to a specific line number (starting from 1 as is
the usual convention when numbering lines in files), move up() or down() one
or more lines relative to my current position, search() for the next
line matching a specific regular expression, etc.
Once I've found the line, I can get the ```line_text()```, ```replace_line()```, ```delete_line()```
or ```insert_line()``` before or after the current line.  Each can also take
a specific line number to treat as current line without having to affect
the location of the file pointer.

### Planned Features

I plan a ```LineEditor``` class that will let me see a specific line and,
yet again, do vi-like commands on it.  It might look like:

```python

with editor.edit_line() as line:
    line.to_start()
    line.to_char(")")
    line.insert_left("~xds1")
    line.re_sub(r'precise-proposed', r'precise')

editor.search(re.compile(r'^Author: '))

with editor.edit_line() as line:
    line.to_start()
    line.to_char(' ')
    line.to_right()    # Put cursor on start of author's name
    line.replace_to(END, 'Fred Bloggs <fred@example.com>')
```

The editor should have a ```cancel_edit()``` method to prevent saving back
at the end of the ```with``` block, and ```__str__()``` and ```__unicode___``` methods.  A ```save()``` method should allow use without a ```with```
block.

## Preparing build environment

```
sudo apt-get install build-essential autoconf automake dpkg-dev devscripts
sudo apt-get build-dep gtk+2.0
sudo apt-get build-dep gtk+3.0
```
