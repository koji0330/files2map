files2map
=========

Generate sitemap from local files

## require

 * lxml

## usage

	./files2map.py --config config.json `find ./path/to/target/ -name '*.html'`

## config file

### example



	{
	"COLUMN_ORDER": [
		"URI",
		"TITLE",
		"BREAD_CRUMBS"
	],
	"PARTS": {
		"URI": {
			"type": "path",
			"replace": [{
				"before": ".*docs.python.org",
				"after": ""
			}, {
				"before": "//",
				"after": "/"
			}]
		},
		"TITLE": {
			"type": "xpath",
			"value": "//title/text()"
		},
		"BREAD_CRUMBS": {
			"type": "xpath",
			"value": "//h3[text()='Navigation']/following-sibling::ul//text()",
			"replace": [{
				"before": "[\\s]+",
				"after": " "
			}, {
				"before": " index modules \\| next \\| previous \\| ",
				"after": ""
			}]
		}
	},
	"NOT_FOUND": "- NOT FOUND -"
	}