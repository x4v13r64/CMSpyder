# Description
web spider (crawler/scrapper) with:
- CMS detection plugins (wordpress, joomla, drupal, magento), including version
- passive plugin/theme/[other] detection, including version
- mongodb to store documents (1 document per domain (or IP?))
    - keep historic versions (not updates)
- subdomain bruteforcer (blog, worpress, wp) - passive
- subdirectory bruteforcer (/blog, /wp) - active, light

# TODO
- CMS detection plugins
	- version detection
	- plugin detection + plugin version detection
- web spider
- multithreaded handler `DONE - pyworker`
- distributed spider architecture (Fabric)
- database configuration (mongodb)

# Possibilities
- use WPScan code for WP detection
- use Wapalyzer code for CMS detection
- version detection with fingerprints

# Considerations
- not crawl same ip subnet often (e.g. 5 min wait per /24)
- dont GET whole page (use "Range" header)

# Projected
- use WPScan API to check for vulnerable versions/plugins for WP
- create website to visualise statistics

# Hardware (time4vps)
- 5x crawler (~40 treads per crawler)
- 2x 1TB db (replication or extension?)

### Database document format
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

## Sources
- http://www.michaelnielsen.org/ddi/how-to-crawl-a-quarter-billion-webpages-in-40-hours/

