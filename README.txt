
INTRODUCTION
============
Syndicate converts all the Markdown files in a directory into HTML files according to a user-defined template. You can use this script to auto-generate static web sites with consistent styles and layout on each page. Learn more at http://www.princeton.edu/~saha/syndicate/

USAGE
=====
1. Download markdown.pl from http://daringfireball.net/projects/markdown/
2. Place all your markdown.txt files in directories that are children to wherever the syndicate.py script is located
3. Edit post.html to your liking. This file serves as a template for all of your posts. Reserve {{ title }} and {{ body }} patterns for Syndicate to parse. The {{ title }} pattern will be replaced with the first line of each Markdown file, with leading # removed. The {{ body }} pattern will be replaced with the contents of your entire parsed Markdown file.
4. Run "python producer.py post.html"
5. You'll find an index.html in every directory that has a markdown.txt

GENERATING STATIC WEB SITES
===========================
To use Syndicate to auto-generate static web sites, I suggest the following directory structure:

- syndicate.py
- markdown.pl
- post.html
- production/
- - index.html
- - static/
- - - css/
- - - img/
- - - js/
- - article1/
- - - markdown.txt
- - article2/
- - - markdown.txt
- - article3/
- - - markdown.txt

The example above shows a simple web site that contains three articles currently written in Markdown. Performing step #5 as described above will create index.html in the article1/, article2/, and article3/ folders.

To publish the web site, just copy the contents of the production/ folder to your web server. Ideally, you'll have written index.html and post.html to reference the appropriate resources in the static/ folder.
