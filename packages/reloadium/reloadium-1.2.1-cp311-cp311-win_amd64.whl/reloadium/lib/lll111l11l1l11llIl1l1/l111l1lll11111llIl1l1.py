from pathlib import Path
import types
from typing import TYPE_CHECKING, Any, List

from reloadium.lib.lll111l11l1l11llIl1l1.llll11lll11l111lIl1l1 import l1111lll111l1lllIl1l1
from reloadium.corium.l1ll1l1llllll1llIl1l1 import l1l11lll11ll111lIl1l1
from reloadium.corium.lll1111l111ll111Il1l1 import l11ll1l111llll11Il1l1
from dataclasses import dataclass, field


__RELOADIUM__ = True


@dataclass
class l11lll111l1l11l1Il1l1(l1111lll111l1lllIl1l1):
    l11ll111llll11llIl1l1 = 'PyGame'

    l1lll1lllll1llllIl1l1: bool = field(init=False, default=False)

    def ll111lll1l111l1lIl1l1(ll1l11l11llll111Il1l1, l11l111l1l11l1llIl1l1: types.ModuleType) -> None:
        if (ll1l11l11llll111Il1l1.l11l1111llllll11Il1l1(l11l111l1l11l1llIl1l1, 'pygame.base')):
            ll1l11l11llll111Il1l1.l1111l1lll1ll11lIl1l1()

    def l1111l1lll1ll11lIl1l1(ll1l11l11llll111Il1l1) -> None:
        import pygame.display

        l1l1l11l11l11l11Il1l1 = pygame.display.update

        def l1lll1lll11l1111Il1l1(*ll11ll1lll1l1111Il1l1: Any, **lll111ll1ll1lll1Il1l1: Any) -> None:
            if (ll1l11l11llll111Il1l1.l1lll1lllll1llllIl1l1):
                l11ll1l111llll11Il1l1.l11l1lll1l1l1lllIl1l1(0.1)
                return None
            else:
                return l1l1l11l11l11l11Il1l1(*ll11ll1lll1l1111Il1l1, **lll111ll1ll1lll1Il1l1)

        pygame.display.update = l1lll1lll11l1111Il1l1

    def l1l111111lll1ll1Il1l1(ll1l11l11llll111Il1l1, ll111l1l1l1ll1llIl1l1: Path) -> None:
        ll1l11l11llll111Il1l1.l1lll1lllll1llllIl1l1 = True

    def lll1ll1ll11ll111Il1l1(ll1l11l11llll111Il1l1, ll111l1l1l1ll1llIl1l1: Path, ll111llll1l111llIl1l1: List[l1l11lll11ll111lIl1l1]) -> None:
        ll1l11l11llll111Il1l1.l1lll1lllll1llllIl1l1 = False

    def l111l1l111ll1111Il1l1(ll1l11l11llll111Il1l1, llll1l11ll11ll11Il1l1: Exception) -> None:
        ll1l11l11llll111Il1l1.l1lll1lllll1llllIl1l1 = False
