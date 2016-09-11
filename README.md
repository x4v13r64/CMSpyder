#  How to run
- Start the RabbitMQ server `sudo rabbitmq-server`
- Start the worker process `celery -A cmspyder worker -l info --concurrency=500 --pool=eventlet`
- Start django `python manage.py runserver`

# Objective
Web spider (crawler/scrapper) with:
- CMS detection (WordPress, Joomla, Drupal, Magento) - including version detection
    - Keep historic versions (not updates)
- Passive plugin/theme/[other] detection - including version detection
- Subdomain light bruteforcer (common subdomains e.g. blog., store.) - active and passive detection
- Subdirectory bruteforcer (common directories e.g. /blog, /wp) - active, light
- Web interface for results and to monitor spiders (workers)
- Static website to view results (updated with daily statistics)

# Milestones
1. ~~Simple prototype django application using celery (sqlite backend)~~
2. Initial architecture for plugin-based detection (in progress)
3. Container (docker) architecture for spyder and backend
4. Additional features and backend hardening
5. tbd
5. Jekyll github-hosted website with daily statistics

# Technologies
- celery (with eventlet) to run tasks in parallel (event-driven)
- RabbitMQ task queue
- PostgresQL DB to store results
- Docker for worker containers & Docker Machine for deployment
- Django interface for results and monitoring of the backend
- Jekyll for public-facing sites and results

# Possibilities
- truncate/limit number of bytes downloaded (200kb chunks)
- add extraction of domains from spidered pages
- version detection with fingerprints
- scan-proof workers (tar-pit)

# Considerations
- not crawl same ip subnet often (e.g. 5 min wait per /24)
- crawl pages behind CDNs/cloudflare (with cloudflare-scrape and such)
- projected: use WPScan API to check for vulnerable versions/plugins for WP
