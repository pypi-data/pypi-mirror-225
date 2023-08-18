from pydantic import Field
from koil import koilable
from koil.composition import Composition
from unlok.rath import UnlokRath


@koilable(add_connectors=True)
class Unlok(Composition):
    rath: UnlokRath = Field(default_factory=UnlokRath)

    def _repr_html_inline_(self):
        return f"<table><tr><td>rath</td><td>{self.rath._repr_html_inline_()}</td></tr></table>"
