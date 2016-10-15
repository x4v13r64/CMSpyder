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
