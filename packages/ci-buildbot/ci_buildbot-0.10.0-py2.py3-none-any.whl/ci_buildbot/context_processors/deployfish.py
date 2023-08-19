from typing import List

from ..typedefs import MessageContext
from .base import AbstractContextProcessor


class DeployfishDeployProcessor(AbstractContextProcessor):
    """
    Adds the following keys to the context:

    * ``service``: the name of the ECS service being deployed
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.service: str = kwargs['service']

    def annotate(self, context: MessageContext) -> None:
        context['service'] = self.service


class DeployfishTasksDeployProcessor(AbstractContextProcessor):
    """
    Adds the following keys to the context:

    * ``tasks``: a list of the names of the ECS tasks being deployed
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.tasks: List[str] = kwargs['tasks']

    def annotate(self, context: MessageContext) -> None:
        context['tasks'] = self.tasks
