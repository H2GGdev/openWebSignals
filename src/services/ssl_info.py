import ssl
import socket
from datetime import datetime
from typing import Optional, Dict

def get_ssl_info(hostname: str, port: int = 443) -> Dict[str, Optional[str]]:
    """
    Returns SSL certificate info for a domain.
    """
    context = ssl.create_default_context()
    ssl_info = {
        "valid": False,
        "issuer": None,
        "subject": None,
        "not_before": None,
        "not_after": None,
        "days_to_expire": None,
        "error": None
    }
    try:
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                ssl_info["valid"] = True
                ssl_info["issuer"] = dict(x[0] for x in cert.get("issuer"))
                ssl_info["subject"] = dict(x[0] for x in cert.get("subject"))
                ssl_info["not_before"] = cert.get("notBefore")
                ssl_info["not_after"] = cert.get("notAfter")
                
                # Calculate days until expiry
                not_after_dt = datetime.strptime(cert.get("notAfter"), "%b %d %H:%M:%S %Y %Z")
                ssl_info["days_to_expire"] = (not_after_dt - datetime.utcnow()).days
    except Exception as e:
        ssl_info["error"] = str(e)
    
    return ssl_info
