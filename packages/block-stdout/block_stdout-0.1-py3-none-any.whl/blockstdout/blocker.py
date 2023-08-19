import os
import sys


class BlockPrint:
    """A context manager that blocks the standard output, preventing print statements from being displayed.

    >>> BlockPrint

    """

    def __enter__(self):
        """Redirects the standard output to os.devnull, suppressing print statements."""
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_value, traceback):
        """Restores the original standard output."""
        sys.stdout.close()
        sys.stdout = self._original_stdout
