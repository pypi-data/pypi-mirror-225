import types
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Tuple, Type, Union, cast

from reloadium.lib.lll111l11l1l11llIl1l1.llll11lll11l111lIl1l1 import l1111lll111l1lllIl1l1
from reloadium.lib import l1l1lll1ll111l1lIl1l1

from dataclasses import dataclass

if (TYPE_CHECKING):
    ...


__RELOADIUM__ = True


@dataclass
class l11l1111111lllllIl1l1(l1111lll111l1lllIl1l1):
    l11ll111llll11llIl1l1 = 'Multiprocessing'

    def __post_init__(ll1l11l11llll111Il1l1) -> None:
        super().__post_init__()

    def ll111lll1l111l1lIl1l1(ll1l11l11llll111Il1l1, lll1lll11111l111Il1l1: types.ModuleType) -> None:
        if (ll1l11l11llll111Il1l1.l11l1111llllll11Il1l1(lll1lll11111l111Il1l1, 'multiprocessing.popen_spawn_posix')):
            ll1l11l11llll111Il1l1.l1l1l1l111lllll1Il1l1(lll1lll11111l111Il1l1)

        if (ll1l11l11llll111Il1l1.l11l1111llllll11Il1l1(lll1lll11111l111Il1l1, 'multiprocessing.popen_spawn_win32')):
            ll1l11l11llll111Il1l1.l1l11ll1ll111l11Il1l1(lll1lll11111l111Il1l1)

    def l1l1l1l111lllll1Il1l1(ll1l11l11llll111Il1l1, lll1lll11111l111Il1l1: types.ModuleType) -> None:
        import multiprocessing.popen_spawn_posix
        multiprocessing.popen_spawn_posix.Popen._launch = l1l1lll1ll111l1lIl1l1.l11ll11l1lll11llIl1l1.l11l1ll1l11l1l11Il1l1  # type: ignore

    def l1l11ll1ll111l11Il1l1(ll1l11l11llll111Il1l1, lll1lll11111l111Il1l1: types.ModuleType) -> None:
        import multiprocessing.popen_spawn_win32
        multiprocessing.popen_spawn_win32.Popen.__init__ = l1l1lll1ll111l1lIl1l1.l11ll11l1lll11llIl1l1.__init__  # type: ignore
