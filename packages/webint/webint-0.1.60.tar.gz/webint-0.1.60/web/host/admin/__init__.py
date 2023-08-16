import json
import pathlib
import subprocess

import dns.exception
import dns.resolver
import easyuri
import web
import whois

from .. import providers

app = web.application(__name__)
config_file = pathlib.Path(".webapp").expanduser()

domain_registrars = {"101domain grs ltd": "101domain.com"}
domain_hosts = {
    "101domain.com": (
        "101domain",
        "101domain.com",
        "help.101domain.com/domain-management/name-servers-dns/modifying-name-servers-and-records/managing-name-server-records",
    ),
    "domaincontrol.com": (
        "GoDaddy",
        "godaddy.com",
        "www.godaddy.com/help/add-an-a-record-19238",
    ),
    "dreamhost.com": (
        "DreamHost",
        "dreamhost.com",
        "help.dreamhost.com/hc/en-us/articles/360035516812-Adding-custom-DNS-records",
    ),
    "dyna-ns.net": (
        "Dynadot",
        "dynadot.com",
        "www.dynadot.com/community/help/question/create-A-record",
    ),
    "name.com": (
        "Name.com",
        "name.com",
        "www.name.com/support/articles/205188538-pointing-your-domain-to-hosting-with-a-records",
    ),
}


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


def get_onions():
    onions = []
    for hidden_service in pathlib.Path("/var/lib/tor").glob("main*"):
        with (hidden_service / "hostname").open() as fp:
            onions.append(fp.read().strip())
    return onions


@app.wrap
def contextualize(handler, mainapp):
    web.tx.host.local_ip = (
        subprocess.run(["hostname", "-I"], capture_output=True)
        .stdout.split()[0]
        .decode()
    )
    yield


@app.control("")
class Index:
    def get(self):
        config = get_config()
        return app.view.index(
            config.get("application"),
            get_onions(),
            config.get("domains", []),
        )


@app.control("application")
class Application:
    def get(self):
        return app.view.application(get_config().get("application"))


@app.control("onions")
class Onions:
    def get(self):
        return app.view.onions(get_onions())


@app.control("domains")
class Domains:
    def get(self):
        return app.view.domains(get_config().get("domains", []))


class A:
    def get(self):
        form = web.form(name=None, domain=None)
        try:
            with open("/var/lib/tor/main/hostname") as fp:
                onion = fp.read().strip()
        except FileNotFoundError:
            onion = "s9d8df3jhif98.onion"
        local_ip = (
            subprocess.run(["hostname", "-I"], capture_output=True)
            .stdout.split()[0]
            .decode()
        )
        domain_ns = None
        domain_ip = None
        www_domain_ip = None
        domain_whois = None
        domain_host = None
        if form.domain:
            resolver = dns.resolver.Resolver()
            # resolver.nameservers = ["8.8.8.8"]
            try:
                domain_ip = list(resolver.resolve(form.domain).rrset)[0].address
                www_domain_ip = list(resolver.resolve(f"www.{form.domain}").rrset)[
                    0
                ].address
            except dns.exception.DNSException:
                pass
            domain_whois = whois.whois(form.domain)
            try:
                if domain_whois["name_servers"]:
                    _nameservers = sorted(set(domain_whois["name_servers"]))
                    domain_host = domain_hosts[
                        easyuri.parse(_nameservers[0]).suffixed_domain
                    ]
                else:
                    domain_host = domain_hosts[
                        domain_registrars[domain_whois["registrar"].lower()]
                    ]
            except KeyError:
                pass
            if local_ip == domain_ip and form.action == "bootstrap":
                return "bootstrap"
        return app.view.index(
            onion,
            form.name,
            local_ip,
            form.domain,
            domain_whois,
            domain_host,
            domain_ns,
            domain_ip,
            www_domain_ip,
        )
