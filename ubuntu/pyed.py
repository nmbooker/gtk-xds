
"""Edit a text file line-by-line within Python scripts.
"""

import os.path
import errno


class PyEdError(Exception):
    pass

class LineOutOfRange(PyEdError):
    pass

class AtTopOfFile(LineOutOfRange):
    pass

class PastEndOfBuffer(LineOutOfRange):
    pass

class BufferEmpty(PyEdError):
    pass

class CursorFrozen(PyEdError):
    pass

class TextEditor(object):
    """Treat a text file as a series of lines.

    You can edit it with known line numbers, or you can navigate
    around the file line-by-line replacing, inserting and deleting lines
    of text as you go.
    """


    def __init__(self):
        self._lines = []
        # _lineno 0 is just above the first line.
        # Line numbers start from 1, just like in text editors and other
        # file descriptions.
        self._lineno = 0
        self._cursor_frozen = False

    def load(self, filename):
        """Load text in from a named file.

        The buffer is cleared, and its contents replaced with those of the
        named file.
        """
        infile = open(filename, 'r')
        try:
            lines = infile.readlines()
        finally:
            infile.close()
        self.clear()
        self._lines = [l.rstrip('\n') for l in lines]

    def save(self, filename, append=False, fail_if_exists=False):
        """Save text to a named file.

        append: Append to the file instead of overwriting.
        fail_if_exists: Raise an exception if a file of the same name already exists.
        """
        if fail_if_exists:
            if os.path.exists(filename):
                exc = IOError(errno.EEXIST, "File exists", filename)
                raise exc
        if append:
            mode = 'a'
        else:
            mode = 'w'
        outfile = open(filename, mode)
        try:
            outfile.writelines((l + '\n') for l in self._lines)
        finally:
            outfile.close()

    def clear(self):
        """Clear the text buffer of all lines of text.
        """
        self._lines = []

    def up(self, n_lines=1):
        """Move up the file n lines, default is 1"""
        self.down(-n_lines)

    def down(self, n_lines=1):
        """Move down the file n lines, default is 1"""
        self.goto_line(self._lineno + n_lines)

    def goto_line(self, target_line):
        self._validate_lineno(target_line)
        self._lineno = target_line

    def _validate_lineno(self, target_line):
        """Check the target line number is somewhere in the file."""
        if target_line < 1:
            raise AtTopOfFile()
        elif target_line > self.number_of_lines():
            raise PastEndOfBuffer(str(target_line))

    def number_of_lines(self):
        """Return the number of lines in the buffer."""
        return len(self._lines)

    def last_line_number(self):
        """Give the last line number.

        Raise BufferEmpty if the buffer has no lines.
        """
        self._assert_buffer_not_empty()
        return self.number_of_lines()

    def first_line_number(self):
        """Give the first line number.

        Raise BufferEmpty if the buffer has no lines.
        """
        self._assert_buffer_not_empty()
        return 1

    def buffer_is_empty(self):
        """Return whether the buffer is currently empty.
        """
        return self.number_of_lines() == 0

    def _assert_buffer_not_empty(self):
        """Raise BufferEmpty if the buffer is currently empty."""
        if self.buffer_is_empty():
            raise BufferEmpty()

    def new_line(self, text='', above=False):
        """Insert a new line containing the given text, and move to that new line.

        above: If True, the line is inserted above the current one.
               If False, the line is inserted below.
        """
        if above:
            target_line = self.line_number()
        else:
            target_line = self.line_number() + 1
        self._lines.insert(self._line_index(target_line), text)
        self.goto_line(target_line)

    def line_number(self):
        return self._lineno

    def line_text(self, lineno=None):
        """Return the text contained in the current line."""
        self._assert_buffer_not_empty()
        return self._lines[self._line_index(lineno)]

    def _line_index(self, lineno=None):
        if lineno is None:
            lineno = self._lineno
        return lineno - 1

    def line_numbers(self):
        """List of the line numbers 1..number_of_lines.
        """
        return range(1, self.number_of_lines() + 1)

    def iter_line_numbers(self):
        """Iterate over the line numbers 1..number_of_lines."""
        return xrange(1, self.number_of_lines() + 1)

    def delete_line(self, lineno=None):
        """Delete the current line or the line number specified."""
        if lineno is None:
            lineno = self.line_number()
        self._validate_lineno(lineno)
        del self._lines[self._line_index(lineno)]
        if lineno > self.number_of_lines():
            lineno -= 1
        if lineno > 0:
            self.goto_line(lineno)

    def _resolve_lineno(self, lineno):
        """Resolve a line number parameter.

        Basically changes a 'None' lineno to the current line.
        """
        if lineno is None:
            return self.line_number()
        return lineno

    def replace_line(self, text, lineno=None):
        lineno = self._resolve_lineno(lineno)
        self._validate_lineno(lineno)
        self._lines[self._line_index(lineno)] = text

    def line_search(self, regex, lineno=None):
        """Search current or numbered line for a compiled regex."""
        return regex.search(self.line_text(lineno))

    def edit_line(self):
        return LineEditor(self.line_text(), self)

    def freeze_cursor(self):
        self._cursor_frozen = True

    def unfreeze_cursor(self):
        self._cursor_frozen = False

    # TODO: assert the cursor isn't frozen at start of each operation
    # that can move the cursor.
    def _assert_cursor_not_frozen(self):
        if self._cursor_frozen:
            raise CursorFrozen()

class LineEditor(object):
    """Edit a single line.
    """
    def __init__(self, string, editor):
        self._editor = editor
        self._chars = self._explode(string)
        self._in_with = False
        self._cancelled = False
        self._cursor = None         # '0' means 'before start', '1' means first character
        self.goto_start()

    def get_string(self):
        return u''.join(self._chars)

    def __str__(self):
        return str(self.get_string())

    def __unicode__(self):
        return unicode(self.get_string())

    def __enter__(self):
        self._freeze_editor()    # prevent parent moving in file
        self._in_with = True
        return self

    def __exit__(self, exc_type, exc_value, ext_traceback):
        self._unfreeze_editor()
        if not exc_type:
            self.save()
        self._in_with = False

    def cancel_edit(self):
        self._cancelled = True

    def save(self):
        if not self._cancelled:
            self._editor.replace_line(self.get_string())

    def replace_whole_line(self, string):
        self._chars = [char for char in string]
        self.goto_start()

    def goto_start(self):
        if len(self._chars) == 0:
            self._cursor = 0
        else:
            self._cursor = 1

    def goto_end(self):
        self._cursor = len(self._chars)

    def goto_left(self):
        self._cursor -= 1

    def goto_right(self):
        self._cursor += 1

    def __len__(self):
        return len(self._chars)

    def char(self, pos=None):
        """Return the character under the cursor."""
        if pos is None:
            pos = self.pos()
        return self._chars[self._to_index(pos)]

    def pos(self):
        """Return the current position of the cursor (column number)."""
        return self._cursor

    def goto_char(self, char, left=False):
        """Move cursor to the next occurrence of the given character.

        Like 'f' in vim.

        left: Search to the left instead of the right.  Like 'F' in vim.
        """

        index = None        # Make sure index is in scope
        if left:
            # can't use list.index() because it searches forwards not
            # backwards.
            for index in reversed(range(self._to_index(self.pos()))):
                if self._chars[index] == char:
                    break
            else:   # didn't find char
                raise ValueError('Character not found: %r' % char)
        else:
            # can use list.index() for this
            start = self._to_index(self.pos() + 1)  # at next position
            index = self._chars.index(char, start)
        # If got here, the character was found
        self._cursor = self._to_cursor_pos(index)
        return self.pos()

    def _to_index(self, cursor):
        """Return the list index of the given cursor position"""
        return cursor - 1

    def _to_cursor_pos(self, index):
        """Return the cursor position corresponding to the given list index
        """
        return index + 1

    def insert_left(self, text):
        """Insert a string to the left of the current cursor.

        The new cursor position will be on the last character of the
        newly-inserted text.
        """
        new_chars = self._explode(text)
        current_pos = self.pos()
        # Will go to the last character of the newly inserted string.
        # Makes it consistent if it happens to be the end of line, and also
        # makes it consistent with Vim.
        new_pos = current_pos + len(self) - 1
        index = self._to_index(current_pos)
        new_text = self._chars[:index]
        rest = self._chars[index:]
        new_text.extend(new_chars)
        new_text.extend(rest)
        self._chars = new_text
        self._cursor = new_pos
        return new_pos

    def _explode(self, text):
        """Return list of characters in the text.
        """
        return list(text)

    def _freeze_editor(self):
        self._editor.freeze_cursor()

    def _unfreeze_editor(self):
        self._editor.unfreeze_cursor()


def print_buffer(editor):
    for lineno in editor.iter_line_numbers():
        print(editor.line_text(lineno))
