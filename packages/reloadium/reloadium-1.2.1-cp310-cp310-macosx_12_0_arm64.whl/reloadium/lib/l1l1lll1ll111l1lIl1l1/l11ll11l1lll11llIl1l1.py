import sys

__RELOADIUM__ = True


def l11l1ll1l11l1l11Il1l1(ll11l11l11ll11l1Il1l1, l11ll1llll111l11Il1l1):
    from reloadium.lib.environ import env
    from pathlib import Path
    from multiprocessing import util, spawn
    from multiprocessing.context import reduction, set_spawning_popen
    import io
    import os

    env.sub_process += 1
    env.save_to_os_environ()

    def ll11l11llllll1llIl1l1(*l11l11ll1l1ll111Il1l1):

        for llll11llll1111llIl1l1 in l11l11ll1l1ll111Il1l1:
            os.close(llll11llll1111llIl1l1)

    if (sys.version_info > (3, 8, )):
        from multiprocessing import resource_tracker as tracker 
    else:
        from multiprocessing import semaphore_tracker as tracker 

    llllll1111l11111Il1l1 = tracker.getfd()
    ll11l11l11ll11l1Il1l1._fds.append(llllll1111l11111Il1l1)
    ll111l1l111l1lllIl1l1 = spawn.get_preparation_data(l11ll1llll111l11Il1l1._name)
    ll111l1lllll11l1Il1l1 = io.BytesIO()
    set_spawning_popen(ll11l11l11ll11l1Il1l1)

    try:
        reduction.dump(ll111l1l111l1lllIl1l1, ll111l1lllll11l1Il1l1)
        reduction.dump(l11ll1llll111l11Il1l1, ll111l1lllll11l1Il1l1)
    finally:
        set_spawning_popen(None)

    l1lll11111111lllIl1l1ll1l111l1ll1lll1Il1l1l11ll1l11ll1ll1lIl1l1l1l11ll1lll1l11lIl1l1 = None
    try:
        (l1lll11111111lllIl1l1, ll1l111l1ll1lll1Il1l1, ) = os.pipe()
        (l11ll1l11ll1ll1lIl1l1, l1l11ll1lll1l11lIl1l1, ) = os.pipe()
        l111111ll111llllIl1l1 = spawn.get_command_line(tracker_fd=llllll1111l11111Il1l1, pipe_handle=l11ll1l11ll1ll1lIl1l1)


        ll1l111l11llll11Il1l1 = str(Path(ll111l1l111l1lllIl1l1['sys_argv'][0]).absolute())
        l111111ll111llllIl1l1 = [l111111ll111llllIl1l1[0], '-B', '-m', 'reloadium_launcher', 'spawn_process', str(llllll1111l11111Il1l1), 
str(l11ll1l11ll1ll1lIl1l1), ll1l111l11llll11Il1l1]
        ll11l11l11ll11l1Il1l1._fds.extend([l11ll1l11ll1ll1lIl1l1, ll1l111l1ll1lll1Il1l1])
        ll11l11l11ll11l1Il1l1.pid = util.spawnv_passfds(spawn.get_executable(), 
l111111ll111llllIl1l1, ll11l11l11ll11l1Il1l1._fds)
        ll11l11l11ll11l1Il1l1.sentinel = l1lll11111111lllIl1l1
        with open(l1l11ll1lll1l11lIl1l1, 'wb', closefd=False) as lll1ll11ll1ll11lIl1l1:
            lll1ll11ll1ll11lIl1l1.write(ll111l1lllll11l1Il1l1.getbuffer())
    finally:
        ll1l11ll11l11ll1Il1l1 = []
        for llll11llll1111llIl1l1 in (l1lll11111111lllIl1l1, l1l11ll1lll1l11lIl1l1, ):
            if (llll11llll1111llIl1l1 is not None):
                ll1l11ll11l11ll1Il1l1.append(llll11llll1111llIl1l1)
        ll11l11l11ll11l1Il1l1.finalizer = util.Finalize(ll11l11l11ll11l1Il1l1, ll11l11llllll1llIl1l1, ll1l11ll11l11ll1Il1l1)

        for llll11llll1111llIl1l1 in (l11ll1l11ll1ll1lIl1l1, ll1l111l1ll1lll1Il1l1, ):
            if (llll11llll1111llIl1l1 is not None):
                os.close(llll11llll1111llIl1l1)


def __init__(ll11l11l11ll11l1Il1l1, l11ll1llll111l11Il1l1):
    from reloadium.lib.environ import env
    from multiprocessing import util, spawn
    from multiprocessing.context import reduction, set_spawning_popen
    from multiprocessing.popen_spawn_win32 import TERMINATE, WINEXE, WINSERVICE, WINENV, _path_eq
    from pathlib import Path
    import os
    import msvcrt
    import sys
    import _winapi

    env.sub_process += 1
    env.save_to_os_environ()

    if (sys.version_info > (3, 8, )):
        from multiprocessing import resource_tracker as tracker 
        from multiprocessing.popen_spawn_win32 import _close_handles
    else:
        from multiprocessing import semaphore_tracker as tracker 
        _close_handles = _winapi.CloseHandle

    ll111l1l111l1lllIl1l1 = spawn.get_preparation_data(l11ll1llll111l11Il1l1._name)







    (llll11111ll11111Il1l1, ll1l11l11lll1lllIl1l1, ) = _winapi.CreatePipe(None, 0)
    lll1l11111lllll1Il1l1 = msvcrt.open_osfhandle(ll1l11l11lll1lllIl1l1, 0)
    l1l1lll1ll11l1l1Il1l1 = spawn.get_executable()
    ll1l111l11llll11Il1l1 = str(Path(ll111l1l111l1lllIl1l1['sys_argv'][0]).absolute())
    l111111ll111llllIl1l1 = ' '.join([l1l1lll1ll11l1l1Il1l1, '-B', '-m', 'reloadium_launcher', 'spawn_process', str(os.getpid()), 
str(llll11111ll11111Il1l1), ll1l111l11llll11Il1l1])



    if ((WINENV and _path_eq(l1l1lll1ll11l1l1Il1l1, sys.executable))):
        l1l1lll1ll11l1l1Il1l1 = sys._base_executable
        env = os.environ.copy()
        env['__PYVENV_LAUNCHER__'] = sys.executable
    else:
        env = None

    with open(lll1l11111lllll1Il1l1, 'wb', closefd=True) as llll1ll1lll1ll11Il1l1:

        try:
            (l111llll1111l1l1Il1l1, lll11l11l1111111Il1l1, l1lll11l1ll1ll11Il1l1, lllll111ll1111llIl1l1, ) = _winapi.CreateProcess(l1l1lll1ll11l1l1Il1l1, l111111ll111llllIl1l1, None, None, False, 0, env, None, None)


            _winapi.CloseHandle(lll11l11l1111111Il1l1)
        except :
            _winapi.CloseHandle(llll11111ll11111Il1l1)
            raise 


        ll11l11l11ll11l1Il1l1.pid = l1lll11l1ll1ll11Il1l1
        ll11l11l11ll11l1Il1l1.returncode = None
        ll11l11l11ll11l1Il1l1._handle = l111llll1111l1l1Il1l1
        ll11l11l11ll11l1Il1l1.sentinel = int(l111llll1111l1l1Il1l1)
        if (sys.version_info > (3, 8, )):
            ll11l11l11ll11l1Il1l1.finalizer = util.Finalize(ll11l11l11ll11l1Il1l1, _close_handles, (ll11l11l11ll11l1Il1l1.sentinel, int(llll11111ll11111Il1l1), 
))
        else:
            ll11l11l11ll11l1Il1l1.finalizer = util.Finalize(ll11l11l11ll11l1Il1l1, _close_handles, (ll11l11l11ll11l1Il1l1.sentinel, ))



        set_spawning_popen(ll11l11l11ll11l1Il1l1)
        try:
            reduction.dump(ll111l1l111l1lllIl1l1, llll1ll1lll1ll11Il1l1)
            reduction.dump(l11ll1llll111l11Il1l1, llll1ll1lll1ll11Il1l1)
        finally:
            set_spawning_popen(None)
