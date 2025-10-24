import dns.resolver
import socket
import ipaddress
from typing import Dict, List, Optional


def get_a_records(domain: str) -> List[str]:
    try:
        answers = dns.resolver.resolve(domain, 'A')
        return [rdata.to_text() for rdata in answers]
    except Exception:
        return []


def get_aaaa_records(domain: str) -> List[str]:
    try:
        answers = dns.resolver.resolve(domain, 'AAAA')
        return [rdata.to_text() for rdata in answers]
    except Exception:
        return []


def get_mx_records(domain: str) -> List[str]:
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        return sorted([rdata.exchange.to_text() for rdata in answers])
    except Exception:
        return []


def get_txt_records(domain: str) -> List[str]:
    try:
        answers = dns.resolver.resolve(domain, 'TXT')
        return [b''.join(rdata.strings).decode('utf-8') for rdata in answers]
    except Exception:
        return []


def get_ns_records(domain: str) -> List[str]:
    try:
        answers = dns.resolver.resolve(domain, 'NS')
        return [rdata.to_text() for rdata in answers]
    except Exception:
        return []


def get_cname_chain(domain: str) -> List[str]:
    chain = []
    try:
        current = domain
        while True:
            answers = dns.resolver.resolve(current, 'CNAME')
            cname = answers[0].target.to_text()
            chain.append(cname)
            current = cname
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
        pass
    return chain


def resolve_ip(domain: str) -> Optional[str]:
    try:
        return socket.gethostbyname(domain)
    except Exception:
        return None


def get_ip_info(ip: str) -> Dict:
    try:
        ip_obj = ipaddress.ip_address(ip)
        return {
            "version": ip_obj.version,
            "is_private": ip_obj.is_private,
            "is_global": ip_obj.is_global,
            "is_loopback": ip_obj.is_loopback,
        }
    except Exception:
        return {}


def lookup(domain: str) -> Dict:
    ip = resolve_ip(domain)

    return {
        "domain": domain,
        "ip": ip,
        "ip_info": get_ip_info(ip) if ip else None,
        "dns": {
            "A": get_a_records(domain),
            "AAAA": get_aaaa_records(domain),
            "MX": get_mx_records(domain),
            "TXT": get_txt_records(domain),
            "NS": get_ns_records(domain)
        },
        "cname_chain": get_cname_chain(domain)
    }
