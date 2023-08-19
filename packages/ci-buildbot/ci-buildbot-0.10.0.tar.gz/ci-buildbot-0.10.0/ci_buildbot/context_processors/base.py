from abc import ABC, abstractmethod
from ..typedefs import MessageContext


class AbstractContextProcessor(ABC):
    """
    Base class for all context processors.
    """

    def __init__(self, **kwargs):
        """
        Args:
            kwargs: the keyword arguments passed to the context processor
        """
        ...

    @abstractmethod
    def annotate(self, context: MessageContext) -> None:
        """
        Add values to the message context ``context``.

        Args:
            context: the current message context
        """
        ...
