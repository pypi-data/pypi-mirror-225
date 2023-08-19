from typing import Optional

from ..typedefs import MessageContext
from .base import AbstractContextProcessor


class GenericProcessor(AbstractContextProcessor):
    """
    Adds the following keys to the context:

    * ``label``: a user supplied label we got from the --label command line option
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.label: Optional[str] = kwargs['label']

    def annotate(self, context: MessageContext) -> None:
        context['label'] = self.label
