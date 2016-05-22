# Description
web spider (crawler/scrapper) with:
- CMS detection plugins (wordpress, joomla, drupal, magento), including version
- passive plugin/theme/[other] detection, including version
- mongodb document store (1 document per domain (or IP?))
    - keep historic versions (not updates)
- subdomain bruteforcer (blog, worpress, wp) - passive
- subdirectory bruteforcer (/blog, /wp) - active, light

# TODO
- design architecture
- CMS detection plugins
	- version detection
	- plugin/other detection + version detection
- web spider 'DONE - spyder'
- multithreaded handler `DONE - pyworker`
- distributed spider architecture (Fabric)
- document store (mongodb)
- add a lot of logging
- make thread count benchmarks to optimize number of threads per spyder

# Possibilities
- use WPScan code for WP detection
- use Wapalyzer code for CMS detection
- version detection with fingerprints

# Considerations
- not crawl same ip subnet often (e.g. 5 min wait per /24)
- crawl pages behind CDNs/cloudflare (with cloudflare-scrape and such)

# Projected
- use WPScan API to check for vulnerable versions/plugins for WP
- create website to visualise statistics

# Hardware (time4vps)
- 10x crawler (~75 treads per crawler == ~2 million URLs / day)
    - 20 million URLs / day -> 150 million URLs / week
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

