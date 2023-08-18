from koil.helpers import unkoil, unkoil_gen
from unlok.rath import current_unlok_rath
from unlok.rath import UnlokRath


def execute(operation, variables, rath: UnlokRath = None):
    return unkoil(aexecute, operation, variables, rath)


async def aexecute(operation, variables, rath: UnlokRath = None):
    rath = rath or current_unlok_rath.get()
    x = await rath.aquery(
        operation.Meta.document, operation.Arguments(**variables).dict(by_alias=True)
    )
    return operation(**x.data)


def subscribe(operation, variables, rath: UnlokRath = None):
    return unkoil_gen(asubscribe, operation, variables, rath)


async def asubscribe(operation, variables, rath: UnlokRath = None):
    rath = rath or current_unlok_rath.get()
    async for event in rath.asubscribe(
        operation.Meta.document, operation.Arguments(**variables).dict(by_alias=True)
    ):
        yield operation(**event.data)
