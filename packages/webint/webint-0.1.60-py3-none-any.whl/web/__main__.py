"""Command line tools for the web."""

import inspect
import json
import logging
import pathlib
import time
import webbrowser

import gevent
import txt
import webagt
from rich.pretty import pprint

import web
import web.host
from web.host import console, providers

__all__ = ["main"]


main = txt.application("web", web.__doc__)


@main.register()
class Apps:
    """Show installed web apps."""

    def run(self, stdin, log):
        for pkg, apps in web.get_apps().items():
            for name, _, ns, obj in apps:
                print(f"{name} {ns}:{obj[0]}")
        return 0


@main.register()
class Fnord:
    def run(self, stdin, log):
        # import asyncio
        # asyncio.run(web.serve("web:abba", port=9999))
        web.StandaloneServer(web.abba, 9999).run()


@main.register()
class Run:
    """Run a web app locally."""

    def setup(self, add_arg):
        add_arg("app", help="name of web application")
        add_arg("--port", help="port to serve on")
        add_arg("--socket", help="file socket to serve on")
        add_arg("--watch", default=".", help="directory to watch for changes")

    def run(self, stdin, log):
        import asyncio

        if self.port:
            asyncio.run(web.serve(self.app, port=self.port, watch_dir=self.watch))
        elif self.socket:
            asyncio.run(web.serve(self.app, socket=self.socket, watch_dir=self.watch))
        else:
            print("must provide a port or a socket")
            return 1
        return 0

        # for pkg, apps in web.get_apps().items():
        #     for name, _, ns, obj in apps:
        #         if self.app == name:
        #             web.serve(ns, obj)
        #             return 0
        # return 1


def get_providers(provider_type):
    return [
        name.lower()
        for name, obj in inspect.getmembers(providers, inspect.isclass)
        if issubclass(obj, provider_type) and obj is not provider_type
    ]


@main.register()
class Config:
    """Config your environments."""

    def setup(self, add_arg):
        add_arg("--token", help="API access token")
        add_arg(
            "--host",
            choices=get_providers(providers.Host),
            help="machine host",
        )
        add_arg(
            "--registrar",
            choices=get_providers(providers.Registrar),
            help="domain registrars",
        )

    def run(self, stdin, log):
        if self.host:
            if not self.token:
                try:
                    if input("Do you need to create a new token? ") in "yY":
                        webbrowser.open(
                            "https://cloud.digitalocean.com/account/api/tokens/new"
                        )
                    self.token = input("Token: ")
                except EOFError:
                    return 1
            web.host.update_config(host=self.host, host_token=self.token)
        elif self.registrar:
            web.host.update_config(registrar=self.registrar, registrar_token=self.token)
        return 0


@main.register()
class Init:
    """Initialize a website."""

    def setup(self, add_arg):
        add_arg("name", help="name of website")
        add_arg("package", help="name of PyPI package to install")
        add_arg("app", help="name of web app to run")
        add_arg("--domain", help="domain name of website")

    def run(self, stdin, log):
        logging.basicConfig(
            level=logging.DEBUG,
            filename="debug.log",
            filemode="w",
            force=True,
            format="%(levelname)s:%(asctime)s:%(name)s:%(message)s",
        )
        config = web.host.get_config()
        if "host" not in config:
            console.print(f"No host configured.")
            return 1
        machines = config.get("machines", {})
        versions = web.host.Machine.versions
        start_time = time.time()
        total_time = 27
        with console.status(f"[bold green]~{total_time} minutes remaining") as status:

            def update_status():
                while True:
                    remaining_time = total_time - round((time.time() - start_time) / 60)
                    if remaining_time < 1:
                        status.update("Finishing up..")
                        return
                    status.update(f"[bold green]~{remaining_time} minutes remaining")
                    gevent.sleep(1)

            gevent.spawn(update_status)
            machine, secret = web.host.setup_website(self.name, self.package, self.app)
            webbrowser.open(f"https://{machine.address}?secret={secret}")
            web.host.finish_setup(machine)
            time.sleep(2)
        console.rule(f"[green]Bootstrapped {self.package} at {machine.address}")
        machines[self.name] = machine.address
        web.host.update_config(machines=machines)
        return 0


@main.register()
class Host:
    """Manage your host."""

    def run(self, stdin, log):
        config = web.host.get_config()
        if config["host"] == "digitalocean":
            host = providers.DigitalOcean(config["host_token"])
        else:
            console.print(f"Host {config['host']} not available.")
            return 1
        for machine in host.machines:
            console.rule(f"[bold red]{machine['name']}")
            pprint(machine)
        return 0


@main.register()
class Registrar:
    """Manage your registrar."""

    def run(self, stdin, log):
        config = web.host.get_config()
        if config["registrar"] == "dynadot":
            registrar = providers.Dynadot(config["registrar_token"])
        else:
            console.print(f"Registrar {config['registrar']} not available.")
            return 1
        for domain in registrar.domains:
            print(domain)
        return 0


if __name__ == "__main__":
    main()

# nuitka-project: --include-package=gevent.signal
# nuitka-project: --include-package=gunicorn.glogging
# nuitka-project: --include-package=gunicorn.workers.sync
# nuitka-project: --include-package=web.framework.templates
# nuitka-project: --include-package=web.host.templates
## nuitka-project: --include-package-data=mf2py
## nuitka-project: --include-package-data=selenium
