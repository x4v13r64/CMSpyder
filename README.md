# Objective
web spider (crawler/scrapper) with:
- CMS detection (WordPress, Joomla, Drupal, Magento) - including version detection
- passive plugin/theme/[other] detection - including version detection
- mongodb document store (1 document per domain)
    - keep historic versions (not updates)
- subdomain bruteforcer (common subdomains e.g. blog., store.) - passive
- subdirectory bruteforcer (common directories e.g. /blog, /wp) - active, light
- website to view statistics (TBD)

# Technologies
- celery + eventlet to run tasks in parallel (event-driven)
- reddis broker for spidering jobs
- mongodb document store for spider results
- Fabric for machine managing
- custom detection plugins
- TBD website to view statistics

# Todo
- design architecture
    - the goal is to have a modular architecture where the spidering is separated from
      the detection plugins
- implement celery + eventlet spider with reddis broker
- CMS detection plugins
	- WordPress
	- Joomla
	- Magento
	- Drupal
- distributed worker handling with Fabric
    - the goal is to have a complete interface to monitor and control workers and tasks
- add a lot of logging (check out logbook + celery logging functionalities)
- website to visualize statistics

# Possibilities
- add extraction of domains from spidered pages
- version detection with fingerprints
- scan-proof workers (tar-pit)

# Considerations
- not crawl same ip subnet often (e.g. 5 min wait per /24)
- crawl pages behind CDNs/cloudflare (with cloudflare-scrape and such)

# Projected
- use WPScan API to check for vulnerable versions/plugins for WP

# Hardware (VPS)
- 1 controller
- 10x spiders
- 2x 2TB db (master-slave replication)

# document store format
```
{
	_id
	domain (unique)
	ip
	country
	date_created
	entries [
		{
			type
			date_created
			version
			country
			subdomain/subpath
			ip
			date_created
			plugins [
				{name, version},
			]
		},
	]
}
```

# Sources
- http://www.michaelnielsen.org/ddi/how-to-crawl-a-quarter-billion-webpages-in-40-hours/
- https://andrewwilkinson.wordpress.com/2011/09/27/beating-google-with-couchdb-celery-and-whoosh-part-1/
- http://danielfrg.com/blog/2013/09/11/django-celery-readability-crawler/

