[![CircleCI](https://circleci.com/gh/j4v/CMSpyder/tree/master.svg?style=shield)](https://circleci.com/gh/j4v/CMSpyder/tree/master)
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/6f2f61d35ba345e7be82fad62c2d883c/badge.svg)](https://www.quantifiedcode.com/app/project/6f2f61d35ba345e7be82fad62c2d883c)

# Project
Web crawler/scrapper with:
- CMS detection
    - Plugin-based architecture
    - Version and plugin detection
    - Maintains historic versions
- Subdomain bruteforcer (common subdomains e.g. blog., store.)
- Subdomain scrapper (1-deep)
- Subdirectory bruteforcer (common directories e.g. /blog, /wp)
- Web interface for results and monitoring
- Static website to view results
    - Updated with daily statistics

#  Running
- Start the RabbitMQ server
`$ rabbitmq-server`
- Start the worker process
`$ DJANGO_SETTINGS_MODULE='cmspyder.settings.dev' celery -A cmspyder worker -l info --concurrency=10 --pool=eventlet`
- Start django
`$ python manage.py runserver 0.0.0.0:80 --settings=cmspyder.settings.dev --insecure`


# Milestones
1. ~~Prototype django application using celery~~
2. ~~Initial architecture for plugin-based detection~~
    1. ~~WordPress basic plugin~~
3. ~~Initial bakend configuration~~
4. ~~CircleCI integration~~
5. ~~QuantifiedCode integration~~
6. Second iteration **[in progress]**
    1. Basic features
    2. Limit crawling of subnets (e.g. 5 min wait per /24)
    3. Add header-based detection
    4. Joomla basic plugin
    5. Drupal basic plugin
    6. Magento basic plugin
    7. Bug fixes
    8. Test cases
7. Flower integration to monitor tasks
8. Backend hardening
    1. Nginx/Gunicorn controller web
    2. celery as service
    3. Firewall rules for all machines
9. Third iteration
    1. Subdomain discovery
    2. Subdirectory discovery
    3. Other features
    4. Test cases
10. Jekyll github-hosted website with daily statistics
11. TBD
12. Container (docker) architecture (currently not supported by VPS hosting)

# Technologies
- celery (with eventlet) to run tasks in parallel
- flow to monitor celery tasks
- RabbitMQ task queue
- PostgresQL DB to store results
- Django interface for results and monitoring of the backend
- Nginx and Gunicorn for controller web
- Jekyll for public-facing sites and results
- Docker for worker containers & Docker Machine for deployment
