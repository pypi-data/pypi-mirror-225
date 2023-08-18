""" This module provides helpers for the mikro rath api
they are wrapped functions for the turms generated api"""
from .rath import MikroNextRath, current_mikro_next_rath
from koil.helpers import unkoil, unkoil_gen


async def aexecute(
    operation,
    variables,
    rath: MikroNextRath = None,
):
    rath = rath or current_mikro_next_rath.get()

    x = await rath.aquery(
        operation.Meta.document,
        operation.Arguments(**variables).dict(by_alias=True),
    )
    return operation(**x.data)


def execute(
    operation,
    variables,
    rath: MikroNextRath = None,
):
    return unkoil(aexecute, operation, variables, rath=rath)


def subscribe(operation, variables, rath: MikroNextRath = None):
    return unkoil_gen(asubscribe, operation, variables, rath=rath)


async def asubscribe(operation, variables, rath: MikroNextRath = None):
    rath = rath or current_mikro_next_rath.get()
    async for event in rath.asubscribe(
        operation.Meta.document, operation.Arguments(**variables)
    ):
        yield operation(**event.data)
