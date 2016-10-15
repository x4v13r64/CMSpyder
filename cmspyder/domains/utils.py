import socket

import tldextract

from models import TLD, Domain, Subdomain


def extract_subdomain(url):
    extract_result = tldextract.extract(url)
    return extract_result


def import_subdomain(url):
    extract_result = extract_subdomain(url)

    new_tld = TLD.objects.get_or_create(tld=extract_result.suffix)
    new_domain = Domain.objects.get_or_create(tld=new_tld[0],
                                              domain=extract_result.domain)
    new_subdomain = Subdomain.objects.get_or_create(domain=new_domain[0],
                                                    subdomain=extract_result.subdomain)
    return new_subdomain[0]


def get_ip(domain):
    """
    This method returns the first IP address string that responds as the given domain name
    """
    try:
        return socket.gethostbyname(domain)
    except Exception:
        return False


def get_ip_ex(domain):
    """
    This method returns an array containing one or more IP address strings that respond as the
    given domain name
    """
    try:
        return socket.gethostbyname_ex(domain)[2]
    except Exception:
        return False


def get_host(ip):
    """
    This method returns the 'True Host' name for a given IP address
    """
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return False


def get_alias(domain):
    """
    This method returns an array containing a list of aliases for the given domain
    """
    try:
        return socket.gethostbyname_ex(domain)[1]
    except Exception:
        return False
