from ..context_processors import (
    GitProcessor,
    NameVersionProcessor,
    CodebuildProcessor,
    DeployfishDeployProcessor
)
from .base import Message


class DeployfishDeployStartMessage(Message):
    """
    Send a slack message about starting a deployfish service deploy.
    """
    template = 'deploy_start.tpl'
    context_processors = [
        NameVersionProcessor,
        DeployfishDeployProcessor,
        GitProcessor,
        CodebuildProcessor,
    ]


class DeployfishDeploySuccessMessage(Message):
    """
    Send a slack message about a successful deployfish service deploy.
    """
    template = 'deploy_success.tpl'
    context_processors = [
        NameVersionProcessor,
        DeployfishDeployProcessor,
        GitProcessor,
        CodebuildProcessor,
    ]


class DeployfishDeployFailureMessage(Message):
    """
    Send a slack message about a unsuccessful deployfish service deploy.
    """
    template = 'deploy_failed.tpl'
    context_processors = [
        NameVersionProcessor,
        DeployfishDeployProcessor,
        GitProcessor,
        CodebuildProcessor,
    ]
