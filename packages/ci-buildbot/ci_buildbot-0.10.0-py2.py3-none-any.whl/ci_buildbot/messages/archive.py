
from ..context_processors import (
    GitProcessor,
    GitChangelogProcessor,
    CodebuildProcessor,
    NameVersionProcessor
)
from .base import Message


class ArchiveCodeMessage(Message):
    """
    Used to send a slack message about archiving code tarballs to an artifactory.
    """

    template = 'archive.tpl'
    context_processors = [
        NameVersionProcessor,
        GitProcessor,
        GitChangelogProcessor,
        CodebuildProcessor,
    ]
