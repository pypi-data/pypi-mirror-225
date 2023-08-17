import re
from contextlib import contextmanager
import os
import sys
import types
from pathlib import Path
from textwrap import dedent
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Set, Tuple, Union

from reloadium.corium.ll11l11l111l1l1lIl1l1 import l11111llll1l1l11Il1l1
from reloadium.lib.lll111l11l1l11llIl1l1.llll11lll11l111lIl1l1 import l1111lll111l1lllIl1l1, l1ll1111lll1llllIl1l1
from reloadium.corium.l111l1ll11l11lllIl1l1 import l1l111111llll1l1Il1l1
from reloadium.corium.lll1111l111ll111Il1l1 import l11ll1l111llll11Il1l1
from dataclasses import dataclass, field

if (TYPE_CHECKING):
    from sqlalchemy.engine.base import Engine, Transaction
    from sqlalchemy.orm.session import Session


__RELOADIUM__ = True


@dataclass(repr=False)
class l1l1l1111ll11l1lIl1l1(l1ll1111lll1llllIl1l1):
    llll11lll11l111lIl1l1: "llll11llllll1lllIl1l1"
    ll1111ll11111111Il1l1: List["Transaction"] = field(init=False, default_factory=list)

    def l1l11l1llll1ll11Il1l1(ll1l11l11llll111Il1l1) -> None:
        from sqlalchemy.orm.session import _sessions

        super().l1l11l1llll1ll11Il1l1()

        llll111lll11l1llIl1l1 = list(_sessions.values())

        for lllll1ll111l1l11Il1l1 in llll111lll11l1llIl1l1:
            if ( not lllll1ll111l1l11Il1l1.is_active):
                continue

            l11l1ll1llllll11Il1l1 = lllll1ll111l1l11Il1l1.begin_nested()
            ll1l11l11llll111Il1l1.ll1111ll11111111Il1l1.append(l11l1ll1llllll11Il1l1)

    def __repr__(ll1l11l11llll111Il1l1) -> str:
        return 'DbMemento'

    def l1ll1ll11lll1lllIl1l1(ll1l11l11llll111Il1l1) -> None:
        super().l1ll1ll11lll1lllIl1l1()

        while ll1l11l11llll111Il1l1.ll1111ll11111111Il1l1:
            l11l1ll1llllll11Il1l1 = ll1l11l11llll111Il1l1.ll1111ll11111111Il1l1.pop()
            if (l11l1ll1llllll11Il1l1.is_active):
                try:
                    l11l1ll1llllll11Il1l1.rollback()
                except :
                    pass

    def ll1l111ll1l11l11Il1l1(ll1l11l11llll111Il1l1) -> None:
        super().ll1l111ll1l11l11Il1l1()

        while ll1l11l11llll111Il1l1.ll1111ll11111111Il1l1:
            l11l1ll1llllll11Il1l1 = ll1l11l11llll111Il1l1.ll1111ll11111111Il1l1.pop()
            if (l11l1ll1llllll11Il1l1.is_active):
                try:
                    l11l1ll1llllll11Il1l1.commit()
                except :
                    pass


@dataclass
class llll11llllll1lllIl1l1(l1111lll111l1lllIl1l1):
    l11ll111llll11llIl1l1 = 'Sqlalchemy'

    l1l1111l11ll11l1Il1l1: List["Engine"] = field(init=False, default_factory=list)
    llll111lll11l1llIl1l1: Set["Session"] = field(init=False, default_factory=set)
    l111l11l111lll11Il1l1: Tuple[int, ...] = field(init=False)

    def ll111lll1l111l1lIl1l1(ll1l11l11llll111Il1l1, lll1lll11111l111Il1l1: types.ModuleType) -> None:
        if (ll1l11l11llll111Il1l1.l11l1111llllll11Il1l1(lll1lll11111l111Il1l1, 'sqlalchemy')):
            ll1l11l11llll111Il1l1.l1l111l11111llllIl1l1(lll1lll11111l111Il1l1)

        if (ll1l11l11llll111Il1l1.l11l1111llllll11Il1l1(lll1lll11111l111Il1l1, 'sqlalchemy.engine.base')):
            ll1l11l11llll111Il1l1.lll1ll11ll1l1lllIl1l1(lll1lll11111l111Il1l1)

    def l1l111l11111llllIl1l1(ll1l11l11llll111Il1l1, lll1lll11111l111Il1l1: Any) -> None:
        l1l1111l11ll1l11Il1l1 = Path(lll1lll11111l111Il1l1.__file__).read_text(encoding='utf-8')
        __version__ = re.findall('__version__\\s*?=\\s*?"(.*?)"', l1l1111l11ll1l11Il1l1)[0]

        l1llllll111l1lllIl1l1 = [int(l1l11ll1l1l1ll11Il1l1) for l1l11ll1l1l1ll11Il1l1 in __version__.split('.')]
        ll1l11l11llll111Il1l1.l111l11l111lll11Il1l1 = tuple(l1llllll111l1lllIl1l1)

    def l1l11l11ll11ll1lIl1l1(ll1l11l11llll111Il1l1, lll11ll1111llll1Il1l1: str, ll1l1lll1l1lll11Il1l1: bool) -> Optional["l1l111111llll1l1Il1l1"]:
        ll11l1llll1l1l11Il1l1 = l1l1l1111ll11l1lIl1l1(lll11ll1111llll1Il1l1=lll11ll1111llll1Il1l1, llll11lll11l111lIl1l1=ll1l11l11llll111Il1l1)
        ll11l1llll1l1l11Il1l1.l1l11l1llll1ll11Il1l1()
        return ll11l1llll1l1l11Il1l1

    def lll1ll11ll1l1lllIl1l1(ll1l11l11llll111Il1l1, lll1lll11111l111Il1l1: Any) -> None:
        l111l1llll111lllIl1l1 = locals().copy()

        l111l1llll111lllIl1l1.update({'original': lll1lll11111l111Il1l1.Engine.__init__, 'reloader_code': l11111llll1l1l11Il1l1, 'engines': ll1l11l11llll111Il1l1.l1l1111l11ll11l1Il1l1})





        l11l11ll11l1ll11Il1l1 = dedent('\n            def patched(\n                    self2: Any,\n                    pool: Any,\n                    dialect: Any,\n                    url: Any,\n                    logging_name: Any = None,\n                    echo: Any = None,\n                    proxy: Any = None,\n                    execution_options: Any = None,\n                    hide_parameters: Any = None,\n            ) -> Any:\n                original(self2,\n                         pool,\n                         dialect,\n                         url,\n                         logging_name,\n                         echo,\n                         proxy,\n                         execution_options,\n                         hide_parameters\n                         )\n                with reloader_code():\n                    engines.append(self2)')
























        l1lll1lllllll1llIl1l1 = dedent('\n            def patched(\n                    self2: Any,\n                    pool: Any,\n                    dialect: Any,\n                    url: Any,\n                    logging_name: Any = None,\n                    echo: Any = None,\n                    query_cache_size: Any = 500,\n                    execution_options: Any = None,\n                    hide_parameters: Any = False,\n            ) -> Any:\n                original(self2,\n                         pool,\n                         dialect,\n                         url,\n                         logging_name,\n                         echo,\n                         query_cache_size,\n                         execution_options,\n                         hide_parameters)\n                with reloader_code():\n                    engines.append(self2)\n        ')
























        if (ll1l11l11llll111Il1l1.l111l11l111lll11Il1l1 <= (1, 3, 24, )):
            exec(l11l11ll11l1ll11Il1l1, {**globals(), **l111l1llll111lllIl1l1}, l111l1llll111lllIl1l1)
        else:
            exec(l1lll1lllllll1llIl1l1, {**globals(), **l111l1llll111lllIl1l1}, l111l1llll111lllIl1l1)

        l11ll1l111llll11Il1l1.llllllll1l11l1l1Il1l1(lll1lll11111l111Il1l1.Engine, '__init__', l111l1llll111lllIl1l1['patched'])
