#!/usr/env/python2

"""todo docstring"""

import requests
# import requesocks
import Queue
import pyworker
import time

__author__ = "j4v"
__copyright__ = "Copyright 2016, www"
__license__ = "GPL"
__version__ = "3"
__maintainer__ = "j4v"
__email__ = "j4v@posteo.net"


def spyder_domain(domain):

        # initialise SOCKS session
        session = requests.session()
        session.verify = False  # don't check certificate
        session.stream = True
        session.allow_redirects = True
        # todo update with pysocks
        # initialise SOCKS session with Tor
        # session_tor = requesocks.session()
        # session_tor.verify = False  # don't check certificate
        # session_tor.stream = True
        # session_tor.proxies = {'http': 'socks5://127.0.0.1:9050',
        #                        'https': 'socks5://127.0.0.1:9050'}

        url_http = 'http://%s' % domain
        url_https = 'https://%s' % domain
        output_path = 'stuff/%s.txt' % domain.replace('.', '_')

        # build request headers
        # todo User-Agent take from list
        headers = \
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
             'Accept': 'text/html, application/xhtml+xml, */*',
             'Accept Encoding': 'gzip, deflate',
             'Accept Language': 'en-US,en;q=0.5',
             #'Referer':'asdf'
             'Connection': 'Keep-Alive'}

        # try to get a valid http response
        valid_response = False  # set to True if success
        try:
            r = session.get(url_http, headers=headers)
            # r = session_tor.get(url, headers=headers)
        # todo better exception handling
        except Exception:
            try:
                r = session.get(url_https, headers=headers)
                # r = session_tor.get(url_https, headers=headers)
            except Exception:
                try:
                    r = session.get(url_http, headers=headers)
                except Exception:
                    try:
                        r = session.get(url_https, headers=headers)
                    except Exception:
                        pass
                else:
                    valid_response = True
            else:
                valid_response = True
        else:
            valid_response = True

        # save file
        if valid_response:
            if r.status_code == 200:
                with open(output_path, 'wb') as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
                f.close()
            else:
                print domain, r.status_code
        else:
            print domain, False

def main():

    # create queue with last x domains from alexa top million
    tasks = Queue.Queue()
    with open('alexa_top_million.txt', 'r') as f:
        last_x = [domain.strip() for domain in f.readlines()[-10000:-1]]
    for domain in last_x:
        tasks.put(domain)

    # create and start timed controller
    timed_thread_controller = pyworker.TimedThreadController(max_job_time=10,
                                                             worker_count=75,
                                                             tasks=tasks,
                                                             job=spyder_domain)
    start = time.time()
    timed_thread_controller.run()
    stop = time.time()
    print stop - start


if __name__ == "__main__":
    main()
