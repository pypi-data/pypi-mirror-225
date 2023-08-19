from typing import Optional

from ..typedefs import MessageContext
from .base import AbstractContextProcessor


class SphinxProcessor(AbstractContextProcessor):
    """
    A context processor that adds the following keys to the context:

    * ``url``: the URL to the Sphinx documentation that was built for
      during this pipeline run.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.url: Optional[str] = kwargs.get('url', None)

    def annotate(self, context: MessageContext) -> None:
        if self.url:
            context['docs_url'] = f'<{self.url}|Click here>'
