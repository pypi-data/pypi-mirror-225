"""Manage machines and domains."""

from __future__ import annotations

import configparser
import functools
import getpass
import io
import json
import logging
import os
import pathlib
import subprocess
import tempfile
import textwrap
import time
from contextlib import contextmanager
from pathlib import Path

import newmath
import toml
import webagt
from rich.console import Console

from .. import templating
from . import providers

__all__ = ["spawn_machine", "Machine"]


console = Console()
templates = templating.templates(__name__)
config_file = pathlib.Path("~/.webint").expanduser()


def get_config():
    """Get configuration."""
    try:
        with config_file.open() as fp:
            config = json.load(fp)
    except FileNotFoundError:
        config = {}
    return config


def update_config(**items):
    """Update configuration."""
    config = get_config()
    config.update(**items)
    with config_file.open("w") as fp:
        json.dump(config, fp, indent=2, sort_keys=True)
        fp.write("\n")
    return get_config()


def setup_website(website, package, app, config=None):
    if config is None:
        config = get_config()
    host = None
    if config["host"] == "digitalocean":
        host = providers.DigitalOcean(config["host_token"])
    elif config["host"] == "linode":
        host = providers.Linode(config["host_token"])
    console.print(f"Spawning virtual machine at {host.__class__.__name__}")
    machine = spawn_machine(website, host)
    console.print("Updating system")
    machine._apt("update")
    console.print("Installing firewall")
    machine._apt("install -yq ufw")
    machine.open_ports(22)
    console.print("Installing system software")
    machine.setup_machine()
    # TODO console.print("Starting to mine for onion")
    console.print("Installing python")
    machine.setup_python()
    console.print("Installing tor")
    machine.setup_tor()

    # machine = Machine("164.92.86.185", "root", "admin_key")
    # machine.onion = "hxpcvad6txrivhondry6htgmlc2idrxz37ofyobe7ynxpdxd7xdn5sid.onion"

    console.print("Installing nginx")
    machine.setup_nginx()
    console.print(f"Installing application: {app} of {package}")
    secret = newmath.nbrandom(4)
    machine.setup_app(package, app, config["host_token"], secret)
    # TODO console.print("Configuring domain name")
    return machine, secret


def finish_setup(machine):
    console.print("Installing node")
    machine.setup_node()
    console.print("Installing mediasoup")
    machine.setup_mediasoup()
    console.print("Installing etherpad")
    machine.setup_etherpad()


def spawn_machine(name: str, host: providers.Host) -> Machine:
    """Spawn a new machine from given `host`."""
    key_path = Path("admin_key")
    key_data = _get_key_data(key_path)
    for key in host.get_keys()["ssh_keys"]:
        if key["public_key"] == key_data:
            break
    else:
        key = host.add_key("admin", key_data)
    machine = host.create_machine(name, ssh_keys=[key["id"]])
    ip_details = {}
    while not ip_details:
        print("waiting for ip address")
        for ip_details in machine["networks"]["v4"]:
            if ip_details["type"] == "public":
                break
    # if not ip_details:
    #     print(machine)
    return Machine(ip_details["ip_address"], "root", key_path)


def _get_key_data(key_path: Path):
    """Return a SSH key, creating one if necessary."""
    pubkey_path = key_path.with_suffix(".pub")
    if not pubkey_path.exists():
        subprocess.run(
            [
                "ssh-keygen",
                "-o",
                "-a",
                "100",
                "-t",
                "ed25519",
                "-N",
                "",
                "-f",
                str(pubkey_path)[:-4],
            ]
        )
    with pubkey_path.open() as fp:
        return fp.read().strip()


class MachineBase:
    """A cloud machine."""

    def __init__(self, address=None, user=None, key=None):
        """Return the machine at `address`."""
        if address is None:
            address = "localhost"
        self.address = address
        if user is None:
            user = getpass.getuser()
        self.user = user
        self.key = key
        self.run = self.get_ssh()
        self.system_dir = Path("/root")
        self.bin_dir = self.system_dir / "bin"
        self.etc_dir = self.system_dir / "etc"
        self.src_dir = self.system_dir / "src"
        self.var_dir = self.system_dir / "var"

    def get_ssh(self, output_handler=None):
        """Return a function for executing commands over SSH."""

        def ssh(*command, env=None, stdin=None):
            combined_env = os.environ.copy()
            if env:
                combined_env.update(env)
            kwargs = {
                "env": combined_env,
                "stderr": subprocess.STDOUT,
                "stdout": subprocess.PIPE,
            }
            if stdin:
                kwargs["stdin"] = subprocess.PIPE

            class Process:
                def __init__(self):
                    self.lines = []

                def __iter__(self):
                    for line in self.lines:
                        yield line

                @property
                def stdout(self):
                    lines = []
                    for line in self.lines:
                        if line != (  # TODO FIXME
                            "bash: warning: setlocale: LC_ALL:"
                            " cannot change locale (en_US.UTF-8)"
                        ):
                            lines.append(line)
                    return "\n".join(lines)

            process = Process()
            key_args = []
            if self.key:
                key_args = ["-i", self.key]
            with subprocess.Popen(
                ["ssh"]
                + key_args
                + [
                    "-tt",  # FIXME necessary?
                    "-o",
                    "IdentitiesOnly=yes",
                    "-o",
                    "StrictHostKeyChecking no",
                    f"{self.user}@{self.address}",
                    *command,
                ],
                **kwargs,
            ) as proc:
                if stdin:
                    try:
                        for line in proc.communicate(
                            input=stdin.encode("utf-8"), timeout=6
                        )[0].decode("utf-8"):
                            process.lines.append(line)
                            if output_handler:
                                output_handler(line)
                            else:
                                logging.debug(line)
                    except subprocess.TimeoutExpired:
                        proc.kill()
                        stdout, stderr = proc.communicate()
                        logging.debug(f"stdout: {stdout}")
                        logging.debug(f"stderr: {stderr}")
                else:
                    for line in proc.stdout:
                        decoded_line = line.decode("utf-8").rstrip("\r\n")
                        process.lines.append(decoded_line)
                        logging.debug(decoded_line)
                        if output_handler:
                            output_handler(decoded_line)
            process.returncode = proc.returncode
            return process

        tries = 20
        while tries:
            result = ssh("true").returncode
            if result == 0:
                return ssh
            time.sleep(1)
            tries -= 1
        raise ConnectionError("SSH connection could not be made")

    def get(self, from_path, to_path=None) -> str:
        """"""

        def cp(path):
            self.cp(f"{self.user}@{self.address}:{from_path}", path)

        if to_path:
            cp(to_path)
        else:
            with tempfile.TemporaryDirectory() as tmpdirname:
                to_path = pathlib.Path(tmpdirname) / "alpha"
                cp(to_path)
                with to_path.open() as fp:
                    return fp.read()

    def send(self, from_path, to_path):
        """"""
        return self.cp(from_path, f"{self.user}@{self.address}:{to_path}")

    def cp(self, from_path, to_path):
        """Return a function for sending/retrieving a file over SCP."""
        with subprocess.Popen(
            [
                "scp",
                "-i",
                "admin_key",
                "-o",
                "IdentitiesOnly=yes",
                "-o",
                "StrictHostKeyChecking=no",
                from_path,
                to_path,
            ],
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
        ) as process:
            for line in process.stdout:
                logging.debug(line.decode("utf-8"))
        return process

    def setup_machine(self, locale="en_US.UTF-8"):
        """Upgrade the system, install system packages and configure the firewall."""
        # NOTE debian 11.3->11.5 upgrading SSH kills connection
        # self._apt("dist-upgrade -yq", bg=True)  # TODO use cron to run upgrade(s)
        self._apt(f"install -yq {' '.join(self.system_packages)}")

        self.run(
            f'echo "locales locales/default_environment_locale select {locale}"'
            " | debconf-set-selections"
        )
        self.run(
            f'echo "locales locales/locales_to_be_generated multiselect {locale} UTF-8"'
            " | debconf-set-selections"
        )
        self.run("rm /etc/locale.gen")
        self.run("dpkg-reconfigure --frontend noninteractive locales")

        self.run("adduser admin --disabled-login --gecos admin")
        # TODO --shell /usr/bin/zsh"
        self.run("chmod 700 ~admin")
        self.run(
            'echo "admin  ALL=NOPASSWD: ALL" | tee -a /etc/sudoers.d/01_admin'
        )  # XXX TODO FIXME !!!
        admin_ssh_dir = "/home/admin/.ssh"
        self.run(f"mkdir {admin_ssh_dir}")
        self.run(f"cp /root/.ssh/authorized_keys {admin_ssh_dir}")
        self.run(f"chown admin:admin {admin_ssh_dir} -R")
        self.run(f"mkdir {self.src_dir} {self.etc_dir}")

    def open_ports(self, *ports):
        """Wall off everything but SSH and web."""
        for port in ports:
            port, _, proto = str(port).partition("/")
            if not proto:
                proto = "tcp"
            self.run(f"ufw allow proto {proto} from any to any port {port}")
        self.run("ufw --force enable")

    def _apt(self, command, bg=False):
        time.sleep(1)  # the aptitude lock sometimes takes a second..
        command = f"apt-get -o DPkg::Lock::Timeout=60 {command}"
        if bg:
            command = f"nohup {command}"
        return self.run(command, env={"DEBIAN_FRONTEND": "noninteractive"})

    def _build(self, archive_url, *config_args):
        time.sleep(1)
        archive = Path(archive_url.rpartition("/")[2])
        with self.cd(self.src_dir) as src_dir:
            src_dir.run(f"wget https://{archive_url}")
            src_dir.run(f"tar xf {archive}")
            with src_dir.cd(archive.stem.removesuffix(".tar")) as archive_dir:
                archive_dir.run(f"bash ./configure {' '.join(config_args)}")
                archive_dir.run("make")
                archive_dir.run("make install")

    @contextmanager
    def cd(self, *directory_parts):
        """Return a context manager that changes the working directory."""
        directory = "/".join([str(p) for p in directory_parts])

        class Directory:
            run = functools.partial(self.run, f"cd {directory} &&")
            cd = functools.partial(self.cd, directory)

        yield Directory()

    @contextmanager
    def supervisor(
        self,
        # local_conf_name,
        section,
    ):
        """Return a context manager that provides access to Supervisor config files."""
        config = configparser.ConfigParser()
        yield config
        # local_conf = f"{local_conf_name}.conf"
        output = io.StringIO()
        config.write(output)

        self.run(
            f"cat > /etc/supervisor/conf.d/{section}.conf", stdin=output.getvalue()
        )
        # self.run(f"cat > {local_conf}", stdin=output.getvalue())
        # self.run(f"ln -sf {local_conf} /etc/supervisor/conf.d/{section}.conf")

        self.run("supervisorctl", "reread")
        self.run("supervisorctl", "update")


class Machine(MachineBase):
    """A full host in the cloud."""

    system_packages = (
        "apache2-utils",  # htpasswd for canopy+git support
        "autoconf",  # onion generation
        "brotli",  # wasm build for DT
        "build-essential",  # build tools
        "ccache",  # nuitka
        "cargo",  # rust (pycryptography)
        "exiftool",  # image/audio/video metadata introspection
        "expect",  # ssh password automation
        "fcgiwrap",  # Git w/ HTTP serving
        "ffmpeg",  # a/v en/de[code]
        "git",
        "graphviz",  # graphing
        "haveged",  # produces entropy for faster key generation
        "htop",
        "imagemagick",  # heic -> jpeg
        "libc6-dev",  # onion generation
        "libicu-dev",
        "libbz2-dev",  # bz2 support
        "libdbus-glib-1-2",  # Firefox
        "libenchant-2-dev",  # pyenchant => sopel => bridging IRC
        "libffi-dev",  # rust (pycryptography)
        "libgtk-3-0",
        "liblzma-dev",  # pronunciation
        "libncurses5-dev",
        "libncursesw5-dev",
        "libopus-dev",  # aiortc
        "libpcre2-dev",
        "libreadline-dev",
        "libsm-dev",
        "libsodium-dev",  # onion generation
        "libsqlite3-dev",  # SQLite Python extension loading
        "libssl-dev",
        "libvpx-dev",  # aiortc
        "neovim",
        "openvpn",
        "pandoc",  # markup translation
        "patchelf",  # nuitka
        "portaudio19-dev",  # PyAudio
        "psmisc",  # killall
        "python3-cryptography",  # pycrypto
        "python3-dev",  # Python build dependencies
        "python3-icu",  # SQLite unicode collation
        "python3-libtorrent",  # libtorrent
        "rsync",
        "silversearcher-ag",
        "sqlite3",  # SQLite flat-file relational database
        "sshfs",
        "stow",  # for dotfiles
        "supervisor",  # service manager
        "tmux",  # automatable terminal multiplexer
        "tree",
        "x11-utils",  # browser automation
        "xvfb",
        "xz-utils",  # .xz support
        "zip",  # .zip support
        "zlib1g-dev",
        "zsh",  # default shell
    )
    versions = {
        "python": "3.10.9",
        "node": "19",
        # "firefox": "97.0",
        # "geckodriver": "0.27.0",
    }
    ssl_ciphers = ":".join(
        (
            "ECDHE-RSA-AES256-GCM-SHA512",
            "DHE-RSA-AES256-GCM-SHA512",
            "ECDHE-RSA-AES256-GCM-SHA384",
            "DHE-RSA-AES256-GCM-SHA384",
            "ECDHE-RSA-AES256-SHA384",
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # XXX self.nginx_dir = self.system_dir / "nginx"
        # XXX self.python_dir = self.system_dir / "python"
        # XXX self.projects_dir = self.system_dir / "projects"
        self.runinenv = "/home/admin/runinenv"
        self.env_dir = pathlib.Path("/home/admin/app")
        self.run_dir = self.env_dir / "run"

    def setup_python(self):
        """
        Install Python (w/ SQLite extensions) for application runtime.

        Additionally create a `runinenv` for running things inside virtual environments.

        """
        self._build(
            "python.org/ftp/python/{0}/Python-{0}.tar.xz".format(
                self.versions["python"]
            ),
            # TODO "--enable-optimizations",  # NOTE adds 9 minutes
            "--enable-loadable-sqlite-extensions",
            # f"--prefix={self.python_dir}",
        )
        self.run(
            f"cat > {self.runinenv}",
            stdin=textwrap.dedent(
                """\
                #!/usr/bin/env bash
                VENV=$1
                . ${VENV}/bin/activate
                shift 1
                exec "$@"
                deactivate"""
            ),
        )
        self.run(f"chown admin:admin {self.runinenv}")
        self.run(f"chmod +x {self.runinenv}")

        self.run("wget https://install.python-poetry.org -q -O install_poetry.py")
        self.run("python3 install_poetry.py")

    def setup_node(self):
        """
        Install Node for application runtime.

        """
        self.run(f"wget https://deb.nodesource.com/setup_{self.versions['node']}.x")
        self.run(f"bash setup_{self.versions['node']}.x")
        self._apt("install -yq nodejs")
        self.run("npm install -g gulp-cli")

    def setup_mediasoup(self):
        """
        Install mediasoup.

        """
        self.open_ports(4443, "40000:49999/udp")
        chat_dir = self.run_dir / "media/chat"
        self.user = "admin"
        self.run(f"mkdir {chat_dir} -p")
        with self.cd(chat_dir) as clone_wd:
            clone_wd.run(
                "git clone https://github.com/angelogladding/mediasoup-demo.git"
            )
            with clone_wd.cd("mediasoup-demo/server") as server_wd:
                server_wd.run("npm install")
                server_wd.run("cat > config.js", stdin=str(templates.mediasoup()))
            with clone_wd.cd("mediasoup-demo/app") as app_wd:
                app_wd.run("npm install --legacy-peer-deps")
                app_wd.run("gulp dist")
        self.user = "root"
        self.mediasoup_dir = self.run_dir / "media/chat/mediasoup-demo"
        self.certs_dir = self.run_dir / "certs"
        with self.supervisor("mediasoup") as config:
            config["program:mediasoup_server"] = {
                "autostart": "true",
                "environment": (
                    f'MEDIASOUP_ANNOUNCED_IP="{self.address}",'
                    f'HTTPS_CERT_FULLCHAIN="{self.certs_dir}/selfsigned-ip.crt",'
                    f'HTTPS_CERT_PRIVKEY="{self.certs_dir}/selfsigned-ip.key"'
                ),
                "command": "node server.js",
                "directory": self.mediasoup_dir / "server",
                "stopsignal": "INT",
                "user": "admin",
            }

    def setup_etherpad(self):
        """
        Install etherpad.

        """
        pad_dir = self.run_dir / "media/pads"
        self.user = "admin"
        self.run(f"mkdir {pad_dir} -p")
        with self.cd(pad_dir) as clone_wd:
            clone_wd.run("git clone https://github.com/ether/etherpad-lite.git")
            with clone_wd.cd("etherpad-lite") as ep_wd:
                with ep_wd.cd("src") as src_wd:
                    src_wd.run("npm install sqlite3")
                password = "CHANGE_THIS"  # TODO
                ep_wd.run(
                    "cat > settings.json", stdin=str(templates.etherpad(password))
                )
                ep_wd.run("bash src/bin/installDeps.sh")
        self.user = "root"
        self.etherpad_dir = self.run_dir / "media/pads/etherpad-lite"
        with self.supervisor("etherpad") as config:
            config["program:etherpad"] = {
                "autostart": "true",
                "environment": 'NODE_ENV="production"',
                "command": "node src/node/server.js",
                "directory": self.etherpad_dir,
                "stopsignal": "INT",
                "user": "admin",
            }

    def setup_tor(self):
        """Install Tor for anonymous routing."""
        self._apt("install -yq tor")
        self.torrc = "/etc/tor/torrc"
        self.tor_data = "/var/lib/tor"
        self.run(
            f"cat > {self.torrc}",
            stdin=textwrap.dedent(
                f"""\
                HiddenServiceDir {self.tor_data}/main
                HiddenServicePort 80 127.0.0.1:80

                # leave this here for cat'ing over SSH..."""
            ),
        )
        self.run("service tor restart")
        self.onion = self.get(f"{self.tor_data}/main/hostname").strip()

    def setup_nginx(self):
        """
        Install Nginx (w/ TLS, HTTPv2, RTMP) for web serving.

        """
        self._apt("install -yq nginx libnginx-mod-rtmp")
        self.nginx_conf = "/etc/nginx"
        self.open_ports(80, 443, 1935)
        self.run(
            f"cat > {self.nginx_conf}/acme-challenge.conf",
            stdin=str(templates.nginx_acme_challenge(self.run_dir)),
        )
        self.run(
            f"cat > {self.nginx_conf}/ssl-params.conf",
            stdin=str(templates.nginx_ssl_params(f"{self.nginx_conf}/dhparam.pem")),
        )
        self.run(
            f"cat > {self.nginx_conf}/application.conf",
            stdin=str(templates.nginx_application(self.run_dir, self.onion)),
        )
        self.run(
            f"cat > {self.nginx_conf}/nginx.conf",
            stdin=str(templates.nginx(self.run_dir, self.address, [self.onion], {})),
        )
        self.run(f"chown admin:admin {self.nginx_conf}/nginx.conf")

        self.user = "admin"

        # streaming server
        streaming_dir = self.run_dir / "media/streaming"
        self.run(f"mkdir {streaming_dir} -p")
        self.run(f"mkdir {streaming_dir}/hls")
        self.run(f"mkdir {streaming_dir}/rec")

        # self-signed TLS certificate for IP address
        self.certs_dir = self.run_dir / "certs"
        self.run(f"mkdir {self.certs_dir} -p")
        domain_cnf = configparser.ConfigParser()
        domain_cnf.optionxform = str
        domain_cnf["req"] = {
            "distinguished_name": "req_distinguished_name",
            "prompt": "no",
        }
        domain_cnf["req_distinguished_name"] = {
            "countryName": "XX",
            "stateOrProvinceName": "N/A",
            "localityName": "N/A",
            "organizationName": "self-signed",
            "commonName": f"{self.address}: self-signed",
        }
        config_output = io.StringIO()
        domain_cnf.write(config_output)
        self.run(
            f"cat > {self.certs_dir}/selfsigned-ip.cnf",
            stdin=config_output.getvalue(),
        )
        self.run(
            "openssl req -x509 -nodes -days 365 -newkey rsa:2048"
            f" -keyout {self.certs_dir}/selfsigned-ip.key"
            f" -out {self.certs_dir}/selfsigned-ip.crt"
            f" -config {self.certs_dir}/selfsigned-ip.cnf"
        )

        self.run(f"sudo cp /var/lib/tor/main/hostname {self.run_dir}/onion")
        self.run(f"sudo chown admin:admin {self.run_dir}/onion")
        self.run(f"touch {self.run_dir}/domains")

        self.user = "root"

        # git server
        self.run(
            "git config --file=/lib/systemd/system/fcgiwrap.service Service.User admin"
        )
        self.run(
            "git config --file=/lib/systemd/system/fcgiwrap.service Service.Group admin"
        )
        self.run("systemctl daemon-reload")
        self.run("service fcgiwrap restart")

        self.generate_dhparam(512)  # NOTE 2048 adds ? minutes
        self.run("service nginx restart")

    def generate_dhparam(self, bits=4096):
        """Generate a unique Diffie-Hellman prime for Nginx."""
        self.run(f"openssl dhparam -out {self.nginx_conf}/dhparam.pem {bits}")
        self.run("service nginx restart")

    def setup_app(self, package, app, do_token=None, secret=None):
        """Install administrative interface."""
        self.user = "admin"
        self.run("python3 -m venv app")
        self.run(f"mkdir {self.run_dir}")

        webcfg = {}
        if do_token:
            webcfg["digitalocean_token"] = do_token
        if secret:
            webcfg["secret"] = secret
        if webcfg:
            self.run(
                f"cat > {self.run_dir}/webcfg.ini",
                stdin="\n".join(f'{k.upper()} = "{v}"' for k, v in webcfg.items())
                + "\n",
            )

        self.run(f"{self.runinenv} app pip install {package}")
        self.user = "root"
        with self.supervisor(package) as config:
            config["program:app"] = {
                "autostart": "true",
                "command": (
                    f"{self.runinenv} {self.env_dir} gunicorn {app} "
                    f"-k gevent -w 2 --bind unix:{self.run_dir}/gunicorn.sock"
                ),
                "directory": self.run_dir,
                "stopsignal": "INT",
                "user": "admin",
            }
            config["program:queue"] = {
                "autostart": "true",
                "command": f"{self.runinenv} {self.env_dir} bgq run",
                "directory": self.run_dir,
                "stopsignal": "INT",
                "user": "admin",
            }

    # def install_project(self, registrar, project_root=Path(".")):
    #     """Install sites from project in `project_root`."""
    #     # TODO install from Git URL
    #     with (project_root / "pyproject.toml").open() as fp:
    #         project = toml.load(fp)["tool"]["poetry"]
    #     try:
    #         sites = project["plugins"]["websites"]
    #     except KeyError:
    #         console.print("No sites found in `pyproject.toml`.")
    #         return
    #     name = project["name"]
    #     wheel = sorted((project_root / "dist").glob("*.whl"))[-1].name
    #     console.print(f"Installing project `{name}`")
    #     project_dir = self.projects_dir / name
    #     env_dir = f"{project_dir}/env"
    #     data_dir = f"{project_dir}/data"
    #     dist_dir = f"{project_dir}/dist"
    #     certs_dir = f"{project_dir}/certs"
    #     challenges_dir = f"{project_dir}/certs/challenges"

    #     # self.run(f"mkdir {data_dir} {dist_dir} {challenges_dir} -p")
    #     # self.run(f"{self.python_dir}/bin/python3 -m venv {env_dir}")
    #     # self.cp(f"dist/{wheel}", dist_dir)
    #     # self.run(f"{self.runinenv} {env_dir} pip install {dist_dir}/{wheel}")
    #     with self.supervisor(f"{self.projects_dir}/{name}", name) as config:
    #         for domain, obj in sites.items():
    #             domain = domain.replace("_", ".")
    #             console.print(f"Pointing https://{domain} to `{obj}`")
    #             d = webagt.uri.parse(domain)
    #             registrar.create_record(
    #                 f"{d.domain}.{d.suffix}", self.address, d.subdomain
    #             )
    #             config[f"program:{domain}-app"] = {
    #                 "autostart": "true",
    #                 "command": (
    #                     f"{self.runinenv} {env_dir} gunicorn {obj} "
    #                     f"-k gevent -w 2 --bind unix:{project_dir}/gunicorn.sock"
    #                 ),
    #                 "directory": data_dir,
    #                 "stopsignal": "INT",
    #                 "user": "root",
    #             }
    #             # config[f"program:{domain}-jobs"] = {
    #             #     "autostart": "true",
    #             #     "command": f"{self.runinenv} {env_dir} loveliness serve",
    #             #     "directory": data_dir,
    #             #     "stopsignal": "INT",
    #             #     "user": "root",
    #             # }
    #             # TODO create non-TLS nginx config for let's encrypting domain
    #             # TODO reload nginx
    #             # TODO initiate let's encrypt flow
    #             # TODO replace non-TLS nginx config with TLS-based config
    #             # TODO reload nginx
    #             local_nginx = project_dir / "nginx.conf"
    #             system_nginx = self.nginx_dir / f"conf/conf.d/project_{name}.conf"
    #             print("local", local_nginx)
    #             print("system", system_nginx)
    #             C = str(templates.nginx_site(domain, project_dir, self.ssl_ciphers))
    #             print(C)
    #             self.run(
    #                 f"cat > {local_nginx}",
    #                 stdin=C,
    #             )
    #             self.run(f"ln -sf {local_nginx} {system_nginx}")
