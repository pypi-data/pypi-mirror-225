import pathlib
import subprocess


from ..typedefs import MessageContext
from .base import AbstractContextProcessor


class NameVersionProcessor(AbstractContextProcessor):
    """
    A context processor that adds the following keys to the context:

    * ``name``: the project name
    * ``version``: the current version of the project

    If this is a python project, we'll get the name and version from setup.py.

    If not, we'll try to get it from Makefile by doing ``make image_name``
    for the name and ``make version`` for the version.
    """

    def annotate(self, context: MessageContext) -> None:
        """
        Add the following keys to ``context``:

        * ``name``: the project name
        * ``version``: the current version of the project

        If this is a python project, we'll get the name and version from
        setup.py.

        If not, we'll try to get it from Makefile by doing ``make image_name``
        for the name and ``make version`` for the version.

        Args:
            context: the current message context
        """
        super().annotate(context)
        setup_py = pathlib.Path.cwd() / 'setup.py'
        if setup_py.exists():
            context['version'] = subprocess.run(
                ['python', str(setup_py), '--version'],
                capture_output=True,
                text=True,
                check=True
            ).stdout.strip()
            context['name'] = subprocess.run(
                ['python', str(setup_py), '--name'],
                capture_output=True,
                text=True,
                check=True
            ).stdout.strip()
        else:
            # No setup.py; let's try Makefile
            makefile = pathlib.Path.cwd() / 'Makefile'
            if makefile.exists():
                context['name'] = subprocess.check_output(['make', 'image_name']).decode('utf8').strip()
                context['version'] = subprocess.check_output(['make', 'version']).decode('utf8').strip()
