# openWebSignals

A FastAPI-based web service that provides comprehensive website intelligence and analysis capabilities. The service offers DNS record analysis, SSL certificate validation, and optional reverse DNS lookup functionality.

## Features

- DNS Record Analysis
  - A Records (IPv4)
  - AAAA Records (IPv6)
  - MX Records (Mail Servers)
  - TXT Records
  - NS Records (Name Servers)
  - CNAME Chain Resolution
- SSL Certificate Information
  - Validity Status
  - Issuer Details
  - Subject Information
  - Expiration Dates
  - Days Until Expiration
- IP Address Information
  - IP Version
  - Private/Public Status
  - Global/Local Status
  - Loopback Status
- Optional Reverse DNS Lookup

## Installation

1. Clone the repository:
```bash
git clone https://github.com/h2ggdev/openWebSignals.git
cd openWebSignals
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Dependencies

- FastAPI v0.111.1
- Requests v2.31.0
- DNSPython v2.3.0
- AsyncIO v4.0.0

## API Endpoints

### Health Check
```
GET /health
```
Returns the service health status.

Response:
```json
{
    "status": "healthy"
}
```

### Website Analysis
```
GET /analyze?url={domain}&reverse_dns={boolean}
```

Parameters:
- `url` (required): The domain to analyze
- `reverse_dns` (optional): Boolean flag to enable reverse DNS lookup

Example Response:
```json
{
    "url": "example.com",
    "domain": "example.com",
    "ip": "93.184.216.34",
    "ip_info": {
        "version": 4,
        "is_private": false,
        "is_global": true,
        "is_loopback": false
    },
    "network": {
        "dns": {
            "A": ["93.184.216.34"],
            "AAAA": ["2606:2800:220:1:248:1893:25c8:1946"],
            "MX": ["mail.example.com"],
            "TXT": ["v=spf1 -all"],
            "NS": ["ns1.example.com", "ns2.example.com"]
        },
        "cname_chain": []
    },
    "ssl": {
        "valid": true,
        "issuer": {
            "O": "DigiCert Inc",
            "CN": "DigiCert TLS RSA SHA256 2020 CA1"
        },
        "subject": {
            "CN": "example.com"
        },
        "not_before": "Oct 1 00:00:00 2025 GMT",
        "not_after": "Oct 30 23:59:59 2025 GMT",
        "days_to_expire": 6
    },
    "reverse_dns": "example.com"
}
```

## Project Structure

```
openWebSignals/
├── src/
│   ├── main.py              # FastAPI application setup and middleware
│   ├── routes/
│   │   ├── analyze.py       # Analysis endpoint handlers
│   │   └── health.py        # Health check endpoint
│   └── services/
│       ├── dns_lookup.py    # DNS record lookup functionality
│       └── ssl_info.py      # SSL certificate analysis
└── requirements.txt         # Project dependencies
```

## Features in Detail

### DNS Lookup Service
The DNS lookup service provides comprehensive domain name system information including:
- IPv4 and IPv6 address records
- Mail exchange records
- Text records (includes SPF, DKIM, etc.)
- Name server records
- CNAME chain resolution
- IP address metadata (version, scope, visibility)

### SSL Certificate Analysis
The SSL service checks and validates SSL certificates, providing:
- Certificate validity status
- Issuer organization and common name
- Subject details
- Validity period
- Expiration countdown

### Request Logging
The application includes built-in request logging middleware that tracks:
- HTTP method
- Request path
- Response time (milliseconds)
- Status code

## Development

To run the development server:

```bash
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`. You can access the interactive API documentation at `http://localhost:8000/docs`.

## License
Apache 2.0

## Author
h2ggdev