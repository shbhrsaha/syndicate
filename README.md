
syndicate
===
A simple Markdown-based static site generator


Introduction
---
Syndicate converts all the Markdown files in a directory into HTML files according to a user-defined template. You can use this script to auto-generate static web sites with consistent styles and layout on each page.

Usage
---
1. Place all your Markdown files in directories that are children to wherever the syndicate.py script is located. Note that all your markdown files should follow one of two naming conventions:

    1. YYYY-MM-DD.[md | mdown | markdown | txt] (where YYYY is replaced with the year of the post date, MM with the month, and so forth), if you want to use the post date in your template.
    2. Simply: 'markdown.txt'.
2. Edit post.html to your liking. This file serves as a template for all of your posts. Reserve {{ title }} and {{ body }} patterns for Syndicate to parse. The {{ title }} pattern will be replaced with the first line of each Markdown file, with leading # removed. The {{ body }} pattern will be replaced with the contents of your entire parsed Markdown file. The {{ date }} pattern will be replaced by the date as specified by the post's file name, if you choose to follow the YYYY-MM-DD convention.
3. Run "python syndicate.py [--gfm] [--minify] [--prettify] [--template template_file] [posts]"

    * [--gfm] indicates that you'd like your posts to be parsed with [GitHub Flavored Markdown](https://help.github.com/articles/github-flavored-markdown) (defaults to 'False'). Requires Ruby.
    * [--minify] indicates that you'd like to have your production/static/*.css files [minified and combined](http://developer.yahoo.com/performance/rules.html#minify). To use this feature, install [cssmin](https://pypi.python.org/pypi/cssmin) and replace your stylesheet links in post.html with

            <link href="{{ minified_css }}"rel="stylesheet">

    * [--prettify] indicates that you'd like to add automatic syntax highlighting to your \<code\> snippets using [Google Code Prettify](https://code.google.com/p/google-code-prettify/). If selected, you need to add '<script src="https://google-code-prettify.googlecode.com/svn/loader/run_prettify.js"></script>' to your HTML <head>. Note that Google Code Prettify will try to infer the target programming language from the code itself. However, if you'd like to specify a language yourself, prefix the code block with: <script style="display:block" type="text/plain"><!--?prettify lang=js?--></script> Where 'js' can be replaced by any of the languages specified [here](http://google-code-prettify.googlecode.com/svn/trunk/README.html).

    * [--template template_file] specifies the HTML post template file (defaults to 'post.html').
    * [posts] is an optional list of posts to be generated (defaults to 'all possible posts'). A post should be identified by the name of its immediate parent directory (e.g., 'post1/index.html' would be generated by listing 'post1' as an argument).
4. You'll find an index.html in every directory that has a markdown.txt

Generating static web sites
---
To use Syndicate to auto-generate static web sites, I suggest the following directory structure:

- syndicate.py
- post.html
- utils/
- - Markdown.pl
- - gfm.rb
- production/
- - index.html
- - static/
- - - css/
- - - img/
- - - js/
- - article1/
- - - YYYY-MM-DD.md (or markdown.txt)
- - article2/
- - - YYYY-MM-DD.md (or markdown.txt)
- - article3/
- - - YYYY-MM-DD.md (or markdown.txt)

The example above shows a simple web site that contains three articles currently written in Markdown. Performing step #5 as described above will create index.html in the article1/, article2/, and article3/ folders.

To publish the web site, just copy the contents of the production/ folder to your web server. Ideally, you'll have written index.html and post.html to reference the appropriate resources in the static/ folder.
