import shutil
from pathlib import Path

from . import Machine

test_dir = Path("/tmp/webint-web.host-test")


def setup_module(module):
    try:
        shutil.rmtree(test_dir)
    except FileNotFoundError:
        pass


# TODO make work inside of `act`
# XXX def test_machine():
# XXX     machine = Machine()
# XXX     assert machine.run(f"mkdir {test_dir}").returncode == 0
# XXX     assert machine.run(f"ls {test_dir} -1").returncode == 0
# XXX
# XXX
# XXX def test_cd():
# XXX     machine = Machine()
# XXX     with machine.cd(test_dir) as root_dir:
# XXX         root_dir.run("mkdir foobar").returncode == 0
# XXX         with root_dir.cd("foobar") as foobar_dir:
# XXX             foobar_dir.run("mkdir batbaz").returncode == 0
# XXX             with foobar_dir.cd("batbaz") as batbaz_dir:
# XXX                 batbaz_dir.run("mkdir a b c").returncode == 0
# XXX                 assert batbaz_dir.run("ls -1").lines[:3] == ["a", "b", "c"]
# XXX     assert (test_dir / "foobar/batbaz/a").exists()
