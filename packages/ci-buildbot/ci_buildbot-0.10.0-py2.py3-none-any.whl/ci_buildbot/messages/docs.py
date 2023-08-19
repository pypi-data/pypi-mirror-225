from ..context_processors import (
    NameVersionProcessor,
    GitProcessor,
    CodebuildProcessor,
)
from .base import Message


class DocsStartMessage(Message):
    """
    Send a slack message about starting a Sphinx docs build.
    """
    template = 'docs_start.tpl'
    context_processors = [
        NameVersionProcessor,
        GitProcessor,
        CodebuildProcessor,
    ]


class DocsSuccessMessage(Message):
    """
    Send a slack message about a successful Sphinx docs build.
    """
    template = 'docs_success.tpl'
    context_processors = [
        NameVersionProcessor,
        GitProcessor,
        CodebuildProcessor,
    ]


class DocsFailureMessage(Message):
    """
    Send a slack message about an unsuccessful Sphinx docs build.
    """
    template = 'docs_failed.tpl'
    context_processors = [
        NameVersionProcessor,
        GitProcessor,
        CodebuildProcessor,
    ]
