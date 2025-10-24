from fastapi import APIRouter, Query
from src.services import dns_lookup, ssl_info
import asyncio
import socket
from concurrent.futures import ThreadPoolExecutor

router = APIRouter(prefix="/analyze", tags=["analyze"])

# Thread pool for async reverse DNS
executor = ThreadPoolExecutor(max_workers=10)

async def reverse_dns_async(ip: str, timeout: float = 1.0) -> str | None:
    """
    Async reverse DNS lookup using socket.getnameinfo.
    Returns hostname or None if lookup fails or times out.
    """
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(executor, socket.getnameinfo, (ip, 0), 0)
    try:
        hostname, _ = await asyncio.wait_for(future, timeout=timeout)
        return hostname
    except Exception:
        return None

@router.get("")
async def analyze(url: str = Query(...), reverse_dns: bool = Query(False)):
    # -----------------------------
    # DNS lookup using updated dns_lookup module
    # -----------------------------
    try:
        domain_data = dns_lookup.lookup(url)
    except Exception as e:
        return {"error": str(e), "url": url}

    if not domain_data["ip"] and not domain_data["dns"]["A"]:
        return {"error": "Domain not found", "url": url}

    # -----------------------------
    # SSL info
    # -----------------------------
    ssl_data = ssl_info.get_ssl_info(url)

    # -----------------------------
    # Optional async reverse DNS
    # -----------------------------
    rdns_result = None
    if reverse_dns and domain_data["ip"]:
        rdns_result = await reverse_dns_async(domain_data["ip"])

    # -----------------------------
    # Build response
    # -----------------------------
    response = {
        "url": url,
        "domain": domain_data["domain"],
        "ip": domain_data["ip"],
        "ip_info": domain_data.get("ip_info"),
        "network": {
            "dns": domain_data["dns"],
            "cname_chain": domain_data.get("cname_chain", [])
        },
        "ssl": ssl_data
    }

    if reverse_dns:
        response["reverse_dns"] = rdns_result

    return response
