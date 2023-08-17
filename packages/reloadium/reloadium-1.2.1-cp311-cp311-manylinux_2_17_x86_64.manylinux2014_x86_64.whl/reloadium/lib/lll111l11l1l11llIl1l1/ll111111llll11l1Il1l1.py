import dataclasses
import types
from reloadium.lib.lll111l11l1l11llIl1l1.llll11lll11l111lIl1l1 import l1111lll111l1lllIl1l1
from reloadium.fast.lll111l11l1l11llIl1l1.ll111111llll11l1Il1l1 import l11l111ll11111l1Il1l1

from dataclasses import dataclass

__RELOADIUM__ = True

import types


@dataclass(repr=False, frozen=False)
class lll1l11l1l111111Il1l1(l1111lll111l1lllIl1l1):
    l11ll111llll11llIl1l1 = 'Pytest'

    def ll111lll1l111l1lIl1l1(ll1l11l11llll111Il1l1, lll1lll11111l111Il1l1: types.ModuleType) -> None:
        if (ll1l11l11llll111Il1l1.l11l1111llllll11Il1l1(lll1lll11111l111Il1l1, 'pytest')):
            ll1l11l11llll111Il1l1.lll1lll1ll1l1111Il1l1(lll1lll11111l111Il1l1)

    def lll1lll1ll1l1111Il1l1(ll1l11l11llll111Il1l1, lll1lll11111l111Il1l1: types.ModuleType) -> None:
        import _pytest.assertion.rewrite
        _pytest.assertion.rewrite.AssertionRewritingHook = l11l111ll11111l1Il1l1  # type: ignore

