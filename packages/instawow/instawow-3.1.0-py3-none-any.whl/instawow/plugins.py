from __future__ import annotations

from collections.abc import Iterable
from functools import lru_cache
from typing import Protocol, cast

import click
import pluggy

from . import resolvers

_project_name = __spec__.parent
_entry_point = f'{_project_name}.plugins'

hookspec = pluggy.HookspecMarker(_project_name)
hookimpl = pluggy.HookimplMarker(_project_name)


class InstawowPlugin(Protocol):  # pragma: no cover
    "The plug-in interface."

    @hookspec
    def instawow_add_commands(self) -> Iterable[click.Command]:
        "Additional commands to register with ``click``."
        ...

    @hookspec
    def instawow_add_resolvers(self) -> Iterable[type[resolvers.Resolver]]:
        "Additional resolvers to load."
        ...


class _InstawowPluginHookRelay(Protocol):  # pragma: no cover
    def instawow_add_commands(self) -> Iterable[Iterable[click.Command]]:
        ...

    def instawow_add_resolvers(self) -> Iterable[Iterable[type[resolvers.Resolver]]]:
        ...


@lru_cache(1)
def load_plugins() -> _InstawowPluginHookRelay:
    plugin_manager = pluggy.PluginManager(_project_name)
    plugin_manager.add_hookspecs(InstawowPlugin)
    plugin_manager.load_setuptools_entrypoints(_entry_point)
    return cast(_InstawowPluginHookRelay, plugin_manager.hook)
