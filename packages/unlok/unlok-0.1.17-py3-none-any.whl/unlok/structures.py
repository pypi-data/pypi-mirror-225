""" Strucutre Registration

"""


from unlok.api.schema import ScopeFragment, Search_scopesQuery, aaget_scope


async def key_shrink(k):
    return k.key


try:
    from rekuest.structures.default import get_default_structure_registry, Scope
    from rekuest.widgets import SearchWidget

    structure_reg = get_default_structure_registry()
    structure_reg.register_as_structure(
        ScopeFragment,
        identifier="@lok/scope",
        scope=Scope.GLOBAL,
        aexpand=aaget_scope,
        ashrink=key_shrink,
        default_widget=SearchWidget(query=Search_scopesQuery.Meta.document, ward="lok"),
    )

except ImportError:
    structure_reg = None
