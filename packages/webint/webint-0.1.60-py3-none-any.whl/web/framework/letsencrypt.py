"""A simple Let's Encrypt interface (via `acme-tiny`)."""

import pathlib
import subprocess

import acme_tiny


def generate_cert(domain, certs_dir="certs"):
    """Generate a TLS certificate signed by Let's Encrypt for given domain."""
    certs_dir = pathlib.Path(certs_dir)
    challenge_dir = certs_dir / "challenges"
    challenge_dir.mkdir(exist_ok=True, parents=True)

    account_key = certs_dir / "account.key"
    if not account_key.exists():
        with account_key.open("w") as fp:
            subprocess.call(["openssl", "genrsa", "4096"], stdout=fp)

    domain_dir = certs_dir / domain
    domain_dir.mkdir(exist_ok=True)
    private_key = domain_dir / "domain.key"
    if not private_key.exists():
        with private_key.open("w") as fp:
            subprocess.call(["openssl", "genrsa", "4096"], stdout=fp)
    csr = domain_dir / "domain.csr"
    with csr.open("w") as fp:
        subprocess.call(
            [
                "openssl",
                "req",
                "-new",
                "-sha256",
                "-key",
                private_key,
                "-subj",
                "/",
                "-addext",
                f"subjectAltName = DNS:{domain}, DNS:www.{domain}",
            ],
            stdout=fp,
        )
    with (domain_dir / "domain.crt").open("w") as fp:
        fp.write(acme_tiny.get_crt(account_key, csr, challenge_dir))
