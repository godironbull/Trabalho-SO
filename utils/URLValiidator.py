
import ipaddress
import re
import socket
from urllib.parse import urlsplit


class URLValidator:
    DOMINIO = re.compile(
        r"^([a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?\.)+"
        r"([a-z]{2,}|xn--[a-z0-9-]+)$"
    )

    def is_valid(self, url):
        """Verifica se a URL possui esquema e host válidos."""
        if not isinstance(url, str) or re.search(r"\s", url):
            return False

        try:
            partes = urlsplit(url)
            partes.port
        except ValueError:
            return False

        host = partes.hostname

        if partes.scheme not in ("http", "https") or not host:
            return False

        if host == "localhost" or self.DOMINIO.fullmatch(host):
            return True

        try:
            ipaddress.ip_address(host)
            return True
        except ValueError:
            return False

    def resolve_dns(self, url):
        """Resolve o DNS da URL."""
        if not self.is_valid(url):
            raise ValueError(f"URL inválida: {url!r}")

        host = urlsplit(url).hostname

        try:
            return list({
                info[4][0]
                for info in socket.getaddrinfo(host, None)
            })
        except socket.gaierror as e:
            raise ConnectionError(
                f"DNS não resolveu {host}"
            ) from e

    def verificar(self, url,proridade=0):
        """Valida uma URL e retorna seus endereços IP."""
        try:
            ips = self.resolve_dns(url)

            return {
                "prioridade": proridade,
                "url": url,
                "ok": True,
                "ips": ips,
                "erro": None
            }

        except (ValueError, ConnectionError) as e:
            return {
                "prioridade": proridade,
                "url": url,
                "ok": False,
                "ips": [],
                "erro": str(e)
            }
