# this script converts your markdown into a production-ready web site

import os, sys, argparse

# get optional command-line arguments
parser = argparse.ArgumentParser("Turn Markdown files into static web sites.")
parser.add_argument('--template', dest='template_file', metavar='template_file', nargs='?', default="post.html", help='post template file')
parser.add_argument('--gfm', dest='gfm', action='store_const', const=True, default=False, help='activate github-flavored markdown')
parser.add_argument('--minify', dest='minify', action='store_const', const=True, default=False, help='activate CSS minification')
parser.add_argument('posts', nargs='*', default=[], help='a list of posts to generate (defaults to all possible posts), specified by the name of the post\'s directory')
args = parser.parse_args()

# gather template file HTML
templateHTML = file(args.template_file, "rb").read()

# iterate over all markdown files in this directory and subdirectories

ROOT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
FILENAME_MATCH = "markdown.txt"
CSS_DIRECTORY = ROOT_DIRECTORY + "/production/static/css/"

# a list of all the files in ROOT_DIRECTORY that match FILENAME_MATCH
def post_filter(path):
    return (not args.posts) or (root.split('/')[-1] in args.posts)
csv_files = [os.path.join(root, name)
             for root, dirs, files in os.walk(ROOT_DIRECTORY)
             for name in files
             if name == FILENAME_MATCH and post_filter(root)]

# set compilation function
compile_markdown = "ruby utils/gfm.rb %s | perl utils/markdown.pl > temp.txt" if args.gfm else "perl utils/markdown.pl %s > temp.txt"

# compress CSS
if args.minify:
    combined_css_path = CSS_DIRECTORY + 'combined.css'
    # delete CSS if already exists
    if os.path.isfile(combined_css_path):
        os.remove(combined_css_path)

    # merge all CSS
    css_files = [os.path.join(root, name) for root, dirs, files in os.walk(CSS_DIRECTORY) for name in files if ".css" in name]
    all_css = ''.join([open(f).read() for f in css_files])

    # compress CSS
    from cssmin import cssmin
    minifed_css = cssmin(all_css)

    # store all CSS in single file
    combined_css = open(combined_css_path, "w+")
    combined_css.write(minifed_css)

# generate blog posts
for file_path in csv_files:

    print "Producing " + file_path

    # determine the current directory
    pathArray = file_path.split("/")
    del(pathArray[-1])
    directory = "/".join(pathArray)

    sys.stdout.flush()

    # extract the title from the markdown
    with open(file_path, 'r') as f:
        title = f.readline()
    while title[0] == "#" or title[0] == " ":
        title = title[1:]

    # run the converter and output to a temp.txt
    os.system(compile_markdown % file_path)

    # now read the output from temp.txt and inject into post.html
    temp_file = open("temp.txt", "rb")
    tempHTML = temp_file.read()

    productionHTML = templateHTML.replace("{{ title }}", title)
    productionHTML = productionHTML.replace("{{ body }}", tempHTML)
    if args.minify:
        # need to get relative path from HTML file to minified css
        common_prefix = os.path.commonprefix([file_path, combined_css_path])
        relative_path = '../' + os.path.relpath(combined_css_path, common_prefix)
        productionHTML = productionHTML.replace("{{ minified_css }}", relative_path)

    # write that production output to index.html in original directory
    productionFile = open(directory+"/index.html", "w")
    productionFile.write(productionHTML)

if os.path.exists("temp.txt"):
    os.system("rm temp.txt")
print "Production complete."
