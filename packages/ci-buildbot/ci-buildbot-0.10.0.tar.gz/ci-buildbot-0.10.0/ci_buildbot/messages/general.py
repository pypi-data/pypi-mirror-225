from ..context_processors import (
    GenericProcessor,
    CodebuildProcessor,
    GitProcessor,
    NameVersionProcessor
)
from .base import Message


class GeneralStartMessage(Message):

    template = 'general_start.tpl'
    context_processors = [
        NameVersionProcessor,
        GenericProcessor,
        GitProcessor,
        CodebuildProcessor,
    ]


class GeneralSuccessMessage(Message):

    template = 'general_success.tpl'
    context_processors = [
        NameVersionProcessor,
        GenericProcessor,
        GitProcessor,
        CodebuildProcessor,
    ]


class GeneralFailureMessage(Message):

    template = 'general_failed.tpl'
    context_processors = [
        NameVersionProcessor,
        GenericProcessor,
        GitProcessor,
        CodebuildProcessor,
    ]
