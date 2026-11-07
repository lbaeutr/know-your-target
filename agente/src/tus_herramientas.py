"""Herramientas iniciales de reconocimiento. AQUÍ PUEDES AÑADIR LAS TUYAS.

WHOIS (whois.py), DNS y crt.sh ya están implementadas y activas en lanzar.py.
DNS y crt.sh proceden de la solución del profesor (herramientas/recon.py).

Para ampliar: una tarea por función, @protegida, sin shell, con timeout,
salida recortada, errores como texto y resultados filtrados por el alcance.
Importa tu nueva función en lanzar.py y añádela a HERRAMIENTAS.

Ideas: subdominios_subfinder, wayback_urls, correos (theHarvester / hunter.io),
infraestructura_ip, correo_postura (SPF/DMARC/MTA-STS/CAA), urlscan, shodan_host.
"""

import json
import subprocess
import urllib.parse
import urllib.request

from guard import protegida, filtrar
from whois import recortar

UA = "aap-recon/1.0 (educativo; IES Rafael Alberti)"
TIPOS_DNS = {"A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"}


def _http(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


@protegida(objetivo="dominio")
def dns_registros(dominio: str, tipo: str = "A") -> str:
    """Consulta registros DNS de un dominio. tipo: A, AAAA, MX, NS, TXT, CNAME o SOA.
    Devuelve los valores, uno por línea."""
    tipo = tipo.upper()
    if tipo not in TIPOS_DNS:
        return f"ERROR: tipo DNS no válido ({tipo}). Usa uno de: {', '.join(sorted(TIPOS_DNS))}."
    try:
        r = subprocess.run(["dig", "+short", tipo, dominio],
                           capture_output=True, text=True, timeout=20)
    except subprocess.TimeoutExpired:
        return "ERROR: dig no respondió en 20 segundos."
    except OSError as e:
        return recortar(f"ERROR: no se pudo ejecutar dig: {e}")
    if r.returncode != 0:
        return recortar(f"ERROR: dig falló ({r.returncode}): {r.stderr.strip() or 'sin detalles'}")
    salida = recortar(r.stdout.strip())
    return salida or f"Sin registros {tipo} para {dominio}."


@protegida(objetivo="dominio")
def subdominios_crtsh(dominio: str) -> str:
    """Enumera subdominios de un dominio por transparencia de certificados (crt.sh).
    Pasivo: no toca el objetivo. Devuelve solo los subdominios dentro del alcance."""
    url = f"https://crt.sh/?q=%25.{urllib.parse.quote(dominio)}&output=json"
    try:
        datos = json.loads(_http(url, timeout=90))
    except Exception as e:
        return (f"ERROR: crt.sh no respondió ({e}). crt.sh suele ir lento; "
                "puedes reintentar más tarde o añadir otra fuente de subdominios.")
    if not isinstance(datos, list) or any(
        not isinstance(fila, dict) or not isinstance(fila.get("name_value"), str)
        for fila in datos
    ):
        return "ERROR: crt.sh devolvió un formato de certificados inesperado."
    nombres = set()
    for fila in datos:
        for n in str(fila.get("name_value", "")).splitlines():
            n = n.strip().lstrip("*.").lower()
            if n:
                nombres.add(n)
    dentro, fuera = filtrar(sorted(nombres))
    cab = f"{len(dentro)} subdominios en alcance ({fuera} filtrados por estar fuera):\n"
    return recortar(cab + "\n".join(dentro))


#  HERRAMIENTAS DE LUIS BAENA

_CDN = ("cloudfront", "akamai", "cloudflare", "fastly", "incapsula", "sucuri",
        "edgekey", "edgesuite", "azureedge", "llnwd")
_NUBE = ("amazon", "aws", "google", "1e100", "microsoft", "azure", "oracle",
         "digitalocean", "hetzner", "ovh", "vercel")


def _dig(args, timeout=20):
    """dig +short <args>. Devuelve (salida, error_texto). Sin shell."""
    try:
        r = subprocess.run(["dig", "+short", *args],
                           capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return "", "dig no respondió en el tiempo máximo"
    except OSError as e:
        return "", f"no se pudo ejecutar dig: {e}"
    if r.returncode != 0:
        return "", (r.stderr.strip() or f"dig devolvió el código {r.returncode}")
    return r.stdout.strip(), ""


@protegida(objetivo="dominio")
def correo_postura(dominio: str) -> str:
    """Postura de correo y DNSSEC de un dominio: SPF, DMARC, CAA y si la zona
    está firmada (DNSSEC). Solo consultas DNS pasivas (dig)."""
    txt, err = _dig(["TXT", dominio])
    if err:
        return recortar(f"ERROR: {err}")
    spf = [l for l in txt.splitlines() if "v=spf1" in l.lower()]
    lineas = ["SPF:    " + (spf[0] if spf else "no encontrado")]
    dmarc, _ = _dig(["TXT", f"_dmarc.{dominio}"])
    dm = [l for l in dmarc.splitlines() if "v=dmarc1" in l.lower()]
    lineas.append("DMARC:  " + (dm[0] if dm else "no encontrado"))
    dnskey, _ = _dig(["DNSKEY", dominio])
    lineas.append("DNSSEC: " + ("firmado" if dnskey else "sin firmar"))
    caa, _ = _dig(["CAA", dominio])
    lineas.append("CAA:    " + (caa.replace("\n", " | ") if caa else "no definido"))
    return recortar("\n".join(lineas))


def _cymru(ip: str):
    """IP -> (ASN, nombre_AS) por DNS (Team Cymru, sin clave). Solo IPv4."""
    octetos = ip.split(".")
    if len(octetos) != 4:
        return None
    rev = ".".join(reversed(octetos))
    txt, err = _dig(["TXT", f"{rev}.origin.asn.cymru.com"])
    if err or not txt:
        return None
    asn = txt.strip('"').split("|")[0].strip().split()[0]
    nombre_txt, _ = _dig(["TXT", f"AS{asn}.asn.cymru.com"])
    nombre = nombre_txt.strip('"').split("|")[-1].strip() if nombre_txt else ""
    return asn, nombre


def _clasificar(texto: str) -> str:
    t = texto.lower()
    if any(c in t for c in _CDN):
        return "-> CDN/WAF"
    if any(c in t for c in _NUBE):
        return "-> nube"
    return "-> posible exposicion directa"


@protegida(objetivo="dominio")
def infraestructura_ip(dominio: str) -> str:
    """Resuelve el dominio a IPv4 y, por cada una, su PTR (DNS inverso) y el
    dueño del rango (ASN y nombre, vía Team Cymru). Indica si la IP es de un
    CDN/WAF, de una nube o una exposición directa. Pasivo, sin clave."""
    salida, err = _dig(["A", dominio])
    if err:
        return recortar(f"ERROR: {err}")
    ips = [l for l in salida.split() if l.count(".") == 3 and l.replace(".", "").isdigit()]
    if not ips:
        return f"Sin registros A para {dominio} (puede ser un CNAME: prueba dns_registros)."
    lineas = []
    for ip in ips[:10]:
        ptr, _ = _dig(["-x", ip])
        info = _cymru(ip)
        dueno = f"AS{info[0]} {info[1]}" if info else "dueno desconocido"
        pista = _clasificar(f"{ptr} {dueno}")
        lineas.append(f"{ip}  [{dueno}]  PTR: {ptr or '-'}  {pista}")
    return recortar("\n".join(lineas))
