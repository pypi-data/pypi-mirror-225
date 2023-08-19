from ..context_processors import (
    DeployfishTasksDeployProcessor,
    CodebuildProcessor,
    GitProcessor,
    NameVersionProcessor
)
from .base import Message


class DeployfishTasksDeployStartMessage(Message):
    """
    Send a slack message about starting a deployfish tasks deploy.
    """

    template = 'deploy_tasks_start.tpl'
    context_processors = [
        NameVersionProcessor,
        DeployfishTasksDeployProcessor,
        CodebuildProcessor,
        GitProcessor,
    ]


class DeployfishTasksDeploySuccessMessage(Message):
    """
    Send a slack message about a successful deployfish tasks deploy.
    """
    template = 'deploy_tasks_success.tpl'
    context_processors = [
        NameVersionProcessor,
        DeployfishTasksDeployProcessor,
        CodebuildProcessor,
        GitProcessor,
    ]


class DeployfishTasksDeployFailureMessage(Message):
    """
    Send a slack message about an unsuccessful deployfish tasks deploy.
    """
    template = 'deploy_tasks_failed.tpl'
    context_processors = [
        NameVersionProcessor,
        DeployfishTasksDeployProcessor,
        CodebuildProcessor,
        GitProcessor,
    ]
