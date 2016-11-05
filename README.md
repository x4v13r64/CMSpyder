[![CircleCI](https://circleci.com/gh/j4v/CMSpyder/tree/master.svg?style=shield)](https://circleci.com/gh/j4v/CMSpyder/tree/master)
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/6f2f61d35ba345e7be82fad62c2d883c/badge.svg)](https://www.quantifiedcode.com/app/project/6f2f61d35ba345e7be82fad62c2d883c)
[![Code Health](https://landscape.io/github/j4v/CMSpyder/master/landscape.svg?style=flat)](https://landscape.io/github/j4v/CMSpyder/master)
[![codecov](https://codecov.io/gh/j4v/CMSpyder/branch/master/graph/badge.svg)](https://codecov.io/gh/j4v/CMSpyder)

# Project
Distributed www crawler/scrapper with:
- CMS detection
    - Plugin-based architecture
    - Version and plugin detection
    - Maintains historic versions
- Subdomain light bruteforcer (common subdomains e.g. blog., store.)
- Subdomain scrapper (1-deep)
- Subdirectory light bruteforcer (common directories e.g. /blog, /wp)
- Web interface for results and monitoring
- Static website to view results
    - Updated with daily statistics

#  Running
- Start the RabbitMQ server
`$ rabbitmq-server`
- Start the worker process
`$ DJANGO_SETTINGS_MODULE='cmspyder.settings.prod' celery -A cmspyder worker --concurrency=50 --pool=eventlet  --without-gossip -Q cmspyder_detect_cms_queue, cmspyder_discover_domains_queue`
- Start django
`$ python manage.py runserver 0.0.0.0:80 --settings=cmspyder.settings.dev --insecure`

# Milestones
1. ~~Prototype django application using celery~~
2. ~~Initial architecture for plugin-based detection~~
3. ~~Initial bakend configuration~~
4. ~~Third-party CI integration~~
5. ~~Second iteration~~
6. ~~Move GitHub site to Jekyll~~
7. Container (docker) build
8. Third iteration
    1. Subdomain discovery
    2. Subdirectory discovery
    3. Limit crawling of subnets (e.g. 5 min wait per /24)
    4. Bug fixes
    5. Test cases
9. Distributed architecture
    1. MongoDB cluster
10. Network hardening
11. Better Jekull website
    1. Statistics, graphs, text search
12. Elasticsearch integration    
13. TBD
