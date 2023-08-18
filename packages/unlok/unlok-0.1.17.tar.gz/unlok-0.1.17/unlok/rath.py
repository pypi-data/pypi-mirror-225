import contextvars

from pydantic import Field

from rath import rath
from rath.links.aiohttp import AIOHttpLink
from rath.links.auth import AuthTokenLink
from rath.links.compose import TypedComposedLink
from rath.links.dictinglink import DictingLink

current_unlok_rath = contextvars.ContextVar("current_unlok_rath")


class UnlokLinkComposition(TypedComposedLink):
    dicting: DictingLink = Field(default_factory=DictingLink)
    auth: AuthTokenLink
    split: AIOHttpLink

    def _repr_html_inline_(self):
        return f"<table><tr><td>refresh attempts</td><td>{self.auth.maximum_refresh_attempts}</td></tr></table>"


class UnlokRath(rath.Rath):
    link: UnlokLinkComposition

    async def __aenter__(self):
        await super().__aenter__()
        current_unlok_rath.set(self)
        return self

    def _repr_html_inline_(self):
        return f"<table><tr><td>link</td><td>{self.link._repr_html_inline_()}</td></tr></table>"

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await super().__aexit__(exc_type, exc_val, exc_tb)
        current_unlok_rath.set(None)
