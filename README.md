files2map
=========

Generate sitemap from local files.

## Require

 * lxml

## Usage

	files2map.py [-h] [--config CONFIG] html_file [html_file ...]

### Example

	# Number of files is less.
	./files2map.py --config config.json `find ./path/to/target/ -name '*.html'`
	# Number of files is large.
	find ./path/to/target/ -name '*.html' -exec ./files2map.py --config config.json {} \;

## Config file

### Description

 * `COLUMN_ORDER`: <br>
   Define a sequence of elements in a part.
 * `PARTS`: <br>
   Define each element.
 * `type`: <br>
   Set `xpath` or `path`.
 * `replace`: <br>
   Define a regular expression substitution.
   

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