import re
import socket

import tldextract

from models import IP, TLD, Domain, Subdomain


def extract_subdomain(url):
    """
    Receives a url and returns an object created by tldextract.
    If there is no proper tldextract subdomain object, returns None.
    If there is an IP, saves it.
    :param url:
    :return:
    """
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
    """
    Receives a url and saves the TLD/domain/subdomain.
    If the subdomain isn't empty, also tries to save with an empty subdomain.
    :param url:
    :param discovered_by: the subdomain that pointed to the url
    :return:
    """
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
    Returns the first IP address string that responds as the given domain name.
    """
    try:
        return socket.gethostbyname(domain)
    except Exception:
        return False


def get_ip_ex(domain):
    """
    Returns an array containing one or more IP address strings that respond as the
    given domain name.
    """
    try:
        return socket.gethostbyname_ex(domain)[2]
    except Exception:
        return False


def get_host(ip):
    """
    Returns the 'True Host' name for a given IP address.
    """
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return False


def get_alias(domain):
    """
    Returns an array containing a list of aliases for the given domain.
    """
    try:
        return socket.gethostbyname_ex(domain)[1]
    except Exception:
        return False
