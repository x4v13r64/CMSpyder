# Objective
Web spider (crawler/scrapper) with:
- CMS detection (WordPress, Joomla, Drupal, Magento) - including version detection
    - Keep historic versions (not updates)
- Passive plugin/theme/[other] detection - including version detection
- Subdomain light bruteforcer (common subdomains e.g. blog., store.) - active and passive detection
- Subdirectory bruteforcer (common directories e.g. /blog, /wp) - active, light
- Web interface for results and to monitor spiders (workers)
- Static website to view results (updated with daily statistics)

#  Running the project
- Start the RabbitMQ server `sudo rabbitmq-server`
- Start the worker process `celery -A cmspyder worker -l info --concurrency=500 --pool=eventlet`
- Start django `python manage.py runserver`

# Milestones
1. ~~Simple prototype django application using celery (sqlite backend)~~
2. ~~Initial architecture for plugin-based detection~~ 
3. Container (docker) architecture for spyder and backend **[in progress]**
4. Flower integration to monitor tasks
5. Additional features and backend hardening
6. Tests, documentation and CI
7. Jekyll github-hosted website with daily statistics
8. Additional plugins

# Features (unordered)
- truncate/limit number of bytes downloaded (200kb chunks)
- version detection with fingerprints
- scan-proof workers (tar-pit)
- Add header-based detection
- not crawl same ip subnet often (e.g. 5 min wait per /24)
- crawl 1-deep to find new subdomains
- crawl pages behind CDNs/cloudflare (with cloudflare-scrape and such)
- projected: use WPScan API to check for vulnerable versions/plugins for WP

# Technologies
- celery (with eventlet) to run tasks in parallel (event-driven)
 - flow to monitor celery tasks
- RabbitMQ task queue
- PostgresQL DB to store results
- Nginx and Gunicorn for controller web
- Docker for worker containers & Docker Machine for deployment
- Django interface for results and monitoring of the backend
- Jekyll for public-facing sites and results
