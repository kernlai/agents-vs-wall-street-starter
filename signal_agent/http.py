from __future__ import annotations

import ssl


def verified_ssl_context() -> ssl.SSLContext:
    """Use platform trust, falling back to certifi for python.org macOS builds."""
    context = ssl.create_default_context()
    if context.cert_store_stats().get("x509_ca", 0):
        return context
    try:
        import certifi
    except ImportError as error:
        raise RuntimeError(
            "Python has no trusted CA certificates; install certifi or run the Python Install Certificates command"
        ) from error
    return ssl.create_default_context(cafile=certifi.where())
