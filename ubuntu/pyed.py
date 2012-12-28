
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

    def line_match(self, regex, lineno=None):
        """Match current or numbered line against a compiled regex."""
        return regex.match(self.line_text(lineno))

def print_buffer(editor):
    orig_line_number = editor.line_number()
    for lineno in editor.iter_line_numbers():
        print(editor.line_text(lineno))
