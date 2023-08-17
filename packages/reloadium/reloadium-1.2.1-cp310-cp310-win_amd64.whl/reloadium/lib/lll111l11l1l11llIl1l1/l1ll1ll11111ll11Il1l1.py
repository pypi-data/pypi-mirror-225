from contextlib import contextmanager
from pathlib import Path
import types
from typing import TYPE_CHECKING, Any, Dict, Generator, List, Tuple, Type

from reloadium.lib.environ import env
from reloadium.corium.ll11l11l111l1l1lIl1l1 import l11111llll1l1l11Il1l1
from reloadium.lib.lll111l11l1l11llIl1l1.lll1l11l1l11ll11Il1l1 import lllll1ll11l1lll1Il1l1
from reloadium.corium.l1ll1l1llllll1llIl1l1 import ll1l1l1l1ll111l1Il1l1, ll11l111111ll11lIl1l1, llll111l1l1l1l1lIl1l1, lllll111l1l1l1llIl1l1
from reloadium.corium.ll11ll111l1l11llIl1l1 import llll1l1ll1l111llIl1l1
from reloadium.corium.lll1111l111ll111Il1l1 import l11ll1l111llll11Il1l1
from dataclasses import dataclass, field


__RELOADIUM__ = True


@dataclass(**lllll111l1l1l1llIl1l1)
class ll11l1lll11l111lIl1l1(llll111l1l1l1l1lIl1l1):
    lllll11llll11lllIl1l1 = 'FlaskApp'

    @classmethod
    def l11l111l1l111l11Il1l1(ll11l1111l11l11lIl1l1, ll1111l1lllllll1Il1l1: llll1l1ll1l111llIl1l1.llll1ll1ll1lllllIl1l1, lll1lll11l1lllllIl1l1: Any, ll1lll11lll11l1lIl1l1: ll1l1l1l1ll111l1Il1l1) -> bool:
        import flask

        if (isinstance(lll1lll11l1lllllIl1l1, flask.Flask)):
            return True

        return False

    def l11lll1ll1l1llllIl1l1(ll1l11l11llll111Il1l1) -> bool:
        return True

    @classmethod
    def l11l11l1l1111l1lIl1l1(ll11l1111l11l11lIl1l1) -> int:
        return (super().l11l11l1l1111l1lIl1l1() + 10)


@dataclass(**lllll111l1l1l1llIl1l1)
class l1111l1l1l11llllIl1l1(llll111l1l1l1l1lIl1l1):
    lllll11llll11lllIl1l1 = 'Request'

    @classmethod
    def l11l111l1l111l11Il1l1(ll11l1111l11l11lIl1l1, ll1111l1lllllll1Il1l1: llll1l1ll1l111llIl1l1.llll1ll1ll1lllllIl1l1, lll1lll11l1lllllIl1l1: Any, ll1lll11lll11l1lIl1l1: ll1l1l1l1ll111l1Il1l1) -> bool:
        if (repr(lll1lll11l1lllllIl1l1) == '<LocalProxy unbound>'):
            return True

        return False

    def l11lll1ll1l1llllIl1l1(ll1l11l11llll111Il1l1) -> bool:
        return True

    @classmethod
    def l11l11l1l1111l1lIl1l1(ll11l1111l11l11lIl1l1) -> int:

        return int(10000000000.0)


@dataclass
class l111l1l11l1111llIl1l1(lllll1ll11l1lll1Il1l1):
    l11ll111llll11llIl1l1 = 'Flask'

    @contextmanager
    def ll11llll11l11111Il1l1(ll1l11l11llll111Il1l1) -> Generator[None, None, None]:




        from flask import Flask as FlaskLib 

        def ll11l11111111l1lIl1l1(*ll11ll1lll1l1111Il1l1: Any, **lll111ll1ll1lll1Il1l1: Any) -> Any:
            def llll1ll1lll111llIl1l1(lll1ll11ll1ll11lIl1l1: Any) -> Any:
                return lll1ll11ll1ll11lIl1l1

            return llll1ll1lll111llIl1l1

        l1llllll11111ll1Il1l1 = FlaskLib.route
        FlaskLib.route = ll11l11111111l1lIl1l1  # type: ignore

        try:
            yield 
        finally:
            FlaskLib.route = l1llllll11111ll1Il1l1  # type: ignore

    def l111ll1ll11l1ll1Il1l1(ll1l11l11llll111Il1l1) -> List[Type[ll11l111111ll11lIl1l1]]:
        return [ll11l1lll11l111lIl1l1, l1111l1l1l11llllIl1l1]

    def ll111lll1l111l1lIl1l1(ll1l11l11llll111Il1l1, l11l111l1l11l1llIl1l1: types.ModuleType) -> None:
        if (ll1l11l11llll111Il1l1.l11l1111llllll11Il1l1(l11l111l1l11l1llIl1l1, 'flask.app')):
            ll1l11l11llll111Il1l1.l1l11ll1111l1111Il1l1()
            ll1l11l11llll111Il1l1.ll1lll11ll1111l1Il1l1()
            ll1l11l11llll111Il1l1.llll1ll1111ll1l1Il1l1()

        if (ll1l11l11llll111Il1l1.l11l1111llllll11Il1l1(l11l111l1l11l1llIl1l1, 'flask.cli')):
            ll1l11l11llll111Il1l1.lll11ll11l1l1l11Il1l1()

    def l1l11ll1111l1111Il1l1(ll1l11l11llll111Il1l1) -> None:
        try:
            import werkzeug.serving
            import flask.cli
        except ImportError:
            return 

        llll1lll111ll1llIl1l1 = werkzeug.serving.run_simple

        def ll1l11lll1l1l111Il1l1(*ll11ll1lll1l1111Il1l1: Any, **lll111ll1ll1lll1Il1l1: Any) -> Any:
            with l11111llll1l1l11Il1l1():
                l111111l1111l1llIl1l1 = lll111ll1ll1lll1Il1l1.get('port')
                if ( not l111111l1111l1llIl1l1):
                    l111111l1111l1llIl1l1 = ll11ll1lll1l1111Il1l1[1]

                ll1l11l11llll111Il1l1.l11ll11l1l11lll1Il1l1 = ll1l11l11llll111Il1l1.l11ll1111ll1ll11Il1l1(l111111l1111l1llIl1l1)
                if (env.page_reload_on_start):
                    ll1l11l11llll111Il1l1.l11ll11l1l11lll1Il1l1.l111l111lllll111Il1l1(1.0)
            llll1lll111ll1llIl1l1(*ll11ll1lll1l1111Il1l1, **lll111ll1ll1lll1Il1l1)

        l11ll1l111llll11Il1l1.llllllll1l11l1l1Il1l1(werkzeug.serving, 'run_simple', ll1l11lll1l1l111Il1l1)
        l11ll1l111llll11Il1l1.llllllll1l11l1l1Il1l1(flask.cli, 'run_simple', ll1l11lll1l1l111Il1l1)

    def llll1ll1111ll1l1Il1l1(ll1l11l11llll111Il1l1) -> None:
        try:
            import flask
        except ImportError:
            return 

        llll1lll111ll1llIl1l1 = flask.app.Flask.__init__

        def ll1l11lll1l1l111Il1l1(ll11l11l11ll11l1Il1l1: Any, *ll11ll1lll1l1111Il1l1: Any, **lll111ll1ll1lll1Il1l1: Any) -> Any:
            llll1lll111ll1llIl1l1(ll11l11l11ll11l1Il1l1, *ll11ll1lll1l1111Il1l1, **lll111ll1ll1lll1Il1l1)
            with l11111llll1l1l11Il1l1():
                ll11l11l11ll11l1Il1l1.config['TEMPLATES_AUTO_RELOAD'] = True

        l11ll1l111llll11Il1l1.llllllll1l11l1l1Il1l1(flask.app.Flask, '__init__', ll1l11lll1l1l111Il1l1)

    def ll1lll11ll1111l1Il1l1(ll1l11l11llll111Il1l1) -> None:
        try:
            import waitress  # type: ignore
        except ImportError:
            return 

        llll1lll111ll1llIl1l1 = waitress.serve


        def ll1l11lll1l1l111Il1l1(*ll11ll1lll1l1111Il1l1: Any, **lll111ll1ll1lll1Il1l1: Any) -> Any:
            with l11111llll1l1l11Il1l1():
                l111111l1111l1llIl1l1 = lll111ll1ll1lll1Il1l1.get('port')
                if ( not l111111l1111l1llIl1l1):
                    l111111l1111l1llIl1l1 = int(ll11ll1lll1l1111Il1l1[1])

                l111111l1111l1llIl1l1 = int(l111111l1111l1llIl1l1)

                ll1l11l11llll111Il1l1.l11ll11l1l11lll1Il1l1 = ll1l11l11llll111Il1l1.l11ll1111ll1ll11Il1l1(l111111l1111l1llIl1l1)
                if (env.page_reload_on_start):
                    ll1l11l11llll111Il1l1.l11ll11l1l11lll1Il1l1.l111l111lllll111Il1l1(1.0)

            llll1lll111ll1llIl1l1(*ll11ll1lll1l1111Il1l1, **lll111ll1ll1lll1Il1l1)

        l11ll1l111llll11Il1l1.llllllll1l11l1l1Il1l1(waitress, 'serve', ll1l11lll1l1l111Il1l1)

    def lll11ll11l1l1l11Il1l1(ll1l11l11llll111Il1l1) -> None:
        try:
            from flask import cli
        except ImportError:
            return 

        ll11ll1111ll1lllIl1l1 = Path(cli.__file__).read_text(encoding='utf-8')
        ll11ll1111ll1lllIl1l1 = ll11ll1111ll1lllIl1l1.replace('.tb_next', '.tb_next.tb_next')

        exec(ll11ll1111ll1lllIl1l1, cli.__dict__)

    def l111l11ll1l1l1l1Il1l1(ll1l11l11llll111Il1l1) -> None:
        super().l111l11ll1l1l1l1Il1l1()
        import flask.app

        llll1lll111ll1llIl1l1 = flask.app.Flask.dispatch_request

        def ll1l11lll1l1l111Il1l1(*ll11ll1lll1l1111Il1l1: Any, **lll111ll1ll1lll1Il1l1: Any) -> Any:
            llllll11ll11lll1Il1l1 = llll1lll111ll1llIl1l1(*ll11ll1lll1l1111Il1l1, **lll111ll1ll1lll1Il1l1)

            if ( not ll1l11l11llll111Il1l1.l11ll11l1l11lll1Il1l1):
                return llllll11ll11lll1Il1l1

            if (isinstance(llllll11ll11lll1Il1l1, str)):
                ll11l1llll1l1l11Il1l1 = ll1l11l11llll111Il1l1.l11ll11l1l11lll1Il1l1.lll1ll1l1l1l11l1Il1l1(llllll11ll11lll1Il1l1)
                return ll11l1llll1l1l11Il1l1
            elif ((isinstance(llllll11ll11lll1Il1l1, flask.app.Response) and 'text/html' in llllll11ll11lll1Il1l1.content_type)):
                llllll11ll11lll1Il1l1.data = ll1l11l11llll111Il1l1.l11ll11l1l11lll1Il1l1.lll1ll1l1l1l11l1Il1l1(llllll11ll11lll1Il1l1.data.decode('utf-8')).encode('utf-8')
                return llllll11ll11lll1Il1l1
            else:
                return llllll11ll11lll1Il1l1

        flask.app.Flask.dispatch_request = ll1l11lll1l1l111Il1l1  # type: ignore
