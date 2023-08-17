from pathlib import Path
import sys
import threading
from types import CodeType, FrameType, ModuleType
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, cast

from reloadium.corium import ll1llll1ll1lll11Il1l1, ll11l11l111l1l1lIl1l1, public, llllllll11ll1111Il1l1, lll1111l111ll111Il1l1
from reloadium.corium.ll111l1ll111l1llIl1l1 import l1ll11llll1l1ll1Il1l1, l1lll1l1lllll11lIl1l1
from reloadium.corium.ll11l11l111l1l1lIl1l1 import lllllllll1llll11Il1l1, l11111llll1l1l11Il1l1, ll11l11ll111ll11Il1l1
from reloadium.corium.llll11lllll11l1lIl1l1 import l11l1l1lll11l11lIl1l1
from reloadium.corium.lll11111lllll1llIl1l1 import lll11111lllll1llIl1l1
from reloadium.corium.l1l1111lll1lllllIl1l1 import ll1l1ll1lll1ll11Il1l1
from reloadium.corium.l111l1ll11l11lllIl1l1 import l1l111111llll1l1Il1l1, l11l1ll111lll1l1Il1l1
from dataclasses import dataclass, field


__RELOADIUM__ = True

__all__ = ['ll11l1lll111l1llIl1l1', 'l1l1l111llllll1lIl1l1', 'l1lll11l1111l1l1Il1l1']


l1l1l1llllll1lllIl1l1 = lll11111lllll1llIl1l1.ll1lll1ll1111l1lIl1l1(__name__)


class ll11l1lll111l1llIl1l1:
    @classmethod
    def l11lll11lll11l11Il1l1(ll1l11l11llll111Il1l1) -> Optional[FrameType]:
        llll11l1l111llllIl1l1: FrameType = sys._getframe(2)
        ll11l1llll1l1l11Il1l1 = next(lll1111l111ll111Il1l1.llll11l1l111llllIl1l1.l11ll1111l1111llIl1l1(llll11l1l111llllIl1l1))
        return ll11l1llll1l1l11Il1l1


class l1l1l111llllll1lIl1l1(ll11l1lll111l1llIl1l1):
    @classmethod
    def l1lllllll1lll1l1Il1l1(ll11l1111l11l11lIl1l1, ll11ll1lll1l1111Il1l1: List[Any], lll111ll1ll1lll1Il1l1: Dict[str, Any], l1lll1111lllll11Il1l1: List[l1l111111llll1l1Il1l1]) -> Any:  # type: ignore
        with l11111llll1l1l11Il1l1():
            assert l11l1l1lll11l11lIl1l1.l1111l1llll1ll1lIl1l1.l1lll11l1lll1lllIl1l1
            llll11l1l111llllIl1l1 = l11l1l1lll11l11lIl1l1.l1111l1llll1ll1lIl1l1.l1lll11l1lll1lllIl1l1.l1l1l1l111ll1lllIl1l1.ll111lllll11ll1lIl1l1()
            llll11l1l111llllIl1l1.l1ll1l11l11l1111Il1l1()

            lllll1llll11ll11Il1l1 = l11l1l1lll11l11lIl1l1.l1111l1llll1ll1lIl1l1.l111llll1l1ll1llIl1l1.ll1llll1l11l1lllIl1l1(llll11l1l111llllIl1l1.ll1l111ll1l1llllIl1l1, llll11l1l111llllIl1l1.ll1111llll1lll11Il1l1.l1lll1l111ll1lllIl1l1())
            assert lllll1llll11ll11Il1l1
            lll1l111lll11l11Il1l1 = ll11l1111l11l11lIl1l1.l11lll11lll11l11Il1l1()

            for ll1llll1ll1l1111Il1l1 in l1lll1111lllll11Il1l1:
                ll1llll1ll1l1111Il1l1.l1ll1ll11lll1lllIl1l1()

            for ll1llll1ll1l1111Il1l1 in l1lll1111lllll11Il1l1:
                ll1llll1ll1l1111Il1l1.ll1l111ll1l11l11Il1l1()


        ll11l1llll1l1l11Il1l1 = lllll1llll11ll11Il1l1(*ll11ll1lll1l1111Il1l1, **lll111ll1ll1lll1Il1l1);        llll11l1l111llllIl1l1.l11l111l1l1lllllIl1l1.additional_info.pydev_step_stop = lll1l111lll11l11Il1l1  # type: ignore

        return ll11l1llll1l1l11Il1l1

    @classmethod
    async def l1llllll11l1ll11Il1l1(ll11l1111l11l11lIl1l1, ll11ll1lll1l1111Il1l1: List[Any], lll111ll1ll1lll1Il1l1: Dict[str, Any], l1lll1111lllll11Il1l1: List[l11l1ll111lll1l1Il1l1]) -> Any:  # type: ignore
        with l11111llll1l1l11Il1l1():
            assert l11l1l1lll11l11lIl1l1.l1111l1llll1ll1lIl1l1.l1lll11l1lll1lllIl1l1
            llll11l1l111llllIl1l1 = l11l1l1lll11l11lIl1l1.l1111l1llll1ll1lIl1l1.l1lll11l1lll1lllIl1l1.l1l1l1l111ll1lllIl1l1.ll111lllll11ll1lIl1l1()
            llll11l1l111llllIl1l1.l1ll1l11l11l1111Il1l1()

            lllll1llll11ll11Il1l1 = l11l1l1lll11l11lIl1l1.l1111l1llll1ll1lIl1l1.l111llll1l1ll1llIl1l1.ll1llll1l11l1lllIl1l1(llll11l1l111llllIl1l1.ll1l111ll1l1llllIl1l1, llll11l1l111llllIl1l1.ll1111llll1lll11Il1l1.l1lll1l111ll1lllIl1l1())
            assert lllll1llll11ll11Il1l1
            lll1l111lll11l11Il1l1 = ll11l1111l11l11lIl1l1.l11lll11lll11l11Il1l1()

            for ll1llll1ll1l1111Il1l1 in l1lll1111lllll11Il1l1:
                await ll1llll1ll1l1111Il1l1.l1ll1ll11lll1lllIl1l1()

            for ll1llll1ll1l1111Il1l1 in l1lll1111lllll11Il1l1:
                await ll1llll1ll1l1111Il1l1.ll1l111ll1l11l11Il1l1()


        ll11l1llll1l1l11Il1l1 = await lllll1llll11ll11Il1l1(*ll11ll1lll1l1111Il1l1, **lll111ll1ll1lll1Il1l1);        llll11l1l111llllIl1l1.l11l111l1l1lllllIl1l1.additional_info.pydev_step_stop = lll1l111lll11l11Il1l1  # type: ignore

        return ll11l1llll1l1l11Il1l1


class l1lll11l1111l1l1Il1l1(ll11l1lll111l1llIl1l1):
    @classmethod
    def l1lllllll1lll1l1Il1l1(ll11l1111l11l11lIl1l1) -> Optional[ModuleType]:  # type: ignore
        with l11111llll1l1l11Il1l1():
            assert l11l1l1lll11l11lIl1l1.l1111l1llll1ll1lIl1l1.l1lll11l1lll1lllIl1l1
            llll11l1l111llllIl1l1 = l11l1l1lll11l11lIl1l1.l1111l1llll1ll1lIl1l1.l1lll11l1lll1lllIl1l1.l1l1l1l111ll1lllIl1l1.ll111lllll11ll1lIl1l1()

            ll1l111l11llll11Il1l1 = Path(llll11l1l111llllIl1l1.lll1lll11l1lllllIl1l1.f_globals['__spec__'].origin).absolute()
            l1ll1111l111llllIl1l1 = llll11l1l111llllIl1l1.lll1lll11l1lllllIl1l1.f_globals['__name__']
            llll11l1l111llllIl1l1.l1ll1l11l11l1111Il1l1()
            l1l11ll1111l11llIl1l1 = l11l1l1lll11l11lIl1l1.l1111l1llll1ll1lIl1l1.l11l1ll1ll1l111lIl1l1.l111l1l1111lll1lIl1l1(ll1l111l11llll11Il1l1)

            if ( not l1l11ll1111l11llIl1l1):
                l1l1l1llllll1lllIl1l1.l1l1ll111111l1llIl1l1('Could not retrieve src.', l11111111111l1l1Il1l1={'file': ll1l1ll1lll1ll11Il1l1.ll111l1l1l1ll1llIl1l1(ll1l111l11llll11Il1l1), 
'fullname': ll1l1ll1lll1ll11Il1l1.l1ll1111l111llllIl1l1(l1ll1111l111llllIl1l1)})

            assert l1l11ll1111l11llIl1l1

        try:
            l1l11ll1111l11llIl1l1.lll1ll111111l111Il1l1()
            l1l11ll1111l11llIl1l1.l1111l111ll1llllIl1l1(ll11lll11111l1llIl1l1=False)
            l1l11ll1111l11llIl1l1.l11ll1lll11l11llIl1l1(ll11lll11111l1llIl1l1=False)
        except lllllllll1llll11Il1l1 as lll1ll1l1lllll11Il1l1:
            llll11l1l111llllIl1l1.l11lll11l11l1l11Il1l1(lll1ll1l1lllll11Il1l1)
            return None

        import importlib.util

        ll11l1l11l1lll11Il1l1 = llll11l1l111llllIl1l1.lll1lll11l1lllllIl1l1.f_locals['__spec__']
        lll1lll11111l111Il1l1 = importlib.util.module_from_spec(ll11l1l11l1lll11Il1l1)

        l1l11ll1111l11llIl1l1.l1l111111ll11l11Il1l1(lll1lll11111l111Il1l1)
        return lll1lll11111l111Il1l1


l1lll1l1lllll11lIl1l1.l1l1ll11l1ll1l11Il1l1(l1ll11llll1l1ll1Il1l1.ll1lll1ll1111lllIl1l1, l1l1l111llllll1lIl1l1.l1lllllll1lll1l1Il1l1)
l1lll1l1lllll11lIl1l1.l1l1ll11l1ll1l11Il1l1(l1ll11llll1l1ll1Il1l1.ll11l1l1lll111l1Il1l1, l1l1l111llllll1lIl1l1.l1llllll11l1ll11Il1l1)
l1lll1l1lllll11lIl1l1.l1l1ll11l1ll1l11Il1l1(l1ll11llll1l1ll1Il1l1.l1l1l111ll111l1lIl1l1, l1lll11l1111l1l1Il1l1.l1lllllll1lll1l1Il1l1)
