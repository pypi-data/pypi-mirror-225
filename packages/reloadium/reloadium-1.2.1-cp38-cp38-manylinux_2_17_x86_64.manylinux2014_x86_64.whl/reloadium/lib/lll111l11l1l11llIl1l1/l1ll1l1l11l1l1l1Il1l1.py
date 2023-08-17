import asyncio
from contextlib import contextmanager
import os
from pathlib import Path
import sys
import types
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Tuple, Type

from reloadium.corium.llll11lllll11l1lIl1l1 import l11l1l1lll11l11lIl1l1
from reloadium.lib.environ import env
from reloadium.corium.ll11l11l111l1l1lIl1l1 import l11111llll1l1l11Il1l1
from reloadium.lib.lll111l11l1l11llIl1l1.llll11lll11l111lIl1l1 import l1ll1111lll1llllIl1l1, ll1l11lll1lllll1Il1l1
from reloadium.lib.lll111l11l1l11llIl1l1.lll1l11l1l11ll11Il1l1 import lllll1ll11l1lll1Il1l1
from reloadium.corium.l1ll1l1llllll1llIl1l1 import l1l11lll11ll111lIl1l1, ll1l1l1l1ll111l1Il1l1, ll11l111111ll11lIl1l1, llll111l1l1l1l1lIl1l1, lllll111l1l1l1llIl1l1
from reloadium.corium.l111l1ll11l11lllIl1l1 import l1l111111llll1l1Il1l1, l11l1ll111lll1l1Il1l1
from reloadium.corium.ll11ll111l1l11llIl1l1 import llll1l1ll1l111llIl1l1
from reloadium.corium.lll1111l111ll111Il1l1 import l11ll1l111llll11Il1l1
from dataclasses import dataclass, field


if (TYPE_CHECKING):
    from django.db import transaction
    from django.db.transaction import Atomic


__RELOADIUM__ = True


@dataclass(**lllll111l1l1l1llIl1l1)
class llllll1l1111l111Il1l1(llll111l1l1l1l1lIl1l1):
    lllll11llll11lllIl1l1 = 'Field'

    @classmethod
    def l11l111l1l111l11Il1l1(ll11l1111l11l11lIl1l1, ll1111l1lllllll1Il1l1: llll1l1ll1l111llIl1l1.llll1ll1ll1lllllIl1l1, lll1lll11l1lllllIl1l1: Any, ll1lll11lll11l1lIl1l1: ll1l1l1l1ll111l1Il1l1) -> bool:
        from django.db.models.fields import Field

        if ((hasattr(lll1lll11l1lllllIl1l1, 'field') and isinstance(lll1lll11l1lllllIl1l1.field, Field))):
            return True

        return False

    def l1l11l1ll111ll11Il1l1(ll1l11l11llll111Il1l1, ll111ll1ll1llll1Il1l1: ll11l111111ll11lIl1l1) -> bool:
        return True

    @classmethod
    def l11l11l1l1111l1lIl1l1(ll11l1111l11l11lIl1l1) -> int:
        return 200


@dataclass(repr=False)
class l1l1l1111ll11l1lIl1l1(l1ll1111lll1llllIl1l1):
    lllllll1lll1l111Il1l1: "Atomic" = field(init=False)

    l11ll1lll11ll1l1Il1l1: bool = field(init=False, default=False)

    def l1l11l1llll1ll11Il1l1(ll1l11l11llll111Il1l1) -> None:
        super().l1l11l1llll1ll11Il1l1()
        from django.db import transaction

        ll1l11l11llll111Il1l1.lllllll1lll1l111Il1l1 = transaction.atomic()
        ll1l11l11llll111Il1l1.lllllll1lll1l111Il1l1.__enter__()

    def l1ll1ll11lll1lllIl1l1(ll1l11l11llll111Il1l1) -> None:
        super().l1ll1ll11lll1lllIl1l1()
        if (ll1l11l11llll111Il1l1.l11ll1lll11ll1l1Il1l1):
            return 

        ll1l11l11llll111Il1l1.l11ll1lll11ll1l1Il1l1 = True
        from django.db import transaction

        transaction.set_rollback(True)
        ll1l11l11llll111Il1l1.lllllll1lll1l111Il1l1.__exit__(None, None, None)

    def ll1l111ll1l11l11Il1l1(ll1l11l11llll111Il1l1) -> None:
        super().ll1l111ll1l11l11Il1l1()

        if (ll1l11l11llll111Il1l1.l11ll1lll11ll1l1Il1l1):
            return 

        ll1l11l11llll111Il1l1.l11ll1lll11ll1l1Il1l1 = True
        ll1l11l11llll111Il1l1.lllllll1lll1l111Il1l1.__exit__(None, None, None)

    def __repr__(ll1l11l11llll111Il1l1) -> str:
        return 'DbMemento'


@dataclass(repr=False)
class l1l1l11llll11ll1Il1l1(ll1l11lll1lllll1Il1l1):
    lllllll1lll1l111Il1l1: "Atomic" = field(init=False)

    l11ll1lll11ll1l1Il1l1: bool = field(init=False, default=False)

    async def l1l11l1llll1ll11Il1l1(ll1l11l11llll111Il1l1) -> None:
        await super().l1l11l1llll1ll11Il1l1()
        from django.db import transaction
        from asgiref.sync import sync_to_async

        ll1l11l11llll111Il1l1.lllllll1lll1l111Il1l1 = transaction.atomic()


        with l11l1l1lll11l11lIl1l1.l1111l1llll1ll1lIl1l1.l11l1l1l11l1l111Il1l1.lll1l1l1llll1ll1Il1l1(False):
            await sync_to_async(ll1l11l11llll111Il1l1.lllllll1lll1l111Il1l1.__enter__)()

    async def l1ll1ll11lll1lllIl1l1(ll1l11l11llll111Il1l1) -> None:
        from asgiref.sync import sync_to_async

        await super().l1ll1ll11lll1lllIl1l1()
        if (ll1l11l11llll111Il1l1.l11ll1lll11ll1l1Il1l1):
            return 

        ll1l11l11llll111Il1l1.l11ll1lll11ll1l1Il1l1 = True
        from django.db import transaction

        def l1ll11ll111l1lllIl1l1() -> None:
            transaction.set_rollback(True)
            ll1l11l11llll111Il1l1.lllllll1lll1l111Il1l1.__exit__(None, None, None)
        with l11l1l1lll11l11lIl1l1.l1111l1llll1ll1lIl1l1.l11l1l1l11l1l111Il1l1.lll1l1l1llll1ll1Il1l1(False):
            await sync_to_async(l1ll11ll111l1lllIl1l1)()

    async def ll1l111ll1l11l11Il1l1(ll1l11l11llll111Il1l1) -> None:
        from asgiref.sync import sync_to_async

        await super().ll1l111ll1l11l11Il1l1()

        if (ll1l11l11llll111Il1l1.l11ll1lll11ll1l1Il1l1):
            return 

        ll1l11l11llll111Il1l1.l11ll1lll11ll1l1Il1l1 = True
        with l11l1l1lll11l11lIl1l1.l1111l1llll1ll1lIl1l1.l11l1l1l11l1l111Il1l1.lll1l1l1llll1ll1Il1l1(False):
            await sync_to_async(ll1l11l11llll111Il1l1.lllllll1lll1l111Il1l1.__exit__)(None, None, None)

    def __repr__(ll1l11l11llll111Il1l1) -> str:
        return 'AsyncDbMemento'


@dataclass
class l11ll1111ll1lll1Il1l1(lllll1ll11l1lll1Il1l1):
    l11ll111llll11llIl1l1 = 'Django'

    l11llll1111lll1lIl1l1: Optional[int] = field(init=False)
    l111111l1ll1lll1Il1l1: Optional[Callable[..., Any]] = field(init=False, default=None)

    def __post_init__(ll1l11l11llll111Il1l1) -> None:
        super().__post_init__()
        ll1l11l11llll111Il1l1.l11llll1111lll1lIl1l1 = None

    def l111ll1ll11l1ll1Il1l1(ll1l11l11llll111Il1l1) -> List[Type[ll11l111111ll11lIl1l1]]:
        return [llllll1l1111l111Il1l1]

    def llll1l1llll111llIl1l1(ll1l11l11llll111Il1l1) -> None:
        super().llll1l1llll111llIl1l1()
        if ('runserver' in sys.argv):
            sys.argv.append('--noreload')

    def ll111lll1l111l1lIl1l1(ll1l11l11llll111Il1l1, lll1lll11111l111Il1l1: types.ModuleType) -> None:
        if (ll1l11l11llll111Il1l1.l11l1111llllll11Il1l1(lll1lll11111l111Il1l1, 'django.core.management.commands.runserver')):
            ll1l11l11llll111Il1l1.l1lll1111ll1lll1Il1l1()
            ll1l11l11llll111Il1l1.l111ll1l11ll111lIl1l1()

    def l1l11l11ll11ll1lIl1l1(ll1l11l11llll111Il1l1, lll11ll1111llll1Il1l1: str, ll1l1lll1l1lll11Il1l1: bool) -> Optional["l1l111111llll1l1Il1l1"]:
        if ( not os.environ.get('DJANGO_SETTINGS_MODULE')):
            return None

        if (ll1l1lll1l1lll11Il1l1):
            return None
        else:
            ll11l1llll1l1l11Il1l1 = l1l1l1111ll11l1lIl1l1(lll11ll1111llll1Il1l1=lll11ll1111llll1Il1l1, llll11lll11l111lIl1l1=ll1l11l11llll111Il1l1)
            ll11l1llll1l1l11Il1l1.l1l11l1llll1ll11Il1l1()

        return ll11l1llll1l1l11Il1l1

    async def lll1ll11l11l111lIl1l1(ll1l11l11llll111Il1l1, lll11ll1111llll1Il1l1: str) -> Optional["l11l1ll111lll1l1Il1l1"]:
        if ( not os.environ.get('DJANGO_SETTINGS_MODULE')):
            return None

        ll11l1llll1l1l11Il1l1 = l1l1l11llll11ll1Il1l1(lll11ll1111llll1Il1l1=lll11ll1111llll1Il1l1, llll11lll11l111lIl1l1=ll1l11l11llll111Il1l1)
        await ll11l1llll1l1l11Il1l1.l1l11l1llll1ll11Il1l1()
        return ll11l1llll1l1l11Il1l1

    def l1lll1111ll1lll1Il1l1(ll1l11l11llll111Il1l1) -> None:
        import django.core.management.commands.runserver

        llll1lll111ll1llIl1l1 = django.core.management.commands.runserver.Command.handle

        def ll1l11lll1l1l111Il1l1(*ll11ll1lll1l1111Il1l1: Any, **l1111l11ll1l11llIl1l1: Any) -> Any:
            with l11111llll1l1l11Il1l1():
                l111111l1111l1llIl1l1 = l1111l11ll1l11llIl1l1.get('addrport')
                if ( not l111111l1111l1llIl1l1):
                    l111111l1111l1llIl1l1 = django.core.management.commands.runserver.Command.default_port

                l111111l1111l1llIl1l1 = l111111l1111l1llIl1l1.split(':')[ - 1]
                l111111l1111l1llIl1l1 = int(l111111l1111l1llIl1l1)
                ll1l11l11llll111Il1l1.l11llll1111lll1lIl1l1 = l111111l1111l1llIl1l1

            return llll1lll111ll1llIl1l1(*ll11ll1lll1l1111Il1l1, **l1111l11ll1l11llIl1l1)

        l11ll1l111llll11Il1l1.llllllll1l11l1l1Il1l1(django.core.management.commands.runserver.Command, 'handle', ll1l11lll1l1l111Il1l1)

    def l111ll1l11ll111lIl1l1(ll1l11l11llll111Il1l1) -> None:
        import django.core.management.commands.runserver

        llll1lll111ll1llIl1l1 = django.core.management.commands.runserver.Command.get_handler

        def ll1l11lll1l1l111Il1l1(*ll11ll1lll1l1111Il1l1: Any, **l1111l11ll1l11llIl1l1: Any) -> Any:
            with l11111llll1l1l11Il1l1():
                assert ll1l11l11llll111Il1l1.l11llll1111lll1lIl1l1
                ll1l11l11llll111Il1l1.l11ll11l1l11lll1Il1l1 = ll1l11l11llll111Il1l1.l11ll1111ll1ll11Il1l1(ll1l11l11llll111Il1l1.l11llll1111lll1lIl1l1)
                if (env.page_reload_on_start):
                    ll1l11l11llll111Il1l1.l11ll11l1l11lll1Il1l1.l111l111lllll111Il1l1(2.0)

            return llll1lll111ll1llIl1l1(*ll11ll1lll1l1111Il1l1, **l1111l11ll1l11llIl1l1)

        l11ll1l111llll11Il1l1.llllllll1l11l1l1Il1l1(django.core.management.commands.runserver.Command, 'get_handler', ll1l11lll1l1l111Il1l1)

    def l111l11ll1l1l1l1Il1l1(ll1l11l11llll111Il1l1) -> None:
        super().l111l11ll1l1l1l1Il1l1()

        import django.core.handlers.base

        llll1lll111ll1llIl1l1 = django.core.handlers.base.BaseHandler.get_response

        def ll1l11lll1l1l111Il1l1(ll1l11l1l11ll111Il1l1: Any, ll1111l111ll11l1Il1l1: Any) -> Any:
            llllll11ll11lll1Il1l1 = llll1lll111ll1llIl1l1(ll1l11l1l11ll111Il1l1, ll1111l111ll11l1Il1l1)

            if ( not ll1l11l11llll111Il1l1.l11ll11l1l11lll1Il1l1):
                return llllll11ll11lll1Il1l1

            ll11l11111111lllIl1l1 = llllll11ll11lll1Il1l1.get('content-type')

            if (( not ll11l11111111lllIl1l1 or 'text/html' not in ll11l11111111lllIl1l1)):
                return llllll11ll11lll1Il1l1

            l1l1111l11ll1l11Il1l1 = llllll11ll11lll1Il1l1.content

            if (isinstance(l1l1111l11ll1l11Il1l1, bytes)):
                l1l1111l11ll1l11Il1l1 = l1l1111l11ll1l11Il1l1.decode('utf-8')

            l11l1llll1l1llllIl1l1 = ll1l11l11llll111Il1l1.l11ll11l1l11lll1Il1l1.lll1ll1l1l1l11l1Il1l1(l1l1111l11ll1l11Il1l1)

            llllll11ll11lll1Il1l1.content = l11l1llll1l1llllIl1l1.encode('utf-8')
            llllll11ll11lll1Il1l1['content-length'] = str(len(llllll11ll11lll1Il1l1.content)).encode('ascii')
            return llllll11ll11lll1Il1l1

        django.core.handlers.base.BaseHandler.get_response = ll1l11lll1l1l111Il1l1  # type: ignore

    def l1l111111lll1ll1Il1l1(ll1l11l11llll111Il1l1, ll111l1l1l1ll1llIl1l1: Path) -> None:
        super().l1l111111lll1ll1Il1l1(ll111l1l1l1ll1llIl1l1)

        from django.apps.registry import Apps

        ll1l11l11llll111Il1l1.l111111l1ll1lll1Il1l1 = Apps.register_model

        def l1l1111lll11l1l1Il1l1(*ll11ll1lll1l1111Il1l1: Any, **lll111ll1ll1lll1Il1l1: Any) -> Any:
            pass

        Apps.register_model = l1l1111lll11l1l1Il1l1

    def lll1ll1ll11ll111Il1l1(ll1l11l11llll111Il1l1, ll111l1l1l1ll1llIl1l1: Path, ll111llll1l111llIl1l1: List[l1l11lll11ll111lIl1l1]) -> None:
        super().lll1ll1ll11ll111Il1l1(ll111l1l1l1ll1llIl1l1, ll111llll1l111llIl1l1)

        if ( not ll1l11l11llll111Il1l1.l111111l1ll1lll1Il1l1):
            return 

        from django.apps.registry import Apps

        Apps.register_model = ll1l11l11llll111Il1l1.l111111l1ll1lll1Il1l1
