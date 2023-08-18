from pydantic import Field
from .links.upload import UploadLink
from rath import rath
import contextvars
from rath.links.auth import AuthTokenLink
from rath.links.compose import TypedComposedLink
from rath.links.dictinglink import DictingLink
from rath.links.file import FileExtraction
from rath.links.split import SplitLink

current_mikro_next_rath= contextvars.ContextVar("current_mikro_next_rath")


class MikroNextLinkComposition(TypedComposedLink):
    fileextraction: FileExtraction = Field(default_factory=FileExtraction)
    dicting: DictingLink = Field(default_factory=DictingLink)
    upload: UploadLink
    auth: AuthTokenLink
    split: SplitLink


class MikroNextRath(rath.Rath):
    """Mikro Rath

    Mikro Rath is the GraphQL client for mikro_next It is a thin wrapper around Rath
    that provides some default links and a context manager to set the current
    client. (This allows you to use the `mikro_nextrath.current` function to get the
    current client, within the context of mikro app).

    This is a subclass of Rath that adds some default links to convert files and array to support
    the graphql multipart request spec."""

    link: MikroNextLinkComposition

    def _repr_html_inline_(self):
        return (
            f"<table><tr><td>auto_connect</td><td>{self.auto_connect}</td></tr></table>"
        )

    async def __aenter__(self):
        await super().__aenter__()
        current_mikro_next_rath.set(self)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await super().__aexit__(exc_type, exc_val, exc_tb)
        current_mikro_next_rath.set(None)
