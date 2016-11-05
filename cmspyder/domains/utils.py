import socket

import tldextract
import re

from models import TLD, Domain, Subdomain, IP


def extract_subdomain(url):
    extract_result = tldextract.extract(url.lower())
    # make sure we have a valid domain and TLD
    if extract_result.domain and extract_result.suffix:
        return extract_result
    else:
        # try to extract ip from url
        if extract_result.domain:
            ip_list = re.findall(r'[0-9]+(?:\.[0-9]+){3}', extract_result.domain)
            if ip_list:
                for ip in ip_list:
                    new_ip = IP.objects.get_or_create(ip=ip)
        # return nothing
        return None


def import_subdomain(url, discovered_by=None):
    extract_result = extract_subdomain(url.lower())
    if extract_result:
        new_tld = TLD.objects.get_or_create(tld=extract_result.suffix)
        new_domain = Domain.objects.get_or_create(tld=new_tld[0],
                                                  domain=extract_result.domain)
        new_subdomain = Subdomain.objects.get_or_create(domain=new_domain[0],
                                                        subdomain=extract_result.subdomain,
                                                        discovered_by=discovered_by)
        # also create with empty subdomain
        new_empty_subdomain = Subdomain.objects.get_or_create(domain=new_domain[0],
                                                              subdomain="",
                                                              discovered_by=discovered_by)
        return new_subdomain[0]
    else:
        return None


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
