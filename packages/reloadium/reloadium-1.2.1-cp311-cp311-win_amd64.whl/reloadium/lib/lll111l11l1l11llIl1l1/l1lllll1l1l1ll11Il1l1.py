import sys

from reloadium.corium.lll1111l111ll111Il1l1.l1ll11ll1ll11111Il1l1 import l1l1l11llll1ll11Il1l1

__RELOADIUM__ = True

l1l1l11llll1ll11Il1l1()


try:
    import _pytest.assertion.rewrite
except ImportError:
    class ll111l1lllllll1lIl1l1:
        pass

    _pytest = lambda :None  # type: ignore
    sys.modules['_pytest'] = _pytest

    _pytest.assertion = lambda :None  # type: ignore
    sys.modules['_pytest.assertion'] = _pytest.assertion

    _pytest.assertion.rewrite = lambda :None  # type: ignore
    _pytest.assertion.rewrite.AssertionRewritingHook = ll111l1lllllll1lIl1l1  # type: ignore
    sys.modules['_pytest.assertion.rewrite'] = _pytest.assertion.rewrite
